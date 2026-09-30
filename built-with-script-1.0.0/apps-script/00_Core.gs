/** Built with Script 1.0.0. Pure policy functions: also tested under Node. */
var BWS = Object.freeze({version:'1.0.0', maxAttempts:3, tickMs:110000, batch:20,
  actions:['mail.label','mail.replyDraft','mail.applicationDraft','mail.sendDraft',
    'drive.copy','drive.attachment','text.capture','wordpress.draft','feed.collect','local.dispatch'],
  approved:['mail.sendDraft','wordpress.draft','local.dispatch'],
  idempotent:['mail.label','feed.collect']});
function canonical_(x) {
  if (x === null || typeof x === 'boolean') return JSON.stringify(x);
  if (typeof x === 'number') {if (!Number.isSafeInteger(x)) throw Error('VALIDATION: integers only');return JSON.stringify(x);}
  if (typeof x === 'string') return JSON.stringify(x);
  if (Array.isArray(x)) return '['+x.map(canonical_).join(',')+']';
  if (!x || Object.prototype.toString.call(x)!=='[object Object]') throw Error('VALIDATION: JSON object required');
  return '{'+Object.keys(x).sort().map(function(k){
    if(!/^[A-Za-z0-9_.-]+$/.test(k)) throw Error('VALIDATION: ASCII keys required');
    return JSON.stringify(k)+':'+canonical_(x[k]);
  }).join(',')+'}';
}
function digest_(x) {return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,
  typeof x==='string'?x:canonical_(x),Utilities.Charset.UTF_8).map(function(b){return ('0'+(b&255).toString(16)).slice(-2);}).join('');}
function signature_(x,secret) {return Utilities.computeHmacSha256Signature(canonical_(x),secret,Utilities.Charset.UTF_8)
  .map(function(b){return ('0'+(b&255).toString(16)).slice(-2);}).join('');}
function same_(a,b) {if(typeof a!=='string'||typeof b!=='string'||a.length!==b.length)return false;
  var n=0;for(var i=0;i<a.length;i++)n|=a.charCodeAt(i)^b.charCodeAt(i);return n===0;}
function checkTask_(kind,p) {
  if(BWS.actions.indexOf(kind)<0)throw Error('VALIDATION: unknown action '+kind);
  if(!p||Array.isArray(p)||typeof p!=='object')throw Error('VALIDATION: object payload required');
  var s=canonical_(p);if(s.length>30000)throw Error('VALIDATION: payload exceeds 30000 characters');
  var required={'mail.label':['threadId','label'],'mail.replyDraft':['messageId','body'],
    'mail.applicationDraft':['to','subject','body','profileFileId','profileSha256'],
    'mail.sendDraft':['draftId','expectedSha256'],'drive.copy':['fileId'],
    'drive.attachment':['messageId','attachmentIndex'],'text.capture':['title','body'],
    'wordpress.draft':['title','content'],'feed.collect':['url'],'local.dispatch':['task']};
  required[kind].forEach(function(k){if(p[k]===undefined||p[k]===null||p[k]==='')throw Error('VALIDATION: missing '+k);});
  if(kind==='mail.label'&&!/^BWS\/[A-Za-z0-9 _-]{1,60}$/.test(p.label))throw Error('VALIDATION: additive BWS labels only');
  if(kind==='drive.attachment'&&(!Number.isInteger(p.attachmentIndex)||p.attachmentIndex<0))throw Error('VALIDATION: attachment index');
  if(kind==='mail.applicationDraft'&&!/^[^\s<>@,;]+@[^\s<>@,;]+\.[^\s<>@,;]+$/.test(p.to))throw Error('VALIDATION: one recipient required');
  return true;
}
function classify_(subject,from) {
  var t=(subject+' '+from).toLowerCase();
  if(/delivery status|undeliver|mailer-daemon|failure notice|non remis/.test(t))return 'Delivery issue';
  if(/interview|entretien|convocation|rendez-vous/.test(t))return 'Review soon';
  if(/candidature|application|job alert|emploi|recrutement/.test(t))return 'Jobs';
  if(/transcript|storyboard|blender|resolve|writing|lesson|wordpress/.test(t))return 'Projects';
  return 'Other';
}
function failure_(message,attempt,idempotent) {
  var m=String(message);
  if(/AUTH|401|403|permission|authorization/i.test(m))return {state:'BLOCKED',code:'AUTH',next:'Reconnect or authorize the named service; do not retry automatically.'};
  if(/VALIDATION|MISSING|UNSUPPORTED|404|not found/i.test(m))return {state:'BLOCKED',code:'CONFIG',next:'Correct the input, dependency or path; create a new task.'};
  if(idempotent && attempt<BWS.maxAttempts && /429|500|502|503|504|timeout|temporar|quota|rate limit/i.test(m))
    return {state:'RETRY',code:'TRANSIENT',next:'One later attempt; maximum three total.'};
  return {state:idempotent?'FAILED':'REVIEW',code:'CHECK_RESULT',next:'Inspect the destination before retrying; a write may already exist.'};
}
function allowedUrl_(url,hosts) {
  var m=/^https:\/\/([a-z0-9.-]+)(?::443)?([/?#].*)?$/i.exec(String(url));
  if(!m || m[1].endsWith('.') || hosts.indexOf(m[1].toLowerCase())<0 || /^[\d.]+$/.test(m[1]))
    throw Error('VALIDATION: HTTPS URL must match an explicitly allowed hostname');
  return url;
}
function safeCell_(s){s=String(s===undefined?'':s);return /^[\s\x00-\x1f]*[=+@-]/.test(s)?"'"+s:s;}
function cleanName_(s){return String(s).replace(/[\\/:*?"<>|\x00-\x1f]/g,'_').slice(0,100)||'untitled';}
