#!/usr/bin/env python3
import requests, time

API_URL = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
HEADERS = {"X-Sourov-Key": "0767044896thevenet_", "Content-Type": "application/json"}
LC = {
    "A1":{"c":"#27ae60","bg":"#eafaf1","lbl":"A1 Beginner","em":"🌱"},
    "A2":{"c":"#2980b9","bg":"#ebf5fb","lbl":"A2 Elementary","em":"🌿"},
    "B1":{"c":"#e67e22","bg":"#fef9e7","lbl":"B1 Intermediate","em":"🌟"},
    "B2":{"c":"#8e44ad","bg":"#f5eef8","lbl":"B2 Upper-Intermediate","em":"⭐"},
    "C1":{"c":"#c0392b","bg":"#fdedec","lbl":"C1 Advanced","em":"🏆"},
    "Teachers":{"c":"#16a085","bg":"#e8f8f5","lbl":"CELTA Methodology","em":"🎓"},
    "Kids":{"c":"#d35400","bg":"#fdf2e9","lbl":"Young Learners","em":"🦋"},
}
FOOTER="<div style='background:#f8f9fa;padding:14px 28px;border-top:1px solid #eee;font-size:0.78em;color:#777;line-height:1.5;margin-top:24px;'><em>Independent teaching resource. Not affiliated with, endorsed by, or accredited by Cambridge University Press &amp; Assessment. Confers no qualification. Based on publicly available ELT methodology and 18 years of professional experience.</em></div>"

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
 "title":"The Art of the CCQ: Check Meaning Without Asking 'Do You Understand?'",
 "level":"Teachers","framework":"CELTA Technique · Concept Checking",
 "tags":"CELTA methodology, CCQ, concept checking questions, ELT teacher training, 5-Minute English Lab",
 "seo_title":"How to Write Great CCQs: CELTA Concept Checking Questions Explained",
 "meta":"Learn to write effective concept checking questions (CCQs) that verify understanding without asking 'do you understand?' CELTA teaching technique.",
 "anecdote":"During my 120 supervised teaching hours, my tutor wrote this on my feedback form: 'Good use of ICQs, but your CCQs are too close to the meaning.' That note taught me more about language analysis than any handbook. A bad CCQ just restates the sentence you just taught.",
 "aim":"write CCQs that genuinely check meaning — distinguishing them from translation requests, definition repeats, and yes/no dead-ends.",
 "focus":["What is a CCQ?","CCQ vs 'Do you understand?'","Writing effective CCQs","Testing meaning not form","3 CCQ types: binary / multiple choice / open"],
 "explanation":"""<p>A <strong>Concept Checking Question (CCQ)</strong> is a simple question the teacher asks to verify that learners have understood the <em>meaning</em> of a new language item — without asking them to repeat the definition or say 'yes.'</p>
<p><strong>Why not 'Do you understand?'?</strong> Because learners almost always say yes — even when they don't. It checks nothing.</p>
<p><strong>Three CCQ types:</strong></p>
<ol>
<li><strong>Binary (yes/no):</strong> True only if used with a follow-up. <em>'I've been working here since 2015. Am I still working here now? (Yes) Did I start in 2015? (Yes) Did I finish in 2015? (No)'</em></li>
<li><strong>Multiple choice:</strong> <em>'She told him she had finished. Did she finish before or after she told him? (Before)'</em></li>
<li><strong>Open:</strong> <em>'I might go to Paris. Is it certain? (No) Is it possible? (Yes) Am I decided? (No)'</em></li>
</ol>
<p><strong>Rules for a good CCQ:</strong> (a) Simpler language than the target item. (b) Checks the meaning, not the form. (c) Requires thought — not just repetition. (d) Usually 2–3 questions per item.</p>""",
 "tasks":[
  {"title":"Good CCQ or bad CCQ?","instr":"Evaluate each as Good (G) or Bad (B). If bad, say why.<br>1. 'What does <em>deadline</em> mean?' after teaching I missed the deadline. · 2. 'Was the deadline in the past? (yes) Did I meet it? (no) Do I still have time? (no)' · 3. 'Do you understand the present perfect?'","ans":"1. Bad — asks for a definition, not meaning-in-context · 2. Good — three binary questions that verify the three key meaning components (past event, failed obligation, consequence) · 3. Bad — yes/no with no check, learners will just say yes"},
  {"title":"Write CCQs for: 'I used to smoke'","instr":"Write 3 CCQs to check learners understand the meaning of 'used to + infinitive' (past habit, no longer true). Use simple language.","ans":"Do I smoke now? (No) Did I smoke in the past? (Yes) Did I smoke once or many times? (Many times — it was a habit) — These check: past, finished habit, repeated action."},
  {"title":"Fix this CCQ","instr":"Improve this CCQ for the phrase 'She had already left when I arrived.':<br><em>'Did she leave before or after you arrived?'</em><br>Is this sufficient? What's missing?","ans":"It's a good start but incomplete. Add: 'Was this in the past? (Yes) Did she leave and then I arrived, or did I arrive and then she left? (She left THEN I arrived — before is the key meaning) How do you know? (had already — the past perfect signals the earlier action)' — Always check the grammar signal, not just the meaning."},
 ],
 "production":"Choose a piece of target language you teach regularly (a grammar structure, a function, a lexical chunk). Write 3 CCQs for it — one binary, one multiple choice, one open. Test them on a colleague or say them aloud: do they check meaning or just restate it?"
},
{
 "title":"ICQs That Work: Giving Instructions Learners Actually Follow",
 "level":"Teachers","framework":"CELTA Technique · Classroom Management",
 "tags":"CELTA methodology, ICQ, instruction checking, classroom management ELT, 5-Minute English Lab",
 "seo_title":"ICQs: How to Give Instructions That Students Actually Follow | CELTA",
 "meta":"Learn to use Instruction Checking Questions (ICQs) to ensure learners understand tasks before they start. CELTA classroom management technique.",
 "anecdote":"My first solo teaching hour at The ELT Hub in Landerneau: I gave a pair-work instruction and half the class worked individually, half discussed in groups of four. I had not checked the instructions. The five minutes I lost recovering the task cost me the production stage. ICQs are cheap insurance.",
 "aim":"deliver clear, staged instructions and use ICQs to verify task understanding before learners begin.",
 "focus":["STAGE instructions (one at a time)","ICQ before the task","Demonstrate before you instruct","No more than 3 instruction steps","What are you doing? / Are you working alone or with a partner?"],
 "explanation":"""<p>An <strong>Instruction Checking Question (ICQ)</strong> is a short question asked <em>after</em> you give an instruction — and <em>before</em> learners start — to check they understood the task, not the language.</p>
<p><strong>The 4-step instruction sequence:</strong></p>
<ol>
<li><strong>Demonstrate</strong> (show, don't just tell — model the task yourself or with a strong student)</li>
<li><strong>Give the instruction</strong> — one step at a time, simple language, no more than 3 steps</li>
<li><strong>ICQ</strong> — check the most likely points of confusion</li>
<li><strong>Set a time limit</strong> ("You have 3 minutes.")</li>
</ol>
<p><strong>What to ICQ:</strong> Working alone or together? Reading or writing? Speaking or listening? How long? How many items?</p>
<p><strong>What NOT to ICQ:</strong> The content of the task itself ('What is the topic?' — that's a CCQ). ICQs are about <em>logistics</em>, not meaning.</p>
<div style='background:#e8f8f5;border-radius:6px;padding:10px;margin:8px 0;'><strong>Example:</strong><br><em>Instruction: 'Read the text and answer the three questions at the bottom. You have four minutes. Work individually.'</em><br><em>ICQs: 'Are you working alone or with a partner? How many questions are you answering? How long do you have?'</em></div>""",
 "tasks":[
  {"title":"ICQ or CCQ?","instr":"Decide if each question is an ICQ (checking instructions) or CCQ (checking meaning):<br>1. 'Are you writing or speaking?' · 2. 'Does <em>deadline</em> mean you have time or no time left?' · 3. 'How many sentences are you writing?' · 4. 'Did this happen before or after the other event?'","ans":"1. ICQ (logistics — speaking vs writing) · 2. CCQ (meaning of vocabulary) · 3. ICQ (number of items) · 4. CCQ (sequence meaning)"},
  {"title":"Write ICQs for this instruction","instr":"<em>'In pairs, take turns to describe your picture while your partner draws it. Don't show your picture to your partner. You have five minutes.'</em><br>Write 3 ICQs for this task.","ans":"1. Are you working alone or with a partner? (pairs — not groups) · 2. Can you show your picture to your partner? (No — this is the key rule) · 3. How long do you have? (5 minutes)"},
  {"title":"Fix the instruction","instr":"This instruction has 3 problems. Find them:<br><em>'OK, so now what I want you to do is read the text — it's quite long but don't worry about every word — and then answer the questions at the bottom, working together with a partner, if you have one, and try to finish before we have to move on.'</em>","ans":"Problems: 1. Too many steps at once — learners can't process it all · 2. Unclear time limit ('before we have to move on') · 3. Conditional pair work ('if you have one') creates ambiguity — just assign pairs. Fix: demonstrate first, then: 'Read the text. (pause) Answer the three questions. (pause) Work with a partner. (pause) You have four minutes. Go.'"},
 ],
 "production":"Write a complete instruction sequence for a reading task you use (or invent one). Include: (1) the demonstration step, (2) the staged instruction in 3 steps maximum, (3) 3 ICQs, (4) a time limit. Test it mentally: if a learner followed only your words and nothing else, would they do the right task?"
},
{
 "title":"PPP vs TBL: Choosing the Right Framework for Your Lesson",
 "level":"Teachers","framework":"CELTA Methodology · Lesson Planning",
 "tags":"CELTA methodology, PPP lesson plan, task-based learning TBL, lesson frameworks ELT, 5-Minute English Lab",
 "seo_title":"PPP vs TBL: Which Teaching Framework to Choose? | CELTA Lesson Planning",
 "meta":"Compare PPP and TBL lesson frameworks. Learn when to use Presentation-Practice-Production vs Task-Based Learning for ELT. CELTA methodology guide.",
 "anecdote":"My CELTA tutor told me: 'A hammer is not better than a screwdriver. They solve different problems.' I had been using PPP for every lesson, even when the aim was fluency. The lesson framework is a tool — and the tool must match the task.",
 "aim":"select the appropriate lesson framework (PPP, TBL, TTT or PWP) by matching it to the lesson aim and learner profile.",
 "focus":["PPP (Presentation-Practice-Production)","TBL (Task-Based Learning)","TTT (Test-Teach-Test)","PWP (Pre-While-Post) for skills","Main aim drives the framework"],
 "explanation":"""<p>There is no universally 'best' framework. Each serves a specific pedagogic purpose:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.87em;margin:8px 0;'>
<tr style='background:#e8f8f5;'><th style='padding:7px;text-align:left;'>Framework</th><th style='padding:7px;text-align:left;'>Best for</th><th style='padding:7px;text-align:left;'>Structure</th></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;'>PPP</td><td style='padding:7px;border-top:1px solid #ddd;'>Discrete grammar/lexis at lower levels; controlled language input</td><td style='padding:7px;border-top:1px solid #ddd;'>Present → Controlled practice → Freer production</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;'>TBL</td><td style='padding:7px;border-top:1px solid #ddd;'>Fluency; real-world tasks; higher levels; when outcome matters more than accuracy</td><td style='padding:7px;border-top:1px solid #ddd;'>Pre-task → Task → Report → Language focus → Practice</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;'>TTT</td><td style='padding:7px;border-top:1px solid #ddd;'>Revising grammar learners may already partly know; diagnosing gaps</td><td style='padding:7px;border-top:1px solid #ddd;'>Test (discover what they know) → Teach (fill the gaps) → Test again</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;'>PWP</td><td style='padding:7px;border-top:1px solid #ddd;'>Reading and listening skills lessons</td><td style='padding:7px;border-top:1px solid #ddd;'>Pre-task (activate schema) → While-task (gist then detail) → Post-task (respond/produce)</td></tr>
</table>
<p><strong>The decision rule:</strong> Start with your <em>main aim</em>. Is the aim accuracy with a specific structure (PPP)? Fluency with a communicative outcome (TBL)? Checking existing knowledge (TTT)? Developing a skill (PWP)? The aim selects the framework — not the other way round.</p>""",
 "tasks":[
  {"title":"Which framework?","instr":"Match the aim to the best framework:<br>1. Learners will be able to use the present perfect correctly to talk about life experiences. (A1-B1)<br>2. Learners will negotiate and reach a decision about a hotel booking. (B2)<br>3. Learners will develop their ability to identify key information in a listening text. (B1)<br>4. Learners will use reported speech correctly — they've seen it before but keep making errors.","ans":"1. PPP (discrete grammar, lower level, controlled input needed) · 2. TBL (real-world communicative task, fluency outcome) · 3. PWP (listening/reading skills lesson) · 4. TTT (revision — diagnose gaps first, then teach, then test again)"},
  {"title":"PPP in practice","instr":"A PPP lesson on 'should for advice' (A2). Sequence these stages in the correct order:<br>a) Learners roleplay giving advice to classmates about real problems. b) Teacher presents 'should/shouldn't' with a context (problem page). c) Learners complete gap-fill and transformation exercises.","ans":"b (Presentation) → c (Practice) → a (Production) — the teacher-controlled input comes first, then controlled practice, then freer use."},
  {"title":"TBL advantage","instr":"Why might TBL be MORE effective than PPP for a B2 class working on 'negotiating in meetings'?","ans":"TBL puts the communicative outcome first — learners discover which language they need through the task, making the subsequent language focus feel relevant and purposeful. PPP can feel artificial at B2 because learners often already have the form but lack the fluency to deploy it under pressure. TBL creates that pressure authentically."},
 ],
 "production":"Choose a piece of language or a skill you plan to teach soon. Write: (1) your main aim, (2) which framework you'll use and why, (3) the three main stages and what happens in each. Keep it to one paragraph — planning clarity beats planning length."
},
{
 "title":"Animals in English: A Colourful Cambridge Starters Lesson",
 "level":"Kids","framework":"PPP · Cambridge Young Learners Starters",
 "tags":"young learners, Cambridge Starters, animals vocabulary, kids English, 5-Minute English Lab",
 "seo_title":"Animals in English for Kids: Cambridge Starters Vocabulary Lesson 🦁",
 "meta":"Fun colourful lesson teaching 10 animal words for Cambridge Young Learners Starters level. With games, activities and pictures.",
 "anecdote":"My daughter is still small, but I already point at animals in books and say their names in English. Research is clear: early exposure to vocabulary — even before formal schooling — shapes a child's language map for life. This lesson is for the littlest learners.",
 "aim":"name 10 animals in English, say what sound they make, and play a simple animal guessing game.",
 "focus":["cat / dog / bird / fish","elephant / giraffe / lion / monkey","frog / rabbit","What animal is it? / It's a..."],
 "explanation":"""<div style='background:#fdf2e9;border-radius:10px;padding:16px;margin-bottom:14px;'>
<p style='font-size:1.1em;font-weight:700;color:#d35400;margin:0 0 10px;'>🎉 Let's Learn Animal Words!</p>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #f39c12;text-align:center;font-size:1.1em;'>🐱 cat</div>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #f39c12;text-align:center;font-size:1.1em;'>🐶 dog</div>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #f39c12;text-align:center;font-size:1.1em;'>🐦 bird</div>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #f39c12;text-align:center;font-size:1.1em;'>🐟 fish</div>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #e74c3c;text-align:center;font-size:1.1em;'>🐘 elephant</div>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #e74c3c;text-align:center;font-size:1.1em;'>🦒 giraffe</div>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #e74c3c;text-align:center;font-size:1.1em;'>🦁 lion</div>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #e74c3c;text-align:center;font-size:1.1em;'>🐒 monkey</div>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #27ae60;text-align:center;font-size:1.1em;'>🐸 frog</div>
<div style='background:#fff;padding:10px;border-radius:8px;border:2px solid #27ae60;text-align:center;font-size:1.1em;'>🐰 rabbit</div>
</div>
</div>
<p style='color:#555;'><strong>Say it out loud!</strong> Point to each animal and say its name twice — once quietly, once loudly! 🔊</p>
<p style='color:#555;'><strong>Animal sounds in English:</strong> cat → meow · dog → woof · frog → ribbit · lion → roar · bird → tweet</p>""",
 "tasks":[
  {"title":"🌈 Colour the sentence!","instr":"Complete the sentence for each animal. Colour or draw the animal after!<br>1. It's a ___. It says meow. 🐱<br>2. It's a ___. It's very big and grey. 🐘<br>3. It's a ___. It has a long neck. 🦒<br>4. It's a ___. It can swim. 🐟","ans":"1. cat · 2. elephant · 3. giraffe · 4. fish"},
  {"title":"🎲 Animal riddle game!","instr":"Read the clue and guess the animal!<br>1. I am yellow. I am big. I say ROAR! I am a... → ___<br>2. I am small. I am green. I jump! I say ribbit! I am a... → ___<br>3. I am brown. I love bananas. I live in a tree. I am a... → ___","ans":"1. lion 🦁 · 2. frog 🐸 · 3. monkey 🐒"},
  {"title":"👫 Ask your friend!","instr":"Ask someone (a friend, parent, or toy!) these questions:<br>→ 'What's your favourite animal?'<br>→ 'Is it big or small?'<br>→ 'What sound does it make?'<br>Practice saying: 'My favourite animal is a ___. It is ___. It says ___!'","ans":"Example: 'My favourite animal is a dog. It is small and brown. It says woof!' (Any answer is correct — this is speaking practice!)"},
 ],
 "production":"🎨 Draw your favourite animal from the list. Write its name underneath. Then write one sentence: <em>'It is a ___ . It is ___ [colour]. It is ___ [big/small].'</em> Show it to someone and say the sentence out loud!"
},
{
 "title":"What Did You Do Yesterday? Past Tense Fun for Kids",
 "level":"Kids","framework":"PPP · Cambridge Young Learners Movers",
 "tags":"young learners, Cambridge Movers, past tense kids, children English, 5-Minute English Lab",
 "seo_title":"Past Tense for Kids: What Did You Do Yesterday? Cambridge Movers 🌟",
 "meta":"Fun Cambridge Movers lesson teaching past simple to young learners. Activities, games and colourful practice for children learning English.",
 "anecdote":"Children learn past tense faster when it connects to THEIR day. I always start with: 'Yesterday, I woke up and... I made coffee and... I played with...' Then I pass it to them. Their stories are always better than mine.",
 "aim":"talk about past actions using simple past tense verbs — including 3 common irregular forms.",
 "focus":["played / watched / helped","ate / drank / went (irregular)","Yesterday I... / Last night I...","Did you...? / Yes, I did. / No, I didn't."],
 "explanation":"""<div style='background:#fdf2e9;border-radius:10px;padding:16px;margin-bottom:12px;'>
<p style='font-weight:700;color:#d35400;font-size:1.05em;margin:0 0 10px;'>🕐 Talking about YESTERDAY!</p>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>
<div style='background:#fff3cd;border-radius:8px;padding:10px;'>
<p style='margin:0 0 6px;font-weight:700;color:#e67e22;'>Regular verbs: add -ED</p>
play → <strong>played</strong><br>
watch → <strong>watched</strong><br>
help → <strong>helped</strong><br>
jump → <strong>jumped</strong>
</div>
<div style='background:#fce4ec;border-radius:8px;padding:10px;'>
<p style='margin:0 0 6px;font-weight:700;color:#c0392b;'>Irregular verbs: LEARN them! ⭐</p>
eat → <strong>ate</strong><br>
drink → <strong>drank</strong><br>
go → <strong>went</strong><br>
see → <strong>saw</strong>
</div>
</div>
</div>
<p style='color:#555;'><strong>How to say it:</strong></p>
<p style='background:#e8f8f5;padding:10px;border-radius:6px;color:#333;'>✅ Yesterday I <strong>played</strong> football.<br>✅ Last night I <strong>ate</strong> pizza.<br>✅ I <strong>went</strong> to the park.<br>❓ Did you <strong>watch</strong> TV? → Yes, I <strong>did</strong>. / No, I <strong>didn't</strong>.</p>""",
 "tasks":[
  {"title":"🔀 Mix and match!","instr":"Draw a line to match the verb with its past form:<br>go &nbsp;&nbsp;&nbsp;&nbsp;→ &nbsp;&nbsp;&nbsp;&nbsp;ate<br>eat &nbsp;&nbsp;&nbsp;&nbsp;→ &nbsp;&nbsp;&nbsp;&nbsp;played<br>play &nbsp;&nbsp;&nbsp;&nbsp;→ &nbsp;&nbsp;&nbsp;&nbsp;went<br>drink &nbsp;&nbsp;&nbsp;&nbsp;→ &nbsp;&nbsp;&nbsp;&nbsp;drank","ans":"go → went · eat → ate · play → played · drink → drank"},
  {"title":"🌟 True or false about YOU!","instr":"Write T (true) or F (false) about YOUR yesterday:<br>1. Yesterday I played a game. T / F<br>2. I ate pizza for dinner. T / F<br>3. I went to school. T / F<br>4. I watched TV. T / F<br>Then change the false ones to make them TRUE for you!","ans":"All answers depend on the learner — the key is using the past tense correctly. Encourage them to write: 'No, I didn't eat pizza. I ate rice.' etc."},
  {"title":"🎤 Question time!","instr":"Ask a friend (or write the answers yourself):<br>1. Did you play outside yesterday? → Yes, I ___ / No, I ___<br>2. What did you eat for breakfast? → I ___<br>3. Where did you go yesterday? → I ___","ans":"1. Yes, I did. / No, I didn't. · 2. I ate [bread / cereal / eggs...] · 3. I went to [school / the park / home...]"},
 ],
 "production":"🌈 Write or draw your <strong>YESTERDAY STORY</strong>! Use these sentence starters:<br><br>Yesterday I woke up and... → ___<br>Then I ate... → ___<br>After that I played / watched / went... → ___<br>At night I... → ___<br><br>Read it out loud! You can even make a little book with drawings! 📚"
},
{
 "title":"Connected Speech: How English Really Sounds",
 "level":"B2","framework":"PPP · Phonology",
 "tags":"B2 English, connected speech, pronunciation, linking sounds, natural English, 5-Minute English Lab",
 "seo_title":"Connected Speech in English: Linking, Elision and Assimilation | B2 Pronunciation",
 "meta":"Learn the three main features of connected speech — linking, elision and assimilation — to understand natural English and speak more fluently. B2 pronunciation lesson.",
 "anecdote":"When I moved to La Réunion, French people told me my English was 'too clear' — meaning I spoke like a textbook, not a human. Connected speech is what happens when fluency takes over: sounds link, some disappear, others change. Mastering it is the last mile of pronunciation.",
 "aim":"identify and produce three features of connected speech: linking, elision and assimilation.",
 "focus":["Linking: turn_on → 'turn-on'","Elision: next_door → 'nex door'","Assimilation: good_bye → 'goo-bye'","Weak forms: to / of / and","Intrusive /r/: law_and_order → 'lawr and order'"],
 "explanation":"""<p>In natural English speech, words do not arrive separately — they run together. Three main processes:</p>
<div style='display:grid;grid-template-columns:1fr;gap:10px;margin:10px 0;'>
<div style='background:#f5eef8;padding:12px;border-radius:8px;'>
<strong>1. LINKING</strong> — connecting a final consonant to the next vowel<br>
<em>'turn it on'</em> → 'tur-ni-ton' · <em>'an apple'</em> → 'a-napple'<br>
Rule: consonant + vowel → sounds merge smoothly</div>
<div style='background:#fef9e7;padding:12px;border-radius:8px;'>
<strong>2. ELISION</strong> — dropping a sound for speed<br>
<em>'next door'</em> → 'nex door' (the /t/ disappears)<br>
<em>'last night'</em> → 'las night' · <em>'sit down'</em> → 'si down'<br>
Rule: /t/ and /d/ often drop between two consonants</div>
<div style='background:#fdedec;padding:12px;border-radius:8px;'>
<strong>3. ASSIMILATION</strong> — one sound changes to match its neighbour<br>
<em>'good boy'</em> → 'goob boy' (d → b before b)<br>
<em>'ten pins'</em> → 'tem pins' (n → m before p)<br>
Rule: sounds at word boundaries borrow features from adjacent sounds</div>
</div>
<p><strong>Why it matters:</strong> Understanding these features is essential for listening comprehension. Without them, natural speech sounds like a blur — because you're hearing sounds that aren't in the textbook.</p>""",
 "tasks":[
  {"title":"Identify the feature","instr":"Which feature (linking / elision / assimilation) explains each?<br>1. 'not bad' sounds like 'nob bad' · 2. 'stand up' sounds like 'stan up' · 3. 'pick it up' sounds like 'pi-ki-tup'","ans":"1. Assimilation (t → b before b) · 2. Elision (d drops before up) · 3. Linking (k links to i, t links to u)"},
  {"title":"Fast speech challenge","instr":"Write the natural spoken version of these phrases:<br>1. 'I want to go.' · 2. 'Did you eat it?' · 3. 'He went back.'","ans":"1. 'I wanna go' (want to → wanna: elision + vowel reduction) · 2. 'Didja eat it?' (did you → didja: assimilation) · 3. 'He wen back' (went → wen: elision of t before b)"},
  {"title":"Listen for the difference","instr":"In careful speech vs connected speech, which sounds change or disappear in this sentence?<br>'I told him to stop it.'<br>Careful: /aɪ tɒld hɪm tuː stɒp ɪt/<br>Connected: 'aɪ tɒl-dɪm-tə-stɒp-ɪt'","ans":"Changes: 'told him' links (d links to h, h often weakens or drops) · 'to' reduces to /tə/ (weak form) · whole phrase runs together without gaps. The individual words are still intelligible but the boundaries dissolve at natural speed."},
 ],
 "production":"Say this sentence 3 times: <em>'I'd like to find out what time it opens.'</em><br>First: slowly, all sounds clear. Second: at natural speed. Third: at fast speed.<br>Notice which sounds link, which reduce, and which disappear. Write down what you hear yourself say — not what you see on the page."
},
{
 "title":"Discourse Markers: Signposting Your Ideas Like a Pro",
 "level":"B2","framework":"Guided Discovery · Grammar & Writing",
 "tags":"B2 English, discourse markers, linking words, academic writing, 5-Minute English Lab",
 "seo_title":"Discourse Markers in English: Link Your Ideas with Confidence | B2",
 "meta":"Learn to use discourse markers to connect ideas, signal structure and improve fluency in speaking and writing. B2 English lesson.",
 "anecdote":"When I briefed my team at Establishment before service, I learned to signal transitions: 'First, the VIP table... Furthermore, we have a dietary request... Finally, one important reminder...' Those markers kept a team of twelve focused. The same signals guide a reader through your writing.",
 "aim":"use discourse markers to signal contrast, addition, reason, result and exemplification in writing and speaking.",
 "focus":["However / Nevertheless / On the other hand","Furthermore / In addition / What is more","Therefore / As a result / Consequently","For example / For instance / Such as","In contrast / While / Whereas"],
 "explanation":"""<p>Discourse markers are <strong>signposts</strong> — they tell the reader/listener where the text is going. Without them, ideas feel disconnected. With them, even complex arguments become clear.</p>
<table style='width:100%;border-collapse:collapse;font-size:0.87em;margin:8px 0;'>
<tr style='background:#f5eef8;'><th style='padding:7px;text-align:left;'>Function</th><th style='padding:7px;text-align:left;'>Markers</th></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;'>Addition</td><td style='padding:7px;border-top:1px solid #ddd;'>Furthermore · In addition · Moreover · What is more</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;'>Contrast</td><td style='padding:7px;border-top:1px solid #ddd;'>However · Nevertheless · On the other hand · In contrast · While · Whereas</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;'>Result/Consequence</td><td style='padding:7px;border-top:1px solid #ddd;'>Therefore · As a result · Consequently · Hence</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;'>Exemplification</td><td style='padding:7px;border-top:1px solid #ddd;'>For example · For instance · Such as · To illustrate</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;'>Concession</td><td style='padding:7px;border-top:1px solid #ddd;'>Although · Even though · Despite (the fact that) · Admittedly</td></tr>
</table>
<p><strong>Punctuation rule:</strong> When a discourse marker starts a new sentence or clause, follow it with a comma: <em><u>However,</u> the results were different. / <u>Furthermore,</u> motivation plays a key role.</em></p>""",
 "tasks":[
  {"title":"Choose the right marker","instr":"Fill the gap with a suitable discourse marker:<br>1. 'The coffee was excellent. ___, the service was slow.' (contrast)<br>2. 'She speaks three languages. ___, she has lived in four countries.' (addition)<br>3. 'He didn't practise. ___, his performance suffered.' (result)","ans":"1. However / Nevertheless · 2. Furthermore / In addition · 3. As a result / Consequently / Therefore"},
  {"title":"Formal or informal?","instr":"Which version is more appropriate for an essay?<br>A) 'But the results were different.' vs B) 'However, the results were different.'<br>A) 'And it was very expensive.' vs B) 'Furthermore, it was considerably more expensive.'","ans":"B in both cases. 'But' and 'And' are informal/conversational. 'However' and 'Furthermore' are the academic/formal equivalents. In essays: avoid starting sentences with 'And', 'But', 'So'."},
  {"title":"Spot the error","instr":"Fix the mistake in each sentence:<br>1. 'The lesson was long however it was interesting.'<br>2. 'She failed the exam. Despite she studied hard.'<br>3. 'He works in London. On the other hand his family lives in Paris.'","ans":"1. '...long; <u>however,</u> it was interesting.' (semicolon or new sentence + comma after however) · 2. 'Despite <u>studying</u> hard, she failed.' (Despite + -ing, not Despite + clause) · 3. '...London. <u>However,</u>...' (On the other hand signals contrast, but grammatically needs a new sentence and comma)"},
 ],
 "production":"Write a short paragraph (5–6 sentences) comparing two approaches to language learning (e.g. self-study vs classroom learning, formal vs informal methods). Use at least 4 different discourse markers from today's lesson. Underline each one."
},
{
 "title":"Error Correction: When to Step In and When to Step Back",
 "level":"Teachers","framework":"CELTA Technique · Error Correction",
 "tags":"CELTA methodology, error correction, ELT feedback, teacher training, 5-Minute English Lab",
 "seo_title":"Error Correction in ELT: When to Correct and How to Do It | CELTA Guide",
 "meta":"Learn when to correct student errors and which correction techniques to use. CELTA error correction strategies for English teachers.",
 "anecdote":"My first year of teaching, I corrected every error the moment it appeared. Lessons became error-correction sessions. My students stopped speaking. The day I learned to hold a correction until the end of a fluency activity — and use it to teach the whole group — was the day my lessons improved.",
 "aim":"decide when to correct an error (immediately vs delayed) and apply three correction techniques (recast, elicit, metalinguistic).",
 "focus":["Accuracy vs fluency activities","Immediate correction","Delayed correction (board at end)","Recast: modelling the correct form","Eliciting: prompting self-correction","Metalinguistic: naming the error type"],
 "explanation":"""<p>The first decision in error correction is <strong>when</strong> — not how:</p>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0;'>
<div style='background:#e8f8f5;padding:12px;border-radius:8px;'>
<strong>✅ Correct immediately when:</strong><br>
• It's an accuracy-focused activity (controlled practice, drilling)<br>
• The error interferes with meaning<br>
• You just taught the item (so the error is diagnostic)
</div>
<div style='background:#fef9e7;padding:12px;border-radius:8px;'>
<strong>✅ Delay correction when:</strong><br>
• It's a fluency activity (roleplay, discussion, task)<br>
• Interrupting would break flow and confidence<br>
• You want the error to feed a whole-class focus at the end
</div>
</div>
<p><strong>Three correction techniques:</strong></p>
<ol>
<li><strong>Recast:</strong> Repeat the correct form without explicitly marking the error. <em>Student: 'I go there yesterday.' Teacher: 'Oh, you went there yesterday? What was it like?'</em> (Low risk, gentle — but students may not notice)</li>
<li><strong>Elicit:</strong> Prompt the student to self-correct. <em>'You went... or you go...?' / 'Can you say that again?' / raise an eyebrow, pause</em></li>
<li><strong>Metalinguistic:</strong> Name the problem. <em>'Watch your tense — is this past or present?' / 'Is that regular or irregular?'</em></li>
</ol>""",
 "tasks":[
  {"title":"Immediate or delayed?","instr":"Decide: correct immediately (I) or delay until after the activity (D)?<br>1. A learner makes a tense error during a grammar gap-fill exercise.<br>2. A learner mispronounces a word during a group roleplay.<br>3. A learner uses incorrect article during controlled drilling.<br>4. A learner makes a vocabulary error during a fluency discussion.","ans":"1. I (accuracy activity — correct now, it's the point of the exercise) · 2. D (fluency activity — note it, correct after) · 3. I (drilling is accuracy work) · 4. D (discussion is fluency — interrupting kills the task)"},
  {"title":"Which technique?","instr":"Match the teacher's response to the technique (recast / elicit / metalinguistic):<br>1. Student: 'I buyed a car.' Teacher: 'Oh, you <em>bought</em> a car! When?'<br>2. Student: 'I buyed a car.' Teacher: 'Hmm... buy is irregular. What's the past form?'<br>3. Student: 'I buyed a car.' Teacher: 'Is <em>buy</em> a regular or irregular verb?'","ans":"1. Recast (correct form modelled naturally) · 2. Elicit (prompt to self-correct, with a hint) · 3. Metalinguistic (draws attention to grammatical category without giving the answer)"},
  {"title":"Design a delayed correction slot","instr":"You've run a 10-minute fluency task. You noted these errors on your notepad: 'she go' / 'more better' / 'I am agree'. How do you use them at the end? Write a 3-step delayed correction sequence.","ans":"1. Write the 3 errors on the board anonymously (no names). 2. Ask class: 'Can you spot the error in each? What should it be?' Elicit corrections. 3. Board the correct forms: 'she GOES' / 'BETTER (no more)' / 'I AGREE'. Drill the correct form once if needed. Total time: 2–3 minutes."},
 ],
 "production":"Reflect on your last lesson (or a lesson you observed). Write: (1) one error you corrected immediately — was that the right choice? (2) one error you could have used for delayed correction — how would you deliver it? What correction technique would you use and why?"
},
{
 "title":"Intonation: Using Your Voice to Mean More",
 "level":"B1","framework":"PPP · Phonology",
 "tags":"B1 English, intonation, pronunciation, English phonology, falling rising intonation, 5-Minute English Lab",
 "seo_title":"English Intonation: Fall, Rise and Fall-Rise Explained | B1 Pronunciation",
 "meta":"Learn to use falling, rising and fall-rise intonation in English to express certainty, questions and nuance. B1 phonology lesson.",
 "anecdote":"Working the floor at Merivale, I learned that the same words said with different intonation can mean the opposite. 'Of course, sir' said with a falling tone means genuine agreement. Said with a rising tone — especially with a pause — means something closer to 'I doubt that very much.' Intonation is meaning.",
 "aim":"identify and produce three key intonation patterns: falling (statements/wh-questions), rising (yes/no questions) and fall-rise (incomplete thoughts / politeness).",
 "focus":["↘ Falling intonation (certainty, statements)","↗ Rising intonation (yes/no questions, lists)","↘↗ Fall-rise (polite requests, implication, uncertainty)","Tone units","Nuclear stress"],
 "explanation":"""<p>Intonation is the <strong>music of English</strong> — the rise and fall of pitch that signals meaning beyond the words themselves.</p>
<div style='display:grid;grid-template-columns:1fr;gap:10px;margin:10px 0;'>
<div style='background:#ebf5fb;padding:12px;border-radius:8px;'>
<strong>↘ FALLING TONE — certainty, statements, wh-questions</strong><br>
<em>'It's <strong>ready</strong>↘'</em> (statement — finished, certain)<br>
<em>'<strong>Where</strong>↘ did you go?'</em> (wh-question)<br>
<em>'<strong>Thanks</strong>↘'</em> (genuine, final)</div>
<div style='background:#fef9e7;padding:12px;border-radius:8px;'>
<strong>↗ RISING TONE — yes/no questions, surprise, lists (not last item)</strong><br>
<em>'Is it <strong>ready</strong>↗?'</em> (yes/no question)<br>
<em>'I'd like <strong>coffee</strong>↗, <strong>tea</strong>↗, and <strong>juice</strong>↘.'</em> (rising on each item except last)</div>
<div style='background:#fdedec;padding:12px;border-radius:8px;'>
<strong>↘↗ FALL-RISE — implication, incompleteness, politeness</strong><br>
<em>'Of <strong>course</strong>↘↗'</em> (but I'm not entirely sure / there's more to say)<br>
<em>'It's <strong>interesting</strong>↘↗'</em> (implies 'but I'm not convinced')<br>
<em>'Could you <strong>help</strong>↘↗ me?'</em> (polite request)</div>
</div>""",
 "tasks":[
  {"title":"Falling or rising?","instr":"Mark the intonation pattern (↘ or ↗) for each:<br>1. 'That's fantastic!' (genuine excitement)<br>2. 'Did you enjoy it?' (yes/no question)<br>3. 'Where are you from?' (wh-question)<br>4. 'We have tea, coffee, juice and water.' (items in a list — mark each)","ans":"1. ↘ (falling — certain, expressive) · 2. ↗ (rising — yes/no) · 3. ↘ (falling — wh-questions fall) · 4. tea↗, coffee↗, juice↗, water↘ (rising on each except the final item)"},
  {"title":"What does the intonation mean?","instr":"Same words, different intonation. What does each signal?<br>A) 'That's <strong>great</strong>↘' · B) 'That's <strong>great</strong>↘↗'","ans":"A) Genuine enthusiasm — the tone falls firmly, the speaker is satisfied. B) Fall-rise signals reservation — 'That's great... BUT' or 'That's great... for YOU.' The fall-rise is the 'yes but' intonation."},
  {"title":"Practise politeness","instr":"Say this sentence twice with different tones and notice the effect on meaning:<br>'Could you come back later?'<br>Version A: strong fall on 'later' · Version B: fall-rise on 'later'","ans":"A) Direct, almost an instruction — could sound abrupt · B) Polite request, slightly tentative — signals the speaker is being considerate of the listener. In hospitality and professional contexts, fall-rise is often more appropriate than a firm fall."},
 ],
 "production":"Record yourself (or say aloud) having a conversation — even with yourself. Say these three things and pay attention to your intonation:<br>1. A definite statement about your plans.<br>2. A yes/no question to a friend.<br>3. A polite request to a colleague.<br>After each one, ask: did my voice rise, fall, or both?"
},
{
 "title":"Complex Noun Phrases: Pack More Into Every Sentence",
 "level":"C1","framework":"Guided Discovery · Grammar",
 "tags":"C1 English, complex noun phrases, advanced grammar, academic writing C1, 5-Minute English Lab",
 "seo_title":"Complex Noun Phrases in English: Advanced Grammar for C1 Writers",
 "meta":"Learn to build and use complex noun phrases to write with greater precision and economy. C1 advanced English grammar lesson.",
 "anecdote":"I worked on my CELTA written assignments at night, after hotel shifts that lasted until 2am. When I read back my early drafts, each idea occupied a full sentence. When I learned to compress information into noun phrases — 'the decision to appeal the result' instead of 'I decided to appeal and this was because the result was wrong' — the writing tightened instantly.",
 "aim":"build complex noun phrases using pre-modifiers and post-modifiers (relative clauses, participle phrases, infinitives) to write with greater density and precision.",
 "focus":["pre-modifiers: adj + noun","post-modifiers: n + prep phrase","n + relative clause","n + participle phrase","n + infinitive (purpose)"],
 "explanation":"""<p>A noun phrase is any phrase where a noun is the head word. In academic and professional writing, we pack information around the noun rather than spreading it across multiple sentences:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.87em;margin:8px 0;'>
<tr style='background:#fdedec;'><th style='padding:7px;text-align:left;'>Type</th><th style='padding:7px;text-align:left;'>Structure</th><th style='padding:7px;text-align:left;'>Example</th></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;'>Pre-modification</td><td style='padding:7px;border-top:1px solid #ddd;'>adj + adj + NOUN</td><td style='padding:7px;border-top:1px solid #ddd;'>a <u>detailed, evidence-based</u> <strong>report</strong></td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;'>Post-mod: prepositional</td><td style='padding:7px;border-top:1px solid #ddd;'>NOUN + prep phrase</td><td style='padding:7px;border-top:1px solid #ddd;'>the <strong>decision</strong> <u>on the appeal</u></td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;'>Post-mod: relative clause</td><td style='padding:7px;border-top:1px solid #ddd;'>NOUN + which/who/that</td><td style='padding:7px;border-top:1px solid #ddd;'>the <strong>evidence</strong> <u>that was submitted</u></td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;'>Post-mod: participle phrase</td><td style='padding:7px;border-top:1px solid #ddd;'>NOUN + -ing/-ed</td><td style='padding:7px;border-top:1px solid #ddd;'>a <strong>system</strong> <u>designed to maximise efficiency</u></td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;'>Post-mod: infinitive</td><td style='padding:7px;border-top:1px solid #ddd;'>NOUN + to infinitive</td><td style='padding:7px;border-top:1px solid #ddd;'>the <strong>decision</strong> <u>to appeal</u></td></tr>
</table>
<p><strong>Economy:</strong> 'The report was detailed and based on evidence' (11 words) → 'a detailed, evidence-based report' (4 words). Noun phrases compress writing without losing meaning.</p>""",
 "tasks":[
  {"title":"Identify the head noun and modifiers","instr":"Underline the head noun and bracket the modifiers:<br>1. 'the rapidly increasing demand for English teachers in non-Anglophone countries'<br>2. 'a carefully designed assessment tool used in professional development settings'","ans":"1. <u>demand</u> [rapidly increasing] [for English teachers] [in non-Anglophone countries] · 2. <u>tool</u> [carefully designed assessment] [used in professional development settings]"},
  {"title":"Compress the sentences","instr":"Reduce each pair to a single complex noun phrase:<br>1. 'The feedback was positive. It came from the examiners.' → the feedback [from...]<br>2. 'There was a decision. They decided to review the policy.' → the decision [to...]<br>3. 'The teachers were experienced. They were working with mixed-ability groups.' → experienced teachers [working...]","ans":"1. the positive feedback from the examiners · 2. the decision to review the policy · 3. experienced teachers working with mixed-ability groups"},
  {"title":"Build the noun phrase","instr":"Build the most complex noun phrase you can for the word <em>approach</em>. Start simple and add one modifier at a time:<br>Basic: an approach → add an adjective → add a prepositional phrase → add a participle phrase","ans":"an approach → a <u>communicative</u> approach → a communicative approach <u>to grammar teaching</u> → a communicative approach to grammar teaching <u>grounded in task-based methodology</u>"},
 ],
 "production":"Rewrite this paragraph, replacing simple sentences with complex noun phrases wherever possible:<br><em>'The method was effective. It had been tested. Many teachers used it. The results were significant. The researchers had documented them carefully.'</em><br>Aim for 2–3 sentences instead of 5."
},
]

results = []
for i, L in enumerate(lessons):
    print(f"[{i+1}/{len(lessons)}] {L['title'][:60]}...")
    html = build_html(L)
    payload = {"title":L["title"],"content":html,"status":"draft","category":"English Teaching",
               "tags":L["tags"],"meta_description":L["meta"],"seo_title":L["seo_title"]}
    try:
        r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
        pid = r.json().get("post_id") or r.json().get("id") or "?"
        print(f"  ✅ {r.status_code} · ID {pid}")
        results.append((r.status_code, pid, L["title"]))
    except Exception as e:
        print(f"  ❌ {e}")
    time.sleep(1.2)

ok = sum(1 for r in results if str(r[0])=="200")
print(f"\n✅ {ok}/{len(results)} posted")
for r in results: print(f"  {r[0]} | ID {r[1]} | {r[2][:50]}")
