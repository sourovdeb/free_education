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
    return f"<div style='margin:12px 0;padding:14px 16px;background:#fff;border-left:4px solid {c};border-radius:0 8px 8px 0;box-shadow:0 1px 4px rgba(0,0,0,0.06);'><p style='margin:0 0 6px;font-weight:700;color:{c};'>Task {i}: {t['title']}</p><p style='margin:0 0 8px;color:#555;line-height:1.55;'>{t['instr']}</p><details><summary style='cursor:pointer;color:{c};font-size:0.88em;font-weight:600;'>Show answer</summary><div style='padding:10px;background:{bg};border-radius:6px;margin-top:8px;color:#444;line-height:1.55;'>{t['ans']}</div></details></div>"

def build_html(L):
    lv=LC[L["level"]]; c,bg=lv["c"],lv["bg"]
    tasks_html="".join(task_block(t,c,bg,i+1) for i,t in enumerate(L["tasks"]))
    focus_html="".join(pill(f,c) for f in L.get("focus",[]))
    focus_sec=f"<div style='padding:0 28px 16px;'><p style='margin:0 0 8px;font-weight:700;color:#333;font-size:0.85em;text-transform:uppercase;letter-spacing:0.5px;'>Language Focus:</p>{focus_html}</div>" if focus_html else ""
    return f"""<div style='font-family:"Segoe UI",Arial,sans-serif;max-width:820px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.09);'>
<div style='background:{c};padding:26px 28px;color:#fff;'>
  <p style='margin:0;font-size:0.82em;opacity:0.85;letter-spacing:1px;text-transform:uppercase;'>5-Minute English Lab &middot; {lv["lbl"]}</p>
  <h1 style='margin:6px 0 0;font-size:1.55em;line-height:1.2;'>{lv["em"]} {L["title"]}</h1>
  <p style='margin:10px 0 0;opacity:0.9;font-size:0.9em;'>&#9201; 5 minutes &middot; {L["framework"]}</p>
</div>
<div style='background:{bg};padding:16px 28px;border-left:5px solid {c};'>
  <p style='margin:0;color:#444;font-style:italic;line-height:1.6;'><strong>From my own experience:</strong> {L["anecdote"]}</p>
</div>
<div style='padding:20px 28px 10px;'>
  <div style='background:{bg};border-radius:8px;padding:13px 16px;border:1px solid {c}40;'>
    <p style='margin:0;color:{c};font-weight:700;'>By the end of this 5 minutes, you can:</p>
    <p style='margin:6px 0 0;color:#333;'>{L["aim"]}</p>
  </div>
</div>
{focus_sec}
<div style='padding:10px 28px 6px;'>
  <h2 style='color:{c};font-size:1.05em;margin:0 0 10px;border-bottom:2px solid {c}30;padding-bottom:7px;'>Quick Explanation</h2>
  <div style='color:#333;line-height:1.65;'>{L["explanation"]}</div>
</div>
<div style='padding:14px 28px 6px;'>
  <h2 style='color:{c};font-size:1.05em;margin:0 0 6px;border-bottom:2px solid {c}30;padding-bottom:7px;'>Practice</h2>
  {tasks_html}
</div>
<div style='padding:14px 28px 6px;'>
  <h2 style='color:{c};font-size:1.05em;margin:0 0 8px;border-bottom:2px solid {c}30;padding-bottom:7px;'>Use It Now</h2>
  <div style='background:{bg};border-radius:8px;padding:14px 16px;color:#444;line-height:1.65;'>{L["production"]}</div>
</div>
<div style='padding:14px 28px 20px;'>
  <label style='display:flex;align-items:center;gap:9px;margin:5px 0;cursor:pointer;color:#444;'><input type='checkbox' style='width:17px;height:17px;accent-color:{c};'> I understand the main language point</label>
  <label style='display:flex;align-items:center;gap:9px;margin:5px 0;cursor:pointer;color:#444;'><input type='checkbox' style='width:17px;height:17px;accent-color:{c};'> I completed at least one practice task</label>
  <label style='display:flex;align-items:center;gap:9px;margin:5px 0;cursor:pointer;color:#444;'><input type='checkbox' style='width:17px;height:17px;accent-color:{c};'> I tried the production task</label>
</div>
{FOOTER}</div>"""

lessons = [
{
 "title":"Register and Style: Switching Between Formal and Informal English",
 "level":"C1","framework":"Guided Discovery · Language Awareness",
 "tags":"C1 English, register formal informal, language style, advanced English writing, 5-Minute English Lab",
 "seo_title":"Register in English: Formal vs Informal Language | C1 Advanced Lesson",
 "meta":"Master register in English — how to switch between formal and informal language depending on context. C1 advanced language awareness lesson.",
 "anecdote":"Four languages in one head means four different registers per language. In Bengali I speak differently to my mother than to a colleague. In English, I learned the same rule applies: the language you use to a hotel guest at 2am is not the language you use in a board report. Register is not about being posh — it is about being precise.",
 "aim":"identify the features of formal and informal register and rewrite texts appropriately for a given audience and context.",
 "focus":["Formal: no contractions, full verb forms, latinate vocabulary","Informal: contractions, phrasal verbs, colloquial lexis","Neutral/semi-formal: professional but accessible","Register markers: nominalisation, passivisation, hedging"],
 "explanation":"""<p>Register is the variety of language used in a particular social context. The same idea can be expressed at many levels of formality:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.87em;margin:8px 0;'>
<tr style='background:#fdedec;'><th style='padding:7px;text-align:left;'>Register</th><th style='padding:7px;text-align:left;'>Features</th><th style='padding:7px;text-align:left;'>Example</th></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;color:#c0392b;'>Formal (academic/legal)</td><td style='padding:7px;border-top:1px solid #ddd;'>Nominalisation, passive voice, hedging, Latinate lexis, no contractions</td><td style='padding:7px;border-top:1px solid #ddd;'>The implementation of this policy has resulted in significant improvement.</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;color:#e67e22;'>Professional (neutral)</td><td style='padding:7px;border-top:1px solid #ddd;'>Clear, direct, polite; some contractions acceptable; concrete vocabulary</td><td style='padding:7px;border-top:1px solid #ddd;'>The new policy has improved results significantly.</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;font-weight:600;color:#27ae60;'>Informal (conversational)</td><td style='padding:7px;border-top:1px solid #ddd;'>Contractions, phrasal verbs, ellipsis, colloquialisms</td><td style='padding:7px;border-top:1px solid #ddd;'>The new policy's really worked. Things are way better now.</td></tr>
</table>
<p><strong>Key formal feature — nominalisation:</strong> converting verbs/adjectives into nouns: <em>improve → improvement, decide → decision, analyse → analysis</em>. This is one of the fastest ways to shift your register upward.</p>""",
 "tasks":[
  {"title":"Identify the register","instr":"Classify each text as formal (F), neutral (N) or informal (I):<br>1. 'Hey, just letting you know the meeting's been moved to Friday.'<br>2. 'This communication serves to notify you that the scheduled meeting has been rescheduled.'<br>3. 'Please note that the meeting has been moved to Friday, 14th June.'","ans":"1. Informal (contractions, casual opener) · 2. Formal (nominalisation, latinate vocabulary, passive) · 3. Neutral/professional (clear, polite, no contractions in key parts)"},
  {"title":"Formalise the text","instr":"Rewrite this informal email opening in a formal register:<br>'Hi! I got your email about the job and I really want to apply. I think I'd be great for this and I've done loads of similar stuff before.'","ans":"Dear [Name], / I am writing in response to your recent advertisement for the above position. I am very interested in applying and believe I have the relevant experience and skills required for this role."},
  {"title":"Spot the register mismatch","instr":"This formal report has one sentence that is the wrong register. Find it:<br>'The survey results indicate a significant increase in customer satisfaction. Service quality has improved across all departments. The team totally smashed it this quarter. This improvement can be attributed to the new training programme.'","ans":"'The team totally smashed it this quarter' is informal (colloquial phrasal verb). Replace with: 'All departments demonstrated exceptional performance this quarter.' or 'Performance across all teams exceeded targets this quarter.'"},
 ],
 "production":"Write the same piece of information twice — once in formal register (for a written report or professional email), once in informal register (for a message to a close colleague). Information: a project has been delayed by two weeks because of a supplier issue. Keep each version to 3 sentences."
},
{
 "title":"Cohesion and Coherence: Making Your Writing Flow",
 "level":"C1","framework":"PWP · Writing Skills",
 "tags":"C1 English, cohesion coherence, academic writing, advanced writing C1, 5-Minute English Lab",
 "seo_title":"Cohesion vs Coherence in Academic Writing: The Key Difference | C1",
 "meta":"Understand the difference between cohesion and coherence and learn to apply both to produce fluent, connected academic writing. C1 writing lesson.",
 "anecdote":"When I wrote my first CELTA assignment, my tutor marked it: 'Ideas are good — but where is the thread? I lose you between paragraphs.' That was the day I understood that having good ideas is not enough. They must connect. Cohesion is the stitching that holds a piece of writing together.",
 "aim":"distinguish cohesion from coherence and apply six cohesive devices to produce connected, reader-friendly academic writing.",
 "focus":["Reference: it, this, they, such","Substitution: one, do so","Ellipsis: implied words","Lexical cohesion: synonyms, hyponyms","Conjunction: because, although, when","Paragraph coherence: one idea per paragraph"],
 "explanation":"""<p><strong>Coherence</strong> = logical organisation of ideas (macro level — does the argument make sense?)<br>
<strong>Cohesion</strong> = linguistic connections between sentences and clauses (micro level — do the words point to each other?)</p>
<p>A text can be coherent but not cohesive (good ideas, no connectors) or cohesive but not coherent (lots of connectors, no clear logic). Both are needed.</p>
<p><strong>Six cohesive devices:</strong></p>
<ol>
<li><strong>Reference:</strong> <em>The teacher explained the rule. <u>She</u> then checked understanding.</em> (she = the teacher)</li>
<li><strong>Substitution:</strong> <em>The first method was effective. The second <u>one</u> less so.</em></li>
<li><strong>Ellipsis:</strong> <em>He couldn't attend, but she <u>[could]</u>.</em></li>
<li><strong>Lexical cohesion:</strong> <em>The lesson began. The <u>class</u> was quiet. <u>Students</u> listened carefully.</em> (synonymous chain)</li>
<li><strong>Conjunction:</strong> <em>Although motivation is key, <u>it</u> alone is insufficient.</em></li>
<li><strong>Theme/rheme structure:</strong> End each sentence on new information; start the next sentence from that new information.</em></li>
</ol>""",
 "tasks":[
  {"title":"Identify the cohesive device","instr":"Name the device used in each pair:<br>1. 'The report was submitted. It covered three areas.' · 2. 'Some students prefer PPP. Others prefer TBL.' · 3. 'The method proved effective. This effectiveness was noted in all three studies.'","ans":"1. Reference (it = the report) · 2. Substitution (Others = some students; implied parallel) · 3. Lexical cohesion / nominalisation (effectiveness picks up on effective and develops the idea)"},
  {"title":"Improve cohesion","instr":"Rewrite these sentences to improve cohesion. Use reference, substitution or lexical cohesion:<br><em>Language learning takes time. Language learning requires practice. Language learning is rewarding. Language learning is worth the effort.</em>","ans":"Language learning takes time and practice. It is, however, deeply rewarding — and ultimately worth every hour invested. (Reference: it; ellipsis: removed repetition; conjunction: however)"},
  {"title":"Coherence check","instr":"Read this paragraph. Is it coherent? Identify the problem:<br><em>Motivation is a key factor in language learning success. The history of language teaching includes many methods. Students who are motivated tend to achieve better outcomes. However, some methods are more effective than others.</em>","ans":"Not coherent — the paragraph has two unrelated topics (motivation AND methods) with no clear connection between them. A coherent paragraph should develop ONE idea. Split into two paragraphs, or choose one focus: either motivation OR methods, and make every sentence develop that one point."},
 ],
 "production":"Write a short paragraph (5 sentences) arguing for or against one teaching method. Apply three cohesive devices deliberately — use reference at least once, a lexical chain, and one conjunction. Then underline each cohesive device and label it."
},
{
 "title":"Colours and Taste: Describing Wine and Food in English",
 "level":"A1","framework":"PPP · Vocabulary",
 "tags":"A1 English, colours vocabulary, food adjectives, beginner English, 5-Minute English Lab",
 "seo_title":"Colours and Taste Words in English: Food and Drink Vocabulary | A1",
 "meta":"Learn colour words and taste adjectives in English through food and drink. A1 vocabulary lesson with interactive activities.",
 "anecdote":"Becoming a sommelier in Sydney taught me something unexpected: every wine tasting begins with colour. Red, white, rosé, deep ruby, pale gold. The vocabulary of colour is also the vocabulary of observation — and observation is the beginning of description in any language.",
 "aim":"name 8 colours and 6 taste adjectives in English and use them to describe food and drink.",
 "focus":["red / white / rosé / golden","sweet / dry / sour / bitter / spicy / fresh","It tastes...","It looks...","I like / I don't like"],
 "explanation":"""<div style='background:#eafaf1;border-radius:10px;padding:16px;margin-bottom:12px;'>
<p style='font-weight:700;color:#27ae60;font-size:1.05em;margin:0 0 10px;'>Colours in English</p>
<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px;text-align:center;'>
<div style='background:#e74c3c;color:#fff;padding:10px;border-radius:8px;font-weight:600;'>red</div>
<div style='background:#fff;border:2px solid #ccc;padding:10px;border-radius:8px;font-weight:600;'>white</div>
<div style='background:#f1c40f;color:#333;padding:10px;border-radius:8px;font-weight:600;'>yellow</div>
<div style='background:#e8b4b8;padding:10px;border-radius:8px;font-weight:600;'>pink</div>
<div style='background:#27ae60;color:#fff;padding:10px;border-radius:8px;font-weight:600;'>green</div>
<div style='background:#3498db;color:#fff;padding:10px;border-radius:8px;font-weight:600;'>blue</div>
<div style='background:#8b4513;color:#fff;padding:10px;border-radius:8px;font-weight:600;'>brown</div>
<div style='background:#f8f9fa;border:2px solid #ccc;padding:10px;border-radius:8px;font-weight:600;'>gold</div>
</div>
</div>
<p><strong>Taste adjectives:</strong></p>
<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:10px;'>
<div style='background:#fef9e7;padding:8px;border-radius:6px;text-align:center;'>sweet (honey, cake)</div>
<div style='background:#fdedec;padding:8px;border-radius:6px;text-align:center;'>sour (lemon, yoghurt)</div>
<div style='background:#ebf5fb;padding:8px;border-radius:6px;text-align:center;'>bitter (dark chocolate, coffee)</div>
<div style='background:#fdf2e9;padding:8px;border-radius:6px;text-align:center;'>spicy (chilli, curry)</div>
<div style='background:#eafaf1;padding:8px;border-radius:6px;text-align:center;'>fresh (mint, salad)</div>
<div style='background:#f5eef8;padding:8px;border-radius:6px;text-align:center;'>dry (wine, crackers)</div>
</div>
<p><strong>Sentence pattern:</strong> It is + colour. It tastes + adjective. I like/don't like it.</p>""",
 "tasks":[
  {"title":"Match the colour","instr":"What colour are these things?<br>1. an orange · 2. a lemon · 3. grass · 4. coffee with milk · 5. the sea · 6. a strawberry","ans":"1. orange (bonus: it is called an orange!) · 2. yellow · 3. green · 4. brown · 5. blue · 6. red"},
  {"title":"Which taste?","instr":"Which taste adjective fits?<br>1. You eat dark chocolate. It is ___ but also a little ___.<br>2. You drink espresso. It is ___ and strong.<br>3. You eat a lemon. It is very ___!","ans":"1. bitter / sweet · 2. bitter · 3. sour"},
  {"title":"Describe your drink","instr":"Look at a drink you have nearby (water, tea, coffee, juice). Write 3 sentences:<br>1. It is ___. (colour)<br>2. It tastes ___. (taste adjective)<br>3. I like it / I don't like it.","ans":"Example: It is dark brown. It tastes bitter. I like it. (espresso)"},
 ],
 "production":"Write a short description of your favourite food or drink (3-4 sentences). Use a colour word AND a taste word. Start with: <em>My favourite [food/drink] is ___. It is ___. It tastes ___. I like it because...</em>"
},
{
 "title":"Where Are You From? Countries, Nationalities and Languages",
 "level":"A2","framework":"PPP · Vocabulary & Speaking",
 "tags":"A2 English, nationalities vocabulary, countries languages, 5-Minute English Lab, beginner speaking",
 "seo_title":"Countries, Nationalities and Languages in English | A2 Vocabulary Lesson",
 "meta":"Learn country names, nationalities and language names in English. A2 vocabulary lesson with patterns, exceptions and speaking practice.",
 "anecdote":"I am Bangladeshi. I grew up speaking Bengali. I live in France, in La Réunion, and my daughter hears English, French and Bengali before she can even read. Nationality, language, and identity are three different things in English — and they each have their own grammar.",
 "aim":"say where you are from, your nationality, and the language you speak — including the common spelling patterns and exceptions.",
 "focus":["I am from [country].","I am [nationality].","I speak [language].","England → English","France → French","Bangladesh → Bengali (not Bangladeshi!)"],
 "explanation":"""<p>In English, <strong>country, nationality, and language</strong> are three different words — and they are not always predictable:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.87em;margin:8px 0;'>
<tr style='background:#ebf5fb;'><th style='padding:7px;'>Country</th><th style='padding:7px;'>Nationality</th><th style='padding:7px;'>Language</th></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>England</td><td style='padding:6px;border-top:1px solid #ddd;'>English</td><td style='padding:6px;border-top:1px solid #ddd;'>English</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>France</td><td style='padding:6px;border-top:1px solid #ddd;'>French</td><td style='padding:6px;border-top:1px solid #ddd;'>French</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Germany</td><td style='padding:6px;border-top:1px solid #ddd;'>German</td><td style='padding:6px;border-top:1px solid #ddd;'>German</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Japan</td><td style='padding:6px;border-top:1px solid #ddd;'>Japanese</td><td style='padding:6px;border-top:1px solid #ddd;'>Japanese</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Brazil</td><td style='padding:6px;border-top:1px solid #ddd;'>Brazilian</td><td style='padding:6px;border-top:1px solid #ddd;'>Portuguese</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Bangladesh</td><td style='padding:6px;border-top:1px solid #ddd;'>Bangladeshi</td><td style='padding:6px;border-top:1px solid #ddd;'>Bengali</td></tr>
</table>
<p><strong>Common patterns:</strong> -ese (Japanese, Chinese, Portuguese) · -ish (Spanish, Swedish, British) · -ian (Brazilian, Italian, Australian) · -i (Israeli, Emirati)</p>
<p><strong>Sentence patterns:</strong> I am <u>from</u> France. / I am <u>French</u>. / I speak <u>French</u>.</p>""",
 "tasks":[
  {"title":"What is the nationality?","instr":"Write the nationality for each country:<br>1. Australia · 2. Spain · 3. China · 4. Italy · 5. Brazil · 6. Portugal · 7. Sweden","ans":"1. Australian · 2. Spanish · 3. Chinese · 4. Italian · 5. Brazilian · 6. Portuguese · 7. Swedish"},
  {"title":"Spot the mismatch","instr":"Find the error in each sentence:<br>1. 'She is from Brazil. She speaks Brazilian.'<br>2. 'He is Japanese. He is from China.'<br>3. 'I am from Australia. I speak Australian.'","ans":"1. She speaks Portuguese (not Brazilian) · 2. He is Japanese means he is from Japan, not China — contradiction · 3. I speak English (Australian is a nationality, not a language)"},
  {"title":"Ask and answer","instr":"Write the question and answer for each person:<br>Person A: from France, speaks French and English<br>Person B: from Bangladesh, speaks Bengali<br>Use: Where are you from? / What is your nationality? / What languages do you speak?","ans":"A: I am from France. I am French. I speak French and English. · B: I am from Bangladesh. I am Bangladeshi. I speak Bengali."},
 ],
 "production":"Write 5 sentences about yourself (or an imaginary person): where you are from, your nationality, the language(s) you speak, and one sentence about why you are learning English. Use all three patterns: I am from... / I am [nationality]. / I speak..."
},
{
 "title":"If Only I Had Known: Second Conditional and Third Conditional",
 "level":"B2","framework":"TTT · Grammar",
 "tags":"B2 English, second conditional, third conditional, hypothetical English, B2 grammar, 5-Minute English Lab",
 "seo_title":"Second and Third Conditional in English: Hypothetical and Regret | B2",
 "meta":"Learn to use the second and third conditional in English to talk about hypothetical situations and past regrets. Clear B2 grammar lesson.",
 "anecdote":"There is a version of my life where I never went to Sydney. Where I stayed in Chittagong and became an engineer as my father wanted. When I use the third conditional, I can visit that life: 'If I had stayed, I would never have become a sommelier, or a teacher, or the person I am now.' The third conditional is the grammar of roads not taken.",
 "aim":"form and use the second conditional (unreal present) and third conditional (unreal past) to discuss hypothetical situations and past regrets.",
 "focus":["2nd: If + past simple, would + inf","3rd: If + past perfect, would have + pp","Mixed: If I had known, I would do...","Wish + past: I wish I had studied harder"],
 "explanation":"""<p>Both conditionals are about <strong>unreal situations</strong> — things that are not true or didn't happen:</p>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0;'>
<div style='background:#f5eef8;padding:12px;border-radius:8px;'>
<strong>2nd Conditional — Unreal PRESENT</strong><br>
If + past simple, would + infinitive<br><br>
<em>If I <u>had</u> more time, I <u>would study</u> music.</em><br>
(I don't have more time — imagining it)<br><br>
<em>If she <u>were</u> here, she <u>would know</u> what to do.</em><br>
(formal: were, not was, in 2nd conditional)</div>
<div style='background:#fdedec;padding:12px;border-radius:8px;'>
<strong>3rd Conditional — Unreal PAST</strong><br>
If + past perfect, would have + past participle<br><br>
<em>If I <u>had stayed</u> in Sydney, I <u>would have missed</u> so much.</em><br>
(I didn't stay — imagining the alternative)<br><br>
<em>If she <u>had applied</u> earlier, she <u>would have got</u> the job.</em></div>
</div>
<p><strong>Wish:</strong> <em>I wish I <u>had studied</u> French earlier.</em> (3rd-conditional logic — past regret)</p>""",
 "tasks":[
  {"title":"2nd or 3rd?","instr":"Complete with the correct conditional form:<br>1. If I ___ (know) the answer now, I ___ (tell) you. (hypothetical present)<br>2. If she ___ (study) harder last year, she ___ (pass) the exam. (past regret)<br>3. If I ___ (be) you, I ___ (accept) the offer. (imaginary present — advice)","ans":"1. knew / would tell · 2. had studied / would have passed · 3. were / would accept"},
  {"title":"Spot the error","instr":"Find the mistake:<br>1. 'If I would know, I would tell you.'<br>2. 'If she had studied, she would pass.'<br>3. 'I wish I studied harder last year.'","ans":"1. If I <u>knew</u> (no would in the if-clause) · 2. she would <u>have passed</u> (3rd conditional — past perfect in result too) · 3. I wish I <u>had studied</u> (past regret needs had + pp)"},
  {"title":"Your own 3rd conditional","instr":"Think of one decision you made in the past. Write a 3rd conditional sentence about the alternative:<br>Example: If I had not [done X], I would have [result Y].","ans":"Any grammatically correct sentence using if + past perfect + would have + past participle. Example: If I had not moved to La Reunion, I would have never started teaching English."},
 ],
 "production":"Write 4 sentences: 2 second conditionals (imaginary present situations) and 2 third conditionals (past regrets or alternative histories). They can be about your own life, career, or learning English journey. Then pick the one that feels most true and expand it into a short paragraph."
},
{
 "title":"Drilling Without Boredom: Making Pronunciation Practice Stick",
 "level":"Teachers","framework":"CELTA Technique · Phonology & Drilling",
 "tags":"CELTA methodology, drilling technique, pronunciation teaching, phonology ELT, 5-Minute English Lab",
 "seo_title":"Drilling Techniques in ELT: Choral, Individual and Substitution Drills | CELTA",
 "meta":"Learn when and how to use drilling in English lessons to teach pronunciation and consolidate new language. CELTA teaching technique guide.",
 "anecdote":"My least favourite memory from early teaching: drilling gone wrong. The same sentence, 15 times, same voice, same pace. The students' eyes glazed over. What I learned is that drilling is a technique, not a punishment. Varied, purposeful, short — it works. Repetitive, monotonous, long — it kills the lesson.",
 "aim":"plan and deliver three types of drill (choral, individual, substitution) correctly — and know when drilling is appropriate.",
 "focus":["Choral drilling (whole class together)","Individual drilling (one student at a time)","Substitution drill (vary one element)","Backchaining (for long items)","When to drill: new forms and new sounds"],
 "explanation":"""<p>Drilling is <strong>controlled oral repetition</strong> of a target language item. Its purpose is to build phonological memory — not rote memorisation.</p>
<p><strong>Three drill types:</strong></p>
<ol>
<li><strong>Choral:</strong> Teacher says the model → whole class repeats together. Safe for shy learners; low exposure risk; good for phonological introduction. Limitation: you can't monitor individual pronunciation.</li>
<li><strong>Individual:</strong> Teacher nominates one student to repeat. Allows monitoring. Risk: anxiety if done too early or without choral first.</li>
<li><strong>Substitution:</strong> Teacher gives the model → students substitute one element each time. <em>'She works in a hotel.' → 'She works in a restaurant.' → 'He works in a school.'</em> Adds variety and meaning while keeping the target form stable.</li>
</ol>
<p><strong>Backchaining</strong> — for long or complex items, build from the end backwards:</p>
<p><em>Target: 'Would you mind closing the window?'</em><br>
Step 1: <em>'...the window?'</em> → Step 2: <em>'...closing the window?'</em> → Step 3: <em>'...mind closing the window?'</em> → Step 4: <em>'Would you mind closing the window?'</em></p>
<p><strong>When to drill:</strong> After presentation, when you have a clear model, for new vocabulary (stress pattern), new grammatical form (stressed syllables), or new phoneme. Not during fluency work.</p>""",
 "tasks":[
  {"title":"Sequence the drill","instr":"Put these steps in the correct order for introducing a new phrase:<br>a) Choral drill of the whole phrase<br>b) Teacher presents the phrase in context with clear model pronunciation<br>c) Individual drill of 3-4 students<br>d) Backchain drill of each section<br>e) Teacher writes the phrase on the board and marks stress","ans":"b (present in context) → e (write and mark stress) → d (backchain if long) → a (choral) → c (individual). The sequence: establish meaning → establish form/pronunciation → whole class → individuals."},
  {"title":"Substitution drill design","instr":"You are drilling: 'I'd like to make a reservation.' Design a 4-step substitution drill that keeps the structure stable but varies one element each time.","ans":"Step 1: 'I'd like to make a reservation.' (model) · Step 2: 'I'd like to make a booking.' (substitute reservation → booking) · Step 3: 'I'd like to make a complaint.' (substitute booking → complaint) · Step 4: 'I'd like to make an enquiry.' — The structure stays the same; vocabulary varies; learners consolidate the pattern."},
  {"title":"What went wrong?","instr":"A teacher drills for 12 minutes, repeating the same sentence 20 times with the whole class. Students look bored and start mumbling. What are the three main errors in this drilling approach?","ans":"1. Too long — drilling should be short (2-4 minutes maximum); beyond that it becomes demotivating · 2. No variety — same sentence, same structure, no substitution or variation to maintain attention · 3. Only choral — no progression to individual drilling, so no check on individual pronunciation. Fix: shorter, varied (choral → individual → substitution), and move on."},
 ],
 "production":"Design a 3-minute drilling sequence for this item: 'I should have left earlier.' Include: (1) backchaining steps, (2) one choral stage, (3) one individual stage, (4) one substitution step. Write out exactly what you (the teacher) say at each step."
},
{
 "title":"Describing Places: The Island Where I Live",
 "level":"B1","framework":"PPP · Vocabulary and Writing",
 "tags":"B1 English, describing places, geography vocabulary, descriptive writing, 5-Minute English Lab",
 "seo_title":"Describing Places in English: Vocabulary and Writing for B1 Learners",
 "meta":"Learn vocabulary and structures for describing places in English. B1 lesson using La Reunion as a model, with writing practice.",
 "anecdote":"La Réunion — the island where I live and teach — is in the Indian Ocean, halfway between Madagascar and Mauritius. It has an active volcano, white-sand beaches, mountain peaks, and four distinct climates depending on where you stand. Describing it in English taught me that a place needs detail, not superlatives. Not 'it is beautiful' — but 'the sea is turquoise and the volcanic rock is black.'",
 "aim":"describe a place using precise vocabulary for geography, climate, and atmosphere — moving from general to specific.",
 "focus":["located / situated / found","surrounded by / overlooking","lush / arid / dramatic","on the coast / inland / at altitude","atmosphere / landscape / architecture"],
 "explanation":"""<p>Strong place descriptions move from <strong>general → specific</strong> and use <strong>concrete language</strong> rather than vague adjectives like 'nice' or 'beautiful':</p>
<div style='background:#fef9e7;padding:12px;border-radius:8px;margin-bottom:10px;'>
<strong>Weak:</strong> 'La Réunion is a beautiful island. It is very nice.'<br>
<strong>Strong:</strong> 'La Réunion is a volcanic island in the Indian Ocean, situated roughly 800 kilometres east of Madagascar. Its coastline alternates between black lava beaches and white coral sand. The Piton de la Fournaise volcano remains one of the most active on earth.'
</div>
<p><strong>Useful structures:</strong></p>
<ul>
<li>Geographical location: <em>situated/located + in/on/off + place</em> → <em>situated in the Indian Ocean</em></li>
<li>Features: <em>characterised by / known for / famous for</em> → <em>known for its active volcano</em></li>
<li>Contrast: <em>While the coast is..., the interior is...</em></li>
<li>Atmosphere: <em>The atmosphere is... / The pace of life is... / The culture combines...</em></li>
</ul>""",
 "tasks":[
  {"title":"Replace the vague adjective","instr":"Replace each vague word with a more precise description:<br>1. 'The beach is beautiful.' → The beach is ___<br>2. 'The city is interesting.' → The city is ___<br>3. 'The weather is nice.' → The weather is ___","ans":"Examples: 1. 'The beach is lined with black volcanic rock and pale sand.' · 2. 'The old town is a mix of colonial architecture and modern apartment blocks.' · 3. 'The weather is warm and humid from November to April, with temperatures averaging 28°C.' (Any specific description is better than vague)"},
  {"title":"General to specific","instr":"Arrange these sentences from most general (1) to most specific (3):<br>a) 'La Réunion is part of France.'<br>b) 'The Piton de la Fournaise erupted most recently in 2024.'<br>c) 'La Réunion is a French overseas territory in the Indian Ocean.'","ans":"Most general: a (national identity) → c (geographic specificity) → b (specific local detail). A description should move in this direction: broad → narrow."},
  {"title":"Write 3 sentences","instr":"Write 3 sentences describing a place you know well. Sentence 1: location (use situated/located). Sentence 2: a physical feature (use a concrete adjective, not beautiful/nice). Sentence 3: the atmosphere or character.","ans":"Example: My city is located in the north-west of France, on the Atlantic coast. The old town is built from pale granite and has medieval walls that still encircle the historic centre. The atmosphere is quiet and unhurried, with a strong fishing and maritime heritage."},
 ],
 "production":"Write a short description (6–8 sentences) of a place you know well — your town, a place you visited, or your home. Use: a location sentence, two concrete descriptive sentences, a contrast sentence (while X is..., Y is...), and a sentence about atmosphere. Avoid beautiful, nice, and interesting as adjectives."
},
{
 "title":"Collocations: Words That Live Together",
 "level":"B2","framework":"Guided Discovery · Lexis",
 "tags":"B2 English, collocations, vocabulary B2, lexical chunks, natural English, 5-Minute English Lab",
 "seo_title":"English Collocations: Words That Go Together Naturally | B2 Vocabulary",
 "meta":"Learn how collocations work in English and study key verb-noun and adjective-noun collocations. B2 vocabulary lesson for natural-sounding English.",
 "anecdote":"After 18 years in hospitality, certain phrases were automatic: make a reservation, take an order, deal with a complaint, meet a deadline. None of those verbs is interchangeable — you don't do a reservation or deal a deadline. That automatic knowledge is called collocation, and it is what separates fluent from laboured English.",
 "aim":"identify and use common collocations correctly — distinguishing between similar verbs and understanding why the wrong partner sounds unnatural.",
 "focus":["make / do / take / have","make a reservation / do your homework","take a risk / have a meeting","strong tea (not powerful tea)","heavy traffic (not strong traffic)"],
 "explanation":"""<p>A <strong>collocation</strong> is a pair or group of words that frequently occur together. Native speakers do not choose these consciously — they come as units. Learning vocabulary in collocations, not in isolation, is one of the most efficient strategies for fluency.</p>
<p><strong>The make/do/take/have problem:</strong></p>
<table style='width:100%;border-collapse:collapse;font-size:0.87em;margin:8px 0;'>
<tr style='background:#f5eef8;'><th style='padding:7px;'>Verb</th><th style='padding:7px;text-align:left;'>Common collocations</th></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;font-weight:700;'>make</td><td style='padding:6px;border-top:1px solid #ddd;'>a reservation · a decision · a mistake · a suggestion · progress · an effort</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;font-weight:700;'>do</td><td style='padding:6px;border-top:1px solid #ddd;'>homework · research · damage · your best · a favour · the cleaning</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;font-weight:700;'>take</td><td style='padding:6px;border-top:1px solid #ddd;'>a risk · an exam · notes · action · responsibility · a break</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;font-weight:700;'>have</td><td style='padding:6px;border-top:1px solid #ddd;'>a meeting · a conversation · breakfast · a look · a shower · an idea</td></tr>
</table>
<p><strong>Adjective-noun collocations are equally fixed:</strong> <em>strong tea / coffee</em> (not powerful) · <em>heavy rain / traffic / smoker</em> (not big rain) · <em>make a mess</em> (not do a mess)</p>""",
 "tasks":[
  {"title":"Make, do, take or have?","instr":"Complete with the correct verb:<br>1. Could you ___ me a favour? · 2. She always ___ her homework immediately after class. · 3. The manager had to ___ a difficult decision. · 4. Let's ___ a break before the next session. · 5. We need to ___ action on this immediately.","ans":"1. do · 2. does · 3. make · 4. take · 5. take"},
  {"title":"Strong or heavy?","instr":"Which adjective? Strong or heavy?<br>1. ___ rain · 2. ___ coffee · 3. ___ traffic · 4. ___ accent · 5. ___ smoker","ans":"1. heavy · 2. strong · 3. heavy · 4. strong · 5. heavy"},
  {"title":"Spot the wrong collocation","instr":"Find and correct the error:<br>1. 'She did a good impression at the interview.' · 2. 'Can you do a reservation for 8?' · 3. 'He took a mistake in the report.'","ans":"1. She <u>made</u> a good impression. · 2. Can you <u>make</u> a reservation? · 3. He <u>made</u> a mistake. (make is the correct verb with impression, reservation, mistake — do, make and take are not interchangeable)"},
 ],
 "production":"Write 6 sentences about a typical working day. Each sentence must use a different collocation from today's lesson (make / do / take / have + noun). Then check each verb: is it the right one? Challenge yourself to use at least one adjective-noun collocation too (heavy, strong, etc.)."
},
{
 "title":"Making Suggestions: What About...? Why Not...? Shall We...?",
 "level":"B1","framework":"PPP · Functional Language",
 "tags":"B1 English, making suggestions, functional language, B1 speaking, 5-Minute English Lab",
 "seo_title":"Making Suggestions in English: What About, Why Not, Shall We | B1",
 "meta":"Learn 6 ways to make suggestions in English — from casual to polite. B1 functional language lesson with clear practice activities.",
 "anecdote":"Teaching adults in mixed-ability groups taught me that the language of suggestion is also the language of inclusion. If you only know 'I want to do X,' the room stays yours. When you can say 'What if we tried X?' or 'Shall we give that a go?', you invite everyone in. Suggestion language is collaborative language.",
 "aim":"make and respond to suggestions using 6 different expressions — choosing the right register for the context.",
 "focus":["What about + -ing?","Why don't we...?","Shall we...?","How about + -ing?","We could always...","Let's...!"],
 "explanation":"""<p>English has six common ways to make a suggestion, ranging from very casual to slightly more formal:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.87em;margin:8px 0;'>
<tr style='background:#fef9e7;'><th style='padding:7px;text-align:left;'>Expression</th><th style='padding:7px;text-align:left;'>Register</th><th style='padding:7px;text-align:left;'>Example</th></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Let's + infinitive</td><td style='padding:6px;border-top:1px solid #ddd;'>Casual / enthusiastic</td><td style='padding:6px;border-top:1px solid #ddd;'>Let's go for a walk!</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>What about / How about + -ing</td><td style='padding:6px;border-top:1px solid #ddd;'>Casual</td><td style='padding:6px;border-top:1px solid #ddd;'>What about trying a different approach?</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Why don't we + infinitive</td><td style='padding:6px;border-top:1px solid #ddd;'>Neutral</td><td style='padding:6px;border-top:1px solid #ddd;'>Why don't we start earlier tomorrow?</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Shall we + infinitive</td><td style='padding:6px;border-top:1px solid #ddd;'>Neutral / polite</td><td style='padding:6px;border-top:1px solid #ddd;'>Shall we take a short break?</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>We could (always) + infinitive</td><td style='padding:6px;border-top:1px solid #ddd;'>Tentative / gentle</td><td style='padding:6px;border-top:1px solid #ddd;'>We could always rearrange the meeting.</td></tr>
</table>
<p><strong>Responding to suggestions:</strong> Accepting: 'That sounds good! / Great idea! / Yes, let's.' Declining: 'I'm not sure... / I'd rather not... / How about [counter-suggestion] instead?'</p>""",
 "tasks":[
  {"title":"Which form?","instr":"Rewrite using the expression in brackets:<br>1. 'We should try the new café.' → What about ___?<br>2. 'Start at 9 tomorrow.' → Shall we ___?<br>3. 'You could take a different route.' → Why don't we ___?","ans":"1. What about trying the new café? · 2. Shall we start at 9 tomorrow? · 3. Why don't we take a different route?"},
  {"title":"Accept or decline","instr":"Write a natural response to each suggestion:<br>1. 'What about meeting at 3 instead of 2?' → Accept<br>2. 'Shall we cancel the project?' → Decline with counter-suggestion","ans":"1. 'That sounds perfect! See you at 3.' / 'Good idea — 3 works much better for me.' · 2. 'I'd rather not cancel it completely — how about delaying it by a month instead?'"},
  {"title":"Casual or professional?","instr":"Which suggestion is more appropriate for a professional meeting?<br>A) 'Let's just do it differently.' B) 'We could consider an alternative approach.'","ans":"B is more appropriate in a formal professional context. 'Let's just do it' sounds too casual and dismissive. 'We could consider' is tentative, collaborative and professional."},
 ],
 "production":"Write a short conversation (8 lines) in which two colleagues are planning a team event. One person makes 3 suggestions using 3 different expressions. The other responds to each — accepting one, declining one with a counter-suggestion, and asking a clarifying question about the third."
},
{
 "title":"A Day in La Réunion: Present Perfect for Recent Events",
 "level":"Kids","framework":"PPP · Cambridge Young Learners Flyers",
 "tags":"young learners, Cambridge Flyers, present perfect kids, children English lesson, 5-Minute English Lab",
 "seo_title":"Present Perfect for Kids: A Day in La Reunion Story | Cambridge Flyers",
 "meta":"Fun Cambridge Flyers level lesson on the present perfect tense for young learners, set in the tropical island of La Reunion. Interactive with activities.",
 "anecdote":"My daughter will grow up on an island with a volcano, beaches, and three languages around her. Every day on this island is a little adventure — and adventures are best told in the present perfect: I have climbed, I have seen, I have tried. This lesson is her world, put into grammar.",
 "aim":"use the present perfect to talk about recent events and experiences, using <em>have/has + past participle</em>.",
 "focus":["I have seen / She has eaten","Have you ever...? Yes, I have. / No, I haven't.","just / already / yet","ever / never"],
 "explanation":"""<div style='background:#fdf2e9;border-radius:10px;padding:16px;margin-bottom:12px;'>
<p style='font-weight:700;color:#d35400;font-size:1.1em;margin:0 0 10px;'>Welcome to La Réunion! A Volcanic Island Adventure!</p>
<p style='color:#555;'>La Réunion is a French island in the Indian Ocean. It has a real volcano, white and black beaches, tropical fruit, and beautiful mountains. Let's learn the present perfect with a day on the island!</p>
</div>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;'>
<div style='background:#fff3cd;border-radius:8px;padding:12px;'>
<p style='margin:0 0 6px;font-weight:700;color:#e67e22;'>I / You / We / They</p>
I <strong>have visited</strong> the volcano!<br>
We <strong>have eaten</strong> tropical fruit.<br>
They <strong>have swum</strong> in the sea.
</div>
<div style='background:#fce4ec;border-radius:8px;padding:12px;'>
<p style='margin:0 0 6px;font-weight:700;color:#c0392b;'>He / She / It</p>
She <strong>has seen</strong> a sea turtle!<br>
He <strong>has climbed</strong> the mountain.<br>
It <strong>has erupted</strong> before!
</div>
</div>
<p style='background:#e8f8f5;padding:10px;border-radius:6px;'>Questions: <strong>Have you ever seen a volcano?</strong><br>Yes, I <strong>have</strong>! / No, I <strong>haven't</strong>. / No, I <strong>never have</strong>.</p>""",
 "tasks":[
  {"title":"The Island Day Story!","instr":"Complete Mia's story with the correct form (have/has + past participle):<br><em>Today Mia ___ (visit) the famous Piton de la Fournaise volcano. She ___ (see) real lava rocks! Her friends ___ (swim) in a beautiful lagoon. They ___ (eat) mango ice cream. Mia ___ (take) many photos. It ___ (be) the best day ever!</em>","ans":"has visited / has seen / have swum / have eaten / has taken / has been"},
  {"title":"Have you ever...?","instr":"Answer these questions about YOURSELF. Write YES or NO, then a full sentence:<br>1. Have you ever seen the sea? → ___<br>2. Have you ever eaten tropical fruit? → ___<br>3. Have you ever climbed a big hill or mountain? → ___","ans":"Learner's own answers. Model: 1. Yes, I have seen the sea! / No, I have never seen the sea. etc."},
  {"title":"Just and already!","instr":"Add JUST or ALREADY to make the sentence correct:<br>1. Mia has ___ arrived at the beach. She got there 2 minutes ago! (very recent)<br>2. The children have ___ finished their ice cream. It is all gone!","ans":"1. just (very recent event) · 2. already (it happened before expected time)"},
 ],
 "production":"Write your own ISLAND ADVENTURE story (4-5 sentences). Imagine you are on a tropical island. Use the present perfect to tell your friend what you have done today! Start with: <em>Today has been amazing! I have...</em> Draw a picture of your adventure if you like!"
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
        print(f"  OK {r.status_code} ID {pid}")
        results.append((r.status_code, pid, L["title"]))
    except Exception as e:
        print(f"  ERR {e}")
    time.sleep(1.2)

ok = sum(1 for r in results if str(r[0])=="200")
print(f"\nTotal: {ok}/{len(results)} posted")
for r in results: print(f"  {r[0]} | ID {r[1]} | {r[2][:55]}")
