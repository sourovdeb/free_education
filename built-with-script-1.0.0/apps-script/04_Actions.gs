function folder_(name){return DriveApp.getFolderById(props_().getProperty('BWS_'+name+'_ID'));}
function writeOnce_(folder,name,text,mime){var it=folder.getFilesByName(name);if(it.hasNext()){var f=it.next();if(f.getBlob().getDataAsString('UTF-8')!==text)throw Error('VALIDATION: existing output differs');return f;}
  return folder.createFile(name,text,mime||MimeType.PLAIN_TEXT);}
function fetchAllowed_(url){var hosts=JSON.parse(props_().getProperty('BWS_ALLOWED_HOSTS')||'[]');allowedUrl_(url,hosts);
  var r=UrlFetchApp.fetch(url,{muteHttpExceptions:true,followRedirects:false});var c=r.getResponseCode();if(c!==200)throw Error('HTTP '+c+'; redirects require manual validation');
  if(r.getContent().length>2000000)throw Error('VALIDATION: response exceeds 2MB');return r;}
function execute_(kind,p,id){checkTask_(kind,p);
  switch(kind){
    case 'mail.label':
      var label=GmailApp.getUserLabelByName(p.label)||GmailApp.createLabel(p.label);GmailApp.getThreadById(p.threadId).addLabel(label);return {label:p.label,threadId:p.threadId};
    case 'mail.replyDraft':
      var m=GmailApp.getMessageById(p.messageId);var d=m.createDraftReply(String(p.body));return {draftId:d.getId(),sent:false};
    case 'mail.applicationDraft':
      var profile=DriveApp.getFileById(p.profileFileId),bytes=profile.getBlob().getDataAsString('UTF-8');
      if(!same_(digest_(bytes),p.profileSha256))throw Error('VALIDATION: current approved profile changed');
      var verified=JSON.parse(bytes);if(verified.reviewed!==true||!Array.isArray(verified.approved_claims)||!verified.approved_claims.length||verified.approved_claims.some(function(c){return !c.text||!c.source;}))throw Error('VALIDATION: reviewed profile JSON with sourced claims required');
      var d=GmailApp.createDraft(String(p.to),String(p.subject),String(p.body));return {draftId:d.getId(),sent:false,profileSha256:p.profileSha256};
    case 'mail.sendDraft':
      if(props_().getProperty('BWS_ALLOW_SEND')!=='true')throw Error('UNSUPPORTED: sending disabled; send manually in Gmail or opt in');
      var d=GmailApp.getDraft(p.draftId),m=d.getMessage();if(!same_(digest_(m.getRawContent()),p.expectedSha256))throw Error('VALIDATION: draft changed; approve a new snapshot');
      var allowed=JSON.parse(props_().getProperty('BWS_SEND_TO')||'[]');var to=m.getTo().trim().toLowerCase();
      if(!/^[^\s<>@,;]+@[^\s<>@,;]+\.[^\s<>@,;]+$/.test(to)||allowed.indexOf(to)<0||m.getCc()||m.getBcc())throw Error('VALIDATION: exact single allowed recipient; CC/BCC forbidden');
      if(MailApp.getRemainingDailyQuota()<1)throw Error('MISSING: daily send quota exhausted; resume manually after reset');
      var sent=d.send();return {sentMessageId:sent.getId(),state:'SENT_NOT_DELIVERY_CONFIRMED'};
    case 'drive.copy':
      var f=DriveApp.getFileById(p.fileId).makeCopy(id.slice(0,12)+'-'+cleanName_(DriveApp.getFileById(p.fileId).getName()),folder_('ARCHIVE'));return {fileId:f.getId(),url:f.getUrl()};
    case 'drive.attachment':
      var m=GmailApp.getMessageById(p.messageId),labels=m.getThread().getLabels().map(function(l){return l.getName();});
      if(labels.indexOf('BWS/Ready')<0)throw Error('VALIDATION: add BWS/Ready to the source conversation first');
      var as=m.getAttachments({includeInlineImages:false,includeAttachments:true}),a=as[p.attachmentIndex];if(!a)throw Error('MISSING: attachment');
      if(a.getSize()>20000000)throw Error('VALIDATION: attachment exceeds 20MB');
      if(!/\.(pdf|docx|txt|md|csv|json|png|jpe?g|webp|mp3|wav)$/i.test(a.getName()))throw Error('UNSUPPORTED: attachment type needs manual handling');
      var f=folder_('INBOX').createFile(a.copyBlob().setName(id.slice(0,12)+'-'+cleanName_(a.getName())));return {fileId:f.getId(),url:f.getUrl(),executed:false};
    case 'text.capture':
      var f=writeOnce_(folder_('INBOX'),id.slice(0,12)+'-'+cleanName_(p.title)+'.txt',String(p.body));return {fileId:f.getId(),url:f.getUrl(),sourcePreserved:true};
    case 'wordpress.draft': return wpDraft_(p,id);
    case 'feed.collect': return feed_(p);
    case 'local.dispatch':
      var envelope={schema:1,id:id,task:p.task,created_ms:Date.now()};envelope.signature=signature_(envelope,props_().getProperty('BWS_BRIDGE_SECRET'));
      var name=id+'.job.json',it=folder_('OUTBOX').getFilesByName(name);
      if(it.hasNext())return {fileId:it.next().getId(),state:'WAITING_LOCAL'};
      var f=folder_('OUTBOX').createFile(name,canonical_(envelope),MimeType.PLAIN_TEXT);return {fileId:f.getId(),url:f.getUrl(),state:'WAITING_LOCAL'};
  }
  throw Error('UNSUPPORTED: action');
}
function queueDraftForSend(draftId){uiOwner_();return lock_(function(){var d=GmailApp.getDraft(draftId),m=d.getMessage();
  return enqueue_('mail.sendDraft',{draftId:draftId,expectedSha256:digest_(m.getRawContent()),to:m.getTo(),subject:m.getSubject(),body:m.getPlainBody(),cc:m.getCc(),bcc:m.getBcc()});});}
function wpDraft_(p,id){var config=props_(),base=(config.getProperty('BWS_WP_BASE')||'').replace(/\/$/,''),user=config.getProperty('BWS_WP_USER'),pass=config.getProperty('BWS_WP_APP_PASSWORD');
  if(!base||!user||!pass)throw Error('MISSING: WordPress URL, username or Application Password');
  allowedUrl_(base,JSON.parse(config.getProperty('BWS_ALLOWED_HOSTS')||'[]'));
  var url=base+'/wp-json/wp/v2/posts',auth='Basic '+Utilities.base64Encode(user+':'+pass,Utilities.Charset.UTF_8);
  var headers={Authorization:auth};var slug='bws-'+id.slice(0,20);
  var previous=UrlFetchApp.fetch(url+'?context=edit&status=draft,pending,publish,future,private&slug='+slug,{headers:headers,muteHttpExceptions:true,followRedirects:false});
  if(previous.getResponseCode()!==200)throw Error('HTTP '+previous.getResponseCode());var old=JSON.parse(previous.getContentText());
  if(old.length)return {postId:old[0].id,url:old[0].link,status:old[0].status,reconciled:true};
  var r=UrlFetchApp.fetch(url,{method:'post',headers:headers,contentType:'application/json',payload:JSON.stringify({title:p.title,content:p.content,status:'draft',slug:slug}),muteHttpExceptions:true,followRedirects:false});
  if(r.getResponseCode()!==201)throw Error('HTTP '+r.getResponseCode());var data=JSON.parse(r.getContentText());return {postId:data.id,url:data.link,status:data.status};
}
function feed_(p){var text=fetchAllowed_(p.url).getContentText();if(/<!DOCTYPE|<!ENTITY/i.test(text))throw Error('VALIDATION: external entities and document types are not accepted in feeds');var xml=XmlService.parse(text),root=xml.getRootElement(),ns=root.getNamespace();
  var channel=root.getChild('channel'),items=channel?channel.getChildren('item'):root.getChildren('entry',ns),s=sheet_('Sources'),known={};rows_('Sources').forEach(function(r){known[r[0]]=true;});
  var count=0;items.slice(0,50).forEach(function(item){var n=item.getNamespace(),title=item.getChildText('title',n)||'',link=item.getChildText('link',n)||'';
    if(!link){var l=item.getChild('link',n);link=l&&l.getAttribute('href')?l.getAttribute('href').getValue():'';}
    if(!/^https:\/\//i.test(link))return;var key=digest_(link);if(known[key])return;
    s.appendRow([key,safeCell_(link),safeCell_(title),new Date().toISOString()]);known[key]=true;count++;});return {added:count,source:p.url};}
