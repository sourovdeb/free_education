#!/usr/bin/env python3
"""
ELT365 Lesson Batch Creator — Months 6 & 7 (D152–D212)
Posts 61 micro-lessons as drafts to sourovdeb.com via the custom REST API.

Usage: python3 create_elt365_M6_M7_lessons.py
Requires: Python 3.6+, no external dependencies.
"""

import json, time, urllib.request, urllib.error

ENDPOINT = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
KEY = "0767044896thevenet_"
DISCLAIMER = (
    "<hr><p><em>Independent project; not affiliated with, endorsed by, or accredited "
    "by Cambridge University Press &amp; Assessment. Confers no qualification.</em></p>"
)

def make_html(idea, example, try_task):
    return (
        f"<p><strong>Idea — </strong>{idea}</p>"
        f"<p><strong>Example — </strong>{example}</p>"
        f"<p><strong>Try — </strong>{try_task}</p>"
        + DISCLAIMER
    )

# ── MONTH 6: Receptive Skills (D152–D181) ─────────────────────────────────────────────
M6 = [
    ("D152", "What Is a Receptive Skill?",
     "Receptive skills are reading and listening — language comes in. Learners decode meaning without producing output, but active processing is still required.",
     "A learner reads a news headline and extracts the main event without speaking or writing a word.",
     "Give a learner a short text. Ask one question they answer by nodding or pointing — no spoken response needed.",
     "receptive skills"),
    ("D153", "Top-Down Processing",
     "Top-down processing means using prior knowledge, context, and prediction to understand a text. The reader or listener moves from the general to the specific.",
     "Seeing the word ‘Menu’ on a card triggers expectations about food, prices, and choice — before reading a single word.",
     "Show learners an image before a text. Ask: ‘What do you think this is about?’ List three predictions, then read to check.",
     "receptive skills"),
    ("D154", "Bottom-Up Processing",
     "Bottom-up processing builds meaning from individual sounds, words, and sentences upward — decoding first, inference second.",
     "A learner hears ‘bi-cy-cle’ and constructs meaning phoneme by phoneme, then word by word.",
     "Give learners a sentence with one unknown word. Ask them to ignore it, read the rest, and guess the meaning from context.",
     "receptive skills"),
    ("D155", "Schema Theory in Reading",
     "A schema is a mental framework of existing knowledge. Activating schema before reading speeds up comprehension and reduces the cost of unknown vocabulary.",
     "Discussing ‘airport security’ before a reading text pre-loads the scenario so learners are not decoding a blank page.",
     "Before a text, ask learners to write five words they expect to see inside it. Compare predictions after reading.",
     "reading"),
    ("D156", "The Gist Task",
     "The gist task sets one global question, answered by reading or listening to the whole text once. It trains reading-for-the-main-idea, not detail.",
     "‘What is the writer’s main opinion?’ is a gist task. ‘What time did the train leave?’ is not.",
     "Write one gist question for a text you already use. It should be answerable in one sentence or fewer.",
     "reading"),
    ("D157", "The Detail Task",
     "A detail task demands specific information — facts, figures, names, sequences. It comes after the gist task, never before.",
     "‘How much did the flat cost per month?’ is a detail question. It requires locating a number, not understanding the whole text.",
     "Take any text. Write three detail questions targeting different parts. Underline where each answer appears.",
     "reading"),
    ("D158", "Scanning",
     "Scanning means moving quickly across a text to find specific information without reading every word. Readers use visual cues: numbers, proper nouns, keywords.",
     "Finding a phone number in a directory — your eyes sweep the column until the format triggers a stop.",
     "Give learners a dense text and one specific fact to find. Time them. Most can do this faster than they expect.",
     "reading"),
    ("D159", "Skimming",
     "Skimming is reading rapidly for the general idea — a fast tour of the text, not detailed comprehension.",
     "Running your eye over a newspaper article’s first sentence per paragraph gives you the story in 30 seconds.",
     "Give learners 45 seconds to skim a page. Ask: ‘What is this about?’ They answer in one sentence without looking again.",
     "reading"),
    ("D160", "Intensive Reading",
     "Intensive reading means reading closely for detailed understanding of vocabulary, grammar, and argument. It is slow, deliberate, and focused.",
     "Reading a legal contract, noting every clause, is intensive reading at its most demanding.",
     "Give learners one paragraph. Ask them to circle every verb and decide if each is past, present, or future.",
     "reading"),
    ("D161", "Extensive Reading",
     "Extensive reading means reading large amounts of easy text for pleasure or general comprehension — not stopping to analyse every word.",
     "A B1 learner reading graded readers at their level for 15 minutes a day is doing extensive reading.",
     "Find one graded reader or short article at your learners’ level. Recommend it for home reading with no exercises attached.",
     "reading"),
    ("D162", "Pre-Teaching Vocabulary",
     "Pre-teach only words that block comprehension of the task — not every unknown item. Over-teaching empties the lesson of thinking.",
     "Before a text about emigration, pre-teach ‘visa’ only if that word is central to your gist question.",
     "Identify words learners won’t know in a text. Mark only the ones needed to answer your gist question. Leave the rest.",
     "vocabulary"),
    ("D163", "The Lead-In",
     "The lead-in connects learners’ lives to the text before it appears. It activates schema, builds interest, and previews vocabulary through discussion.",
     "‘Have you ever moved to a new city? What was the hardest part?’ — before a text about relocation.",
     "Write a two-question lead-in for a text you already use. Make both questions personal and answerable from experience.",
     "receptive skills"),
    ("D164", "Writing a Gist Question",
     "A strong gist question has one correct answer that requires the whole text — not a detail pulled from the first line.",
     "‘Does the writer think social media is harmful?’ needs the full argument. ‘Who is the writer?’ does not.",
     "Draft a gist question for any text. Test it: can it be answered from the title alone? If yes, rewrite it.",
     "reading"),
    ("D165", "Writing a Detail Question",
     "A good detail question targets specific, locatable information. The wrong answers must be plausible, not absurd.",
     "‘How many students passed the test?’ is specific. ‘What did the teacher do?’ is too vague for a detail task.",
     "Write three detail questions at different difficulty levels for the same text: one easy, one moderate, one that requires inference.",
     "reading"),
    ("D166", "True / False / Not Given",
     "True/False/Not Given tasks include a third option for information absent from the text — a harder skill than True/False alone.",
     "‘The company was founded in 1990.’ If the text only says ‘founded in the 1990s,’ the answer is Not Given.",
     "Write five T/F/NG statements for a text. Include at least two ‘Not Given’ items referencing plausible but absent facts.",
     "reading"),
    ("D167", "Multiple Choice — Writing Clean Distractors",
     "Good multiple-choice distractors come from genuine misreadings, not random wrong answers. Each distractor should plausibly mislead a weak reader.",
     "If the answer is ‘She left because she was bored,’ one distractor might be ‘She left because of the cost’ — plausible but absent from the text.",
     "Write one multiple-choice question for a text. Test your distractors: would a weak reader actually choose each one?",
     "reading"),
    ("D168", "Matching Tasks",
     "Matching tasks pair headings with paragraphs, definitions with words, or speakers with opinions. They test global reading and inference.",
     "‘Match each speaker (1–4) to the opinion they express (A–F)’ is common in listening exams.",
     "Take a three-paragraph text. Write one heading that fits perfectly and two that are plausible but wrong. Try the task yourself first.",
     "receptive skills"),
    ("D169", "Authentic vs Graded Texts",
     "Authentic texts are written for native speakers — unmodified. Graded texts are simplified for a target level. Both have classroom uses.",
     "A B1 class gains from a graded version of a news story; a C1 class benefits from the original.",
     "Take one authentic text. Identify two features that make it hard for your learners. Decide: simplify the text, or simplify the task?",
     "receptive skills"),
    ("D170", "What Makes a Text Difficult?",
     "Text difficulty is not just vocabulary. Length, sentence structure, topic familiarity, text type, and cultural reference all affect how hard a text is.",
     "A short text on an unfamiliar cultural event can be harder than a longer text on a familiar topic.",
     "Choose two texts at the same word count. List three factors beyond vocabulary that make one harder than the other.",
     "receptive skills"),
    ("D171", "Features of Spoken Language",
     "Spoken language is full of false starts, fillers, contractions, ellipsis, and overlap. Listening tasks must reflect this — not clean written English read aloud.",
     "‘I — yeah, so basically, he didn’t — he couldn’t come’ is natural speech. ‘He was unable to attend’ is not.",
     "Record yourself speaking for 30 seconds on any topic. Transcribe it. Count the fillers and incomplete sentences.",
     "listening"),
    ("D172", "The One-Listen Gist",
     "Learners should hear a listening text once for gist before any detail work. Repeated listening without a task trains dependence, not skill.",
     "Play a short recording. Ask: ‘What is the general topic?’ One listen. One sentence answer. No transcript yet.",
     "Set a gist listening task. After one listen, collect answers. Discuss only what the recording was about — nothing more.",
     "listening"),
    ("D173", "Listening in Chunks",
     "Breaking a longer recording into sections and pausing to predict what comes next builds active listening — it is not cheating.",
     "After a speaker introduces a problem, pause and ask: ‘What do you think the solution will be?’ Then play on.",
     "Find a 2-minute recording. Pause it at two natural points. Write one prediction question for each pause.",
     "listening"),
    ("D174", "Using Visuals Before Listening",
     "Images, diagrams, or key words shown before a listening task activate prior knowledge and reduce cognitive load during the listening itself.",
     "A photograph of a factory floor before a listening about industrial disputes helps learners place the conversation immediately.",
     "Find an image that matches a listening text you use. Show it 30 seconds before playing. Ask one prediction question.",
     "listening"),
    ("D175", "Note-Taking as a Listening Task",
     "Structured note-taking — a half-completed grid or diagram — gives learners a purpose and a pencil while listening. Blank paper is harder.",
     "A grid with ‘Topic / Speaker’s opinion / One reason given’ keeps learners anchored during an interview recording.",
     "Design a simple two-column note-taking grid for a listening text. What headings best guide learners to the key information?",
     "listening"),
    ("D176", "Intonation Carries Meaning",
     "Falling intonation signals completion or certainty; rising intonation signals a question, doubt, or incompleteness. Teaching this stops learners misreading tone.",
     "‘That’s fine’ said with a fall means agreement. Said with a rise, it signals the opposite.",
     "Record two versions of ‘I see’ — one falling, one rising. Play both. Ask learners what each version means in context.",
     "listening"),
    ("D177", "Questions to Guide Listening",
     "Pre-listening questions tell learners what to listen for. Without a task, learners try to process everything and miss most of it.",
     "‘Who is speaking, and what is the relationship between the two people?’ is a manageable pre-listening focus.",
     "Write one question for each stage of a listening text — before, during, and after. Make the before-question answerable in ten seconds.",
     "listening"),
    ("D178", "Inferring Meaning from Context",
     "Inferring meaning — working out what is not stated — is a higher-order reading and listening skill. It is trainable, not innate.",
     "‘She didn’t say much after that’ infers a negative reaction without stating it.",
     "Mark three moments in a text where meaning must be inferred. Write a question for each: ‘What does the writer suggest here?’",
     "receptive skills"),
    ("D179", "The Follow-Up Task",
     "A follow-up task bridges from receptive to productive — learners respond to what they read or heard, not just answer questions about it.",
     "After reading about a job interview, learners roleplay their own — content from the text, production from themselves.",
     "Take a reading or listening text you use. Write one follow-up speaking task and one follow-up writing task from the same source.",
     "receptive skills"),
    ("D180", "Building Independent Reading Habits",
     "Extensive reading outside class develops vocabulary depth and reading speed — but only if learners choose texts they enjoy at their level.",
     "A learner who reads one graded reader per month gains significant passive vocabulary over a year.",
     "Ask learners to name one topic they enjoy in their first language. Find one text on that topic in English, at their level.",
     "reading"),
    ("D181", "Month 6 Review — Receptive Skills",
     "Review the core terms from Days 152–180. Check your understanding before moving to productive skills next month.",
     "Can you name the difference between scanning and skimming? Between the gist task and the detail task? Between top-down and bottom-up?",
     "Without looking back: write one sentence defining top-down processing, one for bottom-up. Then check Days 153–154. How close were you?",
     "receptive skills"),
]

# ── MONTH 7: Productive Skills (D182–D212) ────────────────────────────────────────────
M7 = [
    ("D182", "What Is a Productive Skill?",
     "Productive skills are speaking and writing — language goes out. Learners encode meaning and send it, rather than decode incoming text.",
     "A learner explains their weekend plans in English. No one is testing their input processing — they are creating output.",
     "Ask learners to write three sentences about their morning without looking at any English source. Pure production. Note what they struggle with.",
     "productive skills"),
    ("D183", "Accuracy vs Fluency",
     "Accuracy means producing correct language. Fluency means producing language smoothly, prioritising communication. Most activities lean toward one, rarely both at once.",
     "Drilling a grammar pattern develops accuracy. A debate task with no correction develops fluency. Neither alone is enough.",
     "Look at your next lesson. Label each activity A (accuracy) or F (fluency). Is the balance right for your learners?",
     "productive skills"),
    ("D184", "Controlled Practice",
     "Controlled practice limits learner choices — a gap-fill or substitution drill. Learners apply one form correctly before attempting free use.",
     "‘Fill in: I ___ (go) to school every day’ targets simple present with zero ambiguity about what is being practised.",
     "Write one controlled practice task for a grammar point you teach. Make it so focused that wrong answers are impossible if learners know the form.",
     "speaking"),
    ("D185", "Freer Practice",
     "Freer practice removes the scaffold — learners choose their own language to express a communicative aim. Mistakes are expected and informative.",
     "‘Talk to your partner for two minutes about your ideal job’ is freer practice — no script, no restricted form.",
     "Design a freer practice task for a grammar point you have recently taught. Ensure the task creates a genuine need to use that language.",
     "speaking"),
    ("D186", "PPP for Speaking",
     "In PPP for speaking, the teacher presents the target language, learners practise it in controlled tasks, then produce it in a freer communicative activity.",
     "Teach ‘would you like to…?’ → drill it → roleplay a restaurant conversation.",
     "Plan a five-minute PPP sequence for invitations. Write out the presentation, one controlled task, and one freer task in that order.",
     "speaking"),
    ("D187", "Task-Based Learning for Speaking",
     "In TBLT, learners complete a real communicative task first — language emerges from the need, not the plan. Language focus comes after.",
     "Plan a class trip without the teacher giving vocabulary beforehand. Learners negotiate, decide, then report. Language focus follows.",
     "Design one task where speaking is the goal, not the exercise. What real-world outcome does the task produce?",
     "speaking"),
    ("D188", "Information-Gap Activities",
     "In an information-gap task, each learner holds different information. Sharing it is the task. This creates genuine need to speak and listen.",
     "Student A has a train timetable. Student B has the ticket prices. Neither can complete the booking alone.",
     "Take any text or data set. Split the information in two. Write instructions so each student knows what they have and what they need.",
     "speaking"),
    ("D189", "Opinion-Gap Activities",
     "In an opinion-gap task, learners share personal views — not facts. There is no correct answer, only justified positions.",
     "‘Should schools ban mobile phones?’ has no right answer. Each learner defends their view and listens to others.",
     "Write one opinion-gap question relevant to your learners’ lives. Add a prompt: ‘Give two reasons for your view.’",
     "speaking"),
    ("D190", "Reasoning-Gap Activities",
     "Reasoning-gap tasks require learners to process information, draw conclusions, and justify them — not just exchange facts or opinions.",
     "‘You have a budget of £50 and five guests. Plan the dinner.’ Learners must calculate, prioritise, and argue — all in English.",
     "Design a reasoning-gap task around a budget, route, or schedule problem your learners might actually face.",
     "speaking"),
    ("D191", "Roleplay — Setting It Up",
     "Roleplay works when learners know the scenario, the relationship between characters, and the goal. Vague setups produce vague language.",
     "‘You are a tenant. Your landlord is raising the rent by 40%. Negotiate.’ Clear stakes, clear relationship, clear outcome.",
     "Take a roleplay you use. Check: is the scenario clear? Is the relationship clear? Is the goal stated? Fix any gap.",
     "speaking"),
    ("D192", "Discussion Tasks",
     "A discussion task produces language through sustained speaking, but needs a clear structure or it collapses into silence.",
     "A ‘balloon debate’ — each learner defends a famous person’s right to stay in the balloon — gives everyone a stake and a turn.",
     "Design a discussion task with a built-in role for every learner. No one should be able to remain silent and still complete it.",
     "speaking"),
    ("D193", "Drilling for Speaking",
     "Drilling is not mindless repetition — done well, it builds accurate pronunciation and intonation before a pattern becomes automatic.",
     "Choral drill first: everyone says the model together. Then individual drill: each learner produces it alone.",
     "Drill one sentence from your next lesson chorally three times, then individually with five learners. Listen for stress, not just words.",
     "speaking"),
    ("D194", "Monitoring Speaking Tasks",
     "While learners speak, the teacher circulates and notes language — good examples and errors — for feedback after, not during.",
     "A teacher hears ‘He suggest to go’ and notes it. During feedback: ‘I heard this — what’s the correct form?’",
     "Set a speaking task. During it, write down five language samples — at least two correct. Use them all in delayed feedback.",
     "speaking"),
    ("D195", "Content vs Language Feedback in Speaking",
     "After a speaking task, respond to the content first — what learners said. Then address language. Reversing this kills the communicative purpose.",
     "‘That was convincing. You mentioned three reasons — well-structured. One language point: he suggested going, not he suggested to go.’",
     "Plan your next speaking feedback slot. Write content feedback first, then language correction. Practise the sequence before the lesson.",
     "speaking"),
    ("D196", "Delayed vs On-the-Spot Correction in Speaking",
     "On-the-spot correction interrupts fluency — use it sparingly for accuracy tasks. Delayed correction preserves communication in fluency tasks.",
     "In a gap-fill drill, correct immediately. In a discussion, take notes and correct after the task ends.",
     "Decide for your next three activities: correct immediately or delay? Write the reason for each choice in your lesson plan.",
     "error correction"),
    ("D197", "The Process Approach to Writing",
     "Process writing treats writing as a cycle: plan, draft, revise, edit. The product is secondary to the thinking behind it.",
     "Learners brainstorm, write a rough first draft, swap for peer feedback, then revise — no single deadline.",
     "Add one revision stage to a writing task you already use. Ask learners to reread and change at least two things before submitting.",
     "writing"),
    ("D198", "Planning a Piece of Writing",
     "Planning before writing improves coherence and reduces mid-draft paralysis. Teaching learners to plan is itself a productive-skill lesson.",
     "A mind map, a bullet-point list, or a paragraph-by-paragraph outline — any visible structure before drafting helps.",
     "Before a writing task, give learners five minutes to create a plan in any format. Then write. Compare quality with an unplanned attempt.",
     "writing"),
    ("D199", "Drafting",
     "First drafts are for getting ideas down — fluency over accuracy. Teaching learners to draft without self-editing first is a skill in itself.",
     "‘Write for five minutes without stopping. Spelling and grammar can be fixed later.’ This is timed free-writing, and it works.",
     "Set a five-minute timed free-write on any topic. No backspacing, no erasing. Collect the drafts and note the ideas — not the errors.",
     "writing"),
    ("D200", "Editing",
     "Editing is the revision of one’s own writing for accuracy — grammar, punctuation, word choice. It requires learners to distance themselves from their own text.",
     "After drafting, give learners a simple checklist: verb tense? Article use? Sentence boundaries?",
     "Create a five-item editing checklist for a level-appropriate error type. Give it to learners to apply to their own draft before submission.",
     "writing"),
    ("D201", "Genre Awareness in Writing",
     "Every text type has conventions — emails open differently from essays, reports from stories. Teaching the genre before teaching the content cuts confusion.",
     "Before teaching formal letters, show an annotated model: greeting, opening purpose, formal register, closing. Then learners write.",
     "Choose one text type you will teach. List five features that make it recognisably that genre. These become your lesson’s analysis stage.",
     "writing"),
    ("D202", "Writing a Paragraph",
     "A well-formed paragraph has a topic sentence, supporting evidence or detail, and a closing sentence. This structure transfers across genres.",
     "Topic: ‘Commuting by bike saves money.’ Evidence: ‘A monthly bus pass costs €60; a bike lasts ten years.’ Close: ‘The arithmetic is simple.’",
     "Give learners a topic sentence. Ask them to write two supporting sentences and one closing sentence. Swap and check structure, not content.",
     "writing"),
    ("D203", "Cohesion in Writing",
     "Cohesion is how a text holds together — through pronouns, synonyms, discourse markers, and reference chains. Without it, sentences are isolated facts.",
     "‘She arrived late. The teacher was already speaking. This made her nervous.’ Three pronouns link four ideas into one story.",
     "Take a paragraph from learner writing. Highlight every cohesion device. If there are fewer than three, ask them to add more.",
     "writing"),
    ("D204", "Written Feedback — Margin Codes",
     "Margin codes tell learners the type of error without giving the answer: T = tense, Sp = spelling, WO = word order. Learners self-correct.",
     "‘She have been there’ gets a T in the margin. The learner finds and fixes it — and learns more than from a red cross.",
     "Design a ten-code margin-code system for the error types you see most in your learners’ writing. Introduce it on the next set.",
     "writing"),
    ("D205", "Peer Feedback on Writing",
     "Peer feedback builds critical reading skills in the responder and shows the writer how a real reader responds. It is not a shortcut.",
     "Learner A reads Learner B’s paragraph and says: ‘Your first reason was clear. I didn’t follow the example in line three.’",
     "Write two peer-feedback sentence starters: one for content, one for language. Give them to learners before a pair-exchange activity.",
     "writing"),
    ("D206", "Low-Stakes Writing Tasks",
     "Low-stakes tasks — exit tickets, quick reactions, informal lists — build writing confidence without the weight of a graded assignment.",
     "‘Write one thing you learned this lesson in exactly ten words’ is low-stakes, specific, and forces precision.",
     "End your next lesson with a two-minute low-stakes write. Set a clear constraint — a word limit, a sentence opener, or a format.",
     "writing"),
    ("D207", "Dictation",
     "Dictation is a listening-to-writing bridge: learners hear language and transcribe it accurately. Done well, it integrates listening, spelling, punctuation, and grammar.",
     "Read a short passage at natural speed, in meaningful chunks, with one pause per chunk — not word by word.",
     "Dictate four sentences from a text learners have already read. Compare their versions with the original. Discuss differences — not just spelling.",
     "writing"),
    ("D208", "Dictogloss",
     "Dictogloss goes beyond dictation: learners hear a text twice, take notes, then reconstruct the meaning collaboratively — not word for word.",
     "A teacher reads a 60-word paragraph twice. Pairs reconstruct it from notes and compare their version to the original for language accuracy.",
     "Write a 60-word dictogloss text at your learners’ level. Plan what you expect them to reconstruct accurately and where you expect approximation.",
     "writing"),
    ("D209", "Reading Into Writing",
     "Reading-into-writing tasks use a text as a model — learners read, analyse the structure, then produce their own version on a new topic.",
     "Learners read a product review, identify the structure (pro / con / conclusion), then write a review of something they own.",
     "Choose a short model text. Write three analysis questions that reveal its structure. Then set a parallel writing task on a different topic.",
     "writing"),
    ("D210", "Listening Into Speaking",
     "Listening-into-speaking tasks build from input to output: learners hear a model exchange, then produce their own on the same pattern.",
     "Learners hear a hotel check-in conversation, identify the key phrases, then roleplay their own check-in using the same structure.",
     "Find a short dialogue recording. Identify three phrases learners can reuse. Set a speaking task that requires all three.",
     "speaking"),
    ("D211", "The Speaking–Writing Connection",
     "Speaking and writing reinforce each other: speaking first generates ideas; writing consolidates language form. Both directions work.",
     "Learners discuss a problem in pairs, then write a paragraph summarising their solution. The spoken ideas become the written content.",
     "Set a speaking task, then ask learners to write one or two sentences summarising what they said. Same ideas, different mode.",
     "productive skills"),
    ("D212", "Month 7 Review — Productive Skills",
     "Review the core terms from Days 182–211. Check what has settled before moving to classroom management next month.",
     "Without looking back: what is the difference between accuracy and fluency? Name one information-gap activity you could use next week.",
     "Write a 50-word explanation of process writing for a colleague who has never heard the term. Use no jargon. Then check Day 197.",
     "productive skills"),
]

ALL_LESSONS = M6 + M7  # 61 total

def build_post(day_code, title, idea, example, try_task, topic_tag):
    num = day_code[1:]  # e.g. "152"
    return {
        "title": f"ELT365 · Day {num} — {title}",
        "content": make_html(idea, example, try_task),
        "status": "draft",
        "category": "English Teaching",
        "tags": f"ELT365, teacher training, ELT, {topic_tag}",
        "meta_description": f"ELT365 Day {num}: {title}. A 5-minute teacher-training micro-lesson on {topic_tag}.",
        "seo_title": f"ELT365 Day {num} — {title} | Sourov Deb",
    }

def post_to_wp(payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Sourov-Key": KEY,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as ex:
        return 0, str(ex)

def main():
    results = []
    total = len(ALL_LESSONS)
    print(f"Posting {total} lessons to {ENDPOINT}")
    print("=" * 60)

    for i, lesson in enumerate(ALL_LESSONS, 1):
        day_code, title, idea, example, try_task, topic_tag = lesson
        post = build_post(day_code, title, idea, example, try_task, topic_tag)
        status, body = post_to_wp(post)

        try:
            resp_data = json.loads(body)
            post_id = resp_data.get("id") or resp_data.get("post_id") or "?"
            link = resp_data.get("link") or resp_data.get("url") or ""
            outcome = f"OK id={post_id}"
        except Exception:
            outcome = f"FAIL body={body[:120]}"
            post_id = "ERR"
            link = ""

        result = {
            "day": day_code,
            "title": post["title"],
            "http": status,
            "outcome": outcome,
            "post_id": post_id,
            "link": link,
        }
        results.append(result)
        print(f"[{i:02d}/{total}] {day_code} HTTP {status} — {outcome}")

        if status not in (200, 201):
            print(f"    >>> Body: {body[:200]}")

        if i < total:
            time.sleep(0.8)

    print("=" * 60)
    ok = sum(1 for r in results if r["http"] in (200, 201))
    print(f"\nDone. {ok}/{total} posted successfully as draft.")
    with open("elt365_draft_manifest.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Manifest saved to elt365_draft_manifest.json")

if __name__ == "__main__":
    main()
