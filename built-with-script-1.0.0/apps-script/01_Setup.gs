/** Run setupBWS manually once. Nothing is scheduled until startRoutine(). */
function props_(){return PropertiesService.getScriptProperties();}
function owner_(){var want=props_().getProperty('BWS_OWNER');var who=Session.getEffectiveUser().getEmail();
  if(!want||!who||who!==want)throw Error('AUTH: owner identity unavailable or mismatch');}
function uiOwner_(){owner_();var actual=Session.getActiveUser().getEmail();
  if(!actual||actual!==props_().getProperty('BWS_OWNER'))throw Error('AUTH: private owner-only dashboard required');}
function sheet_(name){return SpreadsheetApp.openById(props_().getProperty('BWS_SHEET_ID')).getSheetByName(name);}
function lock_(fn){var l=LockService.getScriptLock();if(!l.tryLock(2000))return {busy:true};
  try{return fn();}finally{l.releaseLock();}}
function setupBWS(){return lock_(function(){
  var p=props_(),email=Session.getEffectiveUser().getEmail();if(!email)throw Error('AUTH: run setup in the Apps Script editor');
  if(p.getProperty('BWS_OWNER')&&p.getProperty('BWS_OWNER')!==email)throw Error('AUTH: different owner');
  p.setProperty('BWS_OWNER',email);
  if(!p.getProperty('BWS_SHEET_ID')){var ss=SpreadsheetApp.create('Built with Script — private register');p.setProperty('BWS_SHEET_ID',ss.getId());}
  if(!p.getProperty('BWS_ROOT_ID')){var f=DriveApp.createFolder('Built with Script — private');p.setProperty('BWS_ROOT_ID',f.getId());}
  var root=DriveApp.getFolderById(p.getProperty('BWS_ROOT_ID'));
  ['INBOX','OUTBOX','RECEIPTS','ARCHIVE'].forEach(function(n){if(!p.getProperty('BWS_'+n+'_ID'))p.setProperty('BWS_'+n+'_ID',root.createFolder(n.toLowerCase()).getId());});
  var headers={Jobs:['id','kind','payload_json','state','attempts','next_at_ms','approved_hash','result_json','updated_at'],
    Mail:['message_id','thread_id','date','from','subject','category','link'],
    Library:['file_id','name','mime','updated','url','parent_id'],
    Scan:['folder_id','page_token','state'],Sources:['key','url','title','retrieved_at'],Plans:['key','enabled','kind','payload_json','interval_hours','last_bucket'],Runs:['time','event','id','detail']};
  var book=SpreadsheetApp.openById(p.getProperty('BWS_SHEET_ID'));
  Object.keys(headers).forEach(function(n){var s=book.getSheetByName(n)||book.insertSheet(n);
    if(!s.getLastRow())s.appendRow(headers[n]);s.setFrozenRows(1);s.getRange(1,1,1,headers[n].length).setFontWeight('bold').setBackground('#17342e').setFontColor('#ffffff');
    s.setColumnWidths(1,headers[n].length,170);s.getDataRange().setWrap(true);});
  var defaults={BWS_ACTIVE:'false',BWS_AUTOLABEL:'false',BWS_ALLOW_SEND:'false',BWS_SEND_TO:'[]',BWS_ALLOWED_HOSTS:'[]',
    BWS_SCAN_START:'2026-03-30',BWS_SCAN_END:'2026-10-01',BWS_MAIL_OFFSET:'0'};
  Object.keys(defaults).forEach(function(k){if(p.getProperty(k)===null)p.setProperty(k,defaults[k]);});
  if(!p.getProperty('BWS_BRIDGE_SECRET'))p.setProperty('BWS_BRIDGE_SECRET',Utilities.getUuid()+Utilities.getUuid());
  var scan=sheet_('Scan');if(scan.getLastRow()===1)scan.appendRow([p.getProperty('BWS_INBOX_ID'),'','READY']);
  return {spreadsheet:book.getUrl(),folder:root.getUrl(),scheduled:false,next:'Run doctorBWS; then startRoutine when ready.'};
});}
function doctorBWS(){owner_();var out={version:BWS.version,timeZone:Session.getScriptTimeZone(),active:props_().getProperty('BWS_ACTIVE')==='true',services:{}};
  [['Drive',function(){return DriveApp.getFolderById(props_().getProperty('BWS_ROOT_ID')).getName();}],
   ['Gmail',function(){return GmailApp.getInboxUnreadCount();}],['Register',function(){return sheet_('Jobs').getLastRow();}]].forEach(function(x){
    try{x[1]();out.services[x[0]]='AVAILABLE';}catch(e){out.services[x[0]]={state:'BLOCKED',error:String(e).slice(0,180)};}});
  out.stages={};['mail','drive','receipts','plans'].forEach(function(n){out.stages[n]=JSON.parse(props_().getProperty('BWS_STAGE_'+n)||'null');});
  out.wordpress=!!props_().getProperty('BWS_WP_BASE');out.local='ON_DEMAND — sync outbox and receipts folders or copy manually';return out;}
function startRoutine(){owner_();props_().setProperty('BWS_ACTIVE','true');
  var exists=ScriptApp.getProjectTriggers().some(function(t){return t.getHandlerFunction()==='routineTick';});
  if(!exists)ScriptApp.newTrigger('routineTick').timeBased().everyHours(1).create();return {active:true,cadence:'hourly, approximate'};}
function stopRoutine(){owner_();props_().setProperty('BWS_ACTIVE','false');ScriptApp.getProjectTriggers().forEach(function(t){if(t.getHandlerFunction()==='routineTick')ScriptApp.deleteTrigger(t);});return {active:false};}
function log_(event,id,detail){sheet_('Runs').appendRow([new Date().toISOString(),event,id,safeCell_(String(detail).slice(0,500))]);}
function doctor(){return doctorBWS();}
