function rows_(name){var s=sheet_(name);return s.getLastRow()<2?[]:s.getRange(2,1,s.getLastRow()-1,s.getLastColumn()).getValues();}
function enqueue_(kind,p){checkTask_(kind,p);var id=digest_({kind:kind,payload:p});var s=sheet_('Jobs');
  var old=rows_('Jobs').find(function(r){return r[0]===id;});if(old)return {id:id,state:old[3],duplicate:true};
  var state=BWS.approved.indexOf(kind)>=0?'APPROVAL':'READY';
  s.appendRow([id,kind,canonical_(p),state,0,0,'','',new Date().toISOString()]);return {id:id,state:state};}
function queueTask(kind,p){uiOwner_();return lock_(function(){return enqueue_(kind,p);});}
function approveTask(id,expectedHash){uiOwner_();return lock_(function(){var rs=rows_('Jobs'),i=rs.findIndex(function(r){return r[0]===id;});
  if(i<0)throw Error('MISSING: task');var r=rs[i];if(r[3]!=='APPROVAL')throw Error('VALIDATION: task is not awaiting approval');
  var hash=digest_({kind:r[1],payload:JSON.parse(r[2])});if(!same_(expectedHash,hash))throw Error('VALIDATION: task changed; reload preview');
  r[3]='READY';r[6]=hash;r[8]=new Date().toISOString();sheet_('Jobs').getRange(i+2,1,1,9).setValues([r]);return {id:id,state:'READY'};});}
function cancelTask(id){uiOwner_();return lock_(function(){var rs=rows_('Jobs'),i=rs.findIndex(function(r){return r[0]===id;});
  if(i<0||['READY','APPROVAL','RETRY','BLOCKED'].indexOf(rs[i][3])<0)throw Error('VALIDATION: cannot cancel this state');
  sheet_('Jobs').getRange(i+2,4).setValue('CANCELLED');return {id:id,state:'CANCELLED'};});}
function processQueue_(deadline){var s=sheet_('Jobs'),rs=rows_('Jobs');
  for(var i=0;i<rs.length&&Date.now()<deadline;i++){
    var r=rs[i];if(r[3]==='RUNNING'){r[3]='REVIEW';r[7]=JSON.stringify({code:'INTERRUPTED',next:'Inspect destination; no blind retry.'});s.getRange(i+2,1,1,9).setValues([r]);continue;}
    if(['READY','RETRY'].indexOf(r[3])<0||Number(r[5])>Date.now())continue;
    var p=JSON.parse(r[2]);var hash=digest_({kind:r[1],payload:p});
    if(hash!==r[0]||(BWS.approved.indexOf(r[1])>=0&&!same_(r[6],hash))){r[3]='APPROVAL';s.getRange(i+2,1,1,9).setValues([r]);continue;}
    r[3]='RUNNING';r[4]=Number(r[4])+1;r[8]=new Date().toISOString();s.getRange(i+2,1,1,9).setValues([r]);SpreadsheetApp.flush();
    try{var result=execute_(r[1],p,r[0]);r[3]=r[1]==='local.dispatch'?'WAITING_LOCAL':'DONE';r[7]=JSON.stringify(result);}
    catch(e){var f=failure_(String(e),r[4],BWS.idempotent.indexOf(r[1])>=0);r[3]=f.state;r[5]=Date.now()+Math.pow(2,r[4])*60000;r[7]=JSON.stringify(f);log_('ACTION_ERROR',r[0],f.code);}
    r[8]=new Date().toISOString();s.getRange(i+2,1,1,9).setValues([r]);
  }
}
function routineTick(){owner_();if(props_().getProperty('BWS_ACTIVE')!=='true')return {paused:true};return lock_(function(){
  var deadline=Date.now()+BWS.tickMs;var stages=[['mail',scanMail_],['drive',scanDrive_],['receipts',importReceipts_],['plans',schedulePlans_]];
  stages.forEach(function(pair){if(Date.now()<deadline)runStage_(pair[0],pair[1],deadline);});
  processQueue_(deadline);return {processed:true};});}
function runReadyOnce(){uiOwner_();return lock_(function(){processQueue_(Date.now()+BWS.tickMs);return {processed:true};});}
function getDashboard(){uiOwner_();return {doctor:doctorBWS(),jobs:rows_('Jobs').slice(-60).reverse().map(function(r){return {id:r[0],kind:r[1],payload:JSON.parse(r[2]),state:r[3],attempts:r[4],result:r[7],hash:digest_({kind:r[1],payload:JSON.parse(r[2])})};}),runs:rows_('Runs').slice(-20).reverse()};}
function doGet(){uiOwner_();return HtmlService.createHtmlOutputFromFile('Dashboard').setTitle('Built with Script — private');}

function runStage_(name,fn,deadline){var key='BWS_STAGE_'+name,p=props_(),record=JSON.parse(p.getProperty(key)||'{"attempts":0,"blocked":false,"next":0}');
  if(record.blocked||record.next>Date.now())return;
  try{fn(deadline);p.deleteProperty(key);}catch(e){record.attempts++;var f=failure_(String(e),record.attempts,true);
    record.blocked=f.state!=='RETRY';record.next=Date.now()+Math.pow(2,record.attempts)*60000;record.code=f.code;record.error=String(e).slice(0,180);
    p.setProperty(key,JSON.stringify(record));log_('STAGE_BLOCKED',name,f.code);}}
function recheckStages(){uiOwner_();['mail','drive','receipts','plans'].forEach(function(n){props_().deleteProperty('BWS_STAGE_'+n);});return doctorBWS();}
function resumeBlockedTask(id){uiOwner_();return lock_(function(){var rs=rows_('Jobs'),i=rs.findIndex(function(r){return r[0]===id;});
  if(i<0||rs[i][3]!=='BLOCKED')throw Error('VALIDATION: only BLOCKED tasks can be resumed after fixing configuration');
  rs[i][3]='READY';rs[i][4]=0;rs[i][5]=0;sheet_('Jobs').getRange(i+2,1,1,9).setValues([rs[i]]);return {state:'READY'};});}

/** Optional recurring recipes: user-created rows only, no automatic backlogged catch-up. */
function schedulePlans_(deadline){var rs=rows_('Plans'),sheet=sheet_('Plans');rs.slice(0,25).forEach(function(r,i){
  if(Date.now()>=deadline||String(r[1]).toLowerCase()!=='true')return;
  if(!/^[A-Za-z0-9_-]{1,60}$/.test(String(r[0])))throw Error('VALIDATION: plan key');
  if(['feed.collect','drive.copy','local.dispatch'].indexOf(r[2])<0)throw Error('VALIDATION: recurring plan supports feeds, backup copies or approved local dispatch only');
  var hours=Number(r[4]);if(!Number.isInteger(hours)||hours<1||hours>720)throw Error('VALIDATION: plan interval 1–720 hours');
  var bucket=Math.floor(Date.now()/(hours*3600000));if(String(r[5])===String(bucket))return;
  var payload=JSON.parse(r[3]);payload.run_nonce='plan-'+r[0]+'-'+bucket;enqueue_(r[2],payload);sheet.getRange(i+2,6).setValue(String(bucket));
});}
function collectOnce(){uiOwner_();return lock_(function(){var deadline=Date.now()+BWS.tickMs;
  [['mail',scanMail_],['drive',scanDrive_],['receipts',importReceipts_]].forEach(function(p){if(Date.now()<deadline)runStage_(p[0],p[1],deadline);});return {collected:true,scheduled:false};});}
