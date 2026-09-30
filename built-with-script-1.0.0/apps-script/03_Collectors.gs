/** Resumable message-ID cursor; metadata only, fixed cutoff per scan. No archive/delete/reply. */
function scanMail_(deadline){var p=props_(),start=p.getProperty('BWS_SCAN_START'),end=p.getProperty('BWS_SCAN_END');
  if(!/^\d{4}-\d{2}-\d{2}$/.test(start)||!/^\d{4}-\d{2}-\d{2}$/.test(end))throw Error('VALIDATION: scan dates');
  var backfill=p.getProperty('BWS_MAIL_DONE')!=='true';
  var lower=backfill?Date.parse(start+'T00:00:00+04:00'):Number(p.getProperty('BWS_MAIL_WATERMARK')||Date.now()-7*86400000)-86400000;
  var upper=backfill?Date.parse(end+'T00:00:00+04:00'):Number(p.getProperty('BWS_LIVE_CUTOFF')||Date.now());
  if(!backfill&&!p.getProperty('BWS_LIVE_CUTOFF'))p.setProperty('BWS_LIVE_CUTOFF',String(upper));
  var q='after:'+Math.floor(lower/1000)+' before:'+Math.floor(upper/1000)+' -in:spam -in:trash -subject:credentials -subject:password';
  var url='https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=20&q='+encodeURIComponent(q);
  if(p.getProperty('BWS_MAIL_TOKEN'))url+='&pageToken='+encodeURIComponent(p.getProperty('BWS_MAIL_TOKEN'));
  var data=googleGet_(url),known={};rows_('Mail').forEach(function(r){known[r[0]]=true;});var messages=data.messages||[];
  for(var i=0;i<messages.length;i++){
    if(Date.now()>=deadline)return; // Keep this page token; already imported IDs are skipped next time.
    var id=messages[i].id;if(known[id])continue;
    var m=googleGet_('https://gmail.googleapis.com/gmail/v1/users/me/messages/'+encodeURIComponent(id)+'?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date');
    var headers={};(m.payload&&m.payload.headers||[]).forEach(function(h){headers[h.name.toLowerCase()]=h.value;});
    var subject=headers.subject||'',from=headers.from||'';if(/credential|password|api.?key|secret/i.test(subject))continue;
    var category=classify_(subject,from);
    sheet_('Mail').appendRow([id,m.threadId,new Date(Number(m.internalDate)).toISOString(),safeCell_(from),safeCell_(subject),category,'https://mail.google.com/mail/u/0/#all/'+m.threadId]);known[id]=true;
    if(p.getProperty('BWS_AUTOLABEL')==='true'&&category!=='Other')enqueue_('mail.label',{threadId:m.threadId,label:'BWS/'+category});
  }
  p.setProperty('BWS_MAIL_TOKEN',data.nextPageToken||'');
  if(!data.nextPageToken){if(backfill){p.setProperty('BWS_MAIL_DONE','true');p.setProperty('BWS_MAIL_WATERMARK',String(Math.min(upper,Date.now())));}
    else{p.setProperty('BWS_MAIL_WATERMARK',String(upper));p.deleteProperty('BWS_LIVE_CUTOFF');}}
}
function googleGet_(url){var r=UrlFetchApp.fetch(url,{headers:{Authorization:'Bearer '+ScriptApp.getOAuthToken()},muteHttpExceptions:true,followRedirects:false});
  if(r.getResponseCode()!==200)throw Error('HTTP '+r.getResponseCode());return JSON.parse(r.getContentText());}
function scanDrive_(deadline){var scans=rows_('Scan'),s=sheet_('Scan'),i=scans.findIndex(function(r){return r[2]==='READY';});if(i<0){
    var last=Number(props_().getProperty('BWS_DRIVE_SCAN_MS')||0);if(Date.now()-last<86400000)return;
    scans.forEach(function(r,n){s.getRange(n+2,2,1,2).setValues([['','READY']]);});
    props_().setProperty('BWS_DRIVE_SCAN_MS',String(Date.now()));return;
  }
  var row=scans[i],folder=String(row[0]);if(!/^[A-Za-z0-9_-]+$/.test(folder))throw Error('VALIDATION: Drive folder ID');
  var query="'"+folder+"' in parents and trashed = false";
  var url='https://www.googleapis.com/drive/v3/files?q='+encodeURIComponent(query)+'&pageSize=25&fields=nextPageToken,files(id,name,mimeType,modifiedTime,webViewLink)';
  if(row[1])url+='&pageToken='+encodeURIComponent(row[1]);var data=googleGet_(url),known={},folders={};
  rows_('Library').forEach(function(r,n){known[r[0]]=n+2;});scans.forEach(function(r){folders[r[0]]=true;});
  (data.files||[]).forEach(function(f){
    if(f.mimeType==='application/vnd.google-apps.folder'){if(!folders[f.id]){s.appendRow([f.id,'','READY']);folders[f.id]=true;}}
    var entry=[f.id,safeCell_(f.name),f.mimeType,f.modifiedTime,f.webViewLink||'',folder];if(!known[f.id]){sheet_('Library').appendRow(entry);known[f.id]=sheet_('Library').getLastRow();}else sheet_('Library').getRange(known[f.id],1,1,6).setValues([entry]);
  });
  s.getRange(i+2,2,1,2).setValues([[data.nextPageToken||'',data.nextPageToken?'READY':'DONE']]);
}
function importReceipts_(deadline){var p=props_(),token=p.getProperty('BWS_RECEIPT_CURSOR'),it,n=0,rs=rows_('Jobs');
  try{it=token?DriveApp.continueFileIterator(token):folder_('RECEIPTS').getFiles();}catch(e){p.deleteProperty('BWS_RECEIPT_CURSOR');throw Error('MISSING: receipt cursor expired; recheck stages to restart');}
  while(it.hasNext()&&n++<20&&Date.now()<deadline){var f=it.next();if(!/\.receipt\.json$/.test(f.getName())||f.getSize()>500000)continue;
    var r,sig;try{r=JSON.parse(f.getBlob().getDataAsString('UTF-8'));sig=r.signature;delete r.signature;if(!same_(sig,signature_(r,p.getProperty('BWS_BRIDGE_SECRET'))))continue;}catch(e){continue;}
    var i=rs.findIndex(function(x){return x[0]===r.id&&x[3]==='WAITING_LOCAL';});if(i<0)continue;
    if(['DONE','PARTIAL','BLOCKED','FAILED','REVIEW'].indexOf(r.state)<0)continue;
    var stored=JSON.parse(rs[i][2]);if(digest_(stored.task)!==r.task_sha256)continue;
    rs[i][3]=r.state==='DONE'?'LOCAL_DONE':r.state;rs[i][7]=JSON.stringify(r).slice(0,45000);rs[i][8]=new Date().toISOString();sheet_('Jobs').getRange(i+2,1,1,9).setValues([rs[i]]);f.moveTo(folder_('ARCHIVE'));
  }
  if(it.hasNext())p.setProperty('BWS_RECEIPT_CURSOR',it.getContinuationToken());else p.deleteProperty('BWS_RECEIPT_CURSOR');
}
