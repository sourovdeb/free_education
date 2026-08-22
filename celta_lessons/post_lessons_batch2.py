#!/usr/bin/env python3
import requests, time

API_URL = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
HEADERS = {"X-Sourov-Key": "0767044896thevenet_", "Content-Type": "application/json"}

LC = {
    "A1":       {"c":"#27ae60","bg":"#eafaf1","lbl":"A1 Beginner","em":"🌱"},
    "A2":       {"c":"#2980b9","bg":"#ebf5fb","lbl":"A2 Elementary","em":"🌿"},
    "B1":       {"c":"#e67e22","bg":"#fef9e7","lbl":"B1 Intermediate","em":"🌟"},
    "B2":       {"c":"#8e44ad","bg":"#f5eef8","lbl":"B2 Upper-Intermediate","em":"⭐"},
    "C1":       {"c":"#c0392b","bg":"#fdedec","lbl":"C1 Advanced","em":"🏆"},
    "Teachers": {"c":"#16a085","bg":"#e8f8f5","lbl":"CELTA Methodology","em":"🎓"},
    "Kids":     {"c":"#d35400","bg":"#fdf2e9","lbl":"Young Learners","em":"🦋"},
}
FOOTER = "<div style='background:#f8f9fa;padding:14px 28px;border-top:1px solid #eee;font-size:0.78em;color:#777;line-height:1.5;margin-top:24px;'><em>Independent teaching resource. Not affiliated with, endorsed by, or accredited by Cambridge University Press &amp; Assessment. Confers no qualification. Based on publicly available ELT methodology and 18 years of professional experience.</em></div>"

def pill(t,c): return f"<span style='display:inline-block;margin:3px;padding:5px 11px;background:{c};color:#fff;border-radius:20px;font-size:0.85em;font-weight:600;'>{t}</span>"
def task_block(t,c,bg,i):
    return f"<div style='margin:12px 0;padding:14px 16px;background:#fff;border-left:4px solid {c};border-radius:0 8px 8px 0;box-shadow:0 1px 4px rgba(0,0,0,0.06);'><p style='margin:0 0 6px;font-weight:700;color:{c};'>Task {i}: {t['title']}</p><p style='margin:0 0 8px;color:#555;line-height:1.55;'>{t['instr']}</p><details><summary style='cursor:pointer;color:{c};font-size:0.88em;font-weight:600;'>💡 Show answer</summary><div style='padding:10px;background:{bg};border-radius:6px;margin-top:8px;color:#444;line-height:1.55;'>{t['ans']}</div></details></div>"

def build_html(L):
    lv=LC[L["level"]]; c,bg=lv["c"],lv["bg"]
    tasks_html="".join(task_block(t,c,bg,i+1) for i,t in enumerate(L["tasks"]))
    focus_html="".join(pill(f,c) for f in L.get("focus",[]))
    focus_sec=f"<div style='padding:0 28px 16px;'><p style='margin:0 0 8px;font-weight:700;color:#333;font-size:0.85em;text-transform:uppercase;letter-spacing:0.5px;'>Language Focus:</p>{focus_html}</div>" if focus_html else ""
    return f"""<div style='font-family:"Segoe UI",Arial,sans-serif;max-width:820px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.09);'>
<div style='background:{c};padding:26px 28px;color:#fff;'>
  <p style='margin:0;font-size:0.82em;opacity:0.85;letter-spacing:1px;text-transform:uppercase;'>5-Minute English Lab · {lv["lbl"]}</p>
  <h1 style='margin:6px 0 0;font-size:1.55em;line-height:1.2;'>{lv["em"]} {L["title"]}</h1>
  <p style='margin:10px 0 0;opacity:0.9;font-size:0.9em;'>⏱ 5 minutes · {L["framework"]}</p>
</div>
<div style='background:{bg};padding:16px 28px;border-left:5px solid {c};'>
  <p style='margin:0;color:#444;font-style:italic;line-height:1.6;'>💬 <strong>From my own experience:</strong> {L["anecdote"]}</p>
</div>
<div style='padding:20px 28px 10px;'>
  <div style='background:{bg};border-radius:8px;padding:13px 16px;border:1px solid {c}40;'>
    <p style='margin:0;color:{c};font-weight:700;'>🎯 By the end of this 5 minutes, you can:</p>
    <p style='margin:6px 0 0;color:#333;'>{L["aim"]}</p>
  </div>
</div>
{focus_sec}
<div style='padding:10px 28px 6px;'>
  <h2 style='color:{c};font-size:1.05em;margin:0 0 10px;border-bottom:2px solid {c}30;padding-bottom:7px;'>📖 Quick Explanation</h2>
  <div style='color:#333;line-height:1.65;'>{L["explanation"]}</div>
</div>
<div style='padding:14px 28px 6px;'>
  <h2 style='color:{c};font-size:1.05em;margin:0 0 6px;border-bottom:2px solid {c}30;padding-bottom:7px;'>✏️ Practice</h2>
  {tasks_html}
</div>
<div style='padding:14px 28px 6px;'>
  <h2 style='color:{c};font-size:1.05em;margin:0 0 8px;border-bottom:2px solid {c}30;padding-bottom:7px;'>🗣 Use It Now</h2>
  <div style='background:{bg};border-radius:8px;padding:14px 16px;color:#444;line-height:1.65;'>{L["production"]}</div>
</div>
<div style='padding:14px 28px 20px;'>
  <h2 style='color:{c};font-size:0.95em;margin:0 0 8px;'>✅ Quick Self-Check</h2>
  <label style='display:flex;align-items:center;gap:9px;margin:5px 0;cursor:pointer;color:#444;'><input type='checkbox' style='width:17px;height:17px;accent-color:{c};'> I understand the main language point</label>
  <label style='display:flex;align-items:center;gap:9px;margin:5px 0;cursor:pointer;color:#444;'><input type='checkbox' style='width:17px;height:17px;accent-color:{c};'> I completed at least one practice task</label>
  <label style='display:flex;align-items:center;gap:9px;margin:5px 0;cursor:pointer;color:#444;'><input type='checkbox' style='width:17px;height:17px;accent-color:{c};'> I tried the production task</label>
</div>
{FOOTER}</div>"""

lessons = [
{
 "title":"Reading Skills: Gist First, Detail Second",
 "level":"B1","framework":"PWP · Receptive Skills",
 "tags":"B1 English, reading skills, skimming scanning, reading strategies, 5-Minute English Lab",
 "seo_title":"Gist Reading vs Detail Reading: Strategy Lesson for B1 Learners",
 "meta":"Learn to read efficiently in English using gist and detail reading strategies. B1 reading skills lesson with real-world texts.",
 "anecdote":"When hotel menus arrived from new suppliers at The Ivy, I had thirty seconds to scan them before service began. Skimming for key information under pressure is a skill — and it is teachable.",
 "aim":"apply two reading strategies — skimming for gist and scanning for detail — to any English text.",
 "focus":["skimming","scanning","topic sentence","key words","gist question","detail question"],
 "explanation":"""<p>Efficient readers don't read every word every time. They choose the right strategy:</p>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0;'>
<div style='background:#fef9e7;padding:12px;border-radius:8px;'>
<strong>🔍 SKIMMING (gist)</strong><br><em>What is this text about?</em><br><br>• Read the title and headings<br>• Read only the first sentence of each paragraph<br>• Look at images or graphs<br>• Takes 30–60 seconds for a page</div>
<div style='background:#fdedec;padding:12px;border-radius:8px;'>
<strong>🎯 SCANNING (detail)</strong><br><em>Find specific information fast</em><br><br>• Know what you are looking for<br>• Move your eyes quickly down the page<br>• Stop only at relevant words/numbers<br>• Do not read everything</div>
</div>
<p><strong>The PWP process:</strong> Pre-reading (predict) → While-reading (gist then detail) → Post-reading (respond). Always set your gist question <em>before</em> you start reading.</p>""",
 "tasks":[
  {"title":"Which strategy?","instr":"Which reading strategy should you use for each task?<br>1. You need to find the price of a hotel room in a long brochure.<br>2. You want to know what a news article is about before deciding to read it.<br>3. You want to find a phone number in a directory.","ans":"1. Scanning (looking for a specific number) · 2. Skimming (general understanding) · 3. Scanning (specific information)"},
  {"title":"Gist question practice","instr":"Before reading any text, you need a gist question. Write one gist question for each text type:<br>1. A restaurant review · 2. A job advertisement · 3. A news report about education","ans":"1. Did the reviewer enjoy the restaurant? / What was the restaurant like overall? · 2. What kind of job is this? / What skills are needed? · 3. What is the main education story?"},
  {"title":"Topic sentence analysis","instr":"Read this paragraph and identify the topic sentence (the one that gives the main idea):<br><em>'English is now spoken by over 1.5 billion people worldwide. It is used as a first language in countries including the UK, USA, and Australia. As a second or foreign language, it is used in most international business, science, and diplomacy. Some linguists argue it has become the world's de facto global language.'</em>","ans":"The first sentence: 'English is now spoken by over 1.5 billion people worldwide.' It states the main point that all other sentences support."},
 ],
 "production":"Choose any text in English (a news headline, a restaurant menu, a product description). First, set yourself a gist question. Skim the text in 30 seconds and answer it. Then scan for one specific piece of information. Write what strategy you used and what you found."
},
{
 "title":"The Passive Voice: When the Action Matters More Than the Actor",
 "level":"B2","framework":"Guided Discovery · Grammar",
 "tags":"B2 English, passive voice, B2 grammar, professional writing, 5-Minute English Lab",
 "seo_title":"The Passive Voice in English: When and How to Use It | B2 Grammar",
 "meta":"Learn when and how to use the passive voice in English for professional and academic writing. Clear B2 grammar lesson.",
 "anecdote":"In hotel incident reports, we always wrote 'The bottle was broken' rather than 'Tom broke the bottle.' That passive form is not evasion — it focuses attention on the event, not the person. Knowing when to use it is professional intelligence.",
 "aim":"form and use passive constructions across three tenses and identify why the passive is chosen over the active.",
 "focus":["is made / was made / has been made","by + agent (optional)","active vs passive choice","professional/academic contexts"],
 "explanation":"""<p><strong>Form:</strong> <em>be</em> (any tense) + <strong>past participle</strong></p>
<table style='width:100%;border-collapse:collapse;font-size:0.88em;margin:8px 0;'>
<tr style='background:#f5eef8;'><th style='padding:7px;text-align:left;'>Tense</th><th style='padding:7px;text-align:left;'>Active</th><th style='padding:7px;text-align:left;'>Passive</th></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Present simple</td><td style='padding:6px;border-top:1px solid #ddd;'>The chef makes the sauce.</td><td style='padding:6px;border-top:1px solid #ddd;'>The sauce <strong>is made</strong> by the chef.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Past simple</td><td style='padding:6px;border-top:1px solid #ddd;'>They built this hotel in 1985.</td><td style='padding:6px;border-top:1px solid #ddd;'>This hotel <strong>was built</strong> in 1985.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Present perfect</td><td style='padding:6px;border-top:1px solid #ddd;'>Someone has stolen the wine.</td><td style='padding:6px;border-top:1px solid #ddd;'>The wine <strong>has been stolen</strong>.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Future</td><td style='padding:6px;border-top:1px solid #ddd;'>We will review the policy.</td><td style='padding:6px;border-top:1px solid #ddd;'>The policy <strong>will be reviewed</strong>.</td></tr>
</table>
<p><strong>Why choose passive?</strong> Use it when: (1) the agent is unknown or obvious, (2) the object is more important than the subject, (3) you want to sound formal or impersonal (academic/professional writing), (4) you want to avoid assigning blame.</p>""",
 "tasks":[
  {"title":"Transform to passive","instr":"Rewrite using the passive:<br>1. Someone cleaned the room. (past)<br>2. They are reviewing all applications. (present continuous)<br>3. We will announce the results tomorrow. (future)<br>4. The manager has cancelled the event. (present perfect)","ans":"1. The room was cleaned. · 2. All applications are being reviewed. · 3. The results will be announced tomorrow. · 4. The event has been cancelled (by the manager)."},
  {"title":"Why passive here?","instr":"Explain why the passive is used:<br>1. 'The new restaurant has been opened in the centre of town.' (newspaper headline)<br>2. 'Mistakes were made.' (political statement)<br>3. 'This wine is produced in the Burgundy region of France.'","ans":"1. The restaurant is the focus, not who opened it · 2. Avoids naming who made the mistakes (strategic evasion) · 3. Unknown/obvious agent; the wine's origin is what matters"},
  {"title":"Active or passive?","instr":"Choose the more appropriate form for a professional incident report:<br>a) 'John spilt coffee on the guest's bag.' OR b) 'Coffee was spilt on the guest's bag.'","ans":"(b) The passive is more appropriate in a formal incident report — it focuses on the event, not on blaming an individual, and sounds more objective."},
 ],
 "production":"Write a short paragraph (4 sentences) using the passive for a professional context of your choice: a company report, a hotel incident report, a news story, or a scientific finding. Use at least 3 different tenses."
},
{
 "title":"Agreeing, Disagreeing and Partly Agreeing: Professional Debate Language",
 "level":"B2","framework":"TBL · Functional Language",
 "tags":"B2 English, agreeing disagreeing, discussion language, professional English, 5-Minute English Lab",
 "seo_title":"Agree, Disagree and Negotiate in English: Professional Discussion Language | B2",
 "meta":"Learn how to agree, disagree and negotiate in English professionally. B2 functional language lesson for meetings and debates.",
 "anecdote":"Running pre-service briefings at Popolo in Sydney with a team of twelve, I had to manage disagreements without losing anyone's commitment. The phrase 'I see your point, however...' saved more relationships than I can count.",
 "aim":"use 12 expressions to agree fully, partly, and disagree politely — without losing professional rapport.",
 "focus":["Absolutely. / Exactly.","I see your point, but...","I'm not sure I agree...","That's fair, although...","With respect, I think...","To play devil's advocate..."],
 "explanation":"""<p>In professional English, blunt disagreement sounds aggressive. English speakers signal disagreement <strong>indirectly and gradually</strong>:</p>
<div style='overflow-x:auto;'><table style='width:100%;border-collapse:collapse;font-size:0.88em;'>
<tr style='background:#f5eef8;'><th style='padding:7px;'>Function</th><th style='padding:7px;'>Expressions</th></tr>
<tr><td style='padding:8px;border-top:1px solid #ddd;font-weight:600;color:#27ae60;'>Full agreement</td><td style='padding:8px;border-top:1px solid #ddd;'>Absolutely. / Exactly. / I couldn't agree more. / That's a very good point.</td></tr>
<tr><td style='padding:8px;border-top:1px solid #ddd;font-weight:600;color:#e67e22;'>Partial agreement</td><td style='padding:8px;border-top:1px solid #ddd;'>I see your point, but... / That's fair, although... / Yes, to an extent, though...</td></tr>
<tr><td style='padding:8px;border-top:1px solid #ddd;font-weight:600;color:#c0392b;'>Polite disagreement</td><td style='padding:8px;border-top:1px solid #ddd;'>I'm not sure I agree... / With respect, I think... / I'd push back on that slightly... / Actually, I'd argue that...</td></tr>
<tr><td style='padding:8px;border-top:1px solid #ddd;font-weight:600;color:#8e44ad;'>Opening debate</td><td style='padding:8px;border-top:1px solid #ddd;'>To play devil's advocate... / Let me challenge that... / Have we considered...?</td></tr>
</table></div>
<p style='margin-top:10px;'><strong>Structure for polite disagreement:</strong> Acknowledge → Soften → Counter → Evidence<br><em>"I see your point. However, I'd argue that explicit grammar instruction <strong>can</strong> be effective when combined with communicative tasks."</em></p>""",
 "tasks":[
  {"title":"Which function?","instr":"Identify whether each phrase agrees (A), partially agrees (P), or disagrees (D):<br>1. 'I couldn't agree more.' · 2. 'I see your point, but I'm not convinced.' · 3. 'With respect, I think that's an oversimplification.' · 4. 'That's absolutely right.'","ans":"1. A · 2. P · 3. D · 4. A"},
  {"title":"Complete the exchange","instr":"Fill the gap with an appropriate phrase:<br>A: 'Grammar translation is the most effective teaching method.'<br>B: '___, it has its place for exam classes, though I'd argue communicative approaches are more motivating for most learners.'","ans":"Possible: 'That's fair...' / 'I see your point...' / 'Yes, to an extent...' — any partial agreement opener works here."},
  {"title":"Rewrite rudely as politely","instr":"Make these disagreements professional:<br>1. 'You're wrong. That never works.' → I'm not sure...<br>2. 'That's a terrible idea.' → With respect...","ans":"1. 'I'm not sure I agree — in my experience, that approach can sometimes backfire.' · 2. 'With respect, I'd have some concerns about that approach. Could we consider...?'"},
 ],
 "production":"Write a 6-line mini-debate between two colleagues discussing whether all English lessons should be taught in English only. One agrees, one partly disagrees. Use at least 4 expressions from today's lesson."
},
{
 "title":"Writing Formal Emails in English: Structure and Tone",
 "level":"B2","framework":"PWP · Writing Skills",
 "tags":"B2 English, formal email writing, professional writing, B2 writing, 5-Minute English Lab",
 "seo_title":"How to Write a Formal Email in English: Structure and Tone | B2 Writing",
 "meta":"Learn the structure, openings, closings and tone for formal emails in English. B2 writing lesson with real examples.",
 "anecdote":"I've written hundreds of professional emails in English — to suppliers, VIP guests, head office. The one rule I wish someone had told me earlier: your email's first and last sentences carry 70% of the impression. Everything else is detail.",
 "aim":"write a well-structured formal email in English with correct opening, body, and closing — matched to the appropriate register.",
 "focus":["Dear Mr/Ms [surname]","I am writing to...","I would be grateful if...","Please do not hesitate to contact me","Yours sincerely / Yours faithfully","Kind regards"],
 "explanation":"""<p><strong>Structure of a formal email:</strong></p>
<ol>
<li><strong>Salutation:</strong> Dear Mr Smith, / Dear Dr Patel, (named) · Dear Sir/Madam, (unnamed)</li>
<li><strong>Opening line:</strong> State your purpose immediately: <em>I am writing to enquire about... / I am writing in response to...</em></li>
<li><strong>Body:</strong> One idea per paragraph. Short sentences. No contractions (<em>I am</em> not <em>I'm</em>).</li>
<li><strong>Request / action:</strong> <em>I would be grateful if you could... / Please find attached... / Could you please...</em></li>
<li><strong>Closing line:</strong> <em>Please do not hesitate to contact me if you require any further information.</em></li>
<li><strong>Sign-off:</strong> Yours sincerely (named recipient) · Yours faithfully (Dear Sir/Madam) · Kind regards (semi-formal)</li>
</ol>
<div style='background:#f5eef8;padding:10px;border-radius:6px;margin:10px 0;'><strong>Register reminder:</strong> Formal = no contractions, no phrasal verbs where possible, full sentences, polite structures (<em>would, could</em>). <em>I'd like</em> → <em>I would like</em>. <em>Can you</em> → <em>Could you please</em>.</div>""",
 "tasks":[
  {"title":"Formal or informal?","instr":"Rewrite these informal phrases in formal register:<br>1. 'Hi John, just checking in about our meeting.' → Dear...<br>2. 'Get back to me ASAP.' → I would...<br>3. 'Cheers!' → Yours...","ans":"1. Dear Mr [surname], / I am writing to follow up on our upcoming meeting. · 2. I would be grateful if you could reply at your earliest convenience. · 3. Yours sincerely, [Full name]"},
  {"title":"Spot 5 errors","instr":"Find 5 errors in this formal email opening:<br><em>'hi there! i'm writing about the job add i seen on your website. can you tell me more info about it? thanks'</em>","ans":"1. 'hi' → Dear Sir/Madam, (no capitalisation, wrong salutation) · 2. 'i'm' → I am (no contractions) · 3. 'add' → advertisement/advert · 4. 'i seen' → I saw (grammar) · 5. 'thanks' → I look forward to hearing from you. / Yours faithfully, [name]"},
  {"title":"Choose the right sign-off","instr":"Which sign-off is correct?<br>1. You wrote 'Dear Dr Moreau' → A) Yours faithfully B) Yours sincerely<br>2. You wrote 'Dear Sir/Madam' → A) Yours faithfully B) Yours sincerely<br>3. Semi-formal email to a colleague you know → A) Kind regards B) Yours sincerely","ans":"1. B — Yours sincerely (you know the name) · 2. A — Yours faithfully (you don't know the name) · 3. A — Kind regards (semi-formal and friendly)"},
 ],
 "production":"Write a formal email (6–8 sentences) to a hotel asking about room availability for a company event. Include: opening line, 2 questions, a polite request, and correct closing. Use no contractions."
},
{
 "title":"Future Forms: Plans, Predictions and Arrangements",
 "level":"B1","framework":"TTT · Grammar",
 "tags":"B1 English, future forms, will going to, B1 grammar, 5-Minute English Lab",
 "seo_title":"Future Forms in English: Will, Going To and Present Continuous | B1 Grammar",
 "meta":"Learn when to use will, going to and present continuous for the future. B1 English grammar with clear examples and practice.",
 "anecdote":"When I decided to leave Sydney and move to La Réunion, three different future forms described my situation: 'I'm going to resign' (plan), 'I'm leaving next month' (arrangement), and 'I think it'll be a good change' (prediction). All three futures, one life decision.",
 "aim":"choose between <em>will, going to</em> and present continuous to express future plans, predictions and arrangements.",
 "focus":["will (prediction/spontaneous decision)","going to (plan/intention)","present continuous (fixed arrangement)","I think it'll...","I've decided to / I'm planning to..."],
 "explanation":"""<p>English has three main ways to talk about the future — and the choice carries meaning:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.88em;margin:8px 0;'>
<tr style='background:#fef9e7;'><th style='padding:7px;text-align:left;'>Form</th><th style='padding:7px;text-align:left;'>Use</th><th style='padding:7px;text-align:left;'>Signal</th><th style='padding:7px;text-align:left;'>Example</th></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'><strong>will</strong></td><td style='padding:6px;border-top:1px solid #ddd;'>Prediction or spontaneous decision</td><td style='padding:6px;border-top:1px solid #ddd;'>I think... / probably / maybe</td><td style='padding:6px;border-top:1px solid #ddd;'>I think I'll take the job.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'><strong>going to</strong></td><td style='padding:6px;border-top:1px solid #ddd;'>Plan or intention (decided before now)</td><td style='padding:6px;border-top:1px solid #ddd;'>I've decided / I'm planning to</td><td style='padding:6px;border-top:1px solid #ddd;'>I'm going to resign next week.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'><strong>Pres. cont.</strong></td><td style='padding:6px;border-top:1px solid #ddd;'>Fixed arrangement (diary event)</td><td style='padding:6px;border-top:1px solid #ddd;'>tomorrow / next Tuesday</td><td style='padding:6px;border-top:1px solid #ddd;'>I'm flying to Paris tomorrow.</td></tr>
</table>
<p><strong>Evidence clue:</strong> If you can see evidence NOW that something will happen, use <em>going to</em>: <em>'Look at those clouds — it's going to rain.'</em></p>""",
 "tasks":[
  {"title":"Choose the right form","instr":"Will, going to, or present continuous?<br>1. 'I've booked my ticket. I ___ fly to London next Thursday.' (arrangement)<br>2. 'Look at the traffic — we ___ be late.' (evidence visible now)<br>3. 'The phone is ringing — don't move, I ___ answer it.' (spontaneous decision)","ans":"1. am flying (fixed arrangement) · 2. are going to be (evidence now) · 3. will answer (spontaneous)"},
  {"title":"Predict or plan?","instr":"What's the difference in meaning?<br>A) 'I'm going to study English this year.' vs B) 'I'll probably study English this year.'","ans":"A = a firm intention (already decided, plan made) · B = a looser prediction (less commitment, might not happen)"},
  {"title":"Your future","instr":"Write 3 sentences about your future using 3 different forms (one each: will / going to / present continuous).","ans":"Example: I think I'll improve my reading this year. (prediction) / I'm going to start an online course in September. (plan) / I'm meeting my language partner on Friday. (arrangement)"},
 ],
 "production":"Write a short paragraph (5 sentences) describing your plans for the next 3 months. Use all three future forms at least once each. Include one prediction, one firm plan, and one fixed arrangement."
},
{
 "title":"Job Interview English: Answering the 5 Key Questions",
 "level":"B1","framework":"TBL · Functional Language & Speaking",
 "tags":"B1 English, job interview, speaking English, professional English, 5-Minute English Lab",
 "seo_title":"Job Interview English: How to Answer the 5 Most Common Questions | B1",
 "meta":"Prepare for English job interviews with the 5 most common questions and model answers. B1 speaking and professional English lesson.",
 "anecdote":"I've been on both sides of the interview table. At Merivale in Sydney, I interviewed dozens of candidates. The ones who stood out weren't necessarily the most fluent — they were the ones who structured their answers with a clear beginning, middle and end. That structure is a learnable skill.",
 "aim":"answer the 5 most common English job interview questions using structured responses.",
 "focus":["Tell me about yourself","Why do you want this job?","What are your strengths?","Tell me about a challenge you overcame","Where do you see yourself in 5 years?"],
 "explanation":"""<p>Great interview answers have a structure. The most useful is the <strong>STAR method</strong> for experience-based questions:</p>
<div style='background:#fef9e7;padding:12px;border-radius:8px;margin:8px 0;'>
<strong>S</strong>ituation — Set the scene briefly<br>
<strong>T</strong>ask — What was your responsibility?<br>
<strong>A</strong>ction — What did YOU do? (use <em>I</em>, not <em>we</em>)<br>
<strong>R</strong>esult — What happened? Use numbers/evidence if possible.
</div>
<p><strong>Q1: 'Tell me about yourself'</strong> → Present → Past → Future: <em>'I currently work as... My background is in... I'm now looking for...'</em></p>
<p><strong>Q2: 'What are your strengths?'</strong> → Strength + Evidence + Relevance: <em>'I'm highly organised. For example, in my last role... This would help me in this position because...'</em></p>
<p><strong>Key language:</strong> <em>I'd say my main strength is... / In my previous role, I was responsible for... / I believe I could contribute by...</em></p>""",
 "tasks":[
  {"title":"STAR structure practice","instr":"A candidate answers: <em>'I once had to deal with a very difficult customer. I stayed calm. It worked out.'</em> Identify what is missing from the STAR structure and suggest what to add.","ans":"Missing: Situation (no context — which job? what exactly happened?), Task (what was their specific role?), Action (too vague — what exactly did they do? what words?), Result (no outcome — what happened? did the customer stay?). A better answer would specify each element with concrete detail."},
  {"title":"Answer structure","instr":"Put these sentences from a 'Tell me about yourself' answer in the correct Present → Past → Future order:<br>a) 'I'm now looking for a role where I can use my management experience in a training capacity.'<br>b) 'I currently work as a shift supervisor at a hotel in the city.'<br>c) 'Before that, I spent eight years in hospitality management in Sydney.'","ans":"Order: b (present) → c (past) → a (future/aim)"},
  {"title":"Improve the answer","instr":"Improve this weak answer to 'What is your biggest weakness?'<br><em>'I work too hard. I'm a perfectionist.'</em>","ans":"This is a cliché that sounds dishonest. A stronger answer names a real area of development with evidence you are working on it: 'I tend to take on too many tasks at once. I've been working on this by using a prioritised task list each morning — it has improved my focus and reduced end-of-day stress.'"},
 ],
 "production":"Write your answer to: <em>'Tell me about a challenge you overcame at work or in your studies.'</em> Use the STAR structure. Aim for 6–8 sentences. Then read it out loud once — fluency matters as much as content."
},
{
 "title":"Present Perfect vs Past Simple: Connecting Past and Present",
 "level":"B1","framework":"Guided Discovery · Grammar",
 "tags":"B1 English, present perfect, past simple, B1 grammar, 5-Minute English Lab",
 "seo_title":"Present Perfect vs Past Simple in English: The Key Difference | B1",
 "meta":"Understand the difference between the present perfect and past simple in English. B1 grammar lesson with clear rules and practice.",
 "anecdote":"Learning French to C1 level as an adult taught me something about tense: in French, the passé composé covers what English splits into two tenses. When I finally understood that the present perfect connects the past to NOW — that was the day both my French and my English teaching clicked into place.",
 "aim":"choose correctly between the present perfect and past simple by understanding the connection to the present.",
 "focus":["I have lived here for 3 years","I lived there in 2010","ever / never / already / yet","yesterday / last year / in 2005","How long have you...?","When did you...?"],
 "explanation":"""<p>The <strong>key question</strong>: is there a connection to the present moment?</p>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0;'>
<div style='background:#fef9e7;padding:12px;border-radius:8px;'>
<strong>✅ Present Perfect</strong><br><em>Connected to now</em><br><br>I <u>have lived</u> in Réunion for 3 years. (still here now)<br>I <u>have visited</u> Sydney. (life experience, no specific time)<br>She <u>has just finished</u>. (very recent)<br>Have you <u>ever</u> tried...?</div>
<div style='background:#ebf5fb;padding:12px;border-radius:8px;'>
<strong>✅ Past Simple</strong><br><em>Completed, no present connection</em><br><br>I <u>lived</u> in Sydney <u>in 2010</u>. (finished, I left)<br>She <u>arrived</u> <u>yesterday</u>. (specific past time)<br><u>When</u> did you go? (asks for specific time)<br>I <u>didn't see</u> him <u>last week</u>.</div>
</div>
<p><strong>Time word signals:</strong></p>
<p>Present Perfect: <em>ever / never / yet / already / just / since / for / recently / so far / today (if the day is not over)</em></p>
<p>Past Simple: <em>yesterday / last week/year / in 2019 / ago / when / at + time</em></p>""",
 "tasks":[
  {"title":"PPS or PS?","instr":"Choose the correct tense:<br>1. I ___ (live) in France since 2017. → Present Perfect or Past Simple?<br>2. She ___ (work) at The Ivy in 2013. → ?<br>3. We ___ never ___ (eat) here before. → ?<br>4. They ___ (arrive) yesterday. → ?","ans":"1. have lived (still living there — since = PP) · 2. worked (2013 = specific finished time) · 3. have never eaten (ever/never = PP) · 4. arrived (yesterday = specific past time = PS)"},
  {"title":"Spot the error","instr":"Find the mistake in each sentence:<br>1. 'I have seen her last Tuesday.'<br>2. 'Did you ever visit Australia?'<br>3. 'She has worked there in 2019.'","ans":"1. I <u>saw</u> her last Tuesday. (specific past time → past simple) · 2. <u>Have</u> you ever visited...? (ever → present perfect) · 3. She <u>worked</u> there in 2019. (specific year → past simple)"},
  {"title":"Question forms","instr":"Write one Present Perfect question and one Past Simple question about someone's travel experience.","ans":"PP: Have you ever been to Japan? / How long have you lived in France? · PS: When did you go to Japan? / Where did you travel last year?"},
 ],
 "production":"Write 6 sentences about your life: 3 using the present perfect (experiences, things that are still true, or recent events) and 3 using the past simple (specific, finished events with a time marker). Underline the time expressions you use."
},
{
 "title":"The Schwa: English's Most Common Sound",
 "level":"B1","framework":"PPP · Phonology",
 "tags":"B1 English, pronunciation, schwa sound, English phonology, 5-Minute English Lab",
 "seo_title":"The Schwa Sound in English: Why /ə/ Changes Everything | B1 Pronunciation",
 "meta":"Learn about the schwa — the most common sound in English — and how mastering it makes your pronunciation sound natural. B1 phonology lesson.",
 "anecdote":"When I was learning French to C1, the nasal vowels were my nemesis. But when I turned to teaching English, I discovered most learners have the opposite problem: they pronounce every vowel fully and clearly — which is exactly what makes English sound unnatural. The schwa changed everything for my students.",
 "aim":"identify the schwa /ə/ sound, produce it naturally, and understand why it is central to natural English pronunciation.",
 "focus":["/ə/ the schwa","unstressed syllables","natural speech vs careful speech","'a' / 'the' / 'to' / 'of' in connected speech"],
 "explanation":"""<p>The schwa /ə/ is the most common sound in spoken English. It is a <strong>neutral, unstressed vowel</strong> — somewhere between 'uh' and 'er'. No lip rounding, no tension. Just open and relaxed.</p>
<p><strong>Where does it appear?</strong> In <em>unstressed</em> syllables and small function words:</p>
<ul>
<li><strong>a</strong> → /ə/: <em>I want <u>a</u> coffee</em> → "I wanna <u>kh</u>offee" (the 'a' reduces)</li>
<li><strong>the</strong> → /ðə/: <em>pass me <u>the</u> salt</em> → 'thuh salt'</li>
<li><strong>of</strong> → /əv/: <em>a cup <u>of</u> tea</em> → 'a cup <u>uv</u> tea'</li>
<li><strong>to</strong> → /tə/: <em>I want <u>to</u> go</em> → 'I wanna go'</li>
</ul>
<p><strong>In longer words</strong>, unstressed syllables reduce to /ə/:</p>
<p><em>photographer</em> → pho-<strong>TO</strong>-gra-phər · <em>company</em> → <strong>COM</strong>-pə-ny · <em>banana</em> → bə-<strong>NA</strong>-nə</p>
<p><strong>Why it matters:</strong> If you say every vowel fully, you sound foreign but not 'wrong'. If you use schwas naturally, you sound like a native speaker. The schwa is the sound of English relaxing.</p>""",
 "tasks":[
  {"title":"Find the schwa","instr":"Mark the schwa /ə/ in these words. Each has at least one:<br>1. problem · 2. together · 3. important · 4. doctor · 5. comfortable","ans":"1. prob-ləm · 2. tə-geth-ər · 3. im-POR-tənt · 4. DOC-tər · 5. COMF-tə-bəl"},
  {"title":"Fast speech reduction","instr":"Say these phrases naturally at speed. Which sounds do you reduce to /ə/?<br>1. 'a cup of tea' · 2. 'I want to go' · 3. 'She's a teacher'","ans":"1. 'a' → /ə/ + 'of' → /əv/ → 'uh cup uv tea' · 2. 'to' → /tə/ → 'I wanna go' · 3. 'a' → /ə/ → 'She's uh teacher'"},
  {"title":"Listen and compare","instr":"Say these two versions of the same sentence and feel the difference:<br>Careful: 'I would like to have a cup of coffee.'<br>Natural: 'I'd like tuh have uh cup uv coffee.'<br>Which sounds more natural in conversation? Why?","ans":"The second version sounds more natural because English is a stress-timed language — stressed syllables are strong and regular, unstressed syllables (like function words) reduce to /ə/ to keep the rhythm consistent."},
 ],
 "production":"Record yourself (or say aloud) this sentence 3 times — once carefully, once at natural speed: <em>'I'd like to go to a restaurant for a cup of coffee and a piece of cake.'</em> Count how many schwas appear in the natural version. (Answer: at least 6)"
},
{
 "title":"Word Stress: Where to Put the BEAT",
 "level":"B1","framework":"PPP · Phonology",
 "tags":"B1 English, word stress, pronunciation, English phonology, stress patterns, 5-Minute English Lab",
 "seo_title":"Word Stress in English: How to Put the Beat in the Right Place | B1",
 "meta":"Learn English word stress rules and patterns. Discover how to stress two-syllable nouns vs verbs and how stress changes meaning. B1 phonology.",
 "anecdote":"In my sommelier training in Sydney, I once said 'deSERT' instead of 'DEssert' — ordering what I thought was a sweet and getting a sand dune. Stress changes meaning. That embarrassing moment became my best classroom example.",
 "aim":"identify and produce correct word stress in two-syllable words, especially where stress changes meaning or part of speech.",
 "focus":["DESert vs deSERT","REcord vs reCORD","INcrease vs inCREASE","noun stress vs verb stress","stress marks: ˈ"],
 "explanation":"""<p>English is a <strong>stress-timed language</strong> — each word has one syllable that is louder, longer and clearer than the others. Getting it wrong makes words unrecognisable, even if each sound is perfect.</p>
<p><strong>Key pattern — Noun vs Verb pairs:</strong><br>
Many two-syllable words shift stress depending on their grammatical role:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.88em;margin:8px 0;'>
<tr style='background:#fef9e7;'><th style='padding:7px;'>Word</th><th style='padding:7px;'>Noun stress</th><th style='padding:7px;'>Verb stress</th></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>record</td><td style='padding:6px;border-top:1px solid #ddd;'><strong>RE</strong>-cord (a record)</td><td style='padding:6px;border-top:1px solid #ddd;'>re-<strong>CORD</strong> (to record)</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>increase</td><td style='padding:6px;border-top:1px solid #ddd;'><strong>IN</strong>-crease (an increase)</td><td style='padding:6px;border-top:1px solid #ddd;'>in-<strong>CREASE</strong> (to increase)</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>present</td><td style='padding:6px;border-top:1px solid #ddd;'><strong>PRE</strong>-sent (a present)</td><td style='padding:6px;border-top:1px solid #ddd;'>pre-<strong>SENT</strong> (to present)</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>permit</td><td style='padding:6px;border-top:1px solid #ddd;'><strong>PER</strong>-mit (a permit)</td><td style='padding:6px;border-top:1px solid #ddd;'>per-<strong>MIT</strong> (to permit)</td></tr>
</table>
<p><strong>Common rule for longer words:</strong> Nouns ending in <em>-tion / -sion / -ity / -ic</em> stress the syllable <em>before</em> the suffix:<br><em>edu<strong>CA</strong>tion · na<strong>TION</strong>ality · pho<strong>NET</strong>ic</em></p>""",
 "tasks":[
  {"title":"Noun or verb stress?","instr":"Mark the stressed syllable. Is the word being used as a noun (N) or verb (V)?<br>1. 'Can I see your PER-mit?' · 2. 'They won't per-MIT photography.' · 3. 'We had a big IN-crease in sales.' · 4. 'Prices in-CREASED by 20%.'","ans":"1. PER-mit = N · 2. per-MIT = V · 3. IN-crease = N · 4. in-CREASE = V"},
  {"title":"Suffix stress rule","instr":"Apply the rule: stress the syllable BEFORE these suffixes (-tion, -ity, -ic). Mark the stress:<br>1. conversation · 2. university · 3. energetic · 4. nationality","ans":"1. conver-SA-tion · 2. uni-VER-sity · 3. ener-GET-ic · 4. nation-AL-ity"},
  {"title":"Minimal pair awareness","instr":"Say these pairs aloud and notice the difference in meaning:<br>A) I need a PER-mit. / They won't per-MIT it.<br>B) Here's the RE-cord. / Can you re-CORD this?","ans":"Both sentences use the same spelling but different stress — this changes the meaning AND the part of speech. In natural speech, native speakers use the stress to signal grammar before the sentence is even complete."},
 ],
 "production":"Choose 5 words from today's lesson. Write one sentence for each — once as a noun, once as a verb — and mark the stressed syllable in both versions. Then say them out loud. Can you feel and hear the difference?"
},
]

results = []
for i, lesson in enumerate(lessons):
    print(f"[{i+1}/{len(lessons)}] Posting: {lesson['title'][:60]}...")
    html = build_html(lesson)
    payload = {"title": lesson["title"], "content": html, "status": "draft",
               "category": "English Teaching", "tags": lesson["tags"],
               "meta_description": lesson["meta"], "seo_title": lesson["seo_title"]}
    try:
        r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
        data = r.json()
        post_id = data.get("post_id") or data.get("id") or "?"
        print(f"  ✅ {r.status_code} · ID: {post_id}")
        results.append({"title": lesson["title"], "status": r.status_code, "id": post_id})
    except Exception as e:
        print(f"  ❌ {e}")
    time.sleep(1.2)

ok = sum(1 for r in results if str(r.get("status")) == "200")
print(f"\n✅ {ok}/{len(results)} posted")
