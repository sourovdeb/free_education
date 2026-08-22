#!/usr/bin/env python3
"""
Create 30 CELTA-style interactive HTML lessons as WordPress drafts.
Personal experience: Sourov Deb — 18 yrs hospitality Sydney, immigration story,
4 languages, La Réunion life, daughter, Cambridge CELTA course completed.
Key: 0767044896thevenet_
No Claude/Anthropic trademarks. No "certified/qualified" for CELTA.
"""
import urllib.request, json, time, sys

WP_API  = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
WP_KEY  = "0767044896thevenet_"
CAT_ELT = 9   # English Teaching

DISCLAIMER = '<p style="font-size:0.72em;color:#a0aec0;text-align:center;margin-top:30px;border-top:1px solid #e2e8f0;padding-top:15px;"><em>Independent project; not affiliated with, endorsed by, or accredited by Cambridge University Press &amp; Assessment. Confers no qualification.</em></p>'

def card(emoji, title, body, bg, border, text_color):
    return f'''<div style="background:{bg};border-left:5px solid {border};border-radius:10px;padding:18px 20px;margin-bottom:18px;">
<h3 style="color:{text_color};margin:0 0 8px;font-size:1.05em;">{emoji} {title}</h3>
<div style="color:#2d3748;line-height:1.7;">{body}</div></div>'''

def quiz_row(q, options, answer_idx):
    opts = ""
    for i, o in enumerate(options):
        letter = chr(65+i)
        opts += f'<label style="display:block;padding:6px 10px;margin:4px 0;background:#fff;border-radius:6px;border:2px solid #e2e8f0;cursor:pointer;"><input type="radio" name="q{q}" value="{i}" onchange="checkQ({q},{answer_idx},this)"> {letter}. {o}</label>'
    return f'''<div id="q{q}wrap" style="margin:10px 0;">{opts}<div id="q{q}result" style="font-weight:700;padding:6px 0;display:none;"></div></div>'''

CHECK_JS = '<script>function checkQ(n,a,el){var r=document.getElementById("q"+n+"result");if(el.value==a){r.style.color="#38a169";r.textContent="✅ Correct!";} else{r.style.color="#e53e3e";r.textContent="❌ Try again!";} r.style.display="block";}</script>'

def header_html(title, level, audience, emoji):
    colors = {
        "A1": "linear-gradient(135deg,#f093fb,#f5576c)",
        "A2": "linear-gradient(135deg,#4facfe,#00f2fe)",
        "B1": "linear-gradient(135deg,#43e97b,#38f9d7)",
        "B2": "linear-gradient(135deg,#fa709a,#fee140)",
        "C1": "linear-gradient(135deg,#a18cd1,#fbc2eb)",
    }
    bg = colors.get(level, "linear-gradient(135deg,#667eea,#764ba2)")
    return f'''<div style="background:{bg};border-radius:16px;padding:28px 24px;margin-bottom:22px;color:#fff;text-align:center;box-shadow:0 4px 15px rgba(0,0,0,.15);">
<span style="font-size:2.6em;display:block;margin-bottom:8px;">{emoji}</span>
<h2 style="margin:0 0 6px;font-size:1.6em;font-weight:800;">{title}</h2>
<p style="margin:0;opacity:.9;font-size:.9em;">Level: <strong>{level}</strong> · 5 minutes · {audience}</p>
</div>'''

def wrap(inner):
    return f'<div style="font-family:\'Segoe UI\',Arial,sans-serif;max-width:820px;margin:0 auto;padding:16px;">{CHECK_JS}{inner}{DISCLAIMER}</div>'

# ─── LESSON DATA ─────────────────────────────────────────────────────────────

LESSONS = [

# ── BATCH 1: Kids A1 ──────────────────────────────────────────────────────────

{
"title": "My Daughter Taught Me: Colours in English",
"level": "A1", "audience": "Young Learners & Parents", "emoji": "🎨",
"tags": ["colours","A1","young learners","vocabulary","kids"],
"meta": "Learn colours in English with a fun interactive lesson for young learners. Inspired by a real moment with my daughter in La Réunion.",
"seo_title": "Colours in English – A1 Interactive Lesson for Kids",
"body": lambda: card("💡","Today's Idea",
    "We use <strong>colour words</strong> to describe the world around us.<br>In English: <em>red, blue, green, yellow, orange, purple, pink, white, black, brown.</em>",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "My daughter was eighteen months old when she pointed at the flamboyan tree outside our window in Saint-Pierre, La Réunion, and said something that sounded like <em>red</em>. She was right — those flowers are a blazing red-orange. Children learn colours before almost anything else. They don't learn rules first; they notice the world first.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Examples",
    "<ul style='margin:0;padding-left:20px;'><li>The sun is <strong>yellow</strong>. ☀️</li><li>The sea is <strong>blue</strong>. 🌊</li><li>Grass is <strong>green</strong>. 🌿</li><li>My daughter's coat is <strong>red</strong>. 🧥</li></ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Look around the room. Name <strong>5 things</strong> and their colour in English. Say them out loud:<br><br>Example: <em>My bag is <strong>black</strong>. The wall is <strong>white</strong>.</em><br><br><strong>Your turn →</strong> Say 5 sentences now!",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>What colour is a ripe banana?</strong></p>" +
quiz_row(1, ["red","yellow","blue","green"], 1) + "</div>"
},

{
"title": "Animals I've Seen: From Sydney to La Réunion",
"level": "A1", "audience": "Young Learners", "emoji": "🦎",
"tags": ["animals","A1","young learners","vocabulary","nature"],
"meta": "Learn animal names in English with a fun lesson inspired by real animals spotted from Sydney to La Réunion island.",
"seo_title": "Animals in English – A1 Lesson for Kids",
"body": lambda: card("💡","Today's Idea",
    "Learn <strong>animal names</strong> in English. Animals are one of the first topics children love to talk about!",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "In Sydney I worked nights at the casino, and one quiet morning I walked along Bondi Beach and watched a pelican land two metres away and stare at me. In La Réunion, geckos live on every wall. My daughter chases them and yells something in her own private language. Animals are everywhere — and knowing their names in English opens a conversation with almost any child on earth.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Animal Words",
    "<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>" +
    "".join(f"<div style='background:#f7fafc;border-radius:6px;padding:8px;text-align:center;'>{e} <strong>{n}</strong></div>" for e,n in [
        ("🐕","dog"),("🐈","cat"),("🐦","bird"),("🐟","fish"),
        ("🐘","elephant"),("🦁","lion"),("🦎","lizard"),("🐆","leopard"),
    ]) + "</div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Point at each animal emoji above and say the word in English. Then: <strong>Which animal do you like best? Say: I like the ___.</strong>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which animal lives in the sea?</strong></p>" +
quiz_row(2,["cat","dog","fish","bird"],2)+"</div>"
},

{
"title": "At the Market: Food Words in English",
"level": "A1", "audience": "Young Learners & Beginners", "emoji": "🛒",
"tags": ["food","A1","vocabulary","young learners","market"],
"meta": "Learn food vocabulary in English with a colourful A1 lesson for kids and beginners. Inspired by the Saint-Pierre market in La Réunion.",
"seo_title": "Food Vocabulary in English – A1 Lesson for Kids & Beginners",
"body": lambda: card("💡","Today's Idea",
    "Learn <strong>food words</strong> in English. Food vocabulary is essential — at school, at home, at the shops!",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "The market in Saint-Pierre opens at six in the morning. I go on Saturdays. The colours are extraordinary — purple aubergines, yellow mangoes, red tomatoes, green beans. After eighteen years in professional kitchens in Sydney — The Ivy, Uccello, the Star Casino — I still find the best ingredient is knowing what you're looking at. Food vocabulary was one of the first things I learned when I arrived in Australia unable to speak 'proper' English. If you can name it, you can ask for it.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Food Words",
    "<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>" +
    "".join(f"<div style='background:#f7fafc;border-radius:6px;padding:8px;text-align:center;'>{e} <strong>{n}</strong></div>" for e,n in [
        ("🍎","apple"),("🍌","banana"),("🍅","tomato"),("🥕","carrot"),
        ("🥚","egg"),("🍞","bread"),("🧀","cheese"),("🍊","orange"),
    ]) + "</div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Open your fridge or cupboard. Name <strong>3 foods</strong> in English. Use: <strong>I have a/an ___ .</strong><br><br>Example: <em>I have an apple. I have some bread.</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which food is a vegetable?</strong></p>" +
quiz_row(3,["apple","banana","carrot","orange"],2)+"</div>"
},

{
"title": "My Family: Family Words in English",
"level": "A1", "audience": "Young Learners & Beginners", "emoji": "👨‍👩‍👧",
"tags": ["family","A1","vocabulary","young learners"],
"meta": "Learn family vocabulary in English with this fun A1 lesson for young learners and beginners.",
"seo_title": "Family Words in English – A1 Lesson for Kids",
"body": lambda: card("💡","Today's Idea",
    "Learn <strong>family words</strong> in English: <em>mother, father, sister, brother, grandmother, grandfather, daughter, son.</em>",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "My family stretches across three continents. My mother is in Bangladesh. My wife Vanessa is French. Our daughter was born here in La Réunion. My brother is in Dhaka. Family vocabulary is personal — it carries the weight of real relationships. When I was learning French, the word for daughter — <em>fille</em> — became more than a word the day she was born.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Family Words",
    "<ul style='margin:0;padding-left:20px;line-height:2;'><li>👩 <strong>mother</strong> — my mother is called Ruma</li><li>👨 <strong>father</strong></li><li>👧 <strong>daughter</strong> — I have one daughter</li><li>👦 <strong>son</strong></li><li>👩 <strong>sister</strong></li><li>👨 <strong>brother</strong> — my brother is younger than me</li><li>👴 <strong>grandfather</strong></li><li>👵 <strong>grandmother</strong></li></ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Draw a simple family tree. Write the English word next to each person.<br><br>Then say: <strong>My ___ is called ___.</strong>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>What do you call your mother's mother?</strong></p>" +
quiz_row(4,["aunt","sister","grandmother","daughter"],2)+"</div>"
},

{
"title": "Numbers 1–20: At the Restaurant",
"level": "A1", "audience": "Young Learners & Beginners", "emoji": "🔢",
"tags": ["numbers","A1","vocabulary","young learners","restaurant"],
"meta": "Learn numbers 1–20 in English with this fun interactive A1 lesson for young learners, set in a restaurant context.",
"seo_title": "Numbers in English 1–20 – A1 Lesson for Kids",
"body": lambda: card("💡","Today's Idea",
    "Learn to say <strong>numbers 1–20</strong> in English. Numbers are everywhere — in the classroom, the shops, the street.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "At The Ivy in Sydney — one of the busiest restaurants in Australia — I managed a team and every night I counted: table fourteen, party of eight, twelve drinks ordered, nine courses served. Numbers are not just maths. They are the language of coordination. My very first job in Australia, before the restaurants, was at a grocery store. The manager asked me to count the boxes on the shelf. I knew the numbers. That was enough to get started.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Numbers 1–20",
    "<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:6px;text-align:center;'>" +
    "".join(f"<div style='background:#ebf8ff;border-radius:6px;padding:8px;font-size:1.1em;'><strong>{n}</strong><br><span style='font-size:.85em;color:#4a5568;'>{w}</span></div>" for n,w in zip(range(1,21),
    ["one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty"])) + "</div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Count aloud from 1 to 20. Then count backwards from 20 to 1. Then: <strong>How old are you? Say: I am ___ years old.</strong>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>What is 5 + 8?</strong></p>" +
quiz_row(5,["twelve","thirteen","fourteen","fifteen"],1)+"</div>"
},

# ── BATCH 2: A2 ─────────────────────────────────────────────────────────────

{
"title": "My Daily Routine in La Réunion",
"level": "A2", "audience": "Teens & Adults", "emoji": "⏰",
"tags": ["present simple","A2","grammar","daily routine","speaking"],
"meta": "Learn to talk about your daily routine using the Present Simple tense. An A2 interactive lesson with a personal story from La Réunion.",
"seo_title": "Daily Routine in English – A2 Present Simple Lesson",
"body": lambda: card("💡","Today's Idea",
    "We use the <strong>Present Simple</strong> to describe habits and routines.<br><em>Subject + base verb</em> (he/she/it → +s): <strong>I wake up</strong> at 7. <strong>She drinks</strong> coffee.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "Since moving to La Réunion from Australia via France, I learned that routine is not boring — it is protective. My psychiatrist here talks about rhythm: same wake time, same walk, same writing hour. For someone with bipolar I, the daily routine is not a schedule. It is the structure that keeps everything else from falling apart. I walk 40 minutes every morning before I write. The Indian Ocean is ten minutes away. That detail in the routine keeps it real.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Examples",
    "<ul style='margin:0;padding-left:20px;line-height:2;'><li>I <strong>wake up</strong> at 7:00.</li><li>I <strong>have</strong> coffee and fruit.</li><li>I <strong>walk</strong> along the seafront.</li><li>I <strong>write</strong> for one hour.</li><li>My daughter <strong>plays</strong> in the afternoon.</li><li>We <strong>eat</strong> dinner at 7:30.</li></ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Write <strong>5 sentences</strong> about YOUR daily routine. Use: <strong>I ___ at ___.</strong><br><br>Then say them aloud to check the <strong>-s ending</strong> for he/she/it.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>He ___ coffee every morning. (drink)</strong></p>" +
quiz_row(6,["drink","drinks","drank","drinking"],1)+"</div>"
},

{
"title": "I Used to Live in Sydney: Talking About the Past",
"level": "A2", "audience": "Teens & Adults", "emoji": "🏙️",
"tags": ["used to","A2","grammar","past habits","speaking"],
"meta": "Learn 'used to' in English to talk about past habits. A2 lesson with personal stories from Sydney to La Réunion.",
"seo_title": "'Used to' in English – A2 Grammar Lesson | Past Habits",
"body": lambda: card("💡","Today's Idea",
    "<strong>Used to + base verb</strong> describes a past habit or state that is no longer true.<br><em>I used to work nights. I didn't use to sleep before 3 a.m.</em>",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I used to work until 3 a.m. at the Star Casino in Sydney. I used to manage a floor of fifty tables. I used to live in a city of five million people. None of that is my life now. I live in Saint-Pierre. Population: 80,000. I used to think silence was something that happened to other people. Now I wake up to birdsong and a gecko on the wall. <em>Used to</em> is one of the most personal structures in English — it forces you to compare then and now.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Form & Examples",
    "<div style='background:#f7fafc;border-radius:8px;padding:12px;margin-bottom:10px;font-family:monospace;'>" +
    "✅ I <strong>used to</strong> live in Sydney.<br>✅ She <strong>used to</strong> work nights.<br>❌ I <strong>didn't use to</strong> speak French.<br>❓ <strong>Did</strong> you <strong>use to</strong> cook professionally?</div>" +
    "<p style='margin:4px 0;'>Key point: it's <strong>use to</strong> (no <em>d</em>) after <em>did/didn't</em>.</p>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Write <strong>3 sentences</strong> about something you used to do but don't do anymore.<br><em>I used to ___ but now I ___.</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>She ___ eat meat, but she's vegetarian now.</strong></p>" +
quiz_row(7,["uses to","used to","use to","was use to"],1)+"</div>"
},

{
"title": "Travel English: At the Airport",
"level": "A2", "audience": "Teens & Adults", "emoji": "✈️",
"tags": ["travel","A2","vocabulary","airport","functional language"],
"meta": "Learn essential airport vocabulary and phrases in English. An A2 interactive lesson with a real immigration story.",
"seo_title": "Airport English – A2 Travel Vocabulary Lesson",
"body": lambda: card("💡","Today's Idea",
    "Learn key <strong>airport vocabulary</strong>: check-in, boarding pass, departure gate, immigration, customs, arrivals hall.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I have been through the immigration line at Sydney Airport (2005), Charles de Gaulle (2017), and Roland Garros in La Réunion more times than I can count. The one that stays with me is CDG in January 2017. It was snowing. Vanessa was waiting. I had come from Bangladesh. I had one bag. The immigration officer asked three questions. I answered in French. I remember thinking: this is working. That feeling — understanding and being understood in a foreign language at a border — is one of the finest feelings a language learner can have.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Key Airport Phrases",
    "<ul style='margin:0;padding-left:20px;line-height:2;'><li>Could I see your <strong>passport</strong>, please?</li><li>Here is my <strong>boarding pass</strong>.</li><li>My <strong>luggage</strong> is checked in.</li><li>Which is the <strong>departure gate</strong>?</li><li>I am here for <strong>tourism / work / family</strong>.</li><li>Do I need to go through <strong>customs</strong>?</li></ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Imagine you are at an airport. Answer these questions:<br><br><em>1. Where are you travelling to?<br>2. How long will you stay?<br>3. What is the purpose of your visit?</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>You give this to the person at the gate before you get on the plane:</strong></p>" +
quiz_row(8,["passport","boarding pass","visa","luggage"],1)+"</div>"
},

{
"title": "Small Talk That Works: Starting a Conversation",
"level": "A2", "audience": "Teens & Adults", "emoji": "💬",
"tags": ["speaking","A2","small talk","functional language","social English"],
"meta": "Learn how to make small talk in English. An A2 lesson on starting and maintaining a conversation, from someone who did it for 18 years in hospitality.",
"seo_title": "Small Talk in English – A2 Speaking Lesson",
"body": lambda: card("💡","Today's Idea",
    "<strong>Small talk</strong> is short, friendly conversation about everyday topics: the weather, work, the weekend. It builds relationships.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "Eighteen years behind a bar and on a restaurant floor taught me one thing about small talk: it is not small. A guest who feels genuinely seen — not just served — becomes a regular. At Merivale in Sydney, the sommelier who remembered a guest's last wine order, the barista who knew their name: that was small talk made into loyalty. I was always the one who remembered. It is a skill, and English small talk has its own rules.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Small Talk Phrases",
    "<div style='line-height:2;'><strong>Opening:</strong><br>" +
    "<em>How are you? / How's it going? / Lovely day, isn't it?</em><br><br>" +
    "<strong>Topics:</strong><br>" +
    "<em>Did you have a good weekend?<br>Have you been busy lately?<br>What do you do?</em><br><br>" +
    "<strong>Keeping it going:</strong><br>" +
    "<em>Oh really? / That's interesting! / Tell me more.</em><br><br>" +
    "<strong>Closing politely:</strong><br>" +
    "<em>Well, it was nice talking to you!</em></div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Have a short conversation — with a partner, or out loud by yourself. Use these steps:<br><br>1️⃣ Open with a question.<br>2️⃣ Listen and respond with <em>Oh really?</em><br>3️⃣ Ask a follow-up question.<br>4️⃣ Close politely.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which is a good small-talk opener?</strong></p>" +
quiz_row(9,["What is your salary?","Lovely weather today, isn't it?","Do you have any health problems?","How much did that cost?"],1)+"</div>"
},

{
"title": "The /θ/ Sound: The One Nobody Gets Right",
"level": "A2", "audience": "All Learners", "emoji": "👅",
"tags": ["pronunciation","A2","phonology","th sound","speaking"],
"meta": "Master the English /θ/ sound — the most common pronunciation challenge for learners worldwide. Interactive A2 lesson with audio practice.",
"seo_title": "The TH Sound in English – A2 Pronunciation Lesson",
"body": lambda: card("💡","Today's Idea",
    "The English <strong>/θ/ sound</strong> (as in <em>think, three, mouth</em>) does not exist in most languages. It is made by placing your tongue gently between your teeth and blowing air.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I am a native Bengali and English speaker. Bengali has no /θ/. When I started teaching English and doing the Cambridge CELTA course — 120 supervised teaching hours — the /θ/ sound was consistently the hardest moment in pronunciation work. A student from France, one from Japan, one from Brazil, all made the same error: <em>sink</em> for <em>think</em>, <em>free</em> for <em>three</em>. The good news: it takes two minutes to place the tongue correctly. After that, it is just practice.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","How to Make /θ/",
    "<ol style='margin:0;padding-left:20px;line-height:2;'><li>Put your <strong>tongue tip</strong> between your upper and lower teeth.</li><li><strong>Blow air</strong> gently — do not vibrate your throat.</li><li>Say: <strong>th-th-th-think</strong></li></ol><br>" +
    "<strong>Practice words:</strong> <em>think · three · thank · tooth · month · birthday · weather · brother</em><br><br>" +
    "<div style='background:#f7fafc;padding:10px;border-radius:6px;'><strong>Tongue twister:</strong> <em>Think of three thin things.</em></div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Say these 5 words OUT LOUD, slowly, feeling your tongue touch your teeth:<br><br><strong>think · thank · three · birthday · tooth</strong><br><br>Then say the tongue twister three times, faster each time.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>To make /θ/ correctly, where is your tongue?</strong></p>" +
quiz_row(10,["Behind your top teeth","Between your teeth","Behind your bottom teeth","On the roof of your mouth"],1)+"</div>"
},

# ── BATCH 3: B1 Grammar ──────────────────────────────────────────────────────

{
"title": "I Have Worked in Four Countries: The Present Perfect",
"level": "B1", "audience": "Teens & Adults", "emoji": "🌍",
"tags": ["present perfect","B1","grammar","career","experience"],
"meta": "Learn the Present Perfect tense in English with a B1 interactive lesson. Real examples from a career across four countries.",
"seo_title": "Present Perfect in English – B1 Grammar Lesson | Life Experience",
"body": lambda: card("💡","Today's Idea",
    "<strong>Present Perfect = have/has + past participle.</strong><br>Use it for: (1) life experience up to now, (2) recent past with present relevance, (3) with <em>just, already, yet, ever, never.</em>",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "Here is a sentence I genuinely use: <em>I have worked in Australia, Bangladesh, France, and La Réunion.</em> That sentence is Present Perfect because I am still alive; the experience is connected to now; it defines who I am. Compare: <em>I worked at the Star Casino from 2009 to 2014</em> — that is Past Simple because it is a finished, dated event. The difference is whether the past is still attached to the present. In my case, every country I have lived in is still part of who I am today.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Form & Examples",
    "<div style='background:#f7fafc;border-radius:8px;padding:12px;margin-bottom:10px;font-family:monospace;'>" +
    "I have <strong>lived</strong> in four countries.<br>" +
    "Have you ever <strong>eaten</strong> tropical fruit?<br>" +
    "I have never <strong>been</strong> to Japan.<br>" +
    "She has just <strong>arrived</strong>.<br>" +
    "Has he <strong>finished</strong> yet?</div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Write <strong>4 true sentences</strong> about your own life experience using Present Perfect:<br><br><em>I have (never/ever/already) ___.</em><br><br>Share them with a partner — or say them aloud.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>___ you ever eaten durian fruit?</strong></p>" +
quiz_row(11,["Do","Did","Have","Are"],2)+"</div>"
},

{
"title": "If I Hadn't Left Sydney… The Second Conditional",
"level": "B1", "audience": "Teens & Adults", "emoji": "🔀",
"tags": ["second conditional","B1","grammar","hypothetical","if clauses"],
"meta": "Learn the Second Conditional in English with a B1 interactive lesson. Real hypothetical examples from an immigrant's life story.",
"seo_title": "Second Conditional in English – B1 Grammar Lesson",
"body": lambda: card("💡","Today's Idea",
    "<strong>Second Conditional: If + Past Simple, would + base verb.</strong><br>Use it for imaginary or unlikely situations in the present or future.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "If I hadn't left Sydney in 2017, I would never have met my daughter. If I had stayed in hospitality, I would still be working until 3 a.m. If I hadn't studied French to C1, I wouldn't be able to have a conversation with my wife's family. These are not sad thoughts — they are the structure of a life examined. The Second Conditional is the grammar of crossroads. Every major decision in your life is a Second Conditional waiting to be written.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Form & Examples",
    "<div style='background:#f7fafc;border-radius:8px;padding:12px;margin-bottom:10px;font-family:monospace;'>" +
    "If I <strong>lived</strong> in Sydney, I <strong>would work</strong> nights.<br>" +
    "If she <strong>spoke</strong> English, she <strong>would get</strong> the job.<br>" +
    "What <strong>would</strong> you do if you <strong>won</strong> a million euros?</div>" +
    "<p><em>Note: Use <strong>were</strong> (not <em>was</em>) in formal writing: <em>If I were you…</em></em></p>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Complete these sentences honestly:<br><br><em>If I spoke perfect English, I would ___.<br>If I could live anywhere, I would live in ___.<br>If I had more time, I would ___.</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>If I ___ the time, I would learn Japanese.</strong></p>" +
quiz_row(12,["have","had","will have","having"],1)+"</div>"
},

{
"title": "Giving Advice: Should, Ought To, Had Better",
"level": "B1", "audience": "Teens & Adults", "emoji": "💡",
"tags": ["modals","B1","grammar","advice","should"],
"meta": "Learn how to give advice in English using should, ought to, and had better. B1 grammar lesson with real-life examples.",
"seo_title": "Giving Advice in English – Should, Ought To, Had Better | B1",
"body": lambda: card("💡","Today's Idea",
    "<strong>Should</strong> (general advice) · <strong>ought to</strong> (duty/expectation) · <strong>had better</strong> (strong advice, warning of consequences).",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "As a team manager in Sydney, giving advice was part of the job. <em>You should speak to the guest directly — don't send a message.</em> <em>You ought to know the menu before the service starts.</em> <em>You'd better be on time tonight — it's a VIP booking.</em> The three structures are not the same. <em>Should</em> is gentle. <em>Had better</em> carries a consequence. Learning which one to use stopped me from sounding harsh when I meant to be helpful.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Form & Examples",
    "<ul style='margin:0;padding-left:20px;line-height:2;'>" +
    "<li><strong>Should + base verb:</strong> You <em>should</em> practise every day.</li>" +
    "<li><strong>Ought to + base verb:</strong> Teachers <em>ought to</em> give clear instructions.</li>" +
    "<li><strong>Had better + base verb:</strong> You <em>had better</em> study — the exam is tomorrow.</li>" +
    "<li>Negative: <em>You <strong>shouldn't</strong> skip class.</em></li></ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Give advice to a friend who is learning English but never practises speaking. Use all three structures:<br><br><em>You should ___. You ought to ___. You'd better ___.</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>You ___ better leave now — the train goes in five minutes.</strong></p>" +
quiz_row(13,["should","had","ought","must"],1)+"</div>"
},

{
"title": "The Passive Voice: When the Actor Disappears",
"level": "B1", "audience": "Teens & Adults", "emoji": "🎭",
"tags": ["passive voice","B1","grammar","writing","formal English"],
"meta": "Learn the Passive Voice in English with this B1 interactive lesson. When to use it and why — with real examples from professional contexts.",
"seo_title": "Passive Voice in English – B1 Grammar Lesson",
"body": lambda: card("💡","Today's Idea",
    "<strong>Passive = to be + past participle.</strong><br>Use it when the action is more important than who does it, or when the actor is unknown/unimportant.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I learned the value of the passive voice in the most unpleasant way. When something went wrong at a restaurant — a dish arrived cold, a booking was lost — the passive was the language of institutional deflection: <em>The booking was not entered into the system.</em> Nobody did it. The passive erases the actor. In formal and institutional writing, this is sometimes deliberate. Understanding it is essential for reading official documents, workplace communication, and academic writing.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Form & Examples",
    "<div style='background:#f7fafc;border-radius:8px;padding:12px;margin-bottom:10px;'>" +
    "<strong>Active:</strong> The chef <em>cooked</em> the meal.<br>" +
    "<strong>Passive:</strong> The meal <em>was cooked</em> by the chef.<br><br>" +
    "<strong>Active:</strong> Someone <em>changed</em> the record.<br>" +
    "<strong>Passive:</strong> The record <em>was changed</em>.<br><br>" +
    "<strong>Present passive:</strong> English <em>is spoken</em> worldwide.</div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Rewrite these sentences in the passive:<br><br><em>1. A teacher marked the essay.<br>2. Someone stole my bag.<br>3. The company sends the report every month.</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>The letter ___ yesterday. (send)</strong></p>" +
quiz_row(14,["is sent","was sent","sent","has sent"],1)+"</div>"
},

{
"title": "Future Plans: Going to vs Will",
"level": "A2", "audience": "Teens & Adults", "emoji": "🔭",
"tags": ["future","A2","grammar","will","going to"],
"meta": "Learn the difference between 'will' and 'going to' in English. An A2 interactive lesson on talking about the future with personal examples.",
"seo_title": "'Will' vs 'Going To' – A2 Future Tense English Lesson",
"body": lambda: card("💡","Today's Idea",
    "<strong>Going to</strong> = plans and intentions (you already decided).<br><strong>Will</strong> = predictions, offers, decisions made right now.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "When I arrived in France in 2017 with one bag and basic French, someone asked what I was planning to do. I said: <em>I'm going to study French properly.</em> That was a plan — already decided. Six months later when I passed the DCL French exam at C1 level, I told Vanessa: <em>I'll cook dinner tonight to celebrate.</em> A spontaneous decision. Same future tense? No — two very different structures, two very different situations.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Form & Examples",
    "<ul style='margin:0;padding-left:20px;line-height:2;'><li>I'<strong>m going to</strong> start a blog. (plan ✅)</li><li>It'<strong>s going to</strong> rain — look at those clouds. (prediction with evidence ✅)</li><li>I'<strong>ll</strong> help you with that. (offer made now ✅)</li><li>I think it'<strong>ll</strong> be fine. (prediction without evidence ✅)</li></ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Answer these questions with a full sentence:<br><br>1. What are you <em>going to</em> do this weekend? (plan)<br>2. Offer to help your partner carry something. (will)",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>\"I can't carry all these bags!\" → \"Don't worry, I ___ help you.\"</strong></p>" +
quiz_row(15,["am going to","will","going to","would"],1)+"</div>"
},

# ── BATCH 4: B1-B2 Skills ────────────────────────────────────────────────────

{
"title": "How to Sound Polite in English",
"level": "B1", "audience": "Adults & Professionals", "emoji": "🎩",
"tags": ["politeness","B1","speaking","functional language","workplace English"],
"meta": "Learn how to sound polite in English with formal and informal language. B1 lesson with examples from luxury hospitality.",
"seo_title": "Polite English – B1 Lesson on Formal and Informal Language",
"body": lambda: card("💡","Today's Idea",
    "Politeness in English is conveyed through <strong>indirect language</strong>, modal verbs, and intonation. Direct is not the same as rude — but context matters.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "At the Establishment Hotel in Sydney, I served guests who paid more for dinner than most people earn in a week. The rule was: never say <em>no</em>. Say <em>I'm afraid we don't have that this evening</em>. Never say <em>you need to</em>. Say <em>we would recommend</em>. The language of luxury hospitality is the language of English politeness at its most developed. It serves a useful purpose: it allows you to say a difficult thing without causing offence.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Polite vs Direct",
    "<div style='background:#f7fafc;border-radius:8px;padding:12px;margin-bottom:10px;'>" +
    "<table style='width:100%;border-collapse:collapse;'><tr style='background:#ebf8ff;'><th style='padding:6px;text-align:left;'>Direct (informal)</th><th style='padding:6px;text-align:left;'>Polite (formal)</th></tr>" +
    "".join(f"<tr style='border-bottom:1px solid #e2e8f0;'><td style='padding:6px;color:#c53030;'>{d}</td><td style='padding:6px;color:#276749;'>{p}</td></tr>" for d,p in [
        ("Give me the menu.","Could I have the menu, please?"),
        ("I want to cancel.","I'd like to cancel, if possible."),
        ("You're wrong.","I'm not sure I agree with that."),
        ("Wait.","Would you mind waiting for a moment?"),
    ]) + "</table></div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Rewrite these as polite English:<br><br><em>1. Tell me the price.<br>2. I want a refund.<br>3. This is wrong.</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which is the most polite?</strong></p>" +
quiz_row(16,["Give me water.","I need water.","Could I have some water, please?","Water!"],2)+"</div>"
},

{
"title": "Email Writing That Actually Works",
"level": "B1", "audience": "Adults & Professionals", "emoji": "📧",
"tags": ["writing","B1","email","professional English","skills"],
"meta": "Learn to write professional emails in English. B1 lesson with real-world templates and structure from 18 years of professional experience.",
"seo_title": "Professional Email Writing in English – B1 Lesson",
"body": lambda: card("💡","Today's Idea",
    "A good professional email has: <strong>Subject line → Greeting → Purpose → Details → Call to action → Closing.</strong><br>Keep it short, clear, and polite.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I have written hundreds of professional emails in English and French — to managers, institutions, lawyers, government agencies. The most important lesson: <em>the subject line is the email</em>. If your subject line does not tell them what you need in five words, most people will not open it. The second lesson: one email, one purpose. When I was fighting a regulatory appeal, I learned to state the issue in the first sentence, the evidence in the second, and the request in the third. Everything else is noise.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Email Structure",
    "<div style='background:#f7fafc;border-radius:8px;padding:14px;font-family:monospace;line-height:2;'>" +
    "<strong>Subject:</strong> Meeting request – 15 June<br>" +
    "<strong>Dear Ms Johnson,</strong><br><br>" +
    "I am writing to request a meeting to discuss my application.<br><br>" +
    "I would be available on Tuesday or Wednesday afternoon.<br><br>" +
    "Please let me know which time suits you.<br><br>" +
    "<strong>Kind regards,</strong><br>Sourov Deb</div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Write a short email (50–80 words) to your English teacher asking to reschedule a class. Use the structure above.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which is the best way to end a professional email?</strong></p>" +
quiz_row(17,["Bye!","Love,","Kind regards,","See ya!"],2)+"</div>"
},

{
"title": "Reading Strategies: How I Read Faster in English",
"level": "B2", "audience": "Teens & Adults", "emoji": "📖",
"tags": ["reading","B2","skills","strategies","comprehension"],
"meta": "Learn effective reading strategies in English. B2 lesson on skimming, scanning, and reading for detail — with real examples.",
"seo_title": "English Reading Strategies – B2 Skills Lesson | Skim, Scan, Detail",
"body": lambda: card("💡","Today's Idea",
    "Three core reading strategies: <strong>Skimming</strong> (get the main idea fast) · <strong>Scanning</strong> (find specific information) · <strong>Reading for detail</strong> (understand fully).",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "When I started reading legal documents for my regulatory appeal in French and English — Ofqual guidance, the Equality Act, CNIL articles — I had to learn to read strategically. The documents were 40–80 pages. I could not read every word. Skimming told me which section applied to me. Scanning found the date, the reference number, the clause. Detailed reading came only when I had isolated the relevant paragraph. This is the strategy of a forensic reader. It applies to academic texts, news articles, and exam passages equally.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","The Three Strategies",
    "<ul style='margin:0;padding-left:20px;line-height:2;'>" +
    "<li><strong>Skimming:</strong> Read the title, headings, first sentence of each paragraph. <em>Time: 30 seconds.</em></li>" +
    "<li><strong>Scanning:</strong> Move your eyes quickly across the page looking for a keyword, number, or name.</li>" +
    "<li><strong>Detailed reading:</strong> Read slowly and carefully. Take notes. Re-read difficult sentences.</li>" +
    "<li>Good readers <strong>choose the right strategy</strong> for each task.</li></ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Find a news article in English. Do this in order:<br><br>1️⃣ Skim: What is the topic? (30 seconds)<br>2️⃣ Scan: Find one number or name in the text. (20 seconds)<br>3️⃣ Read for detail: One paragraph, fully. Can you summarise it in one sentence?",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>You need to find a phone number quickly in a long document. Which strategy do you use?</strong></p>" +
quiz_row(18,["Skimming","Scanning","Detailed reading","Guessing"],1)+"</div>"
},

{
"title": "Listening Between the Lines",
"level": "B1", "audience": "Teens & Adults", "emoji": "👂",
"tags": ["listening","B1","skills","strategies","comprehension"],
"meta": "Learn to understand spoken English better with top-down and bottom-up listening strategies. B1 interactive lesson.",
"seo_title": "English Listening Strategies – B1 Skills Lesson",
"body": lambda: card("💡","Today's Idea",
    "<strong>Top-down listening:</strong> Use your knowledge of the topic to predict and understand.<br><strong>Bottom-up listening:</strong> Focus on individual words, sounds, grammar.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I started my career in Australia unable to understand the Australian accent at speed. Australians swallow half their words. I had two choices: panic, or predict. If I knew the context — a guest was ordering wine — I could guess the gaps. <em>Red or white? How many glasses?</em> I did not need every word. I needed the shape of the conversation. That is top-down listening. Bottom-up came with time, with exposure, with eighteen years of listening in noisy restaurants, casinos, and stockrooms.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","How to Improve Your Listening",
    "<ol style='margin:0;padding-left:20px;line-height:2;'>" +
    "<li><strong>Before listening:</strong> Think about the topic. What do you expect to hear?</li>" +
    "<li><strong>While listening:</strong> Don't translate every word. Focus on key words.</li>" +
    "<li><strong>After:</strong> What did you catch? What was missing?</li>" +
    "<li><strong>Practice tip:</strong> Watch films with English subtitles. Pause. Repeat. Remove subtitles.</li></ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Listen to one minute of a podcast, song, or video in English. Write down <strong>10 words</strong> you heard clearly. Then check: were you using top-down or bottom-up listening?",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>You use your knowledge of the topic to guess words you didn't hear. This is:</strong></p>" +
quiz_row(19,["Bottom-up listening","Top-down listening","Scanning","Inference"],1)+"</div>"
},

# ── BATCH 5: B2-C1 ──────────────────────────────────────────────────────────

{
"title": "Formal vs Informal: Reading the Room in English",
"level": "B2", "audience": "Adults & Professionals", "emoji": "🎯",
"tags": ["register","B2","writing","speaking","formal English","vocabulary"],
"meta": "Learn the difference between formal and informal English register. B2 lesson on when and how to switch — from luxury hospitality to academic writing.",
"seo_title": "Formal vs Informal English – B2 Register Lesson",
"body": lambda: card("💡","Today's Idea",
    "<strong>Register</strong> = the level of formality you choose based on context, audience, and relationship. English has a wide range — from text message to legal document.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "In one day in Sydney I might have had a text from a friend (<em>yo, you working tonight?</em>), written a staff roster (<em>Please ensure the evening team is briefed by 17:00</em>), spoken to a VIP guest (<em>Certainly, Mr Chen — allow me to arrange that immediately</em>), and written a complaint email to HR (<em>I wish to draw your attention to the following matter</em>). Four registers. Same person. Same day. The ability to code-switch is one of the most employable language skills that exists.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Register Spectrum",
    "<div style='background:#f7fafc;border-radius:8px;padding:12px;'>" +
    "<table style='width:100%;border-collapse:collapse;'><tr style='background:#ebf8ff;'><th style='padding:6px;'>Informal</th><th style='padding:6px;'>Neutral</th><th style='padding:6px;'>Formal</th></tr>" +
    "".join(f"<tr style='border-bottom:1px solid #e2e8f0;text-align:center;'><td style='padding:6px;'>{i}</td><td style='padding:6px;'>{n}</td><td style='padding:6px;'>{f}</td></tr>" for i,n,f in [
        ("get","receive","obtain"),
        ("find out","discover","ascertain"),
        ("tell","inform","notify"),
        ("sorry","apologies","I regret to inform you"),
    ]) + "</table></div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Rewrite this informal message in formal English:<br><br><em>\"Hey, can't make it to the meeting tomorrow — something came up. Can we do it another time?\"</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which word is most formal?</strong></p>" +
quiz_row(20,["get","obtain","grab","pick up"],1)+"</div>"
},

{
"title": "Discourse Markers: The Glue Between Ideas",
"level": "C1", "audience": "Adults & Advanced Learners", "emoji": "🔗",
"tags": ["discourse markers","C1","writing","academic English","linking words"],
"meta": "Master discourse markers to write and speak with coherence and flow. C1 lesson on linking language with real essay examples.",
"seo_title": "Discourse Markers in English – C1 Advanced Writing Lesson",
"body": lambda: card("💡","Today's Idea",
    "<strong>Discourse markers</strong> signal how ideas connect: contrast, addition, concession, result, sequence. Without them, ideas exist in isolation. With them, they become argument.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "When I started writing formally in English and French — academic papers, appeals, formal correspondence — I noticed that my ideas were often correct but disconnected. A good sentence, then another good sentence. But no thread between them. The reader does the work of connecting. That is a tax you impose on your reader. Discourse markers reduce that tax. They say: <em>this follows from that, this contradicts that, despite this, that is still true</em>.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Key Discourse Markers",
    "<div style='background:#f7fafc;border-radius:8px;padding:14px;'>" +
    "<table style='width:100%;border-collapse:collapse;'><tr style='background:#ebf8ff;'><th style='padding:6px;text-align:left;'>Function</th><th style='padding:6px;text-align:left;'>Markers</th></tr>" +
    "".join(f"<tr style='border-bottom:1px solid #e2e8f0;'><td style='padding:6px;font-weight:600;'>{fn}</td><td style='padding:6px;'><em>{ms}</em></td></tr>" for fn,ms in [
        ("Addition","furthermore, moreover, in addition"),
        ("Contrast","however, nevertheless, on the other hand"),
        ("Concession","although, despite, even though"),
        ("Result","therefore, consequently, as a result"),
        ("Sequence","firstly, subsequently, finally"),
    ]) + "</table></div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Connect these two ideas with <strong>three different</strong> discourse markers and notice how the meaning changes:<br><br><em>\"I was tired.\" / \"I kept studying.\"</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which discourse marker shows a contrast?</strong></p>" +
quiz_row(21,["Furthermore","Therefore","However","Finally"],2)+"</div>"
},

{
"title": "The Art of Disagreeing Politely in English",
"level": "B2", "audience": "Adults & Professionals", "emoji": "🤝",
"tags": ["disagreement","B2","speaking","functional language","professional English"],
"meta": "Learn how to disagree politely and professionally in English. B2 lesson on diplomatic language for meetings, debates, and discussions.",
"seo_title": "Disagreeing Politely in English – B2 Functional Language Lesson",
"body": lambda: card("💡","Today's Idea",
    "In English professional contexts, <strong>direct disagreement</strong> can damage relationships. Diplomatic disagreement acknowledges the other view first, then offers an alternative.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I managed teams of fifteen people in high-pressure restaurant environments. Disagreement was constant: about rotas, about service standards, about guest complaints. The managers who lost the most staff were those who disagreed loudly and publicly. The ones who retained good people were those who said: <em>I understand what you're saying, and I see it slightly differently.</em> That sentence takes three seconds to say. It changes the entire temperature of the room.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Diplomatic Disagreement Phrases",
    "<ul style='margin:0;padding-left:20px;line-height:2.2;'>" +
    "<li><em>I see your point, but I think…</em></li>" +
    "<li><em>That's an interesting view. I'd add that…</em></li>" +
    "<li><em>I'm not entirely sure I agree with that. In my experience…</em></li>" +
    "<li><em>I take your point, although I'd argue that…</em></li>" +
    "<li><em>That may be the case, but have we considered…?</em></li></ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Your colleague says: <em>\"We should shorten all lessons to 30 minutes — learners have short attention spans.\"</em><br><br>Disagree politely using <strong>two different phrases</strong> from the list above.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which phrase disagrees most diplomatically?</strong></p>" +
quiz_row(22,["You're wrong.","That's ridiculous.","I see your point, but I think we should reconsider.","No."],2)+"</div>"
},

{
"title": "Idioms from the World of Work",
"level": "B2", "audience": "Adults & Professionals", "emoji": "💼",
"tags": ["idioms","B2","vocabulary","workplace English","professional"],
"meta": "Learn essential workplace idioms in English. B2 lesson on figurative language used in offices, meetings, and professional conversations.",
"seo_title": "Workplace Idioms in English – B2 Vocabulary Lesson",
"body": lambda: card("💡","Today's Idea",
    "<strong>Idioms</strong> are phrases whose meaning is different from the literal words. Workplace idioms are common in meetings, emails, and casual conversation — understanding them prevents confusion.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "My first year in Australia, I worked in a café. The manager said: <em>Let's touch base later.</em> I looked for a base. I looked for something to touch. I understood nothing. <em>Touch base</em> means to make brief contact — to check in. English workplaces run on idioms. Understanding them is not decoration; it is access. After eighteen years in Australian hospitality, I collected them like stamps: <em>on the same page, push the envelope, bite the bullet, drop the ball.</em>",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","10 Essential Workplace Idioms",
    "<ul style='margin:0;padding-left:20px;line-height:2;'>" +
    "".join(f"<li><strong>{i}</strong> — {m}</li>" for i,m in [
        ("touch base","make brief contact / check in"),
        ("on the same page","agree; have the same understanding"),
        ("drop the ball","make an error; fail to deliver"),
        ("bite the bullet","do something difficult but necessary"),
        ("think outside the box","think creatively, beyond usual limits"),
        ("up to speed","fully informed and ready"),
        ("go the extra mile","do more than required"),
        ("hit the ground running","start something quickly and energetically"),
        ("read between the lines","understand the hidden meaning"),
        ("the ball is in your court","it's your decision / responsibility now"),
    ]) + "</ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Use <strong>3 idioms</strong> from the list in sentences about your own work or studies.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>\"Let's touch base on Monday.\" means:</strong></p>" +
quiz_row(23,["Let's meet and play sports.","Let's briefly check in with each other.","Let's argue.","Let's cancel."],1)+"</div>"
},

{
"title": "Abstract vs Concrete Language: Write Like You Mean It",
"level": "C1", "audience": "Advanced Learners & Writers", "emoji": "✍️",
"tags": ["writing","C1","Orwell","academic English","style","clarity"],
"meta": "Learn the difference between abstract and concrete language. C1 lesson on clear, powerful writing inspired by Orwell's plain English rules.",
"seo_title": "Abstract vs Concrete Language – C1 Writing Clarity Lesson",
"body": lambda: card("💡","Today's Idea",
    "<strong>Abstract language</strong> talks about ideas, feelings, values, concepts. <strong>Concrete language</strong> names specific things, actions, people, places. The most powerful writing uses concrete language to carry abstract ideas.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "George Orwell wrote: <em>Never use a long word where a short one will do. Never use an abstract word where a concrete one exists.</em> I learned this rule the hard way. My early writing was full of sentences like: <em>The experience of professional displacement has significant implications for personal identity formation.</em> Nothing wrong grammatically. But what does it say? Compare: <em>Losing a job you were good at makes you question who you are.</em> Same idea. Sixteen fewer words. One real human.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Orwell's Plain English Rule",
    "<div style='background:#f7fafc;border-radius:8px;padding:12px;margin-bottom:10px;'>" +
    "<strong>Vague abstract:</strong> <em>The situation presented various challenges in terms of interpersonal dynamics.</em><br><br>" +
    "<strong>Clear concrete:</strong> <em>We argued every day for a month. Nobody apologised.</em></div>" +
    "<p style='margin:4px 0;'><strong>The test:</strong> Can you replace a word with a more specific, visible thing? Do it. Every time.</p>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Rewrite this sentence using concrete language:<br><br><em>\"There was a challenging situation involving a difference of perspective between myself and a colleague regarding professional expectations.\"</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which sentence uses more concrete language?</strong></p>" +
quiz_row(24,["There were socioeconomic challenges.","We had no money and the rent was due Friday.","Existential pressures mounted.","Values were compromised."],1)+"</div>"
},

# ── BATCH 6: Cross-cultural / Life ──────────────────────────────────────────

{
"title": "English Around the World: One Language, Many Voices",
"level": "B1", "audience": "All Learners", "emoji": "🌐",
"tags": ["world Englishes","B1","vocabulary","culture","accents"],
"meta": "Discover how English varies around the world. B1 lesson on accents, vocabulary differences, and the global nature of English.",
"seo_title": "World Englishes – B1 Lesson on Global English Variation",
"body": lambda: card("💡","Today's Idea",
    "There is no single 'correct' English. English is a <strong>global language</strong> with hundreds of varieties — British, American, Australian, Indian, Caribbean, African, and more. Understanding variation makes you a better communicator.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I speak four languages: English (native, with a Bengali-Australian flavour), Bengali, French, and basic Hindi. When I arrived in Sydney from Bangladesh, people asked if I spoke English. I said yes. They were not sure they believed me. The Australian accent was so different from the British English I had learned that I felt like I was starting again. Later, in France, I realised French people had the opposite problem: they found American English incomprehensible but British English easy. The accent question is not about correctness. It is about exposure.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Same Word, Different Meaning",
    "<div style='background:#f7fafc;border-radius:8px;padding:12px;'>" +
    "<table style='width:100%;border-collapse:collapse;'><tr style='background:#ebf8ff;'><th style='padding:6px;'>British</th><th style='padding:6px;'>American</th><th style='padding:6px;'>Australian</th></tr>" +
    "".join(f"<tr style='border-bottom:1px solid #e2e8f0;text-align:center;'><td style='padding:6px;'>{b}</td><td style='padding:6px;'>{a}</td><td style='padding:6px;'>{au}</td></tr>" for b,a,au in [
        ("biscuit","cookie","bickie"),
        ("flat","apartment","flat"),
        ("rubbish","garbage/trash","rubbish/trash"),
        ("chemist","drugstore/pharmacy","chemist"),
        ("boot (car)","trunk","boot"),
    ]) + "</table></div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Which variety of English do you know best? Write <strong>3 words or phrases</strong> from your variety that might confuse someone from a different English-speaking country.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>In American English, what is an 'apartment' called in British English?</strong></p>" +
quiz_row(25,["House","Flat","Studio","Bungalow"],1)+"</div>"
},

{
"title": "Talking About Feelings in English",
"level": "B1", "audience": "All Learners", "emoji": "💙",
"tags": ["feelings","B1","vocabulary","speaking","emotional English"],
"meta": "Expand your vocabulary for emotions and feelings in English. B1 lesson on expressing how you feel — clearly and honestly.",
"seo_title": "Feelings and Emotions in English – B1 Vocabulary Lesson",
"body": lambda: card("💡","Today's Idea",
    "English has a rich vocabulary for emotions — but many learners only know <em>happy, sad, angry.</em> Expanding your emotional vocabulary helps you communicate honestly and precisely.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "When I was diagnosed with bipolar I and complex PTSD in La Réunion, I realised I had been describing my internal experience with three words for forty years. English — and therapy — gave me more: <em>overwhelmed, numb, agitated, melancholy, apprehensive, content, relieved, cautiously hopeful.</em> These are not therapy jargon. They are precise descriptions of real states. The difference between <em>sad</em> and <em>grief-stricken</em> is not trivial — it is the difference between being seen and being summarised.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Emotional Vocabulary: Beyond Basic",
    "<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>" +
    "".join(f"<div style='background:#f7fafc;border-radius:6px;padding:8px;'><strong>{w}</strong><br><span style='color:#718096;font-size:.9em;'>{d}</span></div>" for w,d in [
        ("overwhelmed","too much to handle"),
        ("relieved","glad a worry is gone"),
        ("apprehensive","anxious about what's coming"),
        ("content","peacefully satisfied"),
        ("melancholy","gentle sadness"),
        ("elated","extremely happy"),
        ("numb","unable to feel"),
        ("cautious","careful, not yet trusting"),
    ]) + "</div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "How are you feeling <em>right now</em>? Use at least <strong>two words</strong> from the list above to describe it.<br><br>Then: <em>I feel ___ because ___.</em>",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>If you feel 'relieved', you feel:</strong></p>" +
quiz_row(26,["Very happy","Glad that something worrying has ended","Angry","Tired"],1)+"</div>"
},

{
"title": "My Story in English: The Narrative Tense",
"level": "B1", "audience": "Teens & Adults", "emoji": "📝",
"tags": ["narrative writing","B1","past tenses","storytelling","writing"],
"meta": "Learn how to tell a story in English using narrative tenses. B1 lesson on Past Simple, Past Continuous, and Past Perfect with real storytelling examples.",
"seo_title": "Narrative Tenses in English – B1 Storytelling Lesson",
"body": lambda: card("💡","Today's Idea",
    "Stories in English use three past tenses together:<br><strong>Past Simple</strong> (the main events) · <strong>Past Continuous</strong> (background/interrupted actions) · <strong>Past Perfect</strong> (events before the story began).",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "Here is a paragraph using all three: <em>I was sitting on the kerb outside Sydney Airport (Past Continuous — background). I had arrived three hours earlier (Past Perfect — before the story). I had nothing except a phone number on a piece of paper. Then a taxi driver walked over and asked where I was going (Past Simple — the main event). That question changed everything.</em>",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","The Three Narrative Tenses",
    "<div style='background:#f7fafc;border-radius:8px;padding:12px;margin-bottom:10px;'>" +
    "<strong>Past Simple:</strong> <em>I arrived. I saw. I decided.</em> → Main events.<br><br>" +
    "<strong>Past Continuous:</strong> <em>It was raining. People were rushing.</em> → Background/interrupted.<br><br>" +
    "<strong>Past Perfect:</strong> <em>I had never left my country before.</em> → Before the story.</div>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Write 4–5 sentences about a significant moment in your life. Use all three narrative tenses. Start with the background (Past Continuous), then the main event (Past Simple), then something that happened before (Past Perfect).",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>\"When I arrived, she ___ for two hours.\" (wait)</strong></p>" +
quiz_row(27,["waited","has waited","had been waiting","was waiting"],2)+"</div>"
},

{
"title": "Vocabulary Strategies: How to Learn New Words That Stick",
"level": "B1", "audience": "All Learners", "emoji": "🧠",
"tags": ["vocabulary","B1","learning strategies","lexis","study skills"],
"meta": "Learn proven vocabulary learning strategies in English. B1 lesson on how to make new words stick — spaced repetition, context, and collocations.",
"seo_title": "Vocabulary Learning Strategies – B1 English Lesson",
"body": lambda: card("💡","Today's Idea",
    "The most effective vocabulary learning uses: <strong>context</strong> (words in sentences), <strong>spaced repetition</strong> (review at increasing intervals), and <strong>collocations</strong> (words that go together).",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I learned French to C1 as an adult — starting at around 35, in France, with a French wife. I made a mistake that most adult language learners make: I studied words in isolation. A list. <em>Maison, maison, maison.</em> Nothing. When I started reading real French — news, books, menus, government letters — and writing down words in context, the retention was completely different. I still remember <em>contester</em> (to contest, to challenge) because I read it in a legal document that mattered to me.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","4 Strategies That Work",
    "<ol style='margin:0;padding-left:20px;line-height:2;'>" +
    "<li><strong>Context first:</strong> Read the word in a sentence. Understand it from context before looking it up.</li>" +
    "<li><strong>Collocations:</strong> Don't learn <em>make</em> — learn <em>make a decision, make progress, make a mistake.</em></li>" +
    "<li><strong>Spaced repetition:</strong> Review today, then tomorrow, then in 3 days, then 7, then 30.</li>" +
    "<li><strong>Use it now:</strong> Write one sentence using the new word within 5 minutes. Use it in conversation today.</li></ol>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Pick a new English word you learned this week. Write:<br><br>1. A sentence using it in context.<br>2. Two collocations (words that go with it).<br>3. Set a reminder to review it in 3 days.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>Which is the best way to learn a new word?</strong></p>" +
quiz_row(28,["Write it 50 times","Learn it in a sentence with context","Translate it to your language only","Ignore it and hope you remember"],1)+"</div>"
},

{
"title": "Job Interview English: 5 Questions You Must Prepare",
"level": "B2", "audience": "Adults & Professionals", "emoji": "💼",
"tags": ["job interview","B2","speaking","professional English","career"],
"meta": "Learn how to answer the 5 most common job interview questions in English. B2 lesson for adults and professionals with real example answers.",
"seo_title": "Job Interview English – B2 Speaking Lesson | 5 Key Questions",
"body": lambda: card("💡","Today's Idea",
    "Job interviews in English have predictable questions. The key is to have structured, specific answers — not memorised scripts, but prepared frameworks.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "I have been on both sides of the interview table. As a manager in Sydney, I interviewed hundreds of candidates. The ones who got the job were not always the most qualified — they were the most specific. They gave <em>one example</em>, not a general claim. When I was interviewed for the sommelier role at Uccello, I described one specific wine, one specific guest, one specific outcome. That specificity is what interviewers in English-speaking cultures listen for.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","The 5 Questions & Frameworks",
    "<ol style='margin:0;padding-left:20px;line-height:2.2;'>" +
    "<li><strong>\"Tell me about yourself.\"</strong> → Past, Present, Future (2 minutes max)</li>" +
    "<li><strong>\"What are your strengths?\"</strong> → Name one. Give a specific example. State the result.</li>" +
    "<li><strong>\"Tell me about a challenge you faced.\"</strong> → Use <strong>STAR</strong>: Situation, Task, Action, Result.</li>" +
    "<li><strong>\"Why do you want this job?\"</strong> → Link what they need to what you offer.</li>" +
    "<li><strong>\"Do you have any questions?\"</strong> → Always say yes. Ask one smart question.</li></ol>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Prepare your answer to: <em>\"Tell me about a challenge you faced at work or in your studies.\"</em><br><br>Use STAR: Situation → Task → Action → Result. Say it aloud. Time yourself: 90 seconds maximum.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>What does STAR stand for in interview technique?</strong></p>" +
quiz_row(29,["Smart, Talented, Articulate, Ready","Situation, Task, Action, Result","Subject, Topic, Aim, Response","Strong, True, Accurate, Real"],1)+"</div>"
},

{
"title": "English for Parents: Talking to Your Child's School",
"level": "B1", "audience": "Parents & Carers", "emoji": "🏫",
"tags": ["parents","B1","school English","functional language","real world"],
"meta": "Learn practical English for communicating with your child's school. B1 lesson on writing notes, attending meetings, and understanding school vocabulary.",
"seo_title": "English for Parents – B1 Lesson on School Communication",
"body": lambda: card("💡","Today's Idea",
    "Parents who can communicate with their child's school in English give their child a significant advantage. You don't need perfect English — you need confident, clear communication.",
    "#fff8e1","#f6ad55","#c05621") +
card("📖","From My Experience",
    "My daughter is very young — barely eighteen months as I write this. But I think about the day she starts school here in La Réunion, where instruction is in French, and eventually perhaps in an English-speaking context too. As an immigrant parent — and I know many — the school system can feel impenetrable. The language of education has its own vocabulary. Understanding it makes you a partner in your child's learning, not a spectator.",
    "#f3e8ff","#9f7aea","#553c9a") +
card("📚","Key School Vocabulary & Phrases",
    "<ul style='margin:0;padding-left:20px;line-height:2;'>" +
    "".join(f"<li><strong>{t}</strong> — <em>{d}</em></li>" for t,d in [
        ("parent-teacher meeting","a meeting between parent and teacher to discuss progress"),
        ("progress report / report card","a written assessment of your child's learning"),
        ("homework","schoolwork to do at home"),
        ("curriculum","what is taught at each level"),
        ("attendance","whether your child comes to school"),
        ("\"She is making good progress\"","she is improving"),
        ("\"He finds [subject] challenging\"","it's difficult for him"),
    ]) + "</ul>",
    "#e8f4f8","#4299e1","#2b6cb0") +
card("✏️","Try It! (2 minutes)",
    "Write a short note (3–4 sentences) to your child's teacher explaining that your child will be absent tomorrow. Include: the reason, the date, and your contact details.",
    "#f0fff4","#48bb78","#2d6a4f") +
"<div style='background:#fff;border:2px solid #e2e8f0;border-radius:10px;padding:18px;margin-bottom:18px;'><h3 style='color:#2d3748;margin:0 0 12px;'>🎯 Quick Quiz</h3><p><strong>A teacher says \"Your child is making good progress.\" What does this mean?</strong></p>" +
quiz_row(30,["Your child has problems.","Your child is improving and learning well.","Your child is too advanced.","Your child needs extra help."],1)+"</div>"
},

]

# ─── POST TO WORDPRESS ───────────────────────────────────────────────────────

def post_lesson(lesson):
    body_html = lesson["body"]()
    content = wrap(header_html(lesson["title"], lesson["level"], lesson["audience"], lesson["emoji"]) + body_html)
    
    payload = {
        "title": f"English Bite — {lesson['title']}",
        "content": content,
        "status": "draft",
        "category": "English Teaching",
        "tags": ", ".join(lesson["tags"]),
        "meta_description": lesson["meta"],
        "seo_title": lesson["seo_title"],
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        WP_API,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Sourov-Key": WP_KEY,
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result.get("id", "?"), result.get("link", "")
    except Exception as e:
        return None, str(e)

success, failed = 0, 0
for i, lesson in enumerate(LESSONS):
    print(f"[{i+1}/{len(LESSONS)}] Posting: {lesson['title'][:60]}...")
    pid, link = post_lesson(lesson)
    if pid:
        print(f"  ✅ Draft ID: {pid} — {lesson['level']}")
        success += 1
    else:
        print(f"  ❌ Failed: {link}")
        failed += 1
    time.sleep(1.5)

print(f"\n{'='*50}")
print(f"Done: {success} created, {failed} failed")
