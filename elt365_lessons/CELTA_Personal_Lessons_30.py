#!/usr/bin/env python3
"""30 CELTA Personal-Experience Lessons — posts to sourovdeb.com as drafts

Topics: Grammar (12) · Vocabulary (8) · Skills (7) · Special (3)
Level range: A1 – C1
All lessons: 5-minute bite-size, interactive HTML, Cambridge level badge,
personal anecdote from Sourov Deb's life, toggle answer key.

Usage:
  python3 CELTA_Personal_Lessons_30.py

The script will POST all 30 lessons as drafts and print WP IDs.
To re-run safely: the endpoint creates new drafts on each call — check
existing drafts in WP admin (IDs logged in LESSON_INDEX.md) to avoid posting
duplicates.

Compliance:
- No "certified/qualified/awarded" wording re: CELTA
- Disclaimer on every post footer
- status: "draft" — nothing auto-published
- No AI tool names/trademarks in content
"""
import json, time, urllib.request, urllib.error

EP  = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
KEY = "0767044896thevenet_"

def post_wp(d):
    req = urllib.request.Request(
        EP, json.dumps(d).encode(),
        {"X-Sourov-Key": KEY, "Content-Type": "application/json"}, "POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read())
            return r.status, body.get("id", "?")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:150]

CSS = (
    "<style>"
    ".lb{font-family:system-ui,sans-serif;max-width:660px;margin:0 auto;line-height:1.7}"
    ".b{display:inline-block;padding:2px 10px;border-radius:10px;font-size:.8rem;font-weight:700;color:#fff;margin-right:6px}"
    ".a1{background:#388E3C}.a2{background:#7CB342}.b1{background:#F57C00}.b2{background:#D32F2F}.c1{background:#7B1FA2}"
    ".t{background:#FFF9C4;border:1px solid #FBC02D;border-radius:6px;padding:3px 10px;font-size:.85rem;display:inline-block}"
    ".s{background:#EEF2FF;border-left:4px solid #4F46E5;padding:.8rem 1rem;margin:1rem 0;border-radius:0 6px 6px 0;font-style:italic}"
    ".a{background:#F0FDF4;border:1px solid #86EFAC;border-radius:6px;padding:.6rem 1rem;margin:.8rem 0}"
    ".e{background:#FFFBEB;border:1px solid #FDE68A;border-radius:6px;padding:.8rem 1rem;margin:.8rem 0}"
    ".p{background:#FAF5FF;border:1px solid #C084FC;border-radius:6px;padding:.8rem 1rem;margin:.8rem 0}"
    ".k{background:#F0F9FF;border:1px solid #7DD3FC;border-radius:6px;padding:.6rem 1rem;margin:.8rem 0}"
    "details summary{color:#4F46E5;font-weight:600;cursor:pointer;padding:.3rem 0}"
    "h1{color:#1E293B;font-size:1.4rem;margin:.4rem 0}h2{color:#374151;font-size:1.05rem;margin:1rem 0 .4rem}"
    "table{width:100%;border-collapse:collapse;margin:.6rem 0}"
    "th{background:#E0E7FF;padding:5px 8px;text-align:left}td{padding:5px 8px;border-bottom:1px solid #E5E7EB}"
    ".hi{background:#FEF08A;padding:1px 3px;border-radius:2px}"
    ".disc{font-size:.75rem;color:#9CA3AF;border-top:1px solid #E5E7EB;margin-top:1.5rem;padding-top:.5rem}"
    "</style>"
)

DISC = (
    '<p class="disc">Independent project. Not affiliated with, endorsed by, or '
    'accredited by Cambridge University Press &amp; Assessment. Confers no qualification.</p>'
)

def build_html(lv, ti, story, aim, ex, pr, ans, tip):
    lc = lv.lower().split("/")[0]
    return (
        CSS +
        f'<div class="lb">'
        f'<span class="b {lc}">{lv}</span><span class="t">&#9201; 5 min</span>'
        f'<h1>{ti}</h1>'
        f'<div class="s">&#128483; <strong>From my experience:</strong> {story}</div>'
        f'<div class="a">&#127919; <strong>Aim:</strong> By the end, you will be able to {aim}.</div>'
        f'<h2>&#128218; The Language</h2><div class="e">{ex}</div>'
        f'<h2>&#9998; Practice</h2><div class="p">{pr}'
        f'<details><summary>&#128064; Show answers</summary>{ans}</details></div>'
        f'<div class="k">&#128161; <strong>Takeaway:</strong> {tip}</div>'
        f'{DISC}</div>'
    )

# Tuple order: title, level, category, tags, meta_desc, seo_title,
#              story, aim, ex_html, prac_html, ans_html, tip
LESSONS = [

# ── GRAMMAR (12) ─────────────────────────────────────────────────────────────

("Where Are You From? Countries &amp; Nationalities", "A1",
 "English Teaching", "A1,beginner,nationalities,grammar,speaking",
 "A1 lesson: say where you're from using correct nationality adjectives. 5 minutes.",
 "Countries & Nationalities | A1 English Lesson",
 "I have answered 'Where are you from?' in four countries. In a Sydney restaurant a guest "
 "asked before I had spoken a word. Simple question, important answer.",
 "say where you're from and ask others with correct grammar",
 ("<p><strong>Form:</strong> I am from [country] &rarr; I am [nationality].</p>"
  "<table><tr><th>Country</th><th>Nationality</th></tr>"
  "<tr><td>France</td><td>French</td></tr>"
  "<tr><td>Australia</td><td>Australian</td></tr>"
  "<tr><td>Bangladesh</td><td>Bangladeshi</td></tr>"
  "<tr><td>Japan</td><td>Japanese</td></tr>"
  "<tr><td>Brazil</td><td>Brazilian / Portuguese</td></tr></table>"
  "<p>&#9888;&#65039; 'I am <del>France</del>' &rarr; 'I am <strong>French</strong>'</p>"),
 ("<ol><li>Marco is from Italy. He is ___.</li>"
  "<li>Yuki is from Japan. She is ___.</li>"
  "<li>'Where ___ you from?' &mdash; 'I ___ from Canada.'</li>"
  "<li>They are from Brazil. They speak ___.</li></ol>"),
 "<ol><li>Italian</li><li>Japanese</li><li>are / am</li><li>Portuguese</li></ol>",
 "Country &rarr; nationality ending (-an, -ese, -ish, -i). Exceptions exist &mdash; always worth checking."),

("Jobs &amp; Workplaces: What Do You Do?", "A1",
 "English Teaching", "A1,beginner,jobs,vocabulary,speaking",
 "A1 vocabulary lesson on jobs and workplaces. 5 minutes.",
 "Jobs & Workplaces | A1 English Vocabulary",
 "Before teaching, I was a sommelier and barista in Sydney's finest restaurants &mdash; "
 "The Ivy, Uccello, Establishment. When students ask what I did before, the conversation always gets interesting.",
 "name common jobs, say what you do, and use a/an correctly",
 ("<p><strong>Form:</strong> I am a/an [job]. I work in/at [place].</p>"
  "<table><tr><th>Job</th><th>Workplace</th></tr>"
  "<tr><td>teacher</td><td>school / college</td></tr>"
  "<tr><td>waiter / waitress</td><td>restaurant / caf&eacute;</td></tr>"
  "<tr><td>doctor</td><td>hospital / clinic</td></tr>"
  "<tr><td>chef</td><td>kitchen / restaurant</td></tr>"
  "<tr><td>barista</td><td>coffee shop</td></tr></table>"
  "<p><span class='hi'>I am <strong>a</strong> teacher.</span> (consonant sound &rarr; <em>a</em>)<br>"
  "<span class='hi'>I am <strong>an</strong> actor.</span> (vowel sound &rarr; <em>an</em>)</p>"),
 ("<p>Write <em>a</em> or <em>an</em>:</p>"
  "<ol><li>She is ___ engineer.</li><li>He is ___ nurse.</li>"
  "<li>I am ___ artist.</li></ol>"
  "<p>Match: chef &bull; hospital &bull; school &bull; caf&eacute;</p>"
  "<ol start='4'><li>A teacher works in a ___.</li><li>A doctor works in a ___.</li></ol>"),
 "<ol><li>an</li><li>a</li><li>an</li><li>school</li><li>hospital</li></ol>",
 "Use <em>a</em> before consonant sounds, <em>an</em> before vowel sounds. The rule follows the <strong>sound</strong>, not the spelling."),

("Daily Routines: Present Simple &amp; Adverbs of Frequency", "A2",
 "English Teaching", "A2,grammar,present simple,routine,adverbs",
 "A2 grammar: daily routines using present simple and adverbs of frequency. 5 minutes.",
 "Daily Routines & Adverbs of Frequency | A2 English",
 "Living in R&eacute;union with a baby daughter changed my routine completely. I always wake "
 "up early now &mdash; usually before sunrise. I never sleep past 6 a.m. anymore. Routine is underrated.",
 "describe daily routines using present simple and adverbs of frequency",
 ("<p><strong>Adverbs of frequency</strong> (0% &rarr; 100%):</p>"
  "<table><tr><th>Adverb</th><th>%</th><th>Example</th></tr>"
  "<tr><td>always</td><td>100%</td><td>I <span class='hi'>always</span> drink coffee.</td></tr>"
  "<tr><td>usually</td><td>~80%</td><td>She <span class='hi'>usually</span> walks.</td></tr>"
  "<tr><td>often</td><td>~60%</td><td>We <span class='hi'>often</span> cook at home.</td></tr>"
  "<tr><td>sometimes</td><td>~40%</td><td>He <span class='hi'>sometimes</span> forgets.</td></tr>"
  "<tr><td>rarely</td><td>~10%</td><td>I <span class='hi'>rarely</span> watch TV.</td></tr>"
  "<tr><td>never</td><td>0%</td><td>She <span class='hi'>never</span> eats meat.</td></tr></table>"
  "<p>&#128205; Position: BEFORE the main verb, AFTER <em>be</em>.</p>"),
 ("<p>Put the adverb in the right place:</p>"
  "<ol><li>I eat breakfast. (always)</li><li>She is late. (never)</li>"
  "<li>We go to the cinema. (sometimes)</li><li>He forgets his keys. (often)</li></ol>"),
 ("<ol><li>I <strong>always</strong> eat breakfast.</li>"
  "<li>She is <strong>never</strong> late.</li>"
  "<li>We <strong>sometimes</strong> go to the cinema.</li>"
  "<li>He <strong>often</strong> forgets his keys.</li></ol>"),
 "Adverbs of frequency go BEFORE the main verb but AFTER 'be'. One rule, almost every sentence."),

("Comparatives &amp; Superlatives: Bigger, Better, Best", "A2",
 "English Teaching", "A2,grammar,comparatives,superlatives,adjectives",
 "A2 grammar: comparatives and superlatives. Compare people, places, things. 5 minutes.",
 "Comparatives & Superlatives | A2 English Grammar",
 "I have lived in Chittagong, Sydney, Paris, and R&eacute;union. People ask: which is the "
 "most beautiful? The hottest? Comparing places is the best conversation starter I know.",
 "compare people and things using comparative and superlative adjectives",
 ("<p><strong>Short adjectives</strong>: add <em>-er / -est</em></p>"
  "<table><tr><th>Adjective</th><th>Comparative</th><th>Superlative</th></tr>"
  "<tr><td>hot</td><td>hotter</td><td>the hottest</td></tr>"
  "<tr><td>big</td><td>bigger</td><td>the biggest</td></tr></table>"
  "<p><strong>Long adjectives</strong>: use <em>more / the most</em></p>"
  "<table><tr><th>Adjective</th><th>Comparative</th><th>Superlative</th></tr>"
  "<tr><td>expensive</td><td>more expensive</td><td>the most expensive</td></tr>"
  "<tr><td>beautiful</td><td>more beautiful</td><td>the most beautiful</td></tr></table>"
  "<p><strong>Irregular:</strong> good &rarr; better &rarr; the best &bull; bad &rarr; worse &rarr; the worst</p>"),
 ("<ol><li>R&eacute;union is ___ (hot) than Paris.</li>"
  "<li>Sydney is one of ___ (expensive) cities in the world.</li>"
  "<li>My coffee is ___ (good) than yours!</li></ol>"),
 "<ol><li>hotter</li><li>the most expensive</li><li>better</li></ol>",
 "1 syllable &rarr; -er/-est. 2+ syllables &rarr; more/the most. Irregulars (good/better/best) must be memorised."),

("Going To vs Will: Talking About the Future", "A2",
 "English Teaching", "A2,grammar,future,will,going to",
 "A2 grammar: will vs going to for future plans and predictions. 5 minutes.",
 "Going To vs Will | A2 Future Grammar",
 "When I decided to move to R&eacute;union I told Vanessa: 'I am going to learn Creole.' "
 "Three years later I will tell you honestly: Creole is harder than French.",
 "choose between 'going to' and 'will' for plans and predictions",
 ("<table><tr><th></th><th>Going to</th><th>Will</th></tr>"
  "<tr><td><strong>Use for</strong></td><td>Plans already decided</td><td>Decisions made now / predictions / offers</td></tr>"
  "<tr><td><strong>Example</strong></td>"
  "<td>I <span class='hi'>am going to</span> study tonight.</td>"
  "<td>I <span class='hi'>will</span> help you. (decided just now)</td></tr></table>"
  "<p>Evidence visible now &rarr; <em>going to</em>: 'Look at those clouds &mdash; it "
  "<span class='hi'>is going to</span> rain.'<br>"
  "No evidence, opinion &rarr; <em>will</em>: 'I think it <span class='hi'>will</span> rain tomorrow.'</p>"),
 ("<ol><li>'The phone is ringing!' 'I ___ answer it.' (decide now)</li>"
  "<li>She has her ticket. She ___ fly to Paris next week. (plan)</li>"
  "<li>Those clouds are dark. It ___ rain. (evidence)</li>"
  "<li>I think English ___ be useful for your career.</li></ol>"),
 "<ol><li>will answer</li><li>is going to fly</li><li>is going to rain</li><li>will be</li></ol>",
 "'Going to' = the decision was made before this moment. 'Will' = decided just now, or an opinion about the future."),

("Prepositions of Place &amp; Movement: In, On, At, To, From", "A2",
 "English Teaching", "A2,grammar,prepositions,place,movement",
 "A2 grammar: prepositions of place and movement. In, on, at, to, from. 5 minutes.",
 "Prepositions of Place & Movement | A2 English",
 "French speakers in R&eacute;union say 'I go <em>at</em> the market' instead of <em>to</em>. "
 "I made the same mistake in French for months after arriving in Paris.",
 "use prepositions of place and movement correctly in common sentences",
 ("<table><tr><th>Preposition</th><th>Use</th><th>Example</th></tr>"
  "<tr><td><strong>in</strong></td><td>enclosed space / city / country</td><td>I live <span class='hi'>in</span> R&eacute;union.</td></tr>"
  "<tr><td><strong>on</strong></td><td>surface / transport</td><td>The book is <span class='hi'>on</span> the table.</td></tr>"
  "<tr><td><strong>at</strong></td><td>specific point / address / event</td><td>Meet me <span class='hi'>at</span> the caf&eacute;.</td></tr>"
  "<tr><td><strong>to</strong></td><td>direction / destination</td><td>I go <span class='hi'>to</span> school.</td></tr>"
  "<tr><td><strong>from</strong></td><td>origin</td><td>I am <span class='hi'>from</span> Bangladesh.</td></tr></table>"),
 ("<ol><li>She lives ___ a small house ___ Paris.</li>"
  "<li>The keys are ___ the table.</li>"
  "<li>We are going ___ the beach tomorrow.</li>"
  "<li>He arrived ___ the airport two hours ago.</li></ol>"),
 "<ol><li>in / in</li><li>on</li><li>to</li><li>at</li></ol>",
 "In = inside/enclosed. On = surface. At = a specific point. To = movement towards. From = origin."),

("Have You Ever...? Present Perfect for Experience", "B1",
 "English Teaching", "B1,grammar,present perfect,experience,have you ever",
 "B1 grammar: present perfect for life experiences. 'Have you ever...?' 5 minutes.",
 "Have You Ever? Present Perfect for Experience | B1",
 "Have you ever lived in four countries? I have. Have you ever started over in a new "
 "language at 30? I have. The present perfect for experience is the tense of a life fully lived.",
 "ask and answer questions about life experiences using the present perfect",
 ("<p><strong>Form:</strong> have/has + past participle</p>"
  "<p>&#10067; <span class='hi'>Have you ever</span> lived abroad?<br>"
  "&#10004; <span class='hi'>Yes, I have.</span> I have lived in four countries.<br>"
  "&#10060; <span class='hi'>No, I haven't.</span> I have never tried it.</p>"
  "<table><tr><th>Verb</th><th>Past Participle</th></tr>"
  "<tr><td>live</td><td>lived</td></tr>"
  "<tr><td>eat</td><td>eaten</td></tr>"
  "<tr><td>see</td><td>seen</td></tr>"
  "<tr><td>go</td><td>gone / been</td></tr>"
  "<tr><td>learn</td><td>learned / learnt</td></tr></table>"
  "<p>&#9888;&#65039; 'Have you ever <strong>been</strong> to Australia?' "
  "(not <em>gone</em> &mdash; you are back now)</p>"),
 ("<ol><li>___ you ever ___ (eat) kangaroo?</li>"
  "<li>She ___ never ___ (visit) R&eacute;union.</li>"
  "<li>We ___ already ___ (see) that film.</li>"
  "<li>Write one true sentence: I have never ___.</li></ol>"),
 "<ol><li>Have / eaten</li><li>has / visited</li><li>have / seen</li><li>(open answer)</li></ol>",
 "No specific time = present perfect. Add a time? Switch to past simple: 'I <strong>went</strong> to Sydney <strong>in 2005</strong>.'"),

("Past Simple vs Past Continuous: Telling a Story", "B1",
 "English Teaching", "B1,grammar,past simple,past continuous,storytelling",
 "B1 grammar: past simple vs past continuous for narrating events. 5 minutes.",
 "Past Simple vs Past Continuous | B1 English Grammar",
 "My first shift at The Ivy in Sydney &mdash; 2009. I was carrying a tray of Champagne glasses "
 "when the General Manager walked in. He was watching. Past continuous sets the scene; past simple delivers the action.",
 "use past simple and past continuous together to tell a story",
 ("<table><tr><th></th><th>Past Simple</th><th>Past Continuous</th></tr>"
  "<tr><td><strong>Use</strong></td><td>Completed action; the event itself</td><td>Background scene; longer action in progress</td></tr>"
  "<tr><td><strong>Form</strong></td><td>verb + -ed / irregular</td><td>was/were + verb + -ing</td></tr>"
  "<tr><td><strong>Example</strong></td><td>She <span class='hi'>walked</span> in.</td><td>I <span class='hi'>was carrying</span> a tray.</td></tr></table>"
  "<p><strong>Classic pattern:</strong><br>"
  "While I <span class='hi'>was working</span> (continuous, background), "
  "the phone <span class='hi'>rang</span> (simple, event).</p>"),
 ("<p>Complete with the correct form:</p>"
  "<p>Last Saturday, I ___(sit) in a caf&eacute; when I ___(see) an old friend. "
  "She ___(walk) quickly but I ___(call) her name. She ___(stop) and ___(turn) around. "
  "We ___(talk) for an hour while it ___(rain) outside.</p>"),
 "<p>was sitting / saw / was walking / called / stopped / turned / talked / was raining</p>",
 "Past continuous = the stage (longer background). Past simple = the drama (short, completed event). 'While' and 'when' are your cue words."),

("Phrasal Verbs: Life Changes", "B1",
 "English Teaching", "B1,vocabulary,phrasal verbs,life,changes",
 "B1 vocabulary: phrasal verbs for life changes — give up, move on, settle down. 5 minutes.",
 "Phrasal Verbs for Life Changes | B1 English",
 "I gave up hospitality to retrain as a teacher. I moved on from Sydney after a decade. "
 "I am still settling down in R&eacute;union. Three phrasal verbs for fifteen years of my life.",
 "use common phrasal verbs for life changes in context",
 ("<table><tr><th>Phrasal Verb</th><th>Meaning</th><th>Example</th></tr>"
  "<tr><td><strong>give up</strong></td><td>stop doing something</td><td>I <span class='hi'>gave up</span> working nights.</td></tr>"
  "<tr><td><strong>move on</strong></td><td>leave a situation / stop thinking about the past</td><td>It's time to <span class='hi'>move on</span>.</td></tr>"
  "<tr><td><strong>settle down</strong></td><td>start a stable life</td><td>We finally <span class='hi'>settled down</span> in R&eacute;union.</td></tr>"
  "<tr><td><strong>start over</strong></td><td>begin again from scratch</td><td>After the move, I had to <span class='hi'>start over</span>.</td></tr>"
  "<tr><td><strong>take up</strong></td><td>begin a new hobby or activity</td><td>She <span class='hi'>took up</span> photography.</td></tr>"
  "<tr><td><strong>turn down</strong></td><td>refuse an offer</td><td>He <span class='hi'>turned down</span> the job.</td></tr></table>"),
 ("<ol><li>After the change, she decided to ___ and move to a new city.</li>"
  "<li>He ___ smoking last year. He feels much better now.</li>"
  "<li>They ___ in a small village in the south of France.</li>"
  "<li>She was offered a promotion but she ___ it ___.</li></ol>"),
 "<ol><li>start over</li><li>gave up</li><li>settled down</li><li>turned / down</li></ol>",
 "Phrasal verbs can't be translated word-for-word. Learn them as fixed chunks with an example sentence."),

("MAKE or DO? High-Frequency Collocations", "B1",
 "English Teaching", "B1,vocabulary,collocations,make,do,common mistakes",
 "B1 vocabulary: when to use MAKE vs DO. Learn the most common collocations. 5 minutes.",
 "Make or Do? | B1 English Vocabulary",
 "My students in R&eacute;union say 'I will do an effort' and 'I need to make my homework.' "
 "Both are direct translations from French (<em>faire</em> = both make and do). "
 "This is the lesson I teach most often.",
 "use MAKE and DO correctly with the most common collocations",
 ("<p><strong>MAKE</strong> &rarr; creation, production, something new:</p>"
  "<ul><li>make a <span class='hi'>decision</span> &bull; mistake &bull; plan &bull; effort &bull; noise &bull; money &bull; friends &bull; a phone call</li></ul>"
  "<p><strong>DO</strong> &rarr; tasks, duties, general activities:</p>"
  "<ul><li>do <span class='hi'>homework</span> &bull; research &bull; exercise &bull; business &bull; a favour &bull; your best &bull; sport</li></ul>"
  "<p>Quick test: can you touch or produce the result? Often MAKE. Is it a general task or duty? Often DO.</p>"),
 ("<ol><li>I need to ___ my homework before dinner.</li>"
  "<li>She ___ a difficult decision last week.</li>"
  "<li>Can you ___ me a favour?</li>"
  "<li>Stop ___ so much noise!</li>"
  "<li>He ___ a lot of research for his project.</li></ol>"),
 "<ol><li>do</li><li>made</li><li>do</li><li>making</li><li>did</li></ol>",
 "MAKE = create or produce. DO = carry out a task. When unsure, check against the fixed-list approach &mdash; learn the chunks, not just the rule."),

("Second Conditional: What Would You Do If...?", "B2",
 "English Teaching", "B2,grammar,second conditional,hypothetical,speaking",
 "B2 grammar: second conditional for hypothetical situations. 5 minutes.",
 "Second Conditional | B2 English Grammar",
 "If I hadn't left Bangladesh in 2005, I would never have become an English teacher. "
 "The second conditional is the grammar of 'what if' &mdash; one of the most human things in language.",
 "form and use the second conditional for imaginary or hypothetical situations",
 ("<p><strong>Form:</strong> If + past simple, would + infinitive</p>"
  "<table><tr><th>Clause</th><th>Form</th><th>Example</th></tr>"
  "<tr><td>If-clause (condition)</td><td>if + past simple</td><td>If I <span class='hi'>lived</span> in Paris...</td></tr>"
  "<tr><td>Main clause (result)</td><td>would + infinitive</td><td>...I <span class='hi'>would visit</span> the Louvre.</td></tr></table>"
  "<p>&#9888;&#65039; Use <span class='hi'>were</span> (not <em>was</em>) with I/he/she in formal writing: "
  "'If I <strong>were</strong> you, I would apply.'</p>"
  "<p><strong>Meaning:</strong> The situation is NOT real now. Imaginary or unlikely.<br>"
  "Compare: 'If it <span class='hi'>rains</span>, I <span class='hi'>will</span> stay home.' (1st cond: possible)<br>"
  "'If it <span class='hi'>rained</span> every day, I <span class='hi'>would</span> move.' (2nd: unlikely)</p>"),
 ("<ol><li>If I ___ (have) more time, I ___ (learn) the guitar.</li>"
  "<li>What ___ you ___ (do) if you ___ (lose) your passport abroad?</li>"
  "<li>Write your own: If I _____, I would _____.</li></ol>"),
 "<ol><li>had / would learn</li><li>would you do / lost</li><li>(open)</li></ol>",
 "Second conditional = imaginary present or future. If + past simple; result + would. It's the grammar of dreams, polite advice, and alternative lives."),

("Inversion for Emphasis: Never Had I Imagined...", "C1",
 "English Teaching", "C1,grammar,inversion,emphasis,advanced,Cambridge",
 "C1 advanced grammar: inversion with negative adverbials for emphasis. 5 minutes.",
 "Inversion for Emphasis | C1 Advanced English Grammar",
 "Never had I imagined I would end up teaching English on an island in the Indian Ocean. "
 "Rarely do things turn out as planned. Seldom does a career follow the path you drew at twenty. "
 "Inversion sounds dramatic &mdash; because it is.",
 "form and use inversion with negative adverbials for formal emphasis",
 ("<p><strong>Form:</strong> Negative adverbial + auxiliary + subject + main verb</p>"
  "<table><tr><th>Normal order</th><th>Inverted (emphatic)</th></tr>"
  "<tr><td>I had <em>never</em> seen anything like it.</td><td><span class='hi'>Never had I</span> seen anything like it.</td></tr>"
  "<tr><td>He <em>rarely</em> makes mistakes.</td><td><span class='hi'>Rarely does he</span> make mistakes.</td></tr>"
  "<tr><td>We <em>only then</em> understood.</td><td><span class='hi'>Only then did we</span> understand.</td></tr>"
  "<tr><td>She had <em>hardly</em> sat down when...</td><td><span class='hi'>Hardly had she</span> sat down when...</td></tr></table>"
  "<p><strong>Common triggers:</strong> never, rarely, seldom, hardly, barely, scarcely, not only, only then, under no circumstances</p>"),
 ("<ol><li>I have rarely felt so proud.</li>"
  "<li>She had barely arrived when the meeting started.</li>"
  "<li>Under no circumstances you should leave early. (find the error)</li>"
  "<li>Not only I passed the exam but also won a scholarship. (find the error)</li></ol>"),
 ("<ol><li>Rarely have I felt so proud.</li>"
  "<li>Hardly had she arrived when the meeting started.</li>"
  "<li>Under no circumstances <strong>should you</strong> leave early. (auxiliary before subject)</li>"
  "<li>Not only <strong>did I</strong> pass the exam but I also won a scholarship.</li></ol>"),
 "Inversion = auxiliary before subject. Formal register. One well-placed inversion in an essay or speech is powerful; overuse becomes parody."),

# ── VOCABULARY (8) ───────────────────────────────────────────────────────────

("Food &amp; Flavours: Vocabulary for Taste", "A2",
 "English Teaching", "A2,vocabulary,food,taste,adjectives,culture",
 "A2 vocabulary: taste and food adjectives. Bengali spices to French cuisine to Réunion Creole. 5 minutes.",
 "Food & Flavours Vocabulary | A2 English",
 "I grew up eating <em>hilsa</em> curry in Chittagong, learned to appreciate Burgundy at The Ivy in Sydney, "
 "and now cook for my daughter in R&eacute;union where <em>rougail saucisses</em> is Sunday lunch. "
 "Food teaches language faster than almost anything.",
 "describe food using precise taste and texture adjectives",
 ("<table><tr><th>Adjective</th><th>Meaning</th><th>Example food</th></tr>"
  "<tr><td>sweet</td><td>sugar flavour</td><td>mango, chocolate</td></tr>"
  "<tr><td>sour</td><td>acid, like lemon</td><td>lemon, yoghurt</td></tr>"
  "<tr><td>bitter</td><td>sharp, not sweet</td><td>coffee, dark chocolate</td></tr>"
  "<tr><td>spicy / hot</td><td>chilli heat</td><td>curry, chilli sauce</td></tr>"
  "<tr><td>salty</td><td>salt flavour</td><td>crisps, soy sauce</td></tr>"
  "<tr><td>creamy</td><td>smooth, rich</td><td>butter, cream sauce</td></tr>"
  "<tr><td>crispy / crunchy</td><td>hard, makes a sound</td><td>toast, apple</td></tr>"
  "<tr><td>tender</td><td>soft and easy to eat</td><td>slow-cooked meat</td></tr></table>"),
 ("<p>Choose the best adjective:</p>"
  "<ol><li>This coffee is very ___ &mdash; can I add some sugar?</li>"
  "<li>The fried chicken was golden and ___.</li>"
  "<li>He likes his food ___ &mdash; he puts chilli on everything.</li>"
  "<li>The soup is rich and ___ &mdash; must be a lot of butter in it.</li></ol>"),
 "<ol><li>bitter</li><li>crispy / crunchy</li><li>spicy / hot</li><li>creamy</li></ol>",
 "Precise food vocabulary makes you sound fluent. Learn adjective + food pairs as chunks: <em>tender lamb, crispy skin, bitter espresso</em>."),

("Emotions &amp; Feelings: Beyond Happy and Sad", "B1",
 "English Teaching", "B1,vocabulary,emotions,feelings,precise language",
 "B1 vocabulary: a range of emotions beyond basic words. 5 minutes.",
 "Feelings & Emotions | B1 English Vocabulary",
 "When my father died in 2023, I was in R&eacute;union. I felt grief, guilt, and relief all at once. "
 "'Sad' was not enough. English has words for all of these &mdash; learning them helps you process what you feel.",
 "use precise vocabulary to describe a range of emotions",
 ("<table><tr><th>Emotion</th><th>When to use</th></tr>"
  "<tr><td><strong>anxious</strong></td><td>worried about the future; nervous</td></tr>"
  "<tr><td><strong>overwhelmed</strong></td><td>too much to handle at once</td></tr>"
  "<tr><td><strong>relieved</strong></td><td>glad a worry is over</td></tr>"
  "<tr><td><strong>frustrated</strong></td><td>annoyed because something won't work</td></tr>"
  "<tr><td><strong>content</strong></td><td>quietly happy; satisfied</td></tr>"
  "<tr><td><strong>homesick</strong></td><td>missing home while away</td></tr>"
  "<tr><td><strong>proud</strong></td><td>satisfied with an achievement</td></tr>"
  "<tr><td><strong>ashamed</strong></td><td>embarrassed by a past action</td></tr></table>"
  "<p>&#128205; Form: I feel / I am / I am feeling + adjective</p>"),
 ("<p>Match the sentence to the emotion:</p>"
  "<ol><li>'I have ten deadlines and it's already 9 pm.' &rarr; ___</li>"
  "<li>'The exam is over. I passed.' &rarr; ___</li>"
  "<li>'I miss my family back home.' &rarr; ___</li>"
  "<li>'My daughter took her first steps today.' &rarr; ___</li></ol>"),
 "<ol><li>overwhelmed</li><li>relieved</li><li>homesick</li><li>proud</li></ol>",
 "Precise emotion words do two things: help others understand you, and help you understand yourself."),

("Collocations with MAKE and DO", "B1",
 "English Teaching", "B1,vocabulary,collocations,make,do",
 "B1 vocabulary: MAKE and DO collocations with clear rules and practice. 5 minutes.",
 "Collocations: MAKE and DO | B1 English Vocabulary",
 "My R&eacute;union students say 'I will do an effort' because <em>faire un effort</em> is the French. "
 "My Sydney colleagues said 'make a decision' without thinking. Languages carve the world differently.",
 "use MAKE and DO with their most common collocations accurately",
 ("<p><strong>MAKE collocations:</strong><br>"
  "make a <span class='hi'>mistake</span> &bull; make a <span class='hi'>decision</span> &bull; "
  "make <span class='hi'>money</span> &bull; make an <span class='hi'>effort</span> &bull; "
  "make <span class='hi'>friends</span> &bull; make a <span class='hi'>suggestion</span></p>"
  "<p><strong>DO collocations:</strong><br>"
  "do your <span class='hi'>best</span> &bull; do <span class='hi'>research</span> &bull; "
  "do <span class='hi'>exercise</span> &bull; do someone a <span class='hi'>favour</span> &bull; "
  "do <span class='hi'>business</span> &bull; do the <span class='hi'>washing-up</span></p>"
  "<p>&#128161; Memory hook: MAKE = create something new. DO = carry out an activity.</p>"),
 ("<ol><li>I always ___ a list before I go shopping.</li>"
  "<li>Could you ___ me a favour and pick up the kids?</li>"
  "<li>She ___ a brilliant suggestion in the meeting.</li>"
  "<li>He ___ a lot of exercise &mdash; he runs every morning.</li></ol>"),
 "<ol><li>make</li><li>do</li><li>made</li><li>does</li></ol>",
 "Don't try to derive the rule every time &mdash; memorise the 10 most common collocations for each and you'll cover 90% of use."),

("Wine &amp; Fine Dining Vocabulary", "B2",
 "English Teaching", "B2,vocabulary,hospitality,wine,food,professional",
 "B2 vocabulary: wine and fine dining terminology from a trained sommelier. 5 minutes.",
 "Wine & Fine Dining Vocabulary | B2 English",
 "I worked as a sommelier at The Ivy and other Merivale venues in Sydney. Every evening I "
 "described wines to guests in precise English. Vocabulary without confidence is useless. "
 "These are the words I used every week.",
 "use key wine and fine dining vocabulary accurately in a hospitality context",
 ("<p><strong>Tasting notes vocabulary:</strong></p>"
  "<table><tr><th>Category</th><th>Words</th></tr>"
  "<tr><td>Body</td><td>full-bodied, medium-bodied, light</td></tr>"
  "<tr><td>Finish</td><td>long finish, short finish, lingering, crisp, clean</td></tr>"
  "<tr><td>Tannins</td><td>grippy, silky, soft, astringent</td></tr>"
  "<tr><td>Acidity</td><td>high acidity, bright, tart, fresh</td></tr>"
  "<tr><td>Aroma</td><td>floral, earthy, fruity, oaky, mineral</td></tr></table>"
  "<p><strong>Service phrases:</strong></p>"
  "<ul><li>'May I suggest the Chablis with your seafood?'</li>"
  "<li>'This is a full-bodied red with notes of dark fruit and a long finish.'</li>"
  "<li>'Would you like to taste the wine before I pour?'</li></ul>"),
 ("<p>Complete the wine description:</p>"
  "<p>'This Burgundy is ___ (weight), with ___ (texture of tannins) tannins and a ___ "
  "(length) finish. On the nose, you'll find ___ (type of aroma) notes.'</p>"),
 "<p>Sample: This Burgundy is full-bodied, with silky tannins and a long finish. On the nose, you'll find earthy notes with hints of dark cherry and leather.</p>",
 "Tasting notes are sensory and precise. Practice by describing what you eat and drink &mdash; the vocabulary transfers to any food context."),

("Academic Word List: 10 Essential Words for B2+", "B2",
 "English Teaching", "B2,vocabulary,academic,IELTS,Cambridge,AWL",
 "B2 vocabulary: 10 Academic Word List words for Cambridge exams and IELTS. 5 minutes.",
 "Academic Word List: 10 Essential Words | B2/C1 English",
 "I read Dostoevsky in English not because my English was perfect, but because the "
 "challenge taught me something. Academic vocabulary comes from exposure to complex texts. "
 "These 10 words appear in Cambridge exams constantly.",
 "use 10 high-frequency academic words correctly in context",
 ("<table><tr><th>Word</th><th>POS</th><th>Meaning</th><th>Example</th></tr>"
  "<tr><td><strong>analyse</strong></td><td>v</td><td>examine in detail</td><td>We need to <span class='hi'>analyse</span> the data.</td></tr>"
  "<tr><td><strong>significant</strong></td><td>adj</td><td>important; large enough to notice</td><td>A <span class='hi'>significant</span> increase.</td></tr>"
  "<tr><td><strong>evident</strong></td><td>adj</td><td>clearly seen</td><td>It is <span class='hi'>evident</span> that...</td></tr>"
  "<tr><td><strong>consequently</strong></td><td>adv</td><td>as a result</td><td>He was late; <span class='hi'>consequently</span>, he missed the start.</td></tr>"
  "<tr><td><strong>approach</strong></td><td>n/v</td><td>method / to move towards</td><td>A new <span class='hi'>approach</span> to teaching.</td></tr>"
  "<tr><td><strong>maintain</strong></td><td>v</td><td>keep; state as true</td><td>She <span class='hi'>maintains</span> she is right.</td></tr>"
  "<tr><td><strong>establish</strong></td><td>v</td><td>set up / confirm</td><td>They <span class='hi'>established</span> a new system.</td></tr>"
  "<tr><td><strong>vary</strong></td><td>v</td><td>differ / change</td><td>Results <span class='hi'>vary</span> between groups.</td></tr>"
  "<tr><td><strong>context</strong></td><td>n</td><td>surrounding circumstances</td><td>This is important in <span class='hi'>context</span>.</td></tr>"
  "<tr><td><strong>assess</strong></td><td>v</td><td>evaluate / judge quality</td><td>Teachers <span class='hi'>assess</span> progress.</td></tr></table>"),
 ("<ol><li>The results ___ significantly between the two groups.</li>"
  "<li>It is ___ that further research is needed.</li>"
  "<li>The government ___ a new policy last year.</li>"
  "<li>We must ___ the impact before deciding.</li></ol>"),
 "<ol><li>varied</li><li>evident</li><li>established</li><li>assess</li></ol>",
 "Academic words carry precise meaning. Learn them with their collocations, not in isolation."),

("Idiomatic English: Everyday Expressions", "B1",
 "English Teaching", "B1,vocabulary,idioms,everyday,expressions",
 "B1 vocabulary: 8 common English idioms with meaning and examples. 5 minutes.",
 "Everyday English Idioms | B1 Vocabulary",
 "When I arrived in Sydney in 2005, a colleague said 'it's raining cats and dogs' and I looked "
 "outside expecting something extraordinary. I had perfect textbook English but zero idiom knowledge.",
 "understand and use 8 common English idioms in context",
 ("<table><tr><th>Idiom</th><th>Meaning</th></tr>"
  "<tr><td>raining cats and dogs</td><td>raining very heavily</td></tr>"
  "<tr><td>under the weather</td><td>feeling slightly ill</td></tr>"
  "<tr><td>hit the nail on the head</td><td>say exactly the right thing</td></tr>"
  "<tr><td>bite off more than you can chew</td><td>take on too much responsibility</td></tr>"
  "<tr><td>the ball is in your court</td><td>it's your turn to decide</td></tr>"
  "<tr><td>cost an arm and a leg</td><td>be very expensive</td></tr>"
  "<tr><td>get cold feet</td><td>become nervous about a plan</td></tr>"
  "<tr><td>once in a blue moon</td><td>very rarely</td></tr></table>"),
 ("<ol><li>I offered Tuesday or Thursday. Now ___ to decide.</li>"
  "<li>Don't ___ &mdash; you already have three jobs!</li>"
  "<li>That new car ___ &mdash; it was over 50,000 euros.</li>"
  "<li>I ___ about moving abroad. What if it didn't work out?</li></ol>"),
 "<ol><li>the ball is in your court</li><li>bite off more than you can chew</li><li>cost an arm and a leg</li><li>got cold feet</li></ol>",
 "Learn idioms in context, not lists. Notice them in films and conversation &mdash; then try using one per week."),

("Vocabulary Strategy: Learning Words in Chunks", "B1",
 "English Teaching", "B1,vocabulary,strategy,collocations,word learning",
 "B1 vocabulary strategy: learning words in chunks is more effective than single words. 5 minutes.",
 "Learning Vocabulary in Chunks | B1 English Strategy",
 "When I learned French to C1 level as an adult, the breakthrough came when I stopped "
 "memorising single words and started learning phrases. Not just <em>prendre</em> (to take) "
 "but <em>prendre une d&eacute;cision</em>, <em>prendre le temps</em>. The same works in English.",
 "use a chunk-based vocabulary strategy to learn and remember words more effectively",
 ("<p><strong>What is a chunk?</strong> A group of words that naturally go together.</p>"
  "<p>Instead of learning the single word: <span class='hi'>make</span><br>"
  "Learn: make <strong>a decision</strong> / make <strong>an effort</strong> / "
  "make <strong>a mistake</strong> / make <strong>progress</strong></p>"
  "<p><strong>Why chunks work:</strong></p>"
  "<ul><li>Faster to retrieve in conversation</li>"
  "<li>Sound more natural immediately</li>"
  "<li>Reduce grammar errors (the collocation is pre-built)</li></ul>"
  "<p><strong>How to learn chunks:</strong></p>"
  "<ol><li>When you see a new word, note 2&ndash;3 words that always come with it</li>"
  "<li>Write an example sentence using the chunk</li>"
  "<li>Review the chunk, not the word alone</li></ol>"),
 ("<p>Complete with the correct word to make a natural chunk:</p>"
  "<ol><li>take ___ (for health purposes)</li>"
  "<li>do ___ (a physical activity for health)</li>"
  "<li>pay ___ (what you give someone in a shop)</li>"
  "<li>make ___ (help two people stop arguing)</li></ol>"),
 "<ol><li>take medicine / take a pill / take a break</li><li>do exercise / do sport</li><li>pay attention / pay a bill</li><li>make a compromise / make peace</li></ol>",
 "Don't learn words. Learn words in their natural company. A chunk is a unit of meaning, not just a vocabulary item."),

# ── SKILLS (7) ───────────────────────────────────────────────────────────────

("Reading for Gist: Don&rsquo;t Read Every Word", "B1",
 "English Teaching", "B1,reading,skills,gist,skimming,Cambridge",
 "B1 reading skills: skimming for gist. How to get the main idea quickly. 5 minutes.",
 "Reading for Gist — Skimming Technique | B1 English",
 "When I moved to France, I had to read official documents every day in French. "
 "My strategy: title, first sentence of each paragraph, last sentence. In five minutes I had the gist. "
 "It works in any language.",
 "skim a text to get the main idea without reading every word",
 ("<p><strong>Gist reading (skimming)</strong> = reading <em>quickly</em> to understand "
  "<em>what</em> a text is about &mdash; not the details.</p>"
  "<p><strong>3-step strategy:</strong></p>"
  "<ol><li>Read the <span class='hi'>title / headline</span></li>"
  "<li>Read the <span class='hi'>first sentence of each paragraph</span></li>"
  "<li>Read the <span class='hi'>last sentence</span> of the text</li></ol>"
  "<p>This gives you the main idea in under 60 seconds.</p>"
  "<p><strong>When to skim:</strong> news articles, emails, academic texts, exam reading tasks.</p>"),
 ("<p>Read this text quickly (30 seconds only). Then answer <em>without</em> re-reading:</p>"
  "<blockquote><em>Language learning has changed dramatically over the last decade. Apps, "
  "podcasts, and online tutors have replaced traditional textbooks for millions of learners. "
  "However, research suggests that structured study still produces faster results than passive "
  "exposure alone. The most effective learners combine both approaches.</em></blockquote>"
  "<p>1. What is the main idea?<br>2. What does research suggest?</p>"),
 "<p>1. Language learning has changed, but structured study is still important.<br>"
  "2. Structured study produces faster results than passive exposure alone.</p>",
 "Skim first, read deeply only if needed. In exams and real life, this saves time and reduces anxiety."),

("Writing a Personal Narrative: Your Story in 5 Moments", "B1",
 "English Teaching", "B1,writing,narrative,personal,skills,IELTS",
 "B1 writing: how to write a personal narrative using a 5-moment structure. 5 minutes.",
 "How to Write a Personal Narrative | B1 English Writing",
 "My own story spans Chittagong, Sydney, Paris, and R&eacute;union. When I first tried to "
 "write it in English, I didn't know where to start. Five key moments &mdash; that was the frame that unlocked it.",
 "plan and write a personal narrative using a 5-moment structure",
 ("<p><strong>Structure:</strong></p>"
  "<ol><li><span class='hi'>Hook</span> &mdash; Start with a vivid moment, not 'I was born in...'</li>"
  "<li><span class='hi'>Background</span> &mdash; One sentence of context (who, where, when)</li>"
  "<li><span class='hi'>Turning point</span> &mdash; The key event that changed things</li>"
  "<li><span class='hi'>Result</span> &mdash; What happened / changed</li>"
  "<li><span class='hi'>Reflection</span> &mdash; What you learned or how you feel now</li></ol>"
  "<p><strong>Useful language:</strong></p>"
  "<ul><li>Looking back, ... &bull; At the time, I had no idea that...</li>"
  "<li>It was only later that... &bull; That moment changed the way I...</li></ul>"),
 ("<p>Plan a 5-moment narrative about <em>a change in your life</em>. Write one sentence per moment:</p>"
  "<ol><li>Hook</li><li>Background</li><li>Turning point</li><li>Result</li><li>Reflection</li></ol>"),
 "<p>(Open answer &mdash; share with a partner or teacher for feedback.)</p>",
 "Start in the middle of the action. The hook creates curiosity; the reflection gives meaning."),

("Speaking: How to Tell an Anecdote Fluently", "B2",
 "English Teaching", "B2,speaking,anecdote,fluency,storytelling,Cambridge",
 "B2 speaking skills: tell a personal anecdote using a clear 4-part structure. 5 minutes.",
 "How to Tell an Anecdote | B2 English Speaking",
 "I have told the story of arriving in Sydney &mdash; alone, English barely functional, "
 "sitting outside the airport for three hours &mdash; dozens of times. Each time I tell it differently. "
 "This lesson gives you the structure to tell your story well, every time.",
 "tell a personal anecdote fluently using a clear spoken structure",
 ("<p><strong>4-part anecdote structure:</strong></p>"
  "<table><tr><th>Part</th><th>Function</th><th>Useful phrases</th></tr>"
  "<tr><td><strong>1. Set the scene</strong></td><td>Past context</td><td>'It was 2005... I was sitting outside the airport...'</td></tr>"
  "<tr><td><strong>2. The event</strong></td><td>What happened</td><td>'Then suddenly... At that moment...'</td></tr>"
  "<tr><td><strong>3. Your reaction</strong></td><td>How you felt</td><td>'I couldn't believe it... I had no idea what to do...'</td></tr>"
  "<tr><td><strong>4. The point</strong></td><td>Why you're telling it</td><td>'The funny thing is... That taught me...'</td></tr></table>"
  "<p>&#128205; Use <strong>dramatic present</strong> to make it lively: "
  "'So I am standing there, and suddenly...'</p>"),
 ("<p>Prepare a 1-minute anecdote about <em>a moment when something went wrong</em>. "
  "Plan all 4 parts, then tell it without reading. Aim for fluency, not perfection.</p>"),
 "<p>(Open answer &mdash; record yourself to listen back.)</p>",
 "Structure gives confidence. Know your 4 parts, then forget the script and just talk."),

("Pronunciation: Silent Letters in English", "A2",
 "English Teaching", "A2,pronunciation,silent letters,phonics,spoken English",
 "A2 pronunciation: silent letters in English. 5 minutes.",
 "Silent Letters in English | A2 Pronunciation",
 "A colleague corrected me in Sydney: 'It's not <em>k-nee</em>, it's <em>nee</em>.' "
 "I had been pronouncing the K in 'knee' for a year. Silent letters are one of the first shocks "
 "of English pronunciation for speakers of phonetic languages like French or Bengali.",
 "identify and correctly pronounce words with silent letters",
 ("<table><tr><th>Silent letter</th><th>Words</th></tr>"
  "<tr><td><strong>silent K</strong></td><td>knife /naɪf/ &bull; know /noʊ/ &bull; knee /niː/ &bull; knock /nɒk/</td></tr>"
  "<tr><td><strong>silent W</strong></td><td>write /raɪt/ &bull; wrong /rɒŋ/ &bull; wrist /rɪst/</td></tr>"
  "<tr><td><strong>silent B</strong></td><td>lamb /l&aelig;m/ &bull; climb /klaɪm/ &bull; debt /det/</td></tr>"
  "<tr><td><strong>silent GH</strong></td><td>night /naɪt/ &bull; daughter /dɔːtə/ &bull; though /ðoʊ/</td></tr>"
  "<tr><td><strong>silent H</strong></td><td>honest /ˈɒnɪst/ &bull; hour /aʊə/</td></tr></table>"
  "<p>&#128226; Rule of thumb: in English, spelling and sound often differ. Always check pronunciation separately.</p>"),
 ("<p>Which letter is silent?</p>"
  "<ol><li>knight &rarr; ___</li><li>island &rarr; ___</li><li>Wednesday &rarr; ___</li>"
  "<li>psychology &rarr; ___</li><li>listen &rarr; ___</li></ol>"),
 "<ol><li>k</li><li>s</li><li>d</li><li>p</li><li>t</li></ol>",
 "English spelling reflects history, not modern pronunciation. Use a dictionary with phonetic transcription to check pronunciation."),

("Listening: Understanding Fast Native Speech", "B2",
 "English Teaching", "B2,listening,pronunciation,connected speech,native speakers",
 "B2 listening skills: connected speech features that make native English hard to understand. 5 minutes.",
 "Understanding Fast Native Speech | B2 Listening Skills",
 "I arrived in Sydney speaking textbook English &mdash; clean, deliberate, every word "
 "separate. Native speakers sounded like a different language. 'Whaddya want?' was "
 "'What do you want?' It took months to decode.",
 "identify connected speech features that make natural spoken English difficult to understand",
 ("<p><strong>5 features that make native speech sound fast:</strong></p>"
  "<table><tr><th>Feature</th><th>What happens</th><th>Example</th></tr>"
  "<tr><td><strong>Weak forms</strong></td><td>Unstressed words reduce</td><td>'and' &rarr; /&schwa;nd/</td></tr>"
  "<tr><td><strong>Linking</strong></td><td>Consonant + vowel merge</td><td>'turn it off' &rarr; tur-ni-toff</td></tr>"
  "<tr><td><strong>Elision</strong></td><td>A sound disappears</td><td>'next day' &rarr; 'nex day'</td></tr>"
  "<tr><td><strong>Assimilation</strong></td><td>One sound changes to match next</td><td>'ten boys' &rarr; 'tem boys'</td></tr>"
  "<tr><td><strong>Contractions</strong></td><td>Function words merge</td><td>going to &rarr; gonna &bull; want to &rarr; wanna</td></tr></table>"
  "<p>&#128172; <strong>Strategy:</strong> Grab content words (nouns, verbs, adjectives). Fill in the rest from context.</p>"),
 ("<p>What do these fast-speech forms mean?</p>"
  "<ol><li>'Whaddya think?' &rarr;</li><li>'I dunno.' &rarr;</li>"
  "<li>'Gimme a sec.' &rarr;</li><li>'She's gonna be late.' &rarr;</li></ol>"),
 "<ol><li>What do you think?</li><li>I don't know.</li><li>Give me a second.</li><li>She is going to be late.</li></ol>",
 "Learn contractions to <em>understand</em> others, not necessarily to use them. Native speakers won't think less of your formal version."),

("Cambridge B2 Opinion Essay: Structure and Language", "B2",
 "English Teaching", "B2,writing,essay,Cambridge,opinion,exam",
 "B2 Cambridge First writing: opinion essay structure, phrases, and a model paragraph. 5 minutes.",
 "B2 Opinion Essay Structure | Cambridge First Writing",
 "When I first wrote opinion essays in English, I said everything I thought in paragraph one. "
 "By paragraph three, I had nothing left. The Cambridge B2 essay has a structure. Learn it first.",
 "structure a B2 opinion essay and use appropriate discourse markers",
 ("<p><strong>5-paragraph structure:</strong></p>"
  "<ol><li><strong>Introduction</strong>: Paraphrase the question. State your general position.</li>"
  "<li><strong>Para 2</strong>: Main argument FOR + example</li>"
  "<li><strong>Para 3</strong>: Main argument AGAINST + example</li>"
  "<li><strong>Para 4</strong>: Your position with reasoning</li>"
  "<li><strong>Conclusion</strong>: Restate opinion + wider implication</li></ol>"
  "<p><strong>Useful phrases:</strong></p>"
  "<ul><li>It is widely argued that... / There is no doubt that...</li>"
  "<li>On the one hand... On the other hand...</li>"
  "<li>While some people believe... others maintain that...</li>"
  "<li>Taking everything into consideration, it seems clear that...</li></ul>"),
 ("<p>Plan an essay for: <em>'People who move abroad for work lose more than they gain. Do you agree?'</em></p>"
  "<p>Write one sentence for each of the 5 paragraphs.</p>"),
 "<p>(Open answer &mdash; sample: Para 1: Introduce the debate. Para 2: Career/financial gain. Para 3: Loss of family ties, cultural identity. Para 4: Personal position. Para 5: Balance is possible with deliberate effort.)</p>",
 "Structure first, language second. The Cambridge examiner rewards a clear argument with good cohesion above complex vocabulary alone."),

("Email Writing: Formal vs Informal", "B1",
 "English Teaching", "B1,writing,email,formal,informal,professional",
 "B1 writing: formal vs informal email. Key differences with examples. 5 minutes.",
 "Formal vs Informal Email Writing | B1 English",
 "When looking for teaching positions in R&eacute;union, I wrote dozens of emails in English and French. "
 "One school replied: 'Your English email was impressively professional.' The other didn't reply. "
 "The difference: register, done right.",
 "write clear formal and informal emails using appropriate language and structure",
 ("<table><tr><th></th><th>Formal</th><th>Informal</th></tr>"
  "<tr><td><strong>Opening</strong></td><td>Dear Mr/Ms [Name], / Dear Sir or Madam,</td><td>Hi [Name], / Hey!</td></tr>"
  "<tr><td><strong>Purpose</strong></td><td>I am writing to enquire about...</td><td>Just wanted to ask about...</td></tr>"
  "<tr><td><strong>Request</strong></td><td>I would be grateful if you could...</td><td>Could you...? / Can you...?</td></tr>"
  "<tr><td><strong>Closing</strong></td><td>Yours sincerely, / Kind regards,</td><td>Best, / See you soon,</td></tr>"
  "<tr><td><strong>Contractions</strong></td><td>I am / I would (no contractions)</td><td>I'm / I'd</td></tr></table>"
  "<p>&#9888;&#65039; Rule: Dear Sir/Madam &rarr; Yours faithfully &bull; Dear Mr Jones &rarr; Yours sincerely</p>"),
 ("<p>Rewrite this informal email as a formal one:</p>"
  "<blockquote><em>Hey! I saw the job ad. I wanna apply. Can you send me more info? Thanks, Sam</em></blockquote>"),
 ("<blockquote>Dear Sir or Madam,<br>"
  "I am writing to express my interest in the position advertised. "
  "Could you please send me further information regarding the role?<br>"
  "I look forward to hearing from you.<br>Yours faithfully,<br>Sam</blockquote>"),
 "When in doubt, go formal &mdash; it's easier to become more casual than to recover from seeming unprofessional."),

# ── SPECIAL / MIXED (3) ──────────────────────────────────────────────────────

("English for Hospitality: Welcoming Guests", "B1",
 "Career & Professional Development",
 "B1,hospitality,professional,English,welcoming,service",
 "B1 professional English: hospitality phrases for welcoming guests. 5 minutes.",
 "English for Hospitality: Welcoming Guests | B1",
 "I worked front-of-house at The Ivy, Establishment, and Uccello in Sydney. "
 "The first thirty seconds with a guest set the tone for the entire evening. "
 "This lesson gives you the language I used every night.",
 "welcome guests professionally in English using formal and warm language",
 ("<p><strong>First contact:</strong></p>"
  "<ul><li>'Good evening. Welcome to [Restaurant]. Do you have a reservation?'</li>"
  "<li>'May I take your name, please?'</li>"
  "<li>'Right this way, please. Let me show you to your table.'</li></ul>"
  "<p><strong>Offering assistance:</strong></p>"
  "<ul><li>'Can I take your coats?'</li>"
  "<li>'May I bring you something to drink while you look at the menu?'</li>"
  "<li>'Our specials this evening are...'</li>"
  "<li>'Please don't hesitate to ask if you need anything.'</li></ul>"
  "<p><strong>Register note:</strong> Hospitality English is <em>formal</em> but <em>warm</em>.<br>"
  "&#10060; 'What do you want?' &nbsp; &#10004; 'What can I bring for you?'<br>"
  "May / Could = more polite than Can in formal service.</p>"),
 ("<p>Rewrite these sentences to sound more professional:</p>"
  "<ol><li>'What's your name?'</li><li>'Sit there.'</li>"
  "<li>'You want a drink?'</li><li>'The soup is nice tonight.'</li></ol>"),
 ("<ol><li>'May I take your name, please?'</li>"
  "<li>'Right this way, please.' / 'Please allow me to show you to your table.'</li>"
  "<li>'May I offer you a drink?' / 'What can I bring you to drink?'</li>"
  "<li>'The soup this evening is excellent &mdash; I would recommend it.'</li></ol>"),
 "Warm formality is the goal: guests should feel welcomed, not processed. Modal verbs and softening phrases are your tools."),

("Learning a Language as an Adult: Vocabulary Strategies", "B1",
 "English Teaching",
 "B1,language learning,vocabulary,strategy,adult learning",
 "B1: how to learn vocabulary effectively as an adult. Strategies that work from someone who did it. 5 minutes.",
 "Learning Vocabulary as an Adult | B1 English Strategy",
 "I learned French to C1 level starting in my early thirties &mdash; after moving to France with Vanessa. "
 "No classes at first. Just immersion, a notebook, and a strategy that actually worked.",
 "apply at least three evidence-based vocabulary learning strategies",
 ("<p><strong>5 strategies that work:</strong></p>"
  "<ol><li><span class='hi'>Spaced repetition</span>: Review new words after 1 day, then 3 days, then a week. "
  "Forgetting is part of learning; retrieval practice makes it stick.</li>"
  "<li><span class='hi'>Word families</span>: Don't just learn <em>decide</em> &mdash; learn "
  "<em>decision, decisive, indecisive, undecided</em> together.</li>"
  "<li><span class='hi'>Collocations</span>: Learn words in their natural company. "
  "Not just <em>make</em> but <em>make a decision, make an effort, make friends</em>.</li>"
  "<li><span class='hi'>Contextual guessing</span>: When you meet a new word, try to guess the meaning "
  "from context before checking the dictionary.</li>"
  "<li><span class='hi'>Personalisation</span>: Write one sentence about your own life using each new word. "
  "Personal memory beats abstract flashcards.</li></ol>"),
 ("<p>Which strategy would you use for each situation?</p>"
  "<ol><li>You keep forgetting a word after one night's study.</li>"
  "<li>You have learned <em>analyse</em>. What should you also learn?</li>"
  "<li>You read a new word in a novel. You don't have a dictionary.</li></ol>"),
 ("<ol><li>Spaced repetition &mdash; review after 1 day, then 3, then 7.</li>"
  "<li>Word family: analysis, analytical, analyst, to analyse.</li>"
  "<li>Contextual guessing &mdash; use surrounding sentences to infer meaning.</li></ol>"),
 "The best strategy is the one you use consistently. Pick two from this list and commit to them for three weeks."),

("Your Story in English: Personal Introduction", "A2",
 "English Teaching",
 "A2,speaking,introduction,personal,beginner,Cambridge",
 "A2 speaking: how to introduce yourself confidently in English. Model + template. 5 minutes.",
 "Your Story in English: Personal Introduction | A2",
 "Every new country, every new job, every first day of class starts with the same thing: "
 "who are you? I have introduced myself in Sydney, Paris, and R&eacute;union. Each time, "
 "a clear introduction opened every door.",
 "introduce yourself confidently in English with key personal information",
 ("<p><strong>Introduction structure:</strong></p>"
  "<table><tr><th>Part</th><th>Phrases</th></tr>"
  "<tr><td>Name</td><td>My name is... / I'm... / You can call me...</td></tr>"
  "<tr><td>Where from</td><td>I'm from... / I'm originally from... but I live in...</td></tr>"
  "<tr><td>Work / study</td><td>I work as a... / I'm a... / I'm studying...</td></tr>"
  "<tr><td>Family</td><td>I'm married / I have a daughter / I live with...</td></tr>"
  "<tr><td>Interests</td><td>In my free time I... / I enjoy... / I'm interested in...</td></tr>"
  "<tr><td>Reason for being here</td><td>I'm here because... / I decided to... / My goal is to...</td></tr></table>"
  "<p><strong>Model introduction:</strong><br>"
  "<em>'My name is Sourov. I'm originally from Bangladesh, but I've lived in Australia, France, "
  "and now R&eacute;union. I work as an English teacher. I have a young daughter. "
  "In my free time I enjoy reading and photography. I'm here to help you improve your English &mdash; "
  "because I know exactly how it feels to learn a new language as an adult.'</em></p>"),
 ("<p>Write your own introduction (5&ndash;7 sentences). Use the structure above. "
  "Practise saying it aloud until it feels natural &mdash; not memorised, just comfortable.</p>"),
 "<p>(Open answer &mdash; aim for natural delivery, not a perfect script.)</p>",
 "A confident introduction is not about perfect English &mdash; it's about clear structure and eye contact. Practise out loud."),

]

# ── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    results = []
    for i, row in enumerate(LESSONS, 1):
        title, level, cat, tags, meta, seo, story, aim, ex, pr, ans, tip = row
        lesson = dict(
            title=title,
            content=build_html(level, title, story, aim, ex, pr, ans, tip),
            status="draft",
            category=cat,
            tags=tags,
            meta_description=meta,
            seo_title=seo,
        )
        code, wp_id = post_wp(lesson)
        ok = str(code) in ("200", "201")
        print(f"{'OK' if ok else 'FAIL'} [{code}] ID={wp_id}  {title[:55]}")
        results.append((i, code, wp_id, title))
        time.sleep(1.5)

    ok_count  = sum(1 for _, c, _, _ in results if str(c) in ("200","201"))
    print(f"\n=== {ok_count}/{len(LESSONS)} lessons posted successfully ===")
    print("\nWP IDs:")
    for n, c, wp, t in results:
        print(f"  {n:02d}. ID={wp:<6}  {t[:55]}")
