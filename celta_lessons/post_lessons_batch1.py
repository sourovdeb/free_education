#!/usr/bin/env python3
import requests, time, json, sys

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

def pill(text, color):
    return f"<span style='display:inline-block;margin:3px;padding:5px 11px;background:{color};color:#fff;border-radius:20px;font-size:0.85em;font-weight:600;'>{text}</span>"

def task_block(t, color, bg, idx):
    return f"""<div style='margin:12px 0;padding:14px 16px;background:#fff;border-left:4px solid {color};border-radius:0 8px 8px 0;box-shadow:0 1px 4px rgba(0,0,0,0.06);'>
<p style='margin:0 0 6px;font-weight:700;color:{color};'>Task {idx}: {t['title']}</p>
<p style='margin:0 0 8px;color:#555;line-height:1.55;'>{t['instr']}</p>
<details><summary style='cursor:pointer;color:{color};font-size:0.88em;font-weight:600;'>💡 Show answer</summary>
<div style='padding:10px;background:{bg};border-radius:6px;margin-top:8px;color:#444;line-height:1.55;'>{t['ans']}</div></details></div>"""

def build_html(L):
    lv = LC[L["level"]]
    c, bg = lv["c"], lv["bg"]
    tasks_html = "".join(task_block(t, c, bg, i+1) for i,t in enumerate(L["tasks"]))
    focus_html = "".join(pill(f, c) for f in L.get("focus", []))
    focus_sec = f"<div style='padding:0 28px 16px;'><p style='margin:0 0 8px;font-weight:700;color:#333;font-size:0.85em;text-transform:uppercase;letter-spacing:0.5px;'>Language Focus:</p>{focus_html}</div>" if focus_html else ""

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

# ── LESSONS 1–10 ─────────────────────────────────────────────────────────────

lessons = [

{
 "title":"Your First 10 Words in a Restaurant",
 "level":"A1","framework":"PPP · Vocabulary",
 "tags":"A1 English, restaurant vocabulary, beginner English, 5-Minute English Lab, ELT",
 "seo_title":"10 Essential Restaurant Words for Beginners | 5-Minute English Lab A1",
 "meta":"Learn 10 essential English words for restaurants and cafés in just 5 minutes. Perfect for absolute beginners.",
 "anecdote":"My first week in Sydney, I pointed at the menu instead of speaking. Learning ten words changed everything — I got a job within a month.",
 "aim":"name 10 common restaurant items and use them in a simple sentence: <em>I'd like a _____, please.</em>",
 "focus":["menu","table","bill","order","drink","starter","main course","dessert","water","tip"],
 "explanation":"""<p>These 10 words cover 90% of what you need in any English-speaking restaurant or café. Notice the pattern: <strong>I'd like a [item], please.</strong></p>
<p><strong>Pronunciation tip:</strong> <em>bill</em> (rhymes with 'fill') · <em>menu</em> ('MEN-yoo') · <em>dessert</em> (stress on 2nd syllable: 'deh-ZURT' — not 'DEZ-ert' which is a dry landscape!)</p>
<div style='background:#eafaf1;padding:12px;border-radius:6px;margin-top:10px;'><strong>Memory trick:</strong> Group them in order: arrive → <em>menu → order → starter → main → dessert → bill → tip</em>. That's a complete meal.</div>""",
 "tasks":[
  {"title":"Match the word","instr":"Which word goes where? <strong>bill / menu / tip / dessert / order</strong><br>1. The waiter brings this first so you can choose. → ___<br>2. You pay this at the end. → ___<br>3. Extra money for good service. → ___<br>4. Sweet food after your main course. → ___<br>5. To ask for food or drink. → ___","ans":"1. menu · 2. bill · 3. tip · 4. dessert · 5. order"},
  {"title":"Say it out loud","instr":"Practise saying this sentence with 5 different items from the list: <em>'I'd like a _____, please.'</em> Say each one twice — first slowly, then at natural speed.","ans":"I'd like a menu, please. / I'd like the bill, please. / I'd like a starter, please. (etc.)"},
  {"title":"Odd one out","instr":"Which word does NOT belong? Why?<br>A) starter · main course · dessert · <strong>tip</strong>","ans":"<em>Tip</em> is money, not food. The others are all courses of a meal."},
 ],
 "production":"You are in a café in London. Write 3 sentences using words from the list. Start with: <em>Excuse me, I'd like to order...</em> Then ask for the bill and leave a tip comment."
},

{
 "title":"Numbers That Matter: Prices, Times & Room Numbers",
 "level":"A1","framework":"PPP · Lexis & Phonology",
 "tags":"A1 English, numbers in English, beginner English, 5-Minute English Lab, ELT",
 "seo_title":"Numbers in English: Prices, Times and Rooms | A1 Beginner Lesson",
 "meta":"Master English numbers for prices, times and room numbers in 5 minutes. Essential A1 English lesson.",
 "anecdote":"At the Star Casino in Sydney I once gave a guest the wrong room number because I confused 'fifteen' and 'fifty.' Learning to stress the right syllable saved me many embarrassing moments.",
 "aim":"say prices (£12.50), times (quarter past three) and room/floor numbers correctly — especially distinguishing <em>-teen</em> from <em>-ty</em>.",
 "focus":["13 vs 30","14 vs 40","15 vs 50","£12.50","3:15","Room 214"],
 "explanation":"""<p><strong>The -teen / -ty trap:</strong> English speakers stress the <em>first</em> syllable in -ty numbers and the <em>second</em> in -teen numbers:</p>
<ul><li><strong>THIR-ty</strong> (30) vs <strong>thir-TEEN</strong> (13)</li><li><strong>FOR-ty</strong> (40) vs <strong>four-TEEN</strong> (14)</li><li><strong>FIF-ty</strong> (50) vs <strong>fif-TEEN</strong> (15)</li></ul>
<p><strong>Prices:</strong> £12.50 = "twelve pounds fifty" (drop <em>pence</em> in natural speech).</p>
<p><strong>Times:</strong> 3:15 = "quarter past three" · 3:30 = "half past three" · 3:45 = "quarter to four"</p>""",
 "tasks":[
  {"title":"Which do you hear? (read aloud & decide)","instr":"Say each pair out loud. Which is the higher number?<br>A) thir-TEEN vs THIR-ty · B) fif-TEEN vs FIF-ty · C) four-TEEN vs FOR-ty","ans":"Both the -teen words are lower (13, 15, 14). The -ty words are higher (30, 50, 40). The stress tells you which is which."},
  {"title":"Write the time","instr":"How do you say these times in English?<br>1. 4:15 · 2. 7:30 · 3. 9:45 · 4. 12:00","ans":"1. quarter past four · 2. half past seven · 3. quarter to ten · 4. twelve o'clock / noon / midnight"},
  {"title":"Price practice","instr":"Read these prices out loud: £3.50 · £14.99 · £40.00 · £15.75","ans":"three pounds fifty · fourteen pounds ninety-nine · forty pounds · fifteen pounds seventy-five"},
 ],
 "production":"Imagine you are a hotel receptionist. A guest asks: 'What time is check-out?' and 'How much is the room per night?' Write your reply using times and prices. Speak it out loud if you can."
},

{
 "title":"Hello, Goodbye, Thank You: Survival English in 5 Minutes",
 "level":"A1","framework":"PPP · Functional Language",
 "tags":"A1 English, greetings, survival English, 5-Minute English Lab, beginner ELT",
 "seo_title":"Hello Goodbye Thank You: Survival English for Absolute Beginners | A1",
 "meta":"7 essential English phrases for greetings, farewells and politeness. Perfect first lesson for absolute beginners.",
 "anecdote":"When I first arrived in Sydney from Bangladesh in 2005, I had 'horrible English' — my own words. But I knew 'hello,' 'thank you' and 'sorry.' Those three words opened more doors than I expected.",
 "aim":"use 7 essential phrases for greeting, thanking and apologising in natural spoken English.",
 "focus":["Hello / Hi","Good morning/afternoon/evening","How are you?","Fine thanks, and you?","Goodbye / Bye / See you","Thank you / Thanks / Cheers","Sorry / Excuse me"],
 "explanation":"""<p>These 7 phrases are the skeleton of any social interaction in English. Notice that English has <strong>formal and informal</strong> versions:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.9em;'><tr style='background:#eafaf1;'><th style='padding:7px;text-align:left;'>Formal</th><th style='padding:7px;text-align:left;'>Informal</th></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;'>Good morning</td><td style='padding:7px;border-top:1px solid #ddd;'>Hi / Hey</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;'>Thank you very much</td><td style='padding:7px;border-top:1px solid #ddd;'>Thanks / Cheers (UK/AUS)</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;'>I beg your pardon</td><td style='padding:7px;border-top:1px solid #ddd;'>Sorry? / What?</td></tr>
<tr><td style='padding:7px;border-top:1px solid #ddd;'>Goodbye</td><td style='padding:7px;border-top:1px solid #ddd;'>Bye / See you / Later</td></tr></table>""",
 "tasks":[
  {"title":"Formal or informal?","instr":"Decide: is this formal (F) or informal (I)?<br>1. 'Cheers, mate!' · 2. 'Good evening, sir.' · 3. 'Hey, how's it going?' · 4. 'I beg your pardon?'","ans":"1. I · 2. F · 3. I · 4. F"},
  {"title":"Complete the mini-dialogue","instr":"Fill the gaps: <em>A: Good morning! ___ are you? · B: ___, thanks. And ___? · A: Very well, thank you. ___ you later!</em>","ans":"A: Good morning! <u>How</u> are you? · B: <u>Fine</u>, thanks. And <u>you</u>? · A: Very well, thank you. <u>See</u> you later!"},
  {"title":"Which phrase fits?","instr":"You bump into someone on the street. You want to ask the time. What do you say FIRST?","ans":"'Excuse me...' — this politely gets attention before your question."},
 ],
 "production":"Write a 4-line conversation between two people meeting for the first time in an office. Use at least 4 of the 7 phrases above. Then read it out loud — both parts."
},

{
 "title":"What Do You Do? Present Simple for Jobs & Routines",
 "level":"A2","framework":"PPP · Grammar",
 "tags":"A2 English, present simple, jobs vocabulary, 5-Minute English Lab, ELT grammar",
 "seo_title":"Present Simple for Jobs and Routines | A2 English Grammar Lesson",
 "meta":"Learn to use the present simple tense to describe jobs and daily routines. Clear A2 English grammar lesson with practice.",
 "anecdote":"When I managed the bar team at Uccello in Sydney, new staff always asked me 'What do you do exactly?' I had to describe 15 different things. That's the present simple — your professional identity in sentences.",
 "aim":"use the present simple to describe jobs, routines and facts — including the third-person <em>-s</em> rule.",
 "focus":["I work / She works","He teaches / They teach","Do you...? / Does she...?","always / usually / often / sometimes / never"],
 "explanation":"""<p>The present simple describes <strong>habits, routines and facts</strong>. The key rule: add <strong>-s</strong> (or -es) for <em>he / she / it</em>.</p>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0;'>
<div style='background:#ebf5fb;padding:10px;border-radius:6px;'><strong>✅ Positive:</strong><br>I <u>teach</u> English.<br>She <u>works</u> in a hotel.<br>They <u>manage</u> a team.</div>
<div style='background:#fdedec;padding:10px;border-radius:6px;'><strong>❌ Negative:</strong><br>I <u>don't</u> work weekends.<br>He <u>doesn't</u> speak French.<br>They <u>don't</u> open until 9.</div>
</div>
<p><strong>Questions:</strong> <em>Do</em> you work here? · <em>Does</em> she teach adults?</p>
<p><strong>Frequency adverbs</strong> go BEFORE the main verb: I <u>always</u> arrive early. She <u>usually</u> checks the bookings first.</p>""",
 "tasks":[
  {"title":"Fix the mistake","instr":"Each sentence has one error. Find and correct it:<br>1. She teach English at a language school.<br>2. He don't speaks French.<br>3. I usually arrives at 8 o'clock.<br>4. Does they work on Sundays?","ans":"1. She <u>teaches</u> · 2. He <u>doesn't speak</u> · 3. I usually <u>arrive</u> · 4. <u>Do</u> they work on Sundays?"},
  {"title":"Interview questions","instr":"Write 4 questions to ask someone about their job. Use: work / start / finish / like","ans":"Where do you work? / What time do you start? / When do you finish? / Do you like your job?"},
  {"title":"Your routine","instr":"Write 5 true sentences about YOUR daily routine using: always / usually / sometimes / never","ans":"Example: I always drink coffee in the morning. I sometimes work late. I never skip breakfast."},
 ],
 "production":"Write a short paragraph (4–5 sentences) about someone's job — it can be yours, a friend's, or an imaginary person. Use the present simple and at least 2 frequency adverbs."
},

{
 "title":"Describing People: Adjectives for Appearance and Personality",
 "level":"A2","framework":"PPP · Vocabulary & Speaking",
 "tags":"A2 English, describing people, adjectives, personality vocabulary, 5-Minute English Lab",
 "seo_title":"Describing People in English: Appearance and Personality | A2 Lesson",
 "meta":"Learn the key adjectives for describing people's appearance and personality in English. A2 level with clear practice activities.",
 "anecdote":"Managing a front-of-house team at The Ivy in Sydney meant I needed to brief staff on VIP guests before they arrived. 'She's tall, well-dressed and very direct' — three adjectives that prepared everyone for the interaction.",
 "aim":"use 12 key adjectives to describe someone's appearance and personality accurately.",
 "focus":["tall/short/medium height","slim/stocky/well-built","dark/fair/grey hair","confident","reliable","outgoing/shy","organised","patient"],
 "explanation":"""<p>In English, <strong>appearance adjectives</strong> come before the noun (<em>a tall man</em>) or after <em>be</em> (<em>He is tall</em>). <strong>Personality adjectives</strong> work the same way.</p>
<p><strong>Appearance:</strong> tall · short · slim · well-built · dark-haired · fair · elegant · smartly dressed</p>
<p><strong>Personality:</strong> confident · reliable · outgoing · patient · organised · direct · friendly · serious</p>
<p><strong>Order matters</strong> when you stack adjectives: opinion → size → age → colour → origin → noun<br>Example: <em>a <u>tall</u> <u>young</u> <u>French</u> woman</em> ✅ not <em>a French young tall woman</em> ❌</p>""",
 "tasks":[
  {"title":"Appearance or personality?","instr":"Sort these words into two columns (A = Appearance / P = Personality):<br><em>reliable · slim · outgoing · fair-haired · organised · well-built · patient · elegant</em>","ans":"Appearance: slim, fair-haired, well-built, elegant · Personality: reliable, outgoing, organised, patient"},
  {"title":"Describe the person","instr":"Look at this description and answer: <em>'She's medium height with dark, short hair. She's very confident and always organised.'</em><br>1. How tall is she? · 2. What colour is her hair? · 3. Name two personality traits.","ans":"1. Medium height · 2. Dark · 3. Confident and organised"},
  {"title":"Write a description","instr":"Describe someone you know (or a famous person) in 3 sentences. Include 2 appearance adjectives and 2 personality adjectives.","ans":"Example: My colleague is tall with fair hair. She is outgoing and very reliable — she's always the first one in the office."},
 ],
 "production":"Write a 'wanted poster' description (for a fun roleplay, not real!): describe an imaginary new team member your company is looking for. Use 5 adjectives and the structure: <em>We are looking for someone who is... They should be... In terms of appearance...</em>"
},

{
 "title":"I'd Like to Order: Polite Requests in English",
 "level":"A2","framework":"TBL · Functional Language",
 "tags":"A2 English, polite requests, would like, functional English, 5-Minute English Lab",
 "seo_title":"Polite Requests in English: I'd Like, Could You, Would You Mind | A2",
 "meta":"Learn to make polite requests in English using 'would like', 'could you' and 'would you mind'. A2 functional language lesson.",
 "anecdote":"At Morrison restaurant in Sydney, the difference between 'Give me a water' and 'Could I have a water, please?' was the difference between rude and professional. In hospitality, polite requests are currency.",
 "aim":"make polite requests using <em>I'd like, Could I have, Would you mind</em> — and understand when each one is appropriate.",
 "focus":["I'd like a...","Could I have...?","Would you mind...?","Can I get...? (informal)","Certainly / Of course / I'm afraid..."],
 "explanation":"""<p>English has a <strong>scale of politeness</strong> for requests. The more indirect the form, the more polite it sounds:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.9em;margin:8px 0;'>
<tr style='background:#ebf5fb;'><th style='padding:7px;text-align:left;'>Form</th><th style='padding:7px;text-align:left;'>Politeness</th><th style='padding:7px;text-align:left;'>Example</th></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Give me...</td><td style='padding:6px;border-top:1px solid #ddd;'>❌ Too direct</td><td style='padding:6px;border-top:1px solid #ddd;'>Give me a coffee.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Can I get...?</td><td style='padding:6px;border-top:1px solid #ddd;'>😐 Informal</td><td style='padding:6px;border-top:1px solid #ddd;'>Can I get a coffee?</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>I'd like...</td><td style='padding:6px;border-top:1px solid #ddd;'>✅ Polite</td><td style='padding:6px;border-top:1px solid #ddd;'>I'd like a coffee, please.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Could I have...?</td><td style='padding:6px;border-top:1px solid #ddd;'>✅✅ Very polite</td><td style='padding:6px;border-top:1px solid #ddd;'>Could I have a coffee?</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Would you mind...?</td><td style='padding:6px;border-top:1px solid #ddd;'>✅✅✅ Formal</td><td style='padding:6px;border-top:1px solid #ddd;'>Would you mind bringing the bill?</td></tr>
</table>
<p><strong>Key grammar:</strong> <em>Would you mind</em> + <strong>-ing</strong> (not infinitive): <em>Would you mind <u>waiting</u>?</em> ✅</p>""",
 "tasks":[
  {"title":"Make it polite","instr":"Rewrite each request to make it more polite:<br>1. 'Give me the menu.' → I'd like... / Could I...?<br>2. 'Bring me the bill.' → Would you mind...?<br>3. 'I want a table for two.' → I'd like...","ans":"1. I'd like the menu, please. / Could I have the menu? · 2. Would you mind bringing the bill? · 3. I'd like a table for two, please."},
  {"title":"Would you mind + -ing","instr":"Complete with the correct form:<br>1. Would you mind ___ (wait) a moment? · 2. Would you mind ___ (turn) the music down?","ans":"1. waiting · 2. turning"},
  {"title":"Respond politely","instr":"A guest asks: 'Could I have a glass of water?' Write TWO possible responses — one saying YES, one saying you don't have it.","ans":"Yes: 'Certainly! / Of course, I'll bring it right away.' · No: 'I'm afraid we've run out of still water, but I can offer you sparkling. Would that be OK?'"},
 ],
 "production":"Write a complete dialogue (6 lines) between a customer and a waiter in a restaurant. The customer orders 2 items, asks about one dish, and requests the bill. The waiter responds politely to each."
},

{
 "title":"Telling Stories: Past Simple for Narrative",
 "level":"B1","framework":"TTT · Grammar",
 "tags":"B1 English, past simple, narrative grammar, storytelling in English, 5-Minute English Lab",
 "seo_title":"Telling Stories in English: Past Simple for Narrative | B1 Grammar",
 "meta":"Master the past simple tense for storytelling and narrative. B1 English grammar lesson with irregular verbs and practice.",
 "anecdote":"When I talk about my move from Sydney to La Réunion, I naturally shift into past simple: I <em>packed</em>, I <em>left</em>, we <em>flew</em>, she <em>waited</em> at arrivals in the snow at Charles de Gaulle. The past simple is a storyteller's best tool.",
 "aim":"use past simple (regular and irregular) to tell a coherent short story with correct time markers.",
 "focus":["packed / left / flew / arrived","walked / talked / decided","didn't know / wasn't","When / Then / After that / Finally"],
 "explanation":"""<p>The past simple has two patterns:</p>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0;'>
<div style='background:#fef9e7;padding:10px;border-radius:6px;'><strong>Regular: add -ed</strong><br>walk → walked<br>arrive → arrived<br>decide → decided<br>pack → packed</div>
<div style='background:#fdedec;padding:10px;border-radius:6px;'><strong>Irregular: learn the form</strong><br>go → went<br>fly → flew<br>meet → met<br>know → knew<br>leave → left</div>
</div>
<p><strong>Negative:</strong> <em>didn't</em> + base verb (NOT the -ed form): <em>I didn't know</em> ✅ not <em>I didn't knew</em> ❌</p>
<p><strong>Question:</strong> <em>Did</em> you + base verb: <em>Did you fly direct?</em></p>
<p><strong>Time markers</strong> that signal past simple: yesterday / last year / in 2005 / when I was / at first / then / after that / finally</p>""",
 "tasks":[
  {"title":"Regular or irregular?","instr":"Write the past simple form of these verbs:<br>arrive · fly · decide · meet · pack · know · travel · leave · start · go","ans":"arrived · flew · decided · met · packed · knew · travelled · left · started · went"},
  {"title":"Fix the errors","instr":"Find the mistakes:<br>1. I didn't flew to Sydney. · 2. She leaved at midnight. · 3. We didn't arrived on time.","ans":"1. I didn't <u>fly</u> · 2. She <u>left</u> · 3. We didn't <u>arrive</u>"},
  {"title":"Sequence the story","instr":"Put these sentences in a logical order using: first, then, after that, finally.<br>a) I found a flat in Strathfield. b) I landed in Sydney. c) I packed my bags in Chittagong. d) I started my new job.","ans":"First, <u>c</u> (I packed). Then <u>b</u> (I landed). After that, <u>a</u> (I found a flat). Finally, <u>d</u> (I started work)."},
 ],
 "production":"Write a short story (5–6 sentences) about a journey or a move you made — or imagine one. Use at least 4 irregular past simple verbs and at least 3 time markers (first, then, after that, finally)."
},

{
 "title":"Giving Advice: Should, Ought To and If I Were You...",
 "level":"B1","framework":"PPP · Functional Language & Grammar",
 "tags":"B1 English, giving advice, should ought to, functional English, 5-Minute English Lab",
 "seo_title":"Giving Advice in English: Should, Ought To, If I Were You | B1",
 "meta":"Learn to give advice in English using should, ought to and if I were you. B1 functional language and grammar lesson.",
 "anecdote":"New teachers often ask me: 'What should I do when a student doesn't understand?' I always say: 'If I were you, I'd try a different example before explaining again — never repeat the same explanation louder.' Advice is an art form.",
 "aim":"give and respond to advice using <em>should / shouldn't, ought to, if I were you, why don't you</em>.",
 "focus":["You should try...","You shouldn't...","If I were you, I'd...","Why don't you...?","Have you thought about...?"],
 "explanation":"""<p>English has several ways to give advice, from strong to gentle:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.9em;margin:8px 0;'>
<tr style='background:#fef9e7;'><th style='padding:7px;text-align:left;'>Expression</th><th style='padding:7px;text-align:left;'>Strength</th><th style='padding:7px;text-align:left;'>Example</th></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>You should / shouldn't</td><td style='padding:6px;border-top:1px solid #ddd;'>Strong</td><td style='padding:6px;border-top:1px solid #ddd;'>You should practise every day.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>You ought to</td><td style='padding:6px;border-top:1px solid #ddd;'>Moderate (more formal)</td><td style='padding:6px;border-top:1px solid #ddd;'>You ought to ask for help.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>If I were you, I'd...</td><td style='padding:6px;border-top:1px solid #ddd;'>Friendly/personal</td><td style='padding:6px;border-top:1px solid #ddd;'>If I were you, I'd speak to your manager.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>Why don't you...?</td><td style='padding:6px;border-top:1px solid #ddd;'>Gentle/suggestion</td><td style='padding:6px;border-top:1px solid #ddd;'>Why don't you try a different approach?</td></tr>
</table>
<p><strong>Grammar note:</strong> <em>Should / ought to</em> are followed by the <strong>base verb</strong> (infinitive without <em>to</em>) — except <em>ought to</em> which keeps the <em>to</em>: <em>You ought <u>to</u> try.</em></p>""",
 "tasks":[
  {"title":"Choose the right form","instr":"Complete with should/shouldn't, ought to, or if I were you:<br>1. You ___ arrive late to a job interview. (negative)<br>2. ___, I'd research the company before applying.<br>3. You ___ to practise your presentation out loud.","ans":"1. shouldn't · 2. If I were you · 3. ought"},
  {"title":"Transform the advice","instr":"Give the same advice using 3 different forms:<br><em>Problem: My student keeps making the same grammar mistake.</em>","ans":"You should ask them to write it correctly 5 times. / If I were you, I'd use a different context to explain it. / Why don't you try a grammar game?"},
  {"title":"What would you say?","instr":"A friend says: 'I'm nervous about speaking English at work.' Write 3 pieces of advice using 3 different expressions.","ans":"You should practise with a native speaker. / If I were you, I'd prepare key phrases before each meeting. / Why don't you join an English conversation club?"},
 ],
 "production":"Write a short 'advice column' response. Someone wrote: <em>'I've been learning English for two years but I'm still afraid to speak. Help!'</em> Write 4 sentences of advice using at least 3 different expressions from today's lesson."
},

{
 "title":"Reported Speech: What the Guest Said",
 "level":"B2","framework":"TTT · Grammar",
 "tags":"B2 English, reported speech, indirect speech, B2 grammar, 5-Minute English Lab",
 "seo_title":"Reported Speech in English: What the Guest Said | B2 Grammar Lesson",
 "meta":"Master reported speech in English — direct to indirect, tense backshift, and reporting verbs. B2 grammar lesson.",
 "anecdote":"At team briefings at Establishment in Sydney, I'd report what guests had complained about the night before. 'The guest said the table <em>was</em> too small' — not 'the table <em>is</em> too small.' That tense shift is reported speech, and in a professional context, getting it wrong sounds careless.",
 "aim":"transform direct speech into reported speech with correct tense backshift and reporting verbs.",
 "focus":["said / told / asked / explained","present → past backshift","'I am' → she said she was","'I will' → she said she would"],
 "explanation":"""<p>When we report what someone said, we shift the tense <strong>back one step</strong> into the past:</p>
<table style='width:100%;border-collapse:collapse;font-size:0.88em;margin:8px 0;'>
<tr style='background:#f5eef8;'><th style='padding:7px;text-align:left;'>Direct</th><th style='padding:7px;text-align:left;'>Reported</th></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>"I <strong>am</strong> unhappy."</td><td style='padding:6px;border-top:1px solid #ddd;'>She said she <strong>was</strong> unhappy.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>"The table <strong>is</strong> dirty."</td><td style='padding:6px;border-top:1px solid #ddd;'>He said the table <strong>was</strong> dirty.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>"I <strong>will</strong> return tomorrow."</td><td style='padding:6px;border-top:1px solid #ddd;'>She said she <strong>would</strong> return.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>"We <strong>can't</strong> wait."</td><td style='padding:6px;border-top:1px solid #ddd;'>They said they <strong>couldn't</strong> wait.</td></tr>
<tr><td style='padding:6px;border-top:1px solid #ddd;'>"<strong>Have</strong> you got a table?"</td><td style='padding:6px;border-top:1px solid #ddd;'>He asked if we <strong>had</strong> a table.</td></tr>
</table>
<p><strong>Key difference:</strong> Use <em>said</em> with no object. Use <em>told</em> with a person: <em>She <u>told me</u> she was leaving.</em></p>""",
 "tasks":[
  {"title":"Backshift practice","instr":"Report these sentences:<br>1. 'I'm not happy with my room.' (guest / say)<br>2. 'We will upgrade you.' (manager / promise)<br>3. 'Can you come back later?' (receptionist / ask)","ans":"1. The guest said she wasn't happy with her room. · 2. The manager promised he would upgrade her. · 3. The receptionist asked if I/we could come back later."},
  {"title":"Said or told?","instr":"Choose the correct verb:<br>1. She ___ that the food was cold. (said/told)<br>2. He ___ me the room was ready. (said/told)<br>3. They ___ they'd be late. (said/told)","ans":"1. said · 2. told · 3. said"},
  {"title":"Spot the error","instr":"Find and correct: <em>'The manager said he will speak to the chef and the kitchen is aware of the issue.'</em>","ans":"'...he <u>would</u> speak to the chef and the kitchen <u>was</u> aware of the issue.' (tense backshift needed)"},
 ],
 "production":"Write a short briefing note (5 sentences) for a hotel shift handover. Report what 3 different guests said during the previous shift. Use: <em>said, told, asked, complained, explained.</em>"
},

{
 "title":"Hedging Language: How to Sound Academic and Confident",
 "level":"C1","framework":"Guided Discovery · Academic Language",
 "tags":"C1 English, academic writing, hedging language, advanced English, 5-Minute English Lab",
 "seo_title":"Hedging in Academic English: Softening Claims Like a Pro | C1 Advanced",
 "meta":"Master hedging language for academic writing and professional communication. C1 advanced English lesson with authentic examples.",
 "anecdote":"When I was writing up my teaching observations during the CELTA course — 120 hours of closely supervised practice — I noticed that the most credible feedback always hedged: 'This <em>tends to</em> work well with lower levels' rather than 'This works.' Hedging is not weakness; it is precision.",
 "aim":"use hedging language (modal verbs, adverbs, impersonal structures) to qualify claims appropriately in academic and professional writing.",
 "focus":["may / might / could","tends to / appears to","It is likely that...","It could be argued that...","generally / typically / in most cases"],
 "explanation":"""<p>Academic and professional writers do not say <em>'X is true.'</em> They say <em>'X <strong>appears to</strong> be true'</em> or <em>'X <strong>may</strong> be true in most cases.'</em> This is called <strong>hedging</strong> — limiting the scope of a claim so it can be defended.</p>
<p><strong>Four hedging tools:</strong></p>
<ol>
<li><strong>Modal verbs:</strong> may / might / could / would → <em>This <u>may</u> affect motivation.</em></li>
<li><strong>Adverbs:</strong> generally / typically / often / in most cases → <em>Adult learners <u>generally</u> prefer explicit rules.</em></li>
<li><strong>Verbs of probability:</strong> appears to / tends to / seems to → <em>This approach <u>tends to</u> work at B1+.</em></li>
<li><strong>Impersonal structures:</strong> It is possible that / It could be argued that → <em><u>It is possible that</u> motivation is the key factor.</em></li>
</ol>
<p><strong>Warning:</strong> Over-hedging weakens your argument. Do not hedge every sentence — use it where genuine uncertainty exists.</p>""",
 "tasks":[
  {"title":"Add a hedge","instr":"Make these claims more appropriately cautious for academic writing:<br>1. 'Explicit grammar instruction works better for adults.'<br>2. 'Motivation determines success in language learning.'<br>3. 'Students don't learn from repetitive drilling.'","ans":"1. Explicit grammar instruction <u>may work</u> better for adults <u>in many contexts</u>. · 2. Motivation <u>tends to</u> be a significant factor in language learning success. · 3. <u>It could be argued that</u> students <u>do not always</u> benefit from repetitive drilling."},
  {"title":"Identify the hedging device","instr":"What type of hedge is used in each?<br>1. 'This approach seems to promote fluency.' · 2. 'In most cases, learners prefer communicative tasks.' · 3. 'It is possible that affective factors play a role.'","ans":"1. Verb of probability (seems to) · 2. Adverb phrase (in most cases) · 3. Impersonal structure (it is possible that)"},
  {"title":"Over-hedged or under-hedged?","instr":"Evaluate: <em>'It might perhaps possibly be the case that some learners may sometimes arguably tend to have possible difficulties with certain aspects of grammar.'</em>","ans":"Massively over-hedged — almost meaningless. A better version: 'Some learners <u>may</u> struggle with certain grammar points, <u>particularly</u> at lower levels.'"},
 ],
 "production":"Write a short paragraph (4–5 sentences) making an argument about language learning or your professional field. Use at least 3 different hedging devices — one modal verb, one adverb of frequency/degree, and one impersonal structure."
},

]

results = []
for i, lesson in enumerate(lessons):
    print(f"[{i+1}/{len(lessons)}] Posting: {lesson['title'][:60]}...")
    html = build_html(lesson)
    payload = {
        "title": lesson["title"],
        "content": html,
        "status": "draft",
        "category": "English Teaching",
        "tags": lesson["tags"],
        "meta_description": lesson["meta"],
        "seo_title": lesson["seo_title"]
    }
    try:
        r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
        data = r.json()
        post_id = data.get("post_id") or data.get("id") or "?"
        print(f"  ✅ Status {r.status_code} · Post ID: {post_id}")
        results.append({"title": lesson["title"], "status": r.status_code, "post_id": post_id})
    except Exception as e:
        print(f"  ❌ Error: {e}")
        results.append({"title": lesson["title"], "status": "error", "post_id": None})
    time.sleep(1.2)

print("\n── SUMMARY ──")
ok = [r for r in results if str(r["status"]) == "200"]
print(f"✅ {len(ok)}/{len(results)} lessons posted successfully")
for r in results:
    print(f"  {r['status']} | ID {r['post_id']} | {r['title'][:50]}")
