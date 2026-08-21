#!/usr/bin/env python3
"""Post 30 CELTA personal experience lessons to WordPress as drafts.

Usage: SOUROV_WP_KEY=<key> python3 lesson_poster.py
"""
import json, os, time, requests

WP_ENDPOINT = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
WP_KEY = os.environ["SOUROV_WP_KEY"]
HEADERS = {"X-Sourov-Key": WP_KEY, "Content-Type": "application/json"}

DISCLAIMER = (
    '<hr style="border:none;border-top:1px solid #ddd;margin:32px 0;">'
    '<p style="font-size:0.8em;color:#999;font-style:italic;">'
    'Independent project; not affiliated with, endorsed by, or accredited by '
    'Cambridge University Press &amp; Assessment. Confers no qualification. '
    'Cambridge CELTA course completed — 120 supervised teaching hours and four '
    'written assignments validated to the required standard.</p>'
)

LEVEL_COLORS = {
    "A1": "#43aa8b", "A2": "#4d908e", "B1": "#577590",
    "B2": "#f4a261", "C1": "#e76f51", "C2": "#264653",
    "A2-B1": "#4d908e", "B1-B2": "#6a7fad", "B2-C1": "#d4845a",
    "C1-C2": "#d4603a",
}

def html(level, anecdote, focus, explanation, examples, questions, takeaway):
    color = LEVEL_COLORS.get(level, "#577590")
    ex_rows = "".join(
        f'<tr><td style="padding:8px 12px;border-bottom:1px solid #e0e0e0;'
        f'font-style:italic;color:#264653;">{e}</td></tr>' for e in examples
    )
    q_items = "".join(
        f'<details style="background:#eef2f7;padding:12px 16px;border-radius:8px;'
        f'margin:8px 0;cursor:pointer;">'
        f'<summary style="font-weight:bold;color:#264653;list-style:none;">'
        f'&#9654; {q}</summary>'
        f'<div style="margin-top:10px;padding:10px 14px;background:#d4edda;'
        f'border-radius:6px;color:#155724;">'
        f'<strong>&#10003; Answer:</strong> {a}<br>'
        f'<em style="font-size:0.9em;">{e}</em></div></details>'
        for q, a, e in questions
    )
    return f"""<div style="font-family:Georgia,serif;max-width:760px;margin:0 auto;padding:16px;line-height:1.7;">

<p style="display:inline-block;background:{color};color:#fff;padding:5px 16px;border-radius:20px;font-size:0.82em;font-weight:bold;letter-spacing:1px;margin-bottom:8px;">CEFR {level} &nbsp;&middot;&nbsp; 5 min</p>

<div style="background:#fff7e6;border-left:4px solid #f4a261;padding:16px 20px;margin:20px 0;border-radius:0 8px 8px 0;">
<strong style="color:#d4501c;">From my experience:</strong>
<p style="margin:8px 0 0;">{anecdote}</p>
</div>

<h2 style="color:#264653;border-bottom:2px solid #2a9d8f;padding-bottom:8px;">Today&#39;s focus: {focus}</h2>

<div style="background:#f0f9f8;padding:16px 20px;border-radius:8px;border:1px solid #81b29a;margin:16px 0;">
{explanation}
</div>

<h3 style="color:#e76f51;margin-top:24px;">Examples in context</h3>
<table style="width:100%;border-collapse:collapse;background:#fafafa;border-radius:8px;overflow:hidden;border:1px solid #e0e0e0;">
{ex_rows}
</table>

<h3 style="color:#264653;margin-top:24px;">Try it &#8212; click to reveal the answer</h3>
{q_items}

<div style="background:#264653;color:#edf2f4;padding:18px 22px;border-radius:8px;margin:28px 0;">
<strong style="font-size:1.05em;">&#9889; 5-second rule:</strong>
<p style="margin:8px 0 0;">{takeaway}</p>
</div>

{DISCLAIMER}
</div>"""


LESSONS = [
  {
    "title": "Hello, I'm Sourov — Greetings & Introductions in Real English",
    "level": "A1",
    "category": "English Teaching",
    "tags": "English greetings, A1 English, beginner English, introductions, real English",
    "seo_title": "English Greetings: Formal vs Informal — Real Examples | A1",
    "meta_description": "Learn greetings and introductions at A1 level, from informal Australian English to formal British English, with real context.",
    "anecdote": "When I landed in Sydney Airport in 2005 with one carry-on bag and what I thought was decent English, the first stranger I spoke to said <em>'How ya going?'</em> I had no idea what that meant. It was not in any textbook. This lesson is about greetings that actually get used.",
    "focus": "Greetings (formal + informal) and introductions",
    "explanation": "<p><strong>Three levels:</strong></p><ul><li><strong>Very informal</strong> (friends, Australia): <em>G\'day! How ya going? Hey!</em></li><li><strong>Neutral</strong> (most everyday situations): <em>Hi, how are you? Nice to meet you.</em></li><li><strong>Formal</strong> (interviews, official): <em>Good morning. How do you do?</em></li></ul><p>Use <strong>I\'m [name]</strong> in almost all real situations. \'My name is...\' is textbook-stiff outside job interviews.</p>",
    "examples": [
      "Hi, I'm Sourov. Nice to meet you. (neutral — use this 90% of the time)",
      "Good morning, I'm Sourov Deb. I have an appointment at ten. (formal)",
      "Hey — Sourov! How ya going? (very informal, Australian English)",
    ],
    "questions": [
      ("Which greeting fits a job interview? (a) 'Hey!' &nbsp; (b) 'Good morning, pleased to meet you.' &nbsp; (c) 'How ya going?'",
       "(b) Good morning, pleased to meet you.",
       "Interviews call for formal register. Save 'hey' and 'how ya going' for people you already know."),
      ("Fill the blank: '_____ Sarah. _____ to meet you.' (use I'm / Nice)",
       "I'm Sarah. Nice to meet you.",
       "'I'm' is a contraction of 'I am' — completely correct and natural in speech."),
      ("True or false: 'How do you do?' expects the answer 'Fine, thanks.'",
       "False. The traditional response to 'How do you do?' is 'How do you do?' — it is a formal greeting, not a real question.",
       "Modern usage is fading — you are more likely to hear 'How are you?' in real situations today."),
    ],
    "takeaway": "When in doubt, use <strong>Hi, I'm [name], nice to meet you</strong> — it works in 95% of real situations across all English-speaking countries.",
  },
  {
    "title": "Numbers 1–100: What the Star Casino Taught Me About English Numbers",
    "level": "A1",
    "category": "English Teaching",
    "tags": "English numbers, A1 English, beginner, prices, quantities, numbers 1-100",
    "seo_title": "English Numbers 1-100 | Prices and Quantities for Beginners | A1",
    "meta_description": "Master English numbers 1-100 and prices with real restaurant and casino examples. A1 level, 5 minutes.",
    "anecdote": "At the Star Casino in Sydney, every night was a number problem. Table 17 wants two martinis. Bill for $248. Thirty-five guests on the reservation. I learned English numbers fast because I had to — and so will you.",
    "focus": "Numbers 1–100, prices, and quantities",
    "explanation": "<p><strong>Two tricky zones:</strong></p><ul><li><strong>13 vs 30:</strong> thir<u>TEEN</u> vs <u>THIR</u>ty. The stress changes completely. Say 13 with stress on the second syllable, 30 on the first.</li><li><strong>Prices:</strong> $24.50 = <em>twenty-four dollars fifty</em> (not twenty-four point fifty). The decimal point becomes the word <em>and</em> in spoken British English.</li></ul><p><strong>Teens 13–19:</strong> thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen. <strong>Tens 20–90:</strong> twenty, thirty, forty, fifty, sixty, seventy, eighty, ninety.</p>",
    "examples": [
      "Table twelve needs two glasses of wine, please. (12 + 2)",
      "That comes to forty-nine dollars and fifty cents. ($49.50)",
      "We have thirty-five on the reservation tonight. (35)",
    ],
    "questions": [
      ("Write in words: 47",
       "Forty-seven",
       "Tens first, then units, joined with a hyphen for 21-99."),
      ("Which is correct for $16.30? (a) sixteen point thirty &nbsp; (b) sixteen dollars thirty &nbsp; (c) one six three zero",
       "(b) Sixteen dollars thirty",
       "In everyday spoken English, omit 'cents' when the context is clear."),
      ("Which number has stress on the FIRST syllable: 14 or 40?",
       "40 (FORty). 14 = fourTEEN — stress on the second syllable.",
       "This distinction prevents real misunderstandings in busy environments like restaurants and shops."),
    ],
    "takeaway": "For teens (13-19), stress the <strong>second</strong> syllable. For tens (30, 40...), stress the <strong>first</strong>. Stress is how listeners tell the difference.",
  },
  {
    "title": "Food & Drink Vocabulary: A Sommelier's English Lesson",
    "level": "A2",
    "category": "English Teaching",
    "tags": "food vocabulary, drink vocabulary, A2 English, English adjectives, sommelier English, collocations",
    "seo_title": "Food and Drink Vocabulary in English | A2 Level | Real Collocations",
    "meta_description": "Learn food and drink vocabulary with a sommelier's perspective. Real collocations, real usage, A2 level.",
    "anecdote": "I became a sommelier at The Ivy in Sydney. My job was to describe wine to people who could not see the bottle — only taste it. That forced me to learn that food and drink words are the most sensory vocabulary in English. One wrong adjective and the guest orders the wrong bottle.",
    "focus": "Food and drink vocabulary + key adjective collocations",
    "explanation": "<p>Food adjectives travel in pairs with specific nouns — these are called <strong>collocations</strong>. They are patterns, not rules.</p><table style='width:100%;border-collapse:collapse;'><tr style='background:#2a9d8f;color:#fff;'><th style='padding:8px;text-align:left;'>Food/Drink</th><th style='padding:8px;text-align:left;'>Common adjectives</th></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>Wine</td><td style='padding:8px;border-bottom:1px solid #ddd;'>dry, crisp, full-bodied, velvety, oaky, tannic</td></tr><tr><td style='padding:8px;border-bottom:1px solid #ddd;'>Coffee</td><td style='padding:8px;border-bottom:1px solid #ddd;'>strong, bitter, smooth, rich, aromatic</td></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>Bread</td><td style='padding:8px;border-bottom:1px solid #ddd;'>crusty, soft, dense, airy, fresh</td></tr><tr><td style='padding:8px;'>Sauce</td><td style='padding:8px;'>rich, tangy, silky, spicy, creamy</td></tr></table>",
    "examples": [
      "This is a crisp, dry white wine with a citrus finish. (wine tasting note)",
      "The bread is crusty on the outside and soft inside. (describing texture)",
      "We have a rich, earthy mushroom sauce with the steak tonight. (menu description)",
    ],
    "questions": [
      ("Which adjective goes with WINE? (a) crusty &nbsp; (b) dry &nbsp; (c) silky",
       "(b) dry — and also (c) silky can work for certain wines, but 'dry' is the most standard wine adjective.",
       "'Crusty' belongs to bread. Context tells you which adjective fits which food."),
      ("Complete: 'The espresso was _____ and _____.' (choose 2 from: crisp / strong / silky / crusty)",
       "Strong and silky (or strong and smooth/rich)",
       "Espresso is never described as 'crisp' — that word belongs to wine and pastry."),
      ("What does 'full-bodied' mean when describing wine?",
       "Rich, heavy texture — the wine fills your mouth. Think of full cream milk versus skimmed milk.",
       "Body = texture weight in the mouth. Light-bodied wines feel thin; full-bodied feel heavy and rich."),
    ],
    "takeaway": "Learn food adjectives in context pairs: <strong>dry wine, crusty bread, strong coffee, rich sauce</strong>. Never memorise adjectives alone — always with their partner noun.",
  },
  {
    "title": "Jobs and Workplaces: Talking About What You Do in English",
    "level": "A2",
    "category": "English Teaching",
    "tags": "jobs vocabulary, A2 English, workplaces, career English, what do you do",
    "seo_title": "Jobs and Workplaces Vocabulary in English | A2 Level",
    "meta_description": "Learn to talk about jobs and workplaces in English. A2 level with examples from real hospitality experience.",
    "anecdote": "In twelve years in Sydney I had many titles: waiter, barista, bartender, sommelier, floor manager, restaurant manager. Each title came with its own English vocabulary. In Australia, 'What do you do?' is often the third question a stranger asks — right after your name and where you're from.",
    "focus": "Job titles, workplace nouns, and 'What do you do?'",
    "explanation": "<p><strong>Two natural ways to answer:</strong></p><ul><li><strong>I'm a [job]</strong> — casual and common. 'I'm a barista.'</li><li><strong>I work as a [job]</strong> — slightly more formal. 'I work as a floor manager.'</li></ul><p><strong>Key workplace vocabulary:</strong> restaurant / hotel / bar / kitchen / <em>the floor</em> (= the dining area, not the ground) / cellar / front of house / back of house</p><p>Note: <em>The floor</em> means the dining or customer-facing area in hospitality — not the surface you walk on.</p>",
    "examples": [
      "I'm a restaurant manager. I run the floor every evening. (casual + workplace noun)",
      "She works as a barista at a café in the city centre. (formal structure)",
      "He's been a sommelier for ten years — he knows the cellar better than anyone.",
    ],
    "questions": [
      ("What does 'the floor' mean in a restaurant? (a) the ground &nbsp; (b) the dining area &nbsp; (c) the kitchen",
       "(b) The dining area — where guests sit and staff serve.",
       "'Working the floor' means serving guests in the dining room. 'Back of house' is the kitchen."),
      ("Which is more formal? (a) 'I'm a chef.' &nbsp; (b) 'I work as a chef.'",
       "(b) 'I work as a chef' is slightly more formal, preferred in written CVs or formal introductions.",
       "Both are grammatically correct. Choose based on context."),
      ("Fill the blank: 'She ___ the kitchen for twelve years before opening her own restaurant.'",
       "ran / managed / worked in",
       "'Ran' is the past of 'run' — in hospitality, to 'run' a kitchen means to be in charge of it."),
    ],
    "takeaway": "Use <strong>'I'm a...'</strong> in conversation and <strong>'I work as a...'</strong> in writing. Learn the specialist vocabulary of your workplace — it shows you belong.",
  },
  {
    "title": "Telling the Time in English: From Shift Start to Last Call",
    "level": "A2",
    "category": "English Teaching",
    "tags": "telling the time, A2 English, time expressions, clock English, AM PM",
    "seo_title": "Telling the Time in English | A2 Level | Half Past, Quarter To",
    "meta_description": "Learn to tell the time in English with British and American styles. A2 level, 5-minute lesson.",
    "anecdote": "At Merivale in Sydney — the group that runs The Ivy, Uccello, and Establishment — a shift started at 5:30 PM and ended at 2 AM. Time was everything. A five-minute delay could mean a cold plate arriving at the wrong table. Knowing how to say and read time in English was not optional.",
    "focus": "Telling the time: o'clock, half past, quarter to/past, 24-hour",
    "explanation": "<p><strong>British-style (most common in formal contexts):</strong></p><ul><li>6:00 = six o'clock</li><li>6:15 = quarter past six</li><li>6:30 = half past six</li><li>6:45 = quarter to seven</li></ul><p><strong>American/informal style:</strong></p><ul><li>6:30 = six thirty &nbsp;|&nbsp; 6:45 = six forty-five</li></ul><p><strong>24-hour (schedules, professional):</strong> 18:30 = eighteen thirty. Never say 'eighteen thirty o'clock.'</p>",
    "examples": [
      "Service starts at half past five. (5:30 PM — British style)",
      "Last call is at one forty-five in the morning. (1:45 AM — American/informal)",
      "The reservation is at 19:30. Please arrive by 19:15. (24-hour — hospitality standard)",
    ],
    "questions": [
      ("How do you say 7:45 in British style?",
       "Quarter to eight",
       "7:45 is 15 minutes BEFORE 8:00, so it's 'quarter TO eight' — not quarter past seven."),
      ("Is 'fourteen thirty o'clock' correct?",
       "No. In 24-hour time, just say 'fourteen thirty.' Never add 'o'clock' to 24-hour times.",
       "14:30 = fourteen thirty. 'O'clock' is only for 12-hour times on the exact hour: six o'clock."),
      ("A guest says 'Let's meet at half seven.' What time is this?",
       "7:30 — 'Half seven' is a very common British informal expression for 7:30.",
       "In German, 'halb sieben' means 6:30 (half TO seven). In English, 'half seven' means half PAST seven = 7:30. Important difference!"),
    ],
    "takeaway": "Learn both styles: <strong>half past / quarter to</strong> (British formal) and <strong>six thirty / six forty-five</strong> (American/informal). Both are correct — context decides which to use.",
  },
  {
    "title": "Directions in English: How I Got Lost in Paris and Found My Way Back",
    "level": "A2-B1",
    "category": "English Teaching",
    "tags": "directions in English, A2 English, prepositions of place, giving directions, navigation",
    "seo_title": "Directions in English | A2-B1 Level | Prepositions of Place",
    "meta_description": "Learn to give and follow directions in English. A2-B1 level with real examples from Paris and Sydney.",
    "anecdote": "My first week in Paris in 2017, I got lost in the Métro every single day. Not because I couldn't read French — I could. But I was building the mental map in English, and the English directions I had practised were wrong. I said 'go to the right' when I meant 'turn right.' I said 'it is in front of' when I meant 'it is opposite.' Words matter.",
    "focus": "Giving and following directions in English",
    "explanation": "<p><strong>Key direction phrases:</strong></p><ul><li>Go straight on / straight ahead</li><li>Turn left / right at the [traffic lights / roundabout / corner]</li><li>Take the first/second turning on the left/right</li><li>It's on your left/right</li><li>It's opposite the [place]</li><li>It's between the [place] and the [place]</li><li>It's at the end of the road / street</li></ul><p><strong>Common error:</strong> 'Go to the right' ✗ → 'Turn right' ✓</p>",
    "examples": [
      "Go straight on, then turn left at the roundabout. The station is on your right.",
      "It's opposite the supermarket — you can't miss it.",
      "Take the second turning on the right. It's between the pharmacy and the park.",
    ],
    "questions": [
      ("Which is correct? (a) 'Go to right' &nbsp; (b) 'Turn right' &nbsp; (c) 'Go at the right'",
       "(b) Turn right — this is the standard phrase.",
       "'Go to right' and 'go at the right' are direct translations from other languages and are not natural English."),
      ("Fill the blank: 'The café is _____ the bank and the post office.'",
       "between",
       "'Between' is used for a position with something on each side. 'Opposite' means directly facing something."),
      ("'It's at the end of the road' — does this mean left, right, or straight ahead?",
       "Straight ahead — 'at the end of the road' means you keep going until you can't go further.",
       "If they say 'at the far end,' it's even more emphatic that you need to walk the full length."),
    ],
    "takeaway": "The most useful direction phrase: <strong>'Take the [first/second] turning on the [left/right].'</strong> It's clear, specific, and what native speakers actually say.",
  },
  {
    "title": "Present Perfect: The Tense That Connects Your Past to Right Now",
    "level": "B1",
    "category": "English Teaching",
    "tags": "present perfect, B1 English, English grammar, tenses, for vs since, ever never",
    "seo_title": "Present Perfect in English | B1 Level | For vs Since Explained",
    "meta_description": "Learn the present perfect tense with real examples from real life. B1 level, 5 minutes, interactive.",
    "anecdote": "The first night I arrived in Réunion and looked up at the sky, I said out loud — genuinely surprised, standing in the dark — <em>'I have never seen so many stars.'</em> That sentence is the present perfect in its purest form: your whole life, up to this exact moment. Not yesterday. Not last year. Your entire existence, arriving at now.",
    "focus": "Present perfect: have/has + past participle; for vs since; ever/never; just/already/yet",
    "explanation": "<p>Use the present perfect when the <strong>past connects to NOW</strong>:</p><ul><li><strong>Experience up to now:</strong> 'I have never tried sushi.' (ever in my life)</li><li><strong>Duration up to now:</strong> 'I have lived here for three years.' (still living)</li><li><strong>Recent past with present result:</strong> 'She has just arrived.' (she's here now)</li></ul><p><strong>For vs Since:</strong> <em>for</em> + duration (for two years) · <em>since</em> + starting point (since 2019)</p><p><strong>Compare:</strong> 'I lived in Sydney' (finished — past simple) vs 'I have lived in Réunion for six months' (ongoing — present perfect).</p>",
    "examples": [
      "I have worked in hospitality for eighteen years. (still working — use 'for' + duration)",
      "Have you ever tried Réunion vanilla? It's extraordinary. (life experience up to now)",
      "She has just arrived at the airport — she'll be here in twenty minutes. (very recent past)",
    ],
    "questions": [
      ("Which is correct? 'I have lived here _____ 2019.' (for / since)",
       "since 2019 — 'since' introduces a specific point in time (a year, a date, an event).",
       "'For' introduces a duration: 'for five years.' 'Since' introduces the starting point: 'since 2019.'"),
      ("Choose: 'I ___ to Japan twice.' (went / have been)",
       "have been — this is a life experience (up to now), not a past event with a specific time.",
       "If you added a time reference ('I went to Japan in 2018'), you'd use past simple."),
      ("'She has already eaten.' What does this tell us?",
       "She ate before now, and the fact matters in the present moment — perhaps she doesn't want more food.",
       "'Already' in the present perfect emphasises that something happened sooner than expected."),
    ],
    "takeaway": "Ask yourself: <strong>does the past connect to now?</strong> Yes → present perfect. No, it's finished → past simple. 'I lived in Sydney' (finished). 'I have lived in Réunion' (ongoing).",
  },
  {
    "title": "Past Simple for Stories: How I Tell My Sydney Years in English",
    "level": "B1",
    "category": "English Teaching",
    "tags": "past simple, B1 English, English grammar, irregular verbs, storytelling, past tense",
    "seo_title": "Past Simple in English | B1 Level | Regular and Irregular Verbs",
    "meta_description": "Master the past simple tense with irregular verbs, real stories, and interactive practice. B1 level.",
    "anecdote": "2005 to 2017. Twelve years of Sydney. Every sentence about that chapter of my life starts with 'I worked at...' or 'We lived in...' or 'She told me...' The past simple is the tense of completed time — the shelf where you store the chapters that are finished.",
    "focus": "Past simple: regular/irregular verbs, negative, question form, time markers",
    "explanation": "<p><strong>Past simple = a finished time slot.</strong></p><ul><li><strong>Regular:</strong> add -ed → work<strong>ed</strong>, live<strong>d</strong>, start<strong>ed</strong></li><li><strong>Irregular:</strong> go → <strong>went</strong>, see → <strong>saw</strong>, tell → <strong>told</strong>, leave → <strong>left</strong>, make → <strong>made</strong></li><li><strong>Negative:</strong> didn't + base verb → 'I didn't know anyone.'</li><li><strong>Question:</strong> Did + subject + base verb → 'Did you enjoy it?'</li></ul><p><strong>Time markers:</strong> ago, last year, in 2005, when, yesterday, at [time]</p>",
    "examples": [
      "I arrived in Sydney on a Tuesday in March 2005. (irregular: arrive → arrived ✓)",
      "The first restaurant I worked in didn't pay much, but it taught me everything. (negative + irregular)",
      "Did you ever go back to Bangladesh? — Yes, I did, once, in 2012. (question + short answer)",
    ],
    "questions": [
      ("What is the past simple of 'leave'?",
       "left — irregular verb.",
       "Other common irregulars: buy → bought, bring → brought, think → thought, catch → caught."),
      ("Make this negative: 'He understood the menu.'",
       "He didn't understand the menu. (Use 'didn't' + base verb 'understand' — not 'didn't understood')",
       "Mistake to avoid: 'He didn't understood' ✗. The past is carried by 'didn't' — the main verb returns to base form."),
      ("Which time marker fits past simple? (a) for three years &nbsp; (b) since 2019 &nbsp; (c) in 2005",
       "(c) in 2005 — a specific finished point in time.",
       "'For three years' and 'since 2019' are present perfect markers (duration/starting point up to now)."),
    ],
    "takeaway": "Past simple = <strong>finished time</strong>. Spot the irregular verbs (go/went, see/saw) and never use 'didn't' with a past-tense verb: <strong>didn't understand</strong>, not <em>didn't understood</em>.",
  },
  {
    "title": "'I Used to Work Nights': Past Habits That No Longer Exist",
    "level": "B1",
    "category": "English Teaching",
    "tags": "used to, would, B1 English, past habits, English grammar, past states",
    "seo_title": "Used to vs Would for Past Habits | B1 English Grammar",
    "meta_description": "Learn how to talk about past habits in English using 'used to' and 'would'. B1 level, 5 minutes.",
    "anecdote": "I used to start every shift with a double espresso I pulled myself. I would stand at the empty bar at 5 PM, before any guests arrived, and just breathe. I do not do that anymore — different country, different life. That gap between then and now is exactly what 'used to' is for.",
    "focus": "Used to + infinitive (past habits/states); would + infinitive (past habits only)",
    "explanation": "<p><strong>Used to</strong> describes habits AND states in the past that have now changed:</p><ul><li>'I used to smoke.' (habit, now stopped)</li><li>'He used to be very shy.' (state, now changed)</li></ul><p><strong>Would</strong> describes repeated past actions only — NOT states:</p><ul><li>'She would check the reservations twice every night.' ✓</li><li>'I would live there.' ✗ (state — cannot use 'would' here)</li></ul><p><strong>Simple rule:</strong> If you can replace it with 'used to', 'would' probably works. But 'used to' can go where 'would' cannot.</p>",
    "examples": [
      "I used to work sixty-hour weeks in Sydney. Now I work half that. (past habit → changed)",
      "She would always check the reservations list twice before service. (repeated past action)",
      "He used to be a barista before he became head sommelier. (past state — 'would be' ✗)",
    ],
    "questions": [
      ("Which is correct? 'I ___ live in Paris, but now I'm in Réunion.' (used to / would)",
       "used to — 'live' is a state, not an action. 'Would' cannot be used for states.",
       "States: live, be, know, believe, have, love. These only work with 'used to', not 'would'."),
      ("Both correct or one wrong? 'I used to drink coffee every morning.' / 'I would drink coffee every morning.'",
       "Both are correct! 'Drink' is a repeated action, so both 'used to' and 'would' work here.",
       "For actions, both forms work. Only 'used to' works for states."),
      ("What is the question form of 'used to'?",
       "'Did you use to...?' (not 'did you used to') — 'use' without the 'd'.",
       "Question: 'Did you use to live in Australia?' Negative: 'I didn't use to drink tea.'"),
    ],
    "takeaway": "For <strong>states</strong> (live, be, have, know): only <strong>used to</strong>. For <strong>repeated actions</strong>: both <strong>used to</strong> and <strong>would</strong> work. When unsure, use 'used to' — it's always safe.",
  },
  {
    "title": "Future Plans: 'Going To' vs 'Will' — and Why the Difference Matters",
    "level": "B1",
    "category": "English Teaching",
    "tags": "future English, going to, will, B1 grammar, future plans, predictions",
    "seo_title": "Going To vs Will in English | B1 Level Future Grammar",
    "meta_description": "Learn when to use going to or will for future plans, predictions and decisions. B1 level.",
    "anecdote": "When Vanessa and I decided to move from Paris to Réunion, we had two kinds of sentences. <em>'We're going to find a flat before we arrive'</em> — a plan we had already made. <em>'It will be fine'</em> — a prediction we invented on the spot to calm ourselves down. One was grounded. One was hope. English has a different verb form for each.",
    "focus": "Going to (plans/intentions) vs will (predictions/spontaneous decisions)",
    "explanation": "<p><strong>Going to:</strong> use when you have already decided, or when the evidence is clear:</p><ul><li>'We're going to move to Réunion in September.' (decided plan)</li><li>'Look at those clouds — it's going to rain.' (evidence visible)</li></ul><p><strong>Will:</strong> use for immediate/spontaneous decisions, promises, and opinions about the future:</p><ul><li>'I'll carry that for you.' (spontaneous offer — decided just now)</li><li>'She'll probably be late.' (opinion/prediction, no visible evidence)</li></ul><p><strong>Present continuous:</strong> fixed, diary arrangements with another person: 'I'm meeting the landlord at 3.' </p>",
    "examples": [
      "We're going to start fresh in Réunion — we've already signed the lease. (decided plan)",
      "I'll answer that question — give me a moment. (spontaneous, decided now)",
      "She's meeting the letting agent tomorrow at ten. (diary arrangement — fixed)",
    ],
    "questions": [
      ("Which form? Your friend drops a bag. You say: '_____ pick that up for you!' (I'll / I'm going to)",
       "I'll — this is a spontaneous offer, decided in the moment.",
       "'I'm going to pick that up' sounds like you had already planned to pick it up before you saw it fall."),
      ("'Look at the sky — it ___ rain.' (will / is going to)",
       "is going to rain — you can see the evidence (dark clouds). 'Going to' is used when the cause is visible.",
       "'It will rain' would be a general prediction or guess, not based on visible evidence right now."),
      ("True or false: 'Will' and 'going to' are always interchangeable.",
       "False. They have overlapping uses but carry different meanings about whether a decision was made before or just now.",
       "In casual conversation, many speakers use them interchangeably. In IELTS and formal writing, the distinction matters."),
    ],
    "takeaway": "<strong>Going to</strong> = already decided. <strong>Will</strong> = decided right now or opinion. When you are making an offer or promise on the spot, always use <strong>will</strong>.",
  },
  {
    "title": "Comparatives and Superlatives: Sydney vs Réunion",
    "level": "B1",
    "category": "English Teaching",
    "tags": "comparatives, superlatives, B1 English, adjectives, comparison, as as",
    "seo_title": "Comparatives and Superlatives in English | B1 Level",
    "meta_description": "Learn comparatives and superlatives with real examples comparing Sydney and Réunion. B1 level.",
    "anecdote": "People always ask me: 'Which do you prefer — Sydney or Réunion?' My honest answer is that they are not comparable in the way the question assumes. Sydney is bigger, louder, faster. Réunion is greener, quieter, and the sky is more extraordinary. Comparison is not about better — it is about different. English gives you the grammar to say exactly that.",
    "focus": "Comparatives (-er/more) and superlatives (-est/most); as...as; intensifiers",
    "explanation": "<p><strong>Short adjectives</strong> (1 syllable): add -er/-est: big → bigg<strong>er</strong> → the bigg<strong>est</strong></p><p><strong>Long adjectives</strong> (3+ syllables): more/most: beautiful → <strong>more</strong> beautiful → <strong>the most</strong> beautiful</p><p><strong>Exceptions:</strong> good → better → the best &nbsp;|&nbsp; bad → worse → the worst &nbsp;|&nbsp; far → further → the furthest</p><p><strong>Equality:</strong> as + adjective + as: 'Réunion is as beautiful as any island I've seen.'</p><p><strong>Intensifiers:</strong> <em>much, far, slightly, a little</em> before comparatives: 'far busier' · 'slightly warmer'</p>",
    "examples": [
      "Réunion is much smaller than Australia, but its coastline is more dramatic.",
      "The food in Réunion is far more varied than I expected when I arrived.",
      "Sydney was the most multicultural city I had ever lived in — nothing quite like it.",
    ],
    "questions": [
      ("Comparative of 'expensive': (a) expensiver &nbsp; (b) more expensive &nbsp; (c) most expensive",
       "(b) more expensive — 3 syllables, so use 'more/most', not -er/-est.",
       "Rule of thumb: if you struggle to say it with -er (expensiver sounds wrong), use 'more'."),
      ("Fill: 'Réunion is ___ busy ___ Paris.' (use as...as)",
       "as busy as — 'Réunion is not as busy as Paris.' (or: 'just as busy as' for equality)",
       "For negative comparison: 'not as [adj] as.' For equality: 'just as [adj] as.'"),
      ("Which intensifier fits? 'Réunion is ___ warmer than France in December.' (much / a bit)",
       "Both work: 'much warmer' (big difference) or 'a bit warmer'/'slightly warmer' (small difference). Context decides.",
       "'Much' and 'far' signal large differences. 'A bit', 'slightly', 'a little' signal small ones."),
    ],
    "takeaway": "Short adjective → <strong>-er than</strong>. Long adjective → <strong>more... than</strong>. Exceptions to memorise: <strong>better, worse, further</strong>. Intensify with <strong>much/far</strong> (big gap) or <strong>slightly/a bit</strong> (small gap).",
  },
  {
    "title": "Second Conditional: The Life I Almost Lived",
    "level": "B1-B2",
    "category": "English Teaching",
    "tags": "second conditional, B1 English, B2 English, conditionals, if clauses, hypothetical",
    "seo_title": "Second Conditional in English | B1-B2 Level Grammar",
    "meta_description": "Master the second conditional with real examples. B1-B2 level, interactive, 5 minutes.",
    "anecdote": "Every immigrant has a sentence that begins <em>'If I hadn't left...'</em> Mine is: if I had stayed in Bangladesh, I would never have learned to pour a perfect espresso. But that sentence is about the third conditional. The second conditional is simpler — and just as powerful. It is the grammar of the life you are not living right now.",
    "focus": "Second conditional: if + past simple → would + infinitive (imaginary present)",
    "explanation": "<p><strong>Second conditional = imaginary or unlikely situations NOW:</strong></p><p style='background:#264653;color:#edf2f4;padding:10px 16px;border-radius:6px;font-family:monospace;'>If + [past simple], ... would + [base verb]</p><ul><li>'If I lived in London, I would cycle everywhere.' (I don't live there — imaginary)</li><li>'If she spoke French, she would find the job easier.' (she doesn't — imaginary)</li></ul><p><strong>Compare with 1st conditional (real possibility):</strong></p><ul><li>1st: 'If I study, I will pass.' (real, likely)</li><li>2nd: 'If I studied harder, I would pass.' (imaginary — implying I probably don't study enough)</li></ul>",
    "examples": [
      "If I could choose any language to learn, I would choose Mandarin. (imaginary choice)",
      "She would travel more if she had more annual leave. (unlikely — she doesn't have enough)",
      "What would you do if you won the IELTS Band 9? (impossible/very unlikely hypothetical)",
    ],
    "questions": [
      ("Complete: 'If I ___ (have) more time, I ___ (travel) more.'",
       "If I had more time, I would travel more.",
       "Past simple in the if-clause; would + base verb in the result clause. NOT 'If I would have...'"),
      ("Is this 1st or 2nd conditional? 'If it rains tomorrow, I'll stay inside.'",
       "1st conditional — 'rains' is present simple + 'will'. This is a real possibility.",
       "Rain tomorrow is genuinely possible. 2nd would be: 'If it rained every day, I would move.' (imaginary)"),
      ("Find the error: 'If I would have a car, I would drive to work.'",
       "Error: 'If I would have' ✗ → 'If I had a car, I would drive to work.' ✓",
       "Never use 'would' in the if-clause of a second conditional. Use past simple only."),
    ],
    "takeaway": "<strong>If + past simple, would + base verb.</strong> Never put 'would' in the if-clause. The key question: is this situation real or imaginary? Imaginary → second conditional.",
  },
  {
    "title": "Polite English at Work: Requests, Offers and Suggestions That Land",
    "level": "B1-B2",
    "category": "English Teaching",
    "tags": "polite English, requests, B1 English, B2 English, professional English, modal verbs, offers",
    "seo_title": "Polite Requests in English | B1-B2 Level | Work and Professional Settings",
    "meta_description": "Learn polite requests, offers and suggestions in English for professional contexts. B1-B2 level.",
    "anecdote": "I served thousands of guests at The Ivy and Establishment in Sydney. The guests who said <em>'Do you want to bring the bill?'</em> got one kind of response. The guests who said <em>'Would you mind bringing the bill when you have a moment?'</em> got a different energy in return. Same meaning. Completely different social effect. Politeness in English is a precision tool.",
    "focus": "Polite requests, offers and suggestions using modal verbs",
    "explanation": "<p><strong>Politeness ladder</strong> (from most to least direct):</p><ol><li>'Give me...' — very direct (can sound rude)</li><li>'Can you...?' — neutral/informal</li><li>'Could you...?' — more polite</li><li>'Would you mind...?' — quite polite</li><li>'I was wondering if you could...' — very polite/formal</li></ol><p><strong>Offers:</strong> 'Shall I...?' / 'Would you like me to...?' / 'Can I get you...?'</p><p><strong>Suggestions:</strong> 'Why don't we...?' / 'How about...?' / 'What if we...?'</p>",
    "examples": [
      "Would you mind sending me that document by Friday? (polite work request)",
      "Shall I get you another glass while you wait? (offer — polite, British English)",
      "How about we move the meeting to Thursday instead? (suggestion)",
    ],
    "questions": [
      ("Rank from most to least polite: (a) 'Can you help?' &nbsp; (b) 'Help me.' &nbsp; (c) 'I was wondering if you might be able to help.'",
       "(c) most polite → (a) neutral → (b) most direct/potentially rude.",
       "Longer requests with indirect structures signal more politeness. Direct is not wrong — it depends on the relationship and situation."),
      ("'Would you mind opening the window?' — does the answer 'No' mean yes or no?",
       "'No, I don't mind' = YES, I will open it. This trips up many learners.",
       "'Would you mind...?' asks 'Is this a problem?' So 'No' = 'No problem' = they will do it."),
      ("Make this more polite: 'Tell me the price.'",
       "'Could you tell me the price?' or 'Would you mind telling me the price?'",
       "Add 'could/would' and a question structure to soften any request."),
    ],
    "takeaway": "In professional English: the <strong>longer and more indirect</strong> the request, the more polite it sounds. 'I was wondering if you could...' is not weak — it is skilled.",
  },
  {
    "title": "Phrasal Verbs at Work: What Hospitality Really Taught Me",
    "level": "B1-B2",
    "category": "English Teaching",
    "tags": "phrasal verbs, B1 English, B2 English, work English, hospitality English, professional",
    "seo_title": "Phrasal Verbs for Work | B1-B2 English | Hospitality and Professional",
    "meta_description": "Learn essential phrasal verbs for the workplace with real hospitality examples. B1-B2 level.",
    "anecdote": "The head chef at Uccello had one rule: <em>'Run the kitchen. Don't manage it.'</em> I spent three months figuring out what that meant. Run — take full responsibility, keep it moving, own it. Phrasal verbs are where English gets specific. 'Run', 'set up', 'hand over', 'deal with' — they carry precise meaning that single verbs often miss.",
    "focus": "High-frequency work phrasal verbs: run, set up, take on, hand over, deal with, follow up, carry out",
    "explanation": "<p>Phrasal verbs = verb + particle. The meaning is often <strong>idiomatic</strong> — not literal.</p><table style='width:100%;border-collapse:collapse;'><tr style='background:#2a9d8f;color:#fff;'><th style='padding:8px;'>Phrasal verb</th><th style='padding:8px;'>Meaning in context</th></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>run (a place/team)</td><td style='padding:8px;border-bottom:1px solid #ddd;'>be in charge of, manage actively</td></tr><tr><td style='padding:8px;border-bottom:1px solid #ddd;'>set up</td><td style='padding:8px;border-bottom:1px solid #ddd;'>prepare, arrange, create the conditions</td></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>take on</td><td style='padding:8px;border-bottom:1px solid #ddd;'>accept responsibility / hire someone</td></tr><tr><td style='padding:8px;border-bottom:1px solid #ddd;'>hand over</td><td style='padding:8px;border-bottom:1px solid #ddd;'>transfer responsibility to someone else</td></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>deal with</td><td style='padding:8px;border-bottom:1px solid #ddd;'>handle a situation or problem</td></tr><tr><td style='padding:8px;'>follow up</td><td style='padding:8px;'>check on progress, contact again</td></tr></table>",
    "examples": [
      "She took on the role of duty manager after six months. (accepted new responsibility)",
      "We need to follow up on that complaint from table four. (check what happened/contact them)",
      "I set up the private dining room every Thursday evening. (prepare, arrange the space)",
    ],
    "questions": [
      ("Fill: 'Can you ___ ___ this complaint? I'm busy with service.' (phrasal verb = handle)",
       "deal with — 'Can you deal with this complaint?'",
       "'Deal with' is the standard phrasal verb for handling a problem or situation professionally."),
      ("'She handed over the keys' — what does this mean?",
       "She transferred the keys (and the responsibility they represent) to someone else.",
       "'Hand over' often implies transferring both a physical thing and the responsibility that goes with it."),
      ("Which is correct? (a) 'Follow up the client' &nbsp; (b) 'Follow up with the client' &nbsp; (c) Both",
       "(b) 'Follow up with the client' — you follow up WITH someone.",
       "'Follow up on something' is also correct: 'Follow up on the complaint.' The preposition changes based on what follows."),
    ],
    "takeaway": "Learn phrasal verbs in context, not in lists. The same verb + different particle = completely different meaning: <strong>take off</strong> (remove/fly) vs <strong>take on</strong> (accept/hire) vs <strong>take over</strong> (gain control).",
  },
  {
    "title": "Passive Voice: How Restaurants Speak English",
    "level": "B2",
    "category": "English Teaching",
    "tags": "passive voice, B2 English, English grammar, advanced English, formal writing",
    "seo_title": "Passive Voice in English | B2 Level | With and Without By",
    "meta_description": "Learn the passive voice at B2 level with real restaurant and professional examples. 5 minutes.",
    "anecdote": "As a sommelier at The Ivy, I lived inside the passive voice without knowing it had a name. <em>'The wine is aged for twelve months in French oak.'</em> <em>'The cork is extracted at the table.'</em> <em>'The temperature is maintained at 16 degrees.'</em> In fine dining, the process matters — not who does it. That is exactly when English reaches for the passive.",
    "focus": "Passive voice: is/are + pp, was/were + pp, has been + pp; when and why to use it",
    "explanation": "<p><strong>Form:</strong></p><ul><li>Present: <em>is/are</em> + past participle: 'The wine is served chilled.'</li><li>Past: <em>was/were</em> + pp: 'The reservation was cancelled.'</li><li>Present perfect: <em>has/have been</em> + pp: 'The sauce has been reduced for forty minutes.'</li></ul><p><strong>When to use passive:</strong></p><ol><li>The action matters more than the actor ('Mistakes were made.')</li><li>The actor is obvious, unknown, or unimportant</li><li>Formal/scientific/process descriptions</li></ol><p><strong>Add 'by' only when the actor matters:</strong> 'The dish was created by the head chef.'</p>",
    "examples": [
      "The fish is caught locally and delivered to us every morning. (process — actor not important)",
      "Mistakes were made, but the evening was saved. (actor deliberately vague)",
      "The sauce has been reduced for exactly forty minutes. (process description — passive is natural)",
    ],
    "questions": [
      ("Transform: 'The chef prepares the amuse-bouche fresh every day.'",
       "The amuse-bouche is prepared fresh every day (by the chef).",
       "The 'by the chef' part can be omitted if it's obvious or unimportant."),
      ("Why is passive used here? 'English is spoken in over 50 countries.'",
       "The actor (people/speakers) is too vague and obvious to name. The fact matters, not who does it.",
       "Passive is ideal when the subject would be 'people', 'someone', 'they' — vague or obvious actors."),
      ("Find the error: 'The report was written by me yesterday.'",
       "Grammatically correct but awkward. Better: 'I wrote the report yesterday.' — use active when the actor is clear and the sentence is simple.",
       "Passive is not always better. If the actor is known and the sentence is simple, active is cleaner and stronger."),
    ],
    "takeaway": "Use passive when the <strong>action or result matters more than the person doing it</strong>. Add 'by' only when that person is important. For simple sentences with a known actor, keep it active.",
  },
  {
    "title": "Reported Speech: What My Best Manager Actually Said",
    "level": "B2",
    "category": "English Teaching",
    "tags": "reported speech, B2 English, grammar, reporting verbs, indirect speech, tense backshift",
    "seo_title": "Reported Speech in English | B2 Level | Reporting Verbs and Tense Backshift",
    "meta_description": "Master reported speech in English with clear rules and real workplace examples. B2 level.",
    "anecdote": "My best manager at Merivale never gave direct orders. He said things like: <em>'I was wondering if you might have thought about checking the private dining room.'</em> Reported to a colleague later: <em>'He suggested I check the private dining room.'</em> That gap — between what was said and how we report it — is where grammar and social intelligence meet.",
    "focus": "Reported speech: tense backshift; said/told/asked; reporting verbs",
    "explanation": "<p><strong>Tense backshift (move one step back):</strong></p><table style='width:100%;border-collapse:collapse;font-size:0.9em;'><tr style='background:#2a9d8f;color:#fff;'><th style='padding:8px;'>Direct speech</th><th style='padding:8px;'>Reported speech</th></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>am/is/are</td><td style='padding:8px;border-bottom:1px solid #ddd;'>was/were</td></tr><tr><td style='padding:8px;border-bottom:1px solid #ddd;'>will</td><td style='padding:8px;border-bottom:1px solid #ddd;'>would</td></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>can</td><td style='padding:8px;border-bottom:1px solid #ddd;'>could</td></tr><tr><td style='padding:8px;'>past simple</td><td style='padding:8px;'>past perfect (had done)</td></tr></table><p style='margin-top:12px;'><strong>Said vs told:</strong> say (+ that) / tell (+ person + that): 'He <em>said</em> he was tired.' / 'He <em>told me</em> he was tired.'</p>",
    "examples": [
      "'Close early tonight.' → The manager told us to close early. (command → told + to-infinitive)",
      "'Can you come in at four?' → She asked if I could come in at four. (question → if-clause)",
      "'The kitchen is ready.' → He said that the kitchen was ready. (statement + tense backshift)",
    ],
    "questions": [
      ("Report this: 'I will call you tomorrow.' (She said...)",
       "She said she would call me the next day. ('Will' → 'would'; 'tomorrow' → 'the next day')",
       "Time expressions also change in reported speech: 'today' → 'that day'; 'yesterday' → 'the day before'."),
      ("Which is correct? (a) 'He said me he was tired.' &nbsp; (b) 'He told me he was tired.' &nbsp; (c) 'He told that he was tired.'",
       "(b) 'He told me he was tired.' — 'Tell' needs an object (me/us/her). 'Said' does not.",
       "'He said he was tired' ✓ (no object). 'He told me he was tired' ✓ (with object). 'He said me...' ✗."),
      ("What reporting verb fits? 'Don't touch the wine glasses.' (The sommelier _____ us not to touch them.)",
       "warned / told / instructed",
       "'Warn' carries a sense of danger or consequence. 'Tell' is neutral. 'Instruct' is formal."),
    ],
    "takeaway": "Move tenses <strong>one step back</strong> in reported speech. Use <strong>said (that)</strong> without an object, <strong>told + person</strong> with one. Choose your reporting verb carefully — it carries the speaker's tone.",
  },
  {
    "title": "Discourse Markers: How to Sound Fluent, Not Just Correct",
    "level": "B2",
    "category": "English Teaching",
    "tags": "discourse markers, B2 English, essay writing, cohesion, IELTS writing, linking words",
    "seo_title": "Discourse Markers in English | B2 Level | For Essays and IELTS",
    "meta_description": "Learn discourse markers for clear, cohesive writing at B2 level. For IELTS and professional writing.",
    "anecdote": "I failed my first formal English essay assignment in Australia. The ideas were there — solid, clear. But every paragraph started with 'Also' or 'And'. My tutor wrote just two words in the margin: <em>'Show logic.'</em> That was the day I understood what discourse markers actually do — they are not decoration. They are the architecture of an argument.",
    "focus": "Discourse markers for contrast, addition, result, and exemplification",
    "explanation": "<p><strong>Contrast:</strong> however · nevertheless · on the other hand · in spite of (this) · despite (this) · yet</p><p><strong>Addition:</strong> furthermore · in addition · moreover · what is more · not only... but also</p><p><strong>Result/consequence:</strong> therefore · consequently · as a result · thus · hence</p><p><strong>Exemplification:</strong> for instance · for example · such as · to illustrate</p><p><strong>Key rule:</strong> each marker carries a <em>specific logical relationship</em>. Don't scatter them — each one must be accurate. 'However' signals contrast. 'Therefore' signals result. Use the wrong one and your logic collapses.</p>",
    "examples": [
      "The course was demanding. However, the teaching practice was excellent. (contrast — unexpected positive after negative)",
      "Furthermore, the experience gave me confidence in front of a class. (addition — building the case)",
      "As a result, my first solo lesson went far better than I had expected. (result — consequence of previous point)",
    ],
    "questions": [
      ("Choose the correct marker: 'She studied hard. _____, she passed with distinction.' (However / Therefore)",
       "Therefore — this is a result, not a contrast. Studying hard caused the distinction.",
       "'However' would signal something unexpected: 'She studied hard. However, she failed.' — unexpected contrast."),
      ("Which marker shows CONTRAST? (a) Moreover &nbsp; (b) Nevertheless &nbsp; (c) Consequently",
       "(b) Nevertheless — 'despite what was just said, this is also true.'",
       "'Moreover' = addition. 'Consequently' = result. 'Nevertheless' = contrast/concession."),
      ("Find the error: 'I was nervous. Furthermore, I performed well.' (is 'furthermore' right here?)",
       "No. 'Furthermore' adds to the same point. Here the ideas contrast. Correct: 'I was nervous. Nevertheless/However, I performed well.'",
       "'Furthermore' means 'and in addition to this.' It cannot introduce a contrasting idea."),
    ],
    "takeaway": "Discourse markers signal <strong>logic, not style</strong>. Match the marker to the relationship: <strong>however</strong> (contrast) · <strong>therefore</strong> (result) · <strong>furthermore</strong> (addition). One wrong marker misleads your reader completely.",
  },
  {
    "title": "Collocations: Words That Travel Together in English",
    "level": "B2",
    "category": "English Teaching",
    "tags": "collocations, B2 English, vocabulary, English word pairs, business English, make do take have",
    "seo_title": "English Collocations | B2 Level | Make, Do, Take, Have",
    "meta_description": "Learn essential English collocations at B2 level. Make vs do, take vs have, and adjective-noun pairs.",
    "anecdote": "In English, you do not 'make' homework — you 'do' it. You do not 'do' a mistake — you 'make' one. These are collocations: word partnerships that native speakers use automatically, without thinking. I learned mine slowly, by ear, working at The Ivy. Every menu description, every briefing, every order — patterns emerged. English is a language of partnerships.",
    "focus": "Verb-noun collocations: make/do/take/have; adjective-noun collocations",
    "explanation": "<p><strong>MAKE:</strong> make a mistake, make a decision, make an effort, make progress, make a reservation, make a suggestion</p><p><strong>DO:</strong> do homework, do research, do the washing up, do business, do damage, do well</p><p><strong>TAKE:</strong> take a break, take responsibility, take a seat, take action, take part (in)</p><p><strong>HAVE:</strong> have a meeting, have a conversation, have an argument, have difficulty, have an opportunity</p><p><strong>Adjective-noun collocations:</strong> heavy traffic · strong coffee · golden opportunity · deep sleep · high demand · bitter disappointment</p>",
    "examples": [
      "I made a reservation for two at 7:30. (not 'did' a reservation)",
      "We did a lot of research before moving to Réunion. (not 'made' research)",
      "She gave a presentation to the board on Tuesday. (give a presentation — another common collocation)",
    ],
    "questions": [
      ("Which is correct? (a) 'make homework' &nbsp; (b) 'do homework' &nbsp; (c) 'have homework'",
       "(b) do homework — 'do' is used for tasks and activities.",
       "'Make' is for creating or producing something. 'Homework' is a task, not a created object."),
      ("Fill: 'They ___ a meeting to discuss the budget.' (had / made / did)",
       "had — 'have a meeting' is the standard collocation.",
       "Other 'have' collocations: have a conversation, have a break, have an idea, have difficulty."),
      ("Which adjective fits? '___ traffic delayed us by an hour.' (strong / heavy / big)",
       "heavy traffic — this is a fixed collocation. 'Strong traffic' and 'big traffic' are not natural English.",
       "Collocations are irrational — you simply have to learn the pairs. 'Heavy rain', 'heavy traffic', 'heavy workload.'"),
    ],
    "takeaway": "Learn collocations as <strong>fixed pairs</strong>, not individual words. The fastest way: read and listen widely and notice what comes before and after your target word. <strong>Do homework. Make a mistake. Have a meeting.</strong>",
  },
  {
    "title": "Hedging Language: Sound Confident Without Overclaiming",
    "level": "B2",
    "category": "English Teaching",
    "tags": "hedging language, B2 English, academic writing, professional English, IELTS, formal writing",
    "seo_title": "Hedging Language in English | B2 Level | Academic and Professional Writing",
    "meta_description": "Learn hedging language for professional and academic English. B2 level, with real examples.",
    "anecdote": "My first job application in France said: <em>'I am an excellent communicator.'</em> The interviewer looked up and asked: <em>'Excellent by whose standard?'</em> That was the day I understood that in professional and academic English, confidence sounds different from certainty. You hedge. <em>'I believe my experience in cross-cultural teams demonstrates strong communication skills'</em> is stronger — more credible — than the bold claim.",
    "focus": "Hedging: modal verbs, it seems/appears, arguably, I would suggest, tend to",
    "explanation": "<p><strong>Modal verbs for hedging:</strong> might · could · may · would (softer than 'will')</p><p><strong>Introductory phrases:</strong> It seems that · It would appear that · There is some evidence to suggest that</p><p><strong>Adverbials:</strong> arguably · possibly · apparently · generally · in most cases · to some extent</p><p><strong>Reporting verbs:</strong> suggests · indicates · implies · tends to show</p><p><strong>Why hedge?</strong> Because most claims have exceptions. Hedging shows intellectual honesty. 'Research suggests...' is stronger than 'Everyone knows...' because it is honest about its own limits.</p>",
    "examples": [
      "It would appear that the reservation was not confirmed correctly. (hedged — not blaming anyone directly)",
      "This approach might work better in smaller groups. (might = possible, not certain)",
      "Arguably, the simplest solution tends to be the most effective in this context. (arguably + tends to = double hedge)",
    ],
    "questions": [
      ("Make this less absolute: 'Bilingual children are always more creative.'",
       "'Bilingual children may tend to show greater creativity in some contexts.' (or: 'Some research suggests that bilingualism is associated with...')",
       "'Always' is almost always too strong. Replace with 'often', 'tend to', 'may', 'in many cases.'"),
      ("Which sentence is MORE appropriately hedged for academic writing? (a) 'Climate change will destroy the economy.' &nbsp; (b) 'Climate change may have significant economic consequences.'",
       "(b) — 'may have significant consequences' is hedged and accurate. (a) is overclaimed and unprovable.",
       "Academic writing rarely uses 'will' for predictions — 'may', 'could', 'might', 'is likely to' are preferred."),
      ("Is this over-hedged? 'It might possibly perhaps be the case that this could potentially be true.'",
       "Yes — extreme over-hedging. Use one or two hedges, not five. 'This may be true.' is enough.",
       "Over-hedging sounds evasive and lacks credibility. One precise hedge is more powerful than five vague ones."),
    ],
    "takeaway": "Hedging is a <strong>precision tool</strong>, not a weakness. One well-chosen hedge (<em>might, arguably, tends to</em>) makes your claim more credible. Three hedges in one sentence destroys it.",
  },
  {
    "title": "IELTS Writing Task 2: How to Plan Your Essay in 5 Minutes",
    "level": "B2",
    "category": "Career & Professional Development",
    "tags": "IELTS writing, task 2, essay structure, B2 English, exam English, paragraph writing",
    "seo_title": "IELTS Writing Task 2: Essay Structure | B2 Level",
    "meta_description": "Plan and structure your IELTS Task 2 essay in 5 minutes. B2 level with step-by-step guide.",
    "anecdote": "I took IELTS in 2026. The writing section did not test my vocabulary — it tested whether I could <em>think in paragraphs</em> under pressure. Once I drew a simple box on my paper with four sections, everything became clear: <em>what I think, why I think it (point 1), why I think it (point 2), what I conclude</em>. The structure was the hardest part. Once I had it, the words followed.",
    "focus": "Task 2 structure: introduction → body paragraph 1 → body paragraph 2 → conclusion",
    "explanation": "<p><strong>The 4-part structure:</strong></p><ol><li><strong>Introduction:</strong> Paraphrase the question in your own words (1 sentence) + state your position/thesis (1 sentence). Total: 2 sentences.</li><li><strong>Body paragraph 1:</strong> Topic sentence + explanation + example/evidence. (5-6 sentences)</li><li><strong>Body paragraph 2:</strong> Topic sentence + explanation + example/evidence. (5-6 sentences)</li><li><strong>Conclusion:</strong> Restate your position + broader implication. DO NOT introduce new ideas.</li></ol><p><strong>Planning time:</strong> Spend 5 minutes planning before you write. Write the topic sentence for each paragraph first — the rest follows naturally.</p>",
    "examples": [
      "Introduction: 'The question of whether universities should focus solely on academic subjects has been widely debated. While academic rigour is important, I believe practical skills are equally necessary for graduate success.'",
      "Body 1 topic sentence: 'Practical training prepares students more directly for the demands of the modern job market.'",
      "Conclusion: 'In conclusion, universities serve their students best by combining academic depth with practical application, rather than treating these goals as mutually exclusive.'",
    ],
    "questions": [
      ("What goes in the introduction? (a) Your main argument + evidence &nbsp; (b) Paraphrase + thesis statement &nbsp; (c) A definition of the topic",
       "(b) Paraphrase + thesis statement — these two sentences are all you need.",
       "Do not begin with a definition ('According to the dictionary...'). Examiners have seen it a thousand times. Paraphrase the question, state your view."),
      ("True or false: The conclusion should introduce a new argument to strengthen your essay.",
       "False. The conclusion restates your position and may suggest a broader implication — but never introduces new ideas.",
       "New ideas in a conclusion suggest you ran out of body paragraph space. Plan so you don't need to do this."),
      ("What is a 'topic sentence'?",
       "The first sentence of a body paragraph — it states the ONE main point that the whole paragraph will develop.",
       "If your topic sentence is clear, the paragraph almost writes itself. If it's vague, the whole paragraph loses direction."),
    ],
    "takeaway": "Plan before you write. Draw four boxes: intro / body 1 / body 2 / conclusion. Write the topic sentence for each box first. <strong>5 minutes of planning saves 20 minutes of rewriting.</strong>",
  },
  {
    "title": "IELTS Task 1: Describing Data Without Sounding Like a Robot",
    "level": "B2",
    "category": "Career & Professional Development",
    "tags": "IELTS task 1, data description, B2 English, writing, graphs, charts, trends",
    "seo_title": "IELTS Writing Task 1: Describing Data and Graphs | B2 Level",
    "meta_description": "Learn to describe charts and data for IELTS Task 1 at B2 level. Real vocabulary, real strategies.",
    "anecdote": "At the Star Casino, I read sales reports every Monday morning. Volume, trends, percentage change. I was reading data in hospitality English years before I ever sat an exam. I said things like <em>'Sales rose sharply in December and levelled off in January'</em> to my manager in 2013. That is an IELTS Task 1 sentence. The language was already there — I just didn't know its name.",
    "focus": "Task 1: trend language, overview sentence, selecting key features",
    "explanation": "<p><strong>Trend vocabulary</strong> (always vary your word choice):</p><ul><li><strong>Rise:</strong> rose · increased · went up · grew · climbed · surged</li><li><strong>Fall:</strong> fell · decreased · declined · dropped · dipped · plummeted</li><li><strong>Stable:</strong> remained stable · levelled off · plateaued · held steady</li><li><strong>Peak:</strong> peaked at · reached a high of · hit a maximum of</li></ul><p><strong>Essential overview sentence:</strong> 'Overall, [the most significant trend]...' Write this in your introduction — it shows you can see the big picture.</p><p><strong>Proportion language:</strong> accounted for · represented · made up · constituted · comprised</p>",
    "examples": [
      "The number of overseas visitors rose sharply between 2010 and 2015, before levelling off at around 3 million.",
      "Tourism accounted for approximately 40% of national revenue in the final year of the period.",
      "Overall, there was a clear upward trend in exports throughout the fifteen-year period, despite a brief dip in 2018.",
    ],
    "questions": [
      ("What is the FIRST thing to write in Task 1?",
       "An overview sentence: 'Overall, [the main trend or key feature].' Then describe specific data points.",
       "IELTS examiners specifically assess whether you can identify and state the main trends. No overview = lower band score."),
      ("Which word fits? 'Sales ___ at £2 million in March.' (peaked / rose / levelled)",
       "peaked — 'peaked at' means reached the highest point.",
       "'Rose to £2 million' would mean £2M was not necessarily the highest. 'Peaked at' confirms it was the maximum."),
      ("Which is better for Task 1? (a) 'There were lots of people.' &nbsp; (b) 'The figure rose significantly to approximately 4.5 million.'",
       "(b) — specific data with precise language and an adverb of degree.",
       "IELTS rewards specificity. Always refer to the actual figures, use adverbs (significantly, slightly, dramatically), and vary your vocabulary."),
    ],
    "takeaway": "Always start with an <strong>overview</strong>. Vary your trend vocabulary (rose/increased/grew). <strong>Always refer to actual data</strong> — never describe without numbers. Select the most significant trends rather than describing every single figure.",
  },
  {
    "title": "Speaking Fluently: Fillers, Pausing, and Buying Time in English",
    "level": "B2",
    "category": "English Teaching",
    "tags": "speaking English, fluency, B2 English, IELTS speaking, fillers, pausing strategies",
    "seo_title": "Spoken Fluency in English: Fillers and Pausing | B2 Level",
    "meta_description": "Learn spoken fluency strategies for IELTS Speaking and everyday English conversations. B2 level.",
    "anecdote": "In my IELTS Speaking exam, the examiner asked: <em>'What would you change about where you live?'</em> I had the answer — I needed two seconds to organise it. I said: <em>'That's a good question — well, I suppose if I'm honest...'</em> Those six words gave me exactly the time I needed. The examiner did not mark me down. Fluency is not about speaking fast — it is about managing silence.",
    "focus": "Fluency strategies: fillers, stalling, self-correction, rephrasing",
    "explanation": "<p><strong>Fillers</strong> (natural, normal in spoken English):</p><p>Well... · You know... · I mean... · Right... · So... · Actually... · Basically...</p><p><strong>Stalling phrases</strong> (buy 2-3 seconds):</p><p>'That's a good question...' · 'Let me think about that for a moment...' · 'It's hard to say exactly, but...' · 'I suppose...' · 'Off the top of my head...'</p><p><strong>Self-correction and rephrasing:</strong></p><p>'Or rather...' · 'What I mean is...' · 'Sorry — what I was trying to say is...' · 'Actually, a better way to put it would be...'</p>",
    "examples": [
      "Well, I suppose the one thing I'd change about Réunion is... actually, no — there isn't one thing. It's the transport system, if I'm honest. (filler + self-correction)",
      "Let me think about that for a moment — OK, so if I had to choose... (stalling + transition)",
      "The main problem — or rather, the most visible problem — is the cost of living. (rephrasing for precision)",
    ],
    "questions": [
      ("Is using fillers a sign of weak English?",
       "No. Fillers like 'well', 'I mean', 'you know' are completely natural in spoken English. Even native speakers use them.",
       "In IELTS Speaking, examiners look for natural spoken rhythm. A brief 'well...' before answering is better than a five-second silence."),
      ("Which stalling phrase fits a formal context better? (a) 'Umm, I dunno...' &nbsp; (b) 'That's an interesting question — let me consider it for a moment.'",
       "(b) — clearly signals you are thinking, not struggling. Much more controlled and professional.",
       "In formal or exam contexts, choose stalling phrases that show thoughtfulness rather than uncertainty."),
      ("After saying 'She works at the hospital', you want to correct to 'clinic'. Which rephraser works?",
       "'She works at the hospital — or rather, the clinic.' ('Or rather' signals a correction/clarification.)",
       "'Or rather' is the most elegant rephraser. 'I mean' is slightly more casual. Both are correct."),
    ],
    "takeaway": "Fluency = managing silence smoothly. Use <strong>'Well...'</strong> or <strong>'Let me think about that...'</strong> to buy time. Use <strong>'or rather'</strong> to self-correct elegantly. These are skills, not crutches.",
  },
  {
    "title": "Modal Perfects: The Grammar of Regret and Past Possibility",
    "level": "B2-C1",
    "category": "English Teaching",
    "tags": "modal perfect, B2 English, C1 English, should have, could have, might have, grammar, regret",
    "seo_title": "Modal Perfects in English | B2-C1 Level | Should Have, Could Have",
    "meta_description": "Master modal perfects (should have, could have, might have) with clear examples. B2-C1 level.",
    "anecdote": "On a long flight from Paris to Réunion, I sat with nothing but my thoughts. <em>'Could I have done anything differently?'</em> <em>'Should I have stayed in Sydney?'</em> <em>'Would things have been different if I had finished my accounting degree?'</em> Three modal perfects in two minutes of quiet worry. This grammar is not abstract — it is the shape of how humans think about their past choices.",
    "focus": "Modal perfects: should/could/might/would + have + past participle",
    "explanation": "<p><strong>Each modal carries different meaning:</strong></p><ul><li><strong>Should have + pp</strong> = regret or criticism about the past. 'I should have left earlier.' (I didn't — I regret it.)</li><li><strong>Could have + pp</strong> = past possibility that wasn't taken. 'We could have booked in advance.' (We didn't — it was possible.)</li><li><strong>Might have + pp</strong> = uncertain past possibility. 'She might have missed the flight.' (Not sure if she did.)</li><li><strong>Would have + pp</strong> = imagined past result. 'I would have stayed if I'd known.' (Hypothetical past.)</li></ul>",
    "examples": [
      "I should have learned French before moving to Paris — that would have saved me six months of confusion.",
      "We could have booked the restaurant in advance — now there's no table available.",
      "She might have already left — try calling her mobile.",
    ],
    "questions": [
      ("Which expresses REGRET? (a) 'He could have passed.' &nbsp; (b) 'He should have studied more.' &nbsp; (c) 'He might have passed.'",
       "(b) 'Should have studied more' — this is regret/criticism: he didn't study enough and the speaker thinks he should have.",
       "'Could have passed' = it was possible. 'Might have passed' = uncertain. 'Should have studied' = regret."),
      ("Fill: 'It's raining — I ___ have brought an umbrella.' (should / might / would)",
       "should have brought — regret. I didn't bring it. I wish I had.",
       "'Might have brought' would mean uncertainty about whether I brought it or not — not appropriate here."),
      ("What does 'You needn't have cooked so much food' mean?",
       "You cooked a lot, but it wasn't necessary. The cooking is done — it was unnecessary in hindsight.",
       "'Needn't have' = you did it, but it was not needed. 'Didn't need to' = you didn't do it because it wasn't needed. Subtle but important."),
    ],
    "takeaway": "<strong>Should have</strong> = regret/criticism (it happened and was wrong, or it didn't happen and should have). <strong>Could have</strong> = missed possibility. <strong>Might have</strong> = uncertain past. Tone comes from the modal — choose carefully.",
  },
  {
    "title": "Circumlocution: Talking Around the Words You Don't Know",
    "level": "B2-C1",
    "category": "English Teaching",
    "tags": "circumlocution, B2 English, C1 English, speaking strategies, vocabulary, IELTS speaking",
    "seo_title": "Circumlocution in English | Talking Around Unknown Words | B2-C1",
    "meta_description": "Learn circumlocution strategies for speaking English when you don't know the exact word. B2-C1 level.",
    "anecdote": "My first year of French in Paris, I didn't know the word for 'dishwasher'. So I said: <em>'la machine qui lave les assiettes'</em> — the machine that washes the plates inside your kitchen. My colleague understood immediately and told me the word: <em>lave-vaisselle</em>. Circumlocution is not a failure. It is a strategy — and IELTS examiners give you marks for using it well.",
    "focus": "Circumlocution: describing unknown words using 3 strategies",
    "explanation": "<p><strong>Three circumlocution techniques:</strong></p><ol><li><strong>Category + description:</strong> 'It's a kind of tool that you use to...' / 'It's a type of [category] for...'</li><li><strong>Function:</strong> 'It's used for [verb]-ing...' / 'It's something you use when you want to...'</li><li><strong>Contrast/similarity:</strong> 'It's similar to X, but...' / 'It's like Y, except...' / 'It's the opposite of...'</li></ol><p><strong>Useful frames:</strong></p><ul><li>'It's a device/machine/tool that...'</li><li>'It's the kind of thing you find in a...'</li><li>'It's what you'd call a... in everyday situations'</li></ul>",
    "examples": [
      "It's a kind of container — wider than a bottle, usually glass, that you use to pour wine into before serving. (= a decanter)",
      "It's similar to a manager, but specifically for the finances of the company. (= a CFO / financial controller)",
      "It's what you use to tell the time when you don't have a phone — usually worn on the wrist. (= a watch)",
    ],
    "questions": [
      ("Describe a 'thermometer' without using the word.",
       "'It's a device that measures temperature — you put it in your mouth or under your arm when you're ill.'",
       "Category (device) + function (measures temperature) + typical use context. All three techniques in one sentence."),
      ("Which technique is used here: 'It's like a dictionary but specifically for synonyms and alternative words.'",
       "Contrast/similarity technique — 'like [known thing] but [difference].'",
       "This is often the fastest technique for everyday objects that have a close equivalent."),
      ("Is circumlocution appropriate in IELTS speaking if you forget a word?",
       "Yes — absolutely. IELTS examiners specifically credit lexical resource, which includes the ability to work around gaps in vocabulary.",
       "Stopping and saying 'I don't know the word' costs marks. Circumlocuting smoothly earns them."),
    ],
    "takeaway": "When you don't know a word: <strong>describe it</strong>. Category + function + contrast. 'It's a kind of [category] used for [function], similar to [known thing].' Never stop — keep talking.",
  },
  {
    "title": "Inversion for Emphasis: Never Have I Felt So English",
    "level": "C1",
    "category": "English Teaching",
    "tags": "inversion, C1 English, advanced grammar, emphasis, formal English, never rarely",
    "seo_title": "Inversion for Emphasis in English | C1 Level | Advanced Grammar",
    "meta_description": "Learn inversion structures for formal emphasis in advanced English. C1 level with clear examples.",
    "anecdote": "The most dramatic sentence I ever said in English came without planning. I was explaining my career to someone at a conference in Réunion: <em>'Never have I worked somewhere where I felt truly seen as a professional.'</em> I didn't plan the inversion — it came from the emotion of the moment. The person I was speaking to paused. That pause was the sentence working. Inversion is not showing off — it is precision emphasis.",
    "focus": "Inversion: Never/Rarely/Seldom + auxiliary + subject; Not only...but also; Had I known...",
    "explanation": "<p><strong>Negative adverbial inversion:</strong></p><p>Normal: 'I have never worked so hard.'</p><p>Inverted: '<strong>Never have I</strong> worked so hard.' (auxiliary before subject)</p><p><strong>Common triggers:</strong> Never · Rarely · Seldom · Hardly · Not only · No sooner · Little · Only after/when/if</p><p><strong>Conditional inversion (formal):</strong></p><ul><li>'Had I known...' (= 'If I had known...')</li><li>'Were I to leave...' (= 'If I were to leave...')</li><li>'Should you need help...' (= 'If you should need help...')</li></ul><p><strong>Warning:</strong> Inversion is emphatic — use selectively. One inverted sentence per paragraph at most.</p>",
    "examples": [
      "Not only did she speak four languages, but she also held a teaching qualification in each. (adds dramatic emphasis)",
      "Rarely have I encountered such genuine kindness from a complete stranger. (literary/formal tone)",
      "Had I known the course would be that demanding, I would have started preparing earlier. (formal conditional)",
    ],
    "questions": [
      ("Transform: 'I have never seen anything like this.'",
       "'Never have I seen anything like this.' (auxiliary 'have' moves before subject 'I')",
       "Step 1: identify the negative adverbial (Never). Step 2: move it to the front. Step 3: swap subject and auxiliary."),
      ("Transform to inverted conditional: 'If I had arrived earlier, I would have met her.'",
       "'Had I arrived earlier, I would have met her.' (remove 'if', invert 'had' and 'I')",
       "This is a C1-C2 structure common in formal writing, literature, and speeches. It sounds sophisticated without being unnatural."),
      ("Is this correct? 'Rarely she goes to the cinema.' Why/why not?",
       "Incorrect. With 'rarely', inversion is required: 'Rarely does she go to the cinema.' The auxiliary 'does' must come before the subject.",
       "Without inversion after negative adverbials, the sentence sounds like a direct translation from another language."),
    ],
    "takeaway": "After <strong>Never, Rarely, Seldom, Not only</strong> — invert the subject and auxiliary. In conditional inversion, drop 'if' and move <strong>Had/Were/Should</strong> before the subject. Use sparingly — once per paragraph, maximum.",
  },
  {
    "title": "Nominalisation: Why Formal English Loves Nouns",
    "level": "C1",
    "category": "English Teaching",
    "tags": "nominalisation, C1 English, academic writing, advanced grammar, formal writing, suffixes",
    "seo_title": "Nominalisation in English | C1 Level | Formal and Academic Writing",
    "meta_description": "Learn nominalisation for formal and academic English writing at C1 level.",
    "anecdote": "Immigration paperwork taught me nominalisation before I knew the word for it. On every form: <em>'the application'</em> (not 'I applied'). <em>'The investigation is ongoing'</em> (not 'they are investigating'). <em>'Upon the arrival of'</em> (not 'when someone arrives'). Bureaucracy runs on nouns — and so does academic English. Once you see it, you cannot unsee it.",
    "focus": "Nominalisation: turning verbs and adjectives into nouns for formal effect",
    "explanation": "<p><strong>Common noun suffixes:</strong></p><table style='width:100%;border-collapse:collapse;font-size:0.9em;'><tr style='background:#2a9d8f;color:#fff;'><th style='padding:8px;'>Verb/Adjective</th><th style='padding:8px;'>Noun</th></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>decide → </td><td style='padding:8px;border-bottom:1px solid #ddd;'>decision (-ion)</td></tr><tr><td style='padding:8px;border-bottom:1px solid #ddd;'>develop → </td><td style='padding:8px;border-bottom:1px solid #ddd;'>development (-ment)</td></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>perform → </td><td style='padding:8px;border-bottom:1px solid #ddd;'>performance (-ance)</td></tr><tr><td style='padding:8px;border-bottom:1px solid #ddd;'>arrive → </td><td style='padding:8px;border-bottom:1px solid #ddd;'>arrival (-al)</td></tr><tr style='background:#f0f9f8;'><td style='padding:8px;border-bottom:1px solid #ddd;'>investigate → </td><td style='padding:8px;border-bottom:1px solid #ddd;'>investigation (-ion)</td></tr><tr><td style='padding:8px;'>accurate → </td><td style='padding:8px;'>accuracy (-cy)</td></tr></table><p style='margin-top:12px;'><strong>Effect:</strong> makes writing more compact, formal, and less personal. But don't overuse it — over-nominalization makes writing dense and hard to read.</p>",
    "examples": [
      "The arrival of the new cohort changed the dynamic. (vs 'When the new cohort arrived, the dynamic changed.')",
      "There has been significant improvement in the department's performance. (vs 'The department has improved significantly.')",
      "We conducted a thorough investigation into the incident. (vs 'We investigated the incident thoroughly.')",
    ],
    "questions": [
      ("Nominalise: 'They decided to close the school.'",
       "'The decision to close the school was made.' or 'The closure of the school was decided.'",
       "'Decide' → 'decision' (-ion). 'Close' → 'closure' (-ure). Note how the subject of the verb disappears — this is typical of formal passive nominalisation."),
      ("Which is more formal? (a) 'We investigated the complaint.' &nbsp; (b) 'An investigation into the complaint was conducted.'",
       "(b) is more formal — nominalisation ('investigation') + passive ('was conducted') is the hallmark of official reports.",
       "Neither is wrong. (a) is clearer and more direct. (b) is appropriate for formal reports, legal documents, and academic writing."),
      ("Spot the over-nominalisation: 'The utilisation of the implementation of the modification produced a resultant enhancement.'",
       "Severely over-nominalized. Clearer: 'Using the update improved results.' — never sacrifice clarity for formality.",
       "Orwell's rule applies: if nominalisation makes your sentence harder to understand, it is making your writing worse, not better."),
    ],
    "takeaway": "Nominalisation makes writing formal and compact — but <strong>clarity beats formality</strong>. Use nouns when the actor is unimportant and the action is the focus. Use verbs when clarity matters more than register.",
  },
  {
    "title": "Orwell's Rules: Why Short Words Win in English",
    "level": "C1",
    "category": "English Teaching",
    "tags": "Orwell, plain English, C1 English, writing style, editing, academic writing, clarity",
    "seo_title": "Plain English Writing: Orwell's Six Rules | C1 Level",
    "meta_description": "Apply George Orwell's plain English rules to improve your formal and academic writing. C1 level.",
    "anecdote": "I rewrote my professional biography four times. Each draft was shorter than the last. The fourth draft — eleven lines, no adjectives I couldn't justify — was the one that landed me two callbacks in the same week. George Orwell wrote his six rules in 1946. Every professional writer I have encountered since then has independently arrived at the same conclusions.",
    "focus": "Orwell's six rules for plain English: cut, shorten, activate, clarify",
    "explanation": "<p><strong>Orwell's six rules</strong> (<em>Politics and the English Language</em>, 1946):</p><ol><li>Never use a long word where a short one works.</li><li>If it is possible to cut a word, cut it.</li><li>Never use the passive where you can use the active.</li><li>Never use a foreign phrase, a scientific word, or jargon if an everyday English word exists.</li><li>Never use a long word if a short one will do.</li><li>Break any of these rules before writing something barbarous.</li></ol><p><strong>In practice:</strong> utilize → use · facilitate → help · at this point in time → now · with regard to → about · in order to → to · due to the fact that → because</p>",
    "examples": [
      "'We utilized our available resources to facilitate the process.' → 'We used what we had to make it work.' (shorter, clearer, stronger)",
      "'At this point in time, the situation is complex.' → 'Right now, this is complicated.' (cut: 4 words become 1)",
      "'Results were delivered by the team ahead of schedule.' → 'The team delivered early.' (active, cut, shorter)",
    ],
    "questions": [
      ("Rewrite using Orwell's rules: 'It is of the utmost importance that we commence the facilitation of the onboarding process at the earliest possible opportunity.'",
       "'We need to start onboarding now.' (or: 'Start onboarding as soon as possible.')",
       "Every Orwell rule violated in the original: long words, unnecessary words, passive buried in nominalisations."),
      ("Is the passive always wrong?",
       "No. Use passive when the actor is unknown or unimportant — 'The building was constructed in 1890.' Orwell's rule is 'avoid it where you can use the active', not 'never use it.'",
       "Rule 6 applies: break any rule before writing something barbarous. Context matters. Orwell himself used the passive."),
      ("Which word is shorter and clearer? (a) 'utilize' &nbsp; (b) 'use'",
       "(b) 'use' — three letters vs seven, and identical in meaning.",
       "Every time you write 'utilize', ask: does the extra syllable carry any extra meaning? Usually: no. Use 'use.'"),
    ],
    "takeaway": "Before submitting anything: <strong>cut every word you can</strong>. Replace long words with short ones. Make passives active. If the sentence survives the cut, the word was dead weight.",
  },
  {
    "title": "Mixed Conditionals: When the Past Changes the Present",
    "level": "C1-C2",
    "category": "English Teaching",
    "tags": "mixed conditionals, C1 English, C2 English, advanced grammar, conditionals, hypothetical",
    "seo_title": "Mixed Conditionals in English | C1-C2 Level | Advanced Grammar",
    "meta_description": "Learn mixed conditionals with real life examples. C1-C2 level advanced English grammar.",
    "anecdote": "If I had not left Bangladesh in 2005, I would not be sitting in Réunion writing this lesson right now. That single sentence mixes a past condition with a present result. It is not a rare or exotic structure — it is the most human of all conditional sentences. It is the shape of a life: the choices made, the consequences lived.",
    "focus": "Mixed conditionals: past condition → present result; present state → past result",
    "explanation": "<p><strong>Type A (most common): Past condition → present result</strong></p><p style='background:#264653;color:#edf2f4;padding:8px 14px;border-radius:6px;font-family:monospace;'>If + had + pp ... would + base verb (now)</p><p>E.g. 'If I had stayed in Sydney, I would be a restaurant director now.' (Past choice → present situation)</p><p><strong>Type B (reverse): Present state → past result</strong></p><p style='background:#264653;color:#edf2f4;padding:8px 14px;border-radius:6px;font-family:monospace;'>If + past simple (present) ... would have + pp (past)</p><p>E.g. 'If I were more risk-averse, I would never have moved abroad.' (Current personality → hypothetical past action)</p>",
    "examples": [
      "If we had invested earlier, we would be comfortable financially now. (past decision → present situation)",
      "If I weren't so determined by nature, I would have given up during the first year in Sydney. (present trait → hypothetical past action)",
      "She might be a doctor now if she had studied medicine instead of linguistics. (past → present, with 'might' for uncertainty)",
    ],
    "questions": [
      ("Identify the type: 'If I had learned French earlier, I would be fluent by now.'",
       "Type A: past condition (had learned earlier) → present result (would be fluent now).",
       "The if-clause is in the past perfect. The result clause describes the present. Classic Type A mixed conditional."),
      ("Complete: 'If he ___ (be) less impulsive, he ___ never ___ (make) that mistake.'",
       "'If he were less impulsive, he would never have made that mistake.' (Present trait → past result = Type B)",
       "Were = present subjunctive (imaginary present state). Would have made = past hypothetical result."),
      ("Why use a mixed conditional instead of a standard type 2 or type 3?",
       "Because the condition and result belong to different time frames. Standard type 2 = imaginary present → present result. Standard type 3 = imaginary past → past result. Mixed = when they cross.",
       "This is why mixed conditionals feel so natural when talking about decisions and their long-term effects."),
    ],
    "takeaway": "<strong>Past condition + present result</strong>: If + had done... would be... now. <strong>Present state + past result</strong>: If + were... would have done. The tense in each clause is independent — they come from different time frames.",
  },
  {
    "title": "Register and Style: The Four Englishes of One Working Day",
    "level": "C1-C2",
    "category": "English Teaching",
    "tags": "register, style, C1 English, C2 English, formal English, professional writing, register spectrum",
    "seo_title": "English Register and Style | C1-C2 Level | Formal vs Informal",
    "meta_description": "Understand English register — from informal to official — with real workplace examples. C1-C2 level.",
    "anecdote": "As a restaurant manager in Sydney, I used four different Englishes in one shift. With kitchen staff: <em>'Check if the lamb's ready.'</em> With a VIP guest: <em>'I understand the table wasn't quite to your satisfaction this evening.'</em> With a supplier: <em>'We'll need that confirmed in writing by close of business.'</em> With my wife on the phone: <em>'I'm knackered, home by two.'</em> Same person. Four registers. English is not one language — it is several, stacked.",
    "focus": "Register spectrum: informal → neutral → formal → official; markers of each",
    "explanation": "<p><strong>Four register markers to shift:</strong></p><ol><li><strong>Contractions:</strong> I'm/I am · can't/cannot · it's/it is (fewer = more formal)</li><li><strong>Vocabulary:</strong> get → obtain · buy → purchase · start → commence · help → assist · now → at this juncture</li><li><strong>Sentence structure:</strong> short/simple (informal) vs complex/subordinated (formal)</li><li><strong>Politeness distance:</strong> direct (informal) vs indirect/hedged (formal)</li></ol><p><strong>Register mismatch</strong> — using formal vocabulary in casual chat, or slang in an official letter — is one of the most common C1-C2 errors. It sounds more wrong than a grammar mistake.</p>",
    "examples": [
      "Informal: 'I'm gonna be late — stuck in traffic.' | Formal: 'I regret to inform you that I will be delayed.'",
      "Neutral: 'Please let me know if you have any questions.' | Official: 'Should you require further clarification, do not hesitate to contact our office.'",
      "Informal: 'That's brilliant!' | Formal: 'That is an excellent outcome.' | Official: 'The results have been assessed as highly satisfactory.'",
    ],
    "questions": [
      ("Identify the register: 'Should you require any further assistance, please do not hesitate to contact the undersigned.'",
       "Official/very formal — 'should you require', 'the undersigned', 'do not hesitate to' are all markers of official written register.",
       "This level of formality is appropriate in legal documents, formal correspondence, and official notices — not everyday emails."),
      ("Find the register mismatch: 'Dear Sir/Madam, I am totally gutted to inform you that your application was unsuccessful.'",
       "'Gutted' is informal/colloquial — completely wrong in a formal letter that opens with 'Dear Sir/Madam.'",
       "Correct: 'I regret to inform you...' Register must be consistent throughout any piece of writing."),
      ("Which register fits an email to a new client you haven't met? (a) Very informal &nbsp; (b) Neutral-to-formal &nbsp; (c) Official",
       "(b) Neutral-to-formal — professional but not stiff. Use full words (I am, not I'm), polite structures, but no legal language.",
       "First contact with an unknown professional: always neutral-to-formal. You can drop to neutral once you've established a relationship."),
    ],
    "takeaway": "Register mismatch sounds worse than a grammar mistake. <strong>Identify your audience first, then choose your register</strong>. Formal ≠ better. <strong>Appropriate = better</strong>. Check for consistency throughout every document.",
  },
  {
    "title": "Four Languages in One Head: What Multilingualism Teaches You About English",
    "level": "C1-C2",
    "category": "English Teaching",
    "tags": "multilingualism, code-switching, C1 English, C2 English, language learning, interference errors, advanced",
    "seo_title": "Multilingualism and English: What Four Languages Teach You | C1-C2",
    "meta_description": "Explore what multilingualism reveals about English grammar and usage. C1-C2 level with real examples.",
    "anecdote": "Bengali at home. English at work. French with neighbours. Hindi when I dream. I didn't plan to become multilingual — it happened because I moved, because I had to, because language follows necessity. What I discovered is that each new language does not replace the others. They stack. They interfere. They also teach you things about each other that monolingual speakers never see. This lesson is about what happens inside a multilingual mind — and what it reveals about English.",
    "focus": "Code-switching, interference errors, and what multilingualism reveals about English structure",
    "explanation": "<p><strong>Code-switching</strong> is the natural alternation between languages in a multilingual speaker. It is sophisticated — not lazy or confused.</p><p><strong>Interference errors</strong> happen when an L1 pattern enters L2. They come from your strengths, not your weaknesses:</p><ul><li><strong>French → English:</strong> 'I have 25 years' (j'ai 25 ans → I am 25). Article omission ('Go to hospital' vs 'Go to the hospital')</li><li><strong>Bengali/Hindi → English:</strong> 'She is more tall' (no comparative morphology). 'Is it?' as universal question tag.</li><li><strong>All → English:</strong> Overuse of present continuous ('I am liking this' → stative verbs don't use continuous)</li></ul><p>Recognising your interference errors is the fastest path to eliminating them.</p>",
    "examples": [
      "'He is very intelligent, isn't it?' — Hindi/Bengali English: 'isn't it?' used as a universal tag (vs English: 'isn't he?')",
      "'I have 22 years' — French interference: 'j'ai 22 ans' → should be 'I am 22 years old'",
      "'She suggested me to go' — French/Italian interference: 'elle m'a suggéré d'aller' → should be 'She suggested (that) I go'",
    ],
    "questions": [
      ("Correct this: 'I am knowing the answer.' Why is it wrong?",
       "'I know the answer.' — 'Know' is a stative verb (state of mind/perception) and does not use continuous aspect.",
       "Other stative verbs: believe, understand, want, need, love, hate, see, hear. These describe states, not actions in progress."),
      ("What language likely caused this error: 'She asked me that I come early'?",
       "Likely French or Italian: 'elle m'a demandé que je vienne tôt' → English uses 'She asked me to come early.' (infinitive, not that-clause)",
       "Identifying your L1 as the source helps you target the specific rule to correct. It's efficient, not embarrassing."),
      ("Is code-switching a sign of poor language ability?",
       "No. Research consistently shows code-switching is cognitively sophisticated. It requires mastery of both systems simultaneously.",
       "Grosjean (1982) and many others have shown that bilinguals are not two monolinguals in one — they are a unique language system. Code-switching is evidence of competence, not confusion."),
    ],
    "takeaway": "Your interference errors come from your <strong>strengths</strong> — they prove you have a strong L1. <strong>Identify them, name their source, fix them.</strong> Multilingualism is not a limitation — it is a lens that shows you what English actually does.",
  },
]


def build_post(lesson):
    content = html(
        lesson["level"],
        lesson["anecdote"],
        lesson["focus"],
        lesson["explanation"],
        lesson["examples"],
        lesson["questions"],
        lesson["takeaway"],
    )
    return {
        "title": lesson["title"],
        "content": content,
        "status": "draft",
        "category": lesson["category"],
        "tags": lesson["tags"],
        "seo_title": lesson["seo_title"],
        "meta_description": lesson["meta_description"],
    }


def post_lesson(post, retries=1):
    for attempt in range(retries + 1):
        try:
            r = requests.post(WP_ENDPOINT, headers=HEADERS, json=post, timeout=30)
            return r.status_code, r.json()
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
            else:
                return 0, {"error": str(e)}


results = []
print(f"Posting {len(LESSONS)} lessons to WordPress...")
for i, lesson in enumerate(LESSONS, 1):
    post = build_post(lesson)
    code, resp = post_lesson(post)
    wp_id = resp.get("post_id") or resp.get("id") or "?"
    ok = code in (200, 201)
    status = "OK" if ok else "FAIL"
    results.append({"lesson": lesson["title"], "level": lesson["level"],
                    "wp_id": wp_id, "status": status, "code": code})
    print(f"[{i:02d}/{len(LESSONS)}] {status} (HTTP {code}, ID {wp_id}) — {lesson['title'][:60]}")
    if not ok:
        print(f"       Response: {str(resp)[:200]}")
    time.sleep(1.5)

with open("/tmp/lesson_results.json", "w") as f:
    json.dump(results, f, indent=2)

ok_count = sum(1 for r in results if r["status"] == "OK")
print(f"\nDone. {ok_count}/{len(results)} lessons posted successfully.")
print("Results saved to /tmp/lesson_results.json")
