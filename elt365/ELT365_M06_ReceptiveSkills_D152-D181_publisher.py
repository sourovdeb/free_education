#!/usr/bin/env python3
"""
ELT365 — Batch draft publisher for sourovdeb.com
Months 6 (D152-D181) and 7 (D182-D212) — Receptive & Productive skills
Status: draft  |  Category: English Teaching
Disclaimer: Independent project; not affiliated with Cambridge University Press & Assessment.
"""
import json, time, urllib.request, urllib.error

WP_ENDPOINT = "https://sourovdeb.com/wp-json/sourov/v1/ai-post"
WP_KEY      = "0767044896thevenet_"
DISCLAIMER  = ("<hr><p><em>Independent project; not affiliated with, endorsed by, "
               "or accredited by Cambridge University Press &amp; Assessment. "
               "Confers no qualification.</em></p>")

def html_lesson(idea, example, try_task):
    return (
        f"<p><strong>Idea —</strong> {idea}</p>"
        f"<p><strong>Example —</strong> {example}</p>"
        f"<p><strong>Try —</strong> {try_task}</p>"
        + DISCLAIMER
    )

LESSONS = [
    # ── Month 6: Receptive Skills (D152–D181) ────────────────────────────────
    {
        "day": 152, "title": "What receptive skills are",
        "idea": "Receptive skills are listening and reading — skills where meaning flows in. You decode; you don't produce. Both are active, not passive: the brain selects, predicts, and infers throughout.",
        "example": "A student reads a job ad, skipping words they don't need, zeroing in on salary and hours. That selective attention is a receptive skill in use.",
        "try_task": "Ask learners to listen to 30 seconds of radio news and write three words they catch. Discuss what helped them hear those words.",
        "tags": "ELT365, teacher training, ELT, receptive skills, listening, reading",
        "meta": "Listening and reading are active receptive skills. A 5-minute ELT365 micro-lesson on what teachers need to know.",
    },
    {
        "day": 153, "title": "Top-down vs bottom-up processing",
        "idea": "Top-down: learners use context, topic knowledge, and prediction to build meaning. Bottom-up: they decode individual sounds or words first. Skilled listeners and readers do both simultaneously.",
        "example": "Hearing 'delayed flight' triggers top-down schemas about airports; then 'gate 14B' bottom-up fills in the detail.",
        "try_task": "Give learners a text headline only. Ask what they predict the text is about. This activates top-down processing before a single sentence is read.",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading strategies",
        "meta": "Top-down uses background knowledge; bottom-up decodes sounds and words. Learn both in 5 minutes with ELT365 Day 153.",
    },
    {
        "day": 154, "title": "Gist listening — the first question",
        "idea": "A gist task asks one broad question answered by listening once through. It gives listening a purpose and stops learners trying to catch every word before they're ready.",
        "example": "'Is this conversation at work or at home?' is a gist question. It requires understanding tone and topic, not every word.",
        "try_task": "Design one gist question for any audio you plan to use this week. Make sure it can be answered from overall meaning, not one specific detail.",
        "tags": "ELT365, teacher training, ELT, receptive skills, listening",
        "meta": "Gist listening sets a broad purpose before detail work. ELT365 Day 154 — a 5-minute teacher training micro-lesson.",
    },
    {
        "day": 155, "title": "Detail listening — targeted information",
        "idea": "After gist, a detail task focuses on specific information: a number, a name, a reason. Learners listen again with a narrow purpose. Processing is easier when the general meaning is already clear.",
        "example": "'What time does the next train leave?' — learners scan the audio for one piece of data, ignoring the rest.",
        "try_task": "Write three detail questions for a listening you already use. Check: each targets one specific fact, not a general impression.",
        "tags": "ELT365, teacher training, ELT, receptive skills, listening tasks",
        "meta": "Detail listening tasks follow gist and ask for specific information. ELT365 Day 155 — 5-minute teacher training.",
    },
    {
        "day": 156, "title": "Listening for specific information",
        "idea": "Listening for specific information means scanning the audio stream much as eyes scan a page. Learners know what they want before they hear it and filter everything else out.",
        "example": "Flight arrivals boards train this skill: passengers listen only for their flight number and gate.",
        "try_task": "Play a short news clip. Tell learners in advance to listen only for the country mentioned. Debrief: what did they ignore? What held their attention?",
        "tags": "ELT365, teacher training, ELT, receptive skills, listening strategies",
        "meta": "Scanning audio for specific details mirrors real-world listening. ELT365 Day 156 teacher training micro-lesson.",
    },
    {
        "day": 157, "title": "Pre-listening activities",
        "idea": "Pre-listening sets context, activates schema, and pre-teaches any vocabulary that would block comprehension. Done well, it means learners arrive at the audio ready to process meaning, not decode words.",
        "example": "Before a podcast on urban farming, show a photo and elicit three words learners already know. That takes two minutes and removes three blockers.",
        "try_task": "For your next listening lesson, identify the one vocabulary item that will block most learners. Pre-teach it with a concept-checking question, not a dictionary definition.",
        "tags": "ELT365, teacher training, ELT, receptive skills, lesson planning",
        "meta": "Pre-listening activates schema and removes vocabulary blockers. ELT365 Day 157 — 5-minute teacher training.",
    },
    {
        "day": 158, "title": "Why teachers use authentic texts",
        "idea": "Authentic texts — unaltered real-world material — expose learners to natural speech rate, discourse patterns, and register. The challenge is choosing texts whose difficulty is appropriate to the task, not the text itself.",
        "example": "A B1 class listens to a native-speaker podcast but answers one A2-level gist question. The text is authentic; the task is graded.",
        "try_task": "Find one 60-second authentic audio clip on a topic your class finds motivating. Design a single gist question a B1 learner could answer on one listen.",
        "tags": "ELT365, teacher training, ELT, receptive skills, authentic materials",
        "meta": "Authentic texts expose learners to real language; the task carries the grade. ELT365 Day 158 micro-lesson.",
    },
    {
        "day": 159, "title": "Graded vs authentic texts — choosing wisely",
        "idea": "Graded texts are written to match a CEFR level: controlled vocabulary, short sentences. Authentic texts are real-world material at natural complexity. Neither is better; the choice depends on lesson aim and learner readiness.",
        "example": "A graded A2 story uses past simple throughout; an authentic newspaper uses mixed tenses, idioms, and ellipsis. Both can teach — with the right task.",
        "try_task": "Take an authentic paragraph and grade it to A2: shorten sentences, replace two idioms, cut one clause. Notice what is lost and what is kept.",
        "tags": "ELT365, teacher training, ELT, receptive skills, materials design",
        "meta": "Graded and authentic texts each serve a purpose. ELT365 Day 159 — 5-minute micro-lesson for ELT teachers.",
    },
    {
        "day": 160, "title": "Skimming — reading for the main idea",
        "idea": "Skimming means reading quickly to get the overall meaning — without reading every word. The eyes move fast across headlines, first lines, and concluding sentences to build a mental map.",
        "example": "A student glances through a three-paragraph email to decide if it requires a reply. They read maybe 20% of the words.",
        "try_task": "Give learners a full-page article and 90 seconds. Task: write one sentence saying what the text is about. Debrief whether they needed to read every word.",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading strategies",
        "meta": "Skimming builds the habit of reading for gist without decoding every word. ELT365 Day 160 teacher micro-lesson.",
    },
    {
        "day": 161, "title": "Scanning — reading for specific detail",
        "idea": "Scanning moves the eye rapidly over a text in search of one specific item — a name, a date, a price. The reader ignores everything else. It is purposeful, efficient, and a core real-world skill.",
        "example": "Reading a train timetable to find the last departure to Lyon. The eye jumps to the 'Lyon' column; nothing else is processed.",
        "try_task": "Give learners a classified-ads page. Ask them to find the cheapest one-bedroom flat in 60 seconds. Debrief: what strategy did they use?",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading strategies",
        "meta": "Scanning is targeted, fast reading for specific information. ELT365 Day 161 — five-minute teacher training lesson.",
    },
    {
        "day": 162, "title": "Intensive reading — close study of a text",
        "idea": "Intensive reading involves reading a short text closely, attending to grammar, vocabulary, discourse, and meaning. It builds language awareness. It is slow, deliberate, and teacher-guided.",
        "example": "A class reads one paragraph of a short story, circling all past-tense verbs, then discusses why the author chose each one.",
        "try_task": "Select a 100-word paragraph. Ask learners to underline every linking word. Debrief: how does each connector change the meaning of the sentence that follows it?",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading",
        "meta": "Intensive reading trains close attention to language form and meaning. ELT365 Day 162 — 5-minute micro-lesson.",
    },
    {
        "day": 163, "title": "Extensive reading — volume and fluency",
        "idea": "Extensive reading means reading large amounts of easy, enjoyable material at the learner's independent level. Quantity builds fluency, vocabulary breadth, and reading speed. The text should feel almost too easy.",
        "example": "A B1 learner reads a graded reader (Oxford Bookworms Stage 3) at home — 30 pages an evening. Over a term, that is exposure to tens of thousands of words in context.",
        "try_task": "Ask learners to bring one book, article, or website they read in English for fun. Share titles. Discuss: how often, how long, and why that source?",
        "tags": "ELT365, teacher training, ELT, receptive skills, extensive reading",
        "meta": "Extensive reading builds vocabulary breadth and reading speed through volume. ELT365 Day 163 teacher training.",
    },
    {
        "day": 164, "title": "Prediction tasks in reading",
        "idea": "Prediction tasks ask learners to guess content before they read. This activates schema, gives reading a purpose, and creates a small tension — was I right? — that drives engagement.",
        "example": "Show a headline: 'City bans cars on Sundays.' Ask: Who is affected? What problems might this solve? What objections might there be? Then read to compare.",
        "try_task": "For your next reading lesson, write two prediction questions based only on the title and one image. Run them before learners open the text.",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading tasks",
        "meta": "Prediction before reading activates schema and makes comprehension an active test. ELT365 Day 164.",
    },
    {
        "day": 165, "title": "Schema activation — building context",
        "idea": "Schema is the network of prior knowledge a reader or listener brings to a text. Activating it before a task reduces cognitive load and dramatically improves comprehension.",
        "example": "Before a listening on restaurant complaints, ask: 'What do people most often complain about in restaurants?' The answers prime learners for exactly the content they are about to hear.",
        "try_task": "For any upcoming lesson, write three questions that activate what learners already know about the topic. Use them as a 3-minute lead-in, not a quiz.",
        "tags": "ELT365, teacher training, ELT, receptive skills, lesson planning",
        "meta": "Schema activation before a text reduces cognitive load and aids comprehension. ELT365 Day 165 — teacher training.",
    },
    {
        "day": 166, "title": "Pre-teaching vocabulary for reading",
        "idea": "Pre-teach only vocabulary that blocks meaning and cannot be guessed from context. Teaching too many words steals time; teaching too few risks comprehension breakdown. Nation's research suggests 98% coverage for fluent reading.",
        "example": "A text on solar panels: pre-teach 'photovoltaic' if it appears twice and cannot be inferred. Do not pre-teach 'panel' — learners can guess it.",
        "try_task": "Scan your next reading text. Identify two words learners almost certainly don't know and cannot guess. Teach those two only. Leave the rest for post-reading work.",
        "tags": "ELT365, teacher training, ELT, receptive skills, vocabulary",
        "meta": "Pre-teach only vocabulary that blocks comprehension. Nation's 98% threshold explained. ELT365 Day 166.",
    },
    {
        "day": 167, "title": "Gist tasks for reading",
        "idea": "A reading gist task asks one broad question the whole text answers. Its purpose is to give direction and prevent word-by-word decoding on a first pass. One question; first read; time limit.",
        "example": "'What is the writer's main complaint?' requires understanding the whole text's argument, not any one sentence.",
        "try_task": "Write a gist question for a text you already use. Test it: can a learner answer it without reading more than the first and last paragraph? If yes, it is a good gist question.",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading tasks",
        "meta": "A gist question gives reading a purpose on the first pass. ELT365 Day 167 — 5-minute teacher training micro-lesson.",
    },
    {
        "day": 168, "title": "True / false / not given — using it correctly",
        "idea": "True/False/Not Given tasks train learners to distinguish what the text says from what they believe. The third option — Not Given — is harder than it looks: absence of information is a linguistic skill.",
        "example": "'The company was founded in 1999.' If the text says 2001, False. If the text doesn't mention founding date at all, Not Given.",
        "try_task": "Write three T/F/NG items for a text you use. Swap with a colleague. Did they agree on the answers? Disagreements reveal ambiguity in your items — revise them.",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading, assessment",
        "meta": "True/False/Not Given trains careful text comprehension. How to write good items. ELT365 Day 168.",
    },
    {
        "day": 169, "title": "Multiple choice in reading tasks",
        "idea": "Good multiple-choice reading items test comprehension, not test-taking strategy. Distractors should be plausible but clearly wrong when the text is understood. Avoid 'all of the above' and trick answers.",
        "example": "A strong distractor restates a detail from the text but misapplies it to the question — it sounds right but the text doesn't support it.",
        "try_task": "Take one multiple-choice question from a published coursebook. Analyse each distractor: why might a learner choose it? Is each one testing comprehension or just guesswork?",
        "tags": "ELT365, teacher training, ELT, receptive skills, assessment, reading",
        "meta": "How to write and evaluate multiple-choice reading questions. ELT365 Day 169 — 5-minute teacher training.",
    },
    {
        "day": 170, "title": "Ordering tasks — reconstructing a text",
        "idea": "Ordering tasks ask learners to arrange jumbled sentences or paragraphs into the original sequence. They train awareness of discourse: cohesive devices, logical flow, and topic development.",
        "example": "Five sentences from an argument cut up and shuffled. Learners sequence them, using connectors like 'However,' 'As a result,' and 'In contrast' as guides.",
        "try_task": "Cut a three-paragraph text into six sentences. Give learners the first sentence as an anchor. Time them re-ordering the rest. Debrief: what words told you what came next?",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading, discourse",
        "meta": "Ordering tasks build discourse awareness and knowledge of text structure. ELT365 Day 170 micro-lesson.",
    },
    {
        "day": 171, "title": "Inference — reading between the lines",
        "idea": "Inference is the ability to understand what a text implies but does not state. It draws on word choice, tone, context, and cultural knowledge. It is a higher-order skill often assessed at B2 and above.",
        "example": "'She closed the door quietly.' The text doesn't say she was upset, but the adverb implies it. Learners who infer this are reading beyond surface meaning.",
        "try_task": "Choose a short dialogue from any textbook. Ask: 'What does this person really feel? What word or phrase tells you that?' Make inference visible.",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading, higher order thinking",
        "meta": "Inference means reading implied meaning, not just stated facts. ELT365 Day 171 — 5-minute teacher training.",
    },
    {
        "day": 172, "title": "Text type and genre awareness",
        "idea": "Different text types follow different conventions. A recipe has imperatives and ingredients lists. A formal letter has a salutation and sign-off. Teaching genre awareness helps learners navigate real texts faster.",
        "example": "A student who recognises an opinion column expects the writer to take a side, use hedging language, and anticipate counter-arguments — before reading a word.",
        "try_task": "Give learners the first two lines of three different text types. Ask them to identify the type and predict what comes next. Discuss the clues they used.",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading, genre",
        "meta": "Genre awareness lets learners predict and navigate text types. ELT365 Day 172 teacher training micro-lesson.",
    },
    {
        "day": 173, "title": "Adapting authentic listening texts",
        "idea": "Authentic audio can be shortened, pre-listened for blockers, or paired with a support script for lower levels. The aim is to preserve naturalness while managing cognitive load.",
        "example": "A 4-minute interview clipped to 90 seconds with one gist question is more teachable than the full version with a dense comprehension grid.",
        "try_task": "Take one piece of authentic audio you own. Identify the 60-second section with the clearest content. Design one task for that section only.",
        "tags": "ELT365, teacher training, ELT, receptive skills, listening, materials adaptation",
        "meta": "Adapting authentic listening keeps naturalness while managing level. ELT365 Day 173 — 5-minute micro-lesson.",
    },
    {
        "day": 174, "title": "Using visuals to support listening",
        "idea": "Images, maps, graphs, or short written prompts shown before or during a listening task reduce cognitive load and anchor understanding. They provide the non-verbal context that a live conversation provides naturally.",
        "example": "Before a weather forecast listening, show a blank map with four cities marked. Learners write the forecast next to each city as they listen.",
        "try_task": "Find one listening task you already use that has no visual support. Add one image shown before the audio. Teach it and compare comprehension to last time.",
        "tags": "ELT365, teacher training, ELT, receptive skills, listening, visual support",
        "meta": "Visuals reduce cognitive load and support listening comprehension. ELT365 Day 174 — 5-minute ELT micro-lesson.",
    },
    {
        "day": 175, "title": "Note-taking while listening",
        "idea": "Note-taking is a receptive-plus-productive task. Learners must select, compress, and record meaning simultaneously. It needs scaffolding: partial notes, guided grids, or key-word prompts reduce the initial load.",
        "example": "A partially completed table — speaker, topic, opinion — focuses attention and stops learners writing full sentences while trying to listen.",
        "try_task": "Design a half-completed note grid for a listening you use. Leave deliberate gaps at the highest-information moments. Test it yourself first.",
        "tags": "ELT365, teacher training, ELT, receptive skills, listening, academic skills",
        "meta": "Note-taking scaffolds listening comprehension for academic learners. ELT365 Day 175 teacher training micro-lesson.",
    },
    {
        "day": 176, "title": "The role of context in comprehension",
        "idea": "Context — who is speaking, where, and why — dramatically reduces the linguistic work required to understand a message. Providing context before a listening or reading task is not cheating; it is replicating real communication.",
        "example": "Knowing you are about to hear a landlord leaving a voicemail means the word 'deposit' is instantly understood; without context, it could mean a bank transaction.",
        "try_task": "Before your next listening, give learners one sentence of context only. Measure whether comprehension improves compared to no context. Debrief what changed.",
        "tags": "ELT365, teacher training, ELT, receptive skills, listening, context",
        "meta": "Context before a listening task mirrors real communication and aids comprehension. ELT365 Day 176.",
    },
    {
        "day": 177, "title": "Reading speed and fluency",
        "idea": "Slow reading is often caused by word-by-word processing. Fluent readers chunk language: they process phrases, not individual words. Speed improves with volume and with learning to tolerate unknown words.",
        "example": "A learner who stops at every unfamiliar word loses the thread of the sentence. Training them to read on and infer from context improves both speed and comprehension.",
        "try_task": "Set a timed reading: 200-word text, 90 seconds. Ask two comprehension questions. Do not let learners re-read. Debrief: what did they get? What did they miss?",
        "tags": "ELT365, teacher training, ELT, receptive skills, reading fluency",
        "meta": "Chunking and tolerating ambiguity build reading speed in L2 learners. ELT365 Day 177 teacher micro-lesson.",
    },
    {
        "day": 178, "title": "Learner strategies for unknown words",
        "idea": "Learners who encounter an unknown word have four options: guess from context, infer from word form, ignore it, or look it up. Teaching the first three explicitly reduces dependency on dictionaries mid-task.",
        "example": "'The company was insolvent.' A learner who notices the prefix 'in-' and suffix '-ent' and knows 'solve' can construct a working meaning without a dictionary.",
        "try_task": "Teach one word-attack strategy this week: prefix/suffix analysis. Give five unknown words with shared affixes. Ask learners to guess meanings before checking.",
        "tags": "ELT365, teacher training, ELT, receptive skills, vocabulary, learning strategies",
        "meta": "Teaching word-attack strategies reduces mid-text dictionary dependence. ELT365 Day 178 micro-lesson.",
    },
    {
        "day": 179, "title": "Grading comprehension questions",
        "idea": "Comprehension questions should move from easier to harder: gist first, then detail, then inference, then personal response. Scrambling this order adds unnecessary difficulty and confuses less confident learners.",
        "example": "Q1: What is the article about? (gist) → Q2: When did the event happen? (detail) → Q3: Why does the writer use the word 'catastrophic'? (inference).",
        "try_task": "Take five comprehension questions from a coursebook unit. Sort them: gist, detail, inference, evaluation. Does the original order match? Resequence if it doesn't.",
        "tags": "ELT365, teacher training, ELT, receptive skills, task design, reading",
        "meta": "Sequencing comprehension questions from gist to inference improves task design. ELT365 Day 179.",
    },
    {
        "day": 180, "title": "Receptive to productive — the bridge",
        "idea": "A receptive task should not end with comprehension. The best lessons bridge to production: learners discuss, react, write, or apply what they have read or heard. The text becomes a springboard.",
        "example": "After reading an opinion article, learners write a 50-word response agreeing or disagreeing. The text gave them the ideas and some of the language; now they use both.",
        "try_task": "Add one productive follow-up task to a receptive lesson you already teach. It should reuse at least two pieces of language from the text and ask for the learner's opinion.",
        "tags": "ELT365, teacher training, ELT, receptive skills, lesson design, integration",
        "meta": "Bridging from receptive to productive tasks completes the learning loop. ELT365 Day 180 teacher training.",
    },
    {
        "day": 181, "title": "Month 6 review — receptive skills",
        "idea": "This month covered: receptive skill types · top-down/bottom-up · gist and detail tasks · skimming and scanning · authentic vs graded texts · pre-teaching · inference · genre · bridging to production. One big idea: give listening and reading a purpose before learners start.",
        "example": "A lesson without a gist task is like giving learners a destination without telling them which city they're going to. Purpose first; language second.",
        "try_task": "Which of this month's ideas will you try first? Write one sentence: the lesson, the day number, and what you'll change. Share it with a colleague.",
        "tags": "ELT365, teacher training, ELT, receptive skills, review",
        "meta": "Month 6 review of ELT365 receptive skills lessons D152–D180. Key principles for listening and reading teachers.",
    },
    # ── Month 7: Productive Skills (D182–D212) ───────────────────────────────
    {
        "day": 182, "title": "What productive skills are",
        "idea": "Productive skills are speaking and writing — skills where meaning flows out. Learners encode messages in real time (speaking) or across drafts (writing). Both require control of accuracy and fluency.",
        "example": "Answering a question in class is productive. Writing a complaint email is productive. Both require choosing words, constructing sentences, and attending to the listener or reader.",
        "try_task": "Ask learners to tell a partner one thing they did yesterday (speaking) then write it down (writing). Compare: what changed? What was harder?",
        "tags": "ELT365, teacher training, ELT, productive skills, speaking, writing",
        "meta": "Speaking and writing are active productive skills. ELT365 Day 182 — 5-minute teacher training micro-lesson.",
    },
    {
        "day": 183, "title": "Accuracy vs fluency — the distinction",
        "idea": "Accuracy means producing language correctly; fluency means producing it smoothly, without unnatural pause. Most learners have more of one than the other. Good lessons develop both, but not at the same moment.",
        "example": "A controlled grammar drill targets accuracy. A 2-minute 'tell your partner about your weekend' targets fluency. Running them together undermines both.",
        "try_task": "Label your next lesson's speaking activities: A (accuracy) or F (fluency). If all are A, add one free-speaking stage at the end. If all F, add one focused form stage earlier.",
        "tags": "ELT365, teacher training, ELT, productive skills, speaking, accuracy, fluency",
        "meta": "Accuracy and fluency are different goals needing different lesson stages. ELT365 Day 183 teacher micro-lesson.",
    },
    {
        "day": 184, "title": "Controlled practice vs free practice",
        "idea": "Controlled practice limits what learners can say — substitution tables, gap-fills spoken aloud, sentence prompts — to build accuracy. Free practice removes those constraints. Both are necessary. Neither alone is sufficient.",
        "example": "Controlled: 'I went to… last week.' learners substitute a destination from a list. Free: 'Tell your partner about a trip you took.'",
        "try_task": "Design one controlled speaking activity and one free speaking activity for the same grammar point. Sequence controlled before free. Check: does the controlled stage genuinely prepare learners for the free one?",
        "tags": "ELT365, teacher training, ELT, productive skills, speaking, PPP",
        "meta": "Controlled then free practice sequences accuracy before fluency. ELT365 Day 184 — five-minute ELT micro-lesson.",
    },
    {
        "day": 185, "title": "Drilling — why and how",
        "idea": "A drill is a short, focused repetition practice used to establish pronunciation, form, or chunks in learners' mouths. Choral drill first (whole class together), then individual. Keep it brisk; pace replaces boredom.",
        "example": "Target: 'I haven't been there yet.' Choral: all repeat. Then nominate: 'You — again.' 'You — again.' Ten repetitions in 90 seconds.",
        "try_task": "Pick a sentence your class produced incorrectly last week. Run a 60-second back-chained drill: start with the last word, add chunks backwards until learners say the full sentence correctly.",
        "tags": "ELT365, teacher training, ELT, productive skills, drilling, pronunciation",
        "meta": "Drilling establishes form and pronunciation through focused repetition. ELT365 Day 185 — CELTA-aligned micro-lesson.",
    },
    {
        "day": 186, "title": "Pairwork and groupwork in speaking",
        "idea": "Pairwork and groupwork multiply speaking time. In a class of 20, teacher-led speaking means each learner speaks for under two minutes per hour. In pairs, every learner speaks simultaneously. STT rises; TTT falls.",
        "example": "Ten minutes of teacher-fronted Q&A: each learner speaks for about 30 seconds. Ten minutes of pairwork discussion: each learner speaks for about 4 minutes.",
        "try_task": "Time your TTT (teacher talking time) in one lesson this week. Note it. Next lesson, replace 5 minutes of teacher explanation with a peer-discussion task. Compare the two.",
        "tags": "ELT365, teacher training, ELT, productive skills, classroom management, speaking",
        "meta": "Pairwork and groupwork maximise student talking time. ELT365 Day 186 — 5-minute teacher training micro-lesson.",
    },
    {
        "day": 187, "title": "Role plays — setting them up",
        "idea": "A role play gives learners a situation, a role, and a communicative aim. Setting it up takes longer than running it. Clear instructions (who, where, what you want) and a brief preparation time produce better language.",
        "example": "Situation: a hotel check-in. Student A: guest with a booking problem. Student B: receptionist. Aim: resolve the problem. Preparation: 2 minutes to note what you'll say.",
        "try_task": "Write role-play cards for a situation your class knows. Include: role + situation + one aim. No more than three sentences per card. Run it, then debrief language, not just content.",
        "tags": "ELT365, teacher training, ELT, productive skills, speaking, role play",
        "meta": "How to set up effective role plays with clear roles and aims. ELT365 Day 187 teacher training micro-lesson.",
    },
    {
        "day": 188, "title": "Information-gap tasks",
        "idea": "An information gap exists when two learners have different pieces of information and must communicate to complete a task. It creates genuine communicative purpose — learners need each other, not just a language structure.",
        "example": "Student A has a map with hotels; Student B has a map with restaurants. Together they plan a route. Neither can complete the task without the other.",
        "try_task": "Design one information-gap task for your current unit. Check: does each learner genuinely need what the other has? If both students could complete it alone, the gap doesn't exist.",
        "tags": "ELT365, teacher training, ELT, productive skills, speaking, task design",
        "meta": "Information-gap tasks create genuine communicative need in speaking lessons. ELT365 Day 188.",
    },
    {
        "day": 189, "title": "Discussions and debates in the classroom",
        "idea": "Discussions are less structured than debates but need the same scaffolding: a clear topic, opinion vocabulary pre-taught, and a task that requires interaction — not just turn-taking. The goal is genuine exchange.",
        "example": "Don't say: 'Discuss social media.' Say: 'You have 4 minutes to agree on one social media rule for your school. Report back.'",
        "try_task": "Take any discussion topic you use. Add a constraint that forces negotiation: a time limit, a shared decision, or a role (one person must disagree). See if the language becomes more purposeful.",
        "tags": "ELT365, teacher training, ELT, productive skills, speaking, discussions",
        "meta": "How to structure discussions and debates for genuine language use. ELT365 Day 189 teacher training.",
    },
    {
        "day": 190, "title": "Monitoring during speaking activities",
        "idea": "While learners speak, circulate quietly — close enough to hear, far enough not to interrupt. Note good language and errors for feedback. Don't hover over one pair; move to give every group equal attention.",
        "example": "During a 5-minute pairwork discussion, the teacher notes three good phrases and two systematic errors on a notepad. Neither is corrected mid-task.",
        "try_task": "In your next speaking task, carry a notepad divided into two columns: 'good language' and 'errors to address.' Use your notes for a 3-minute whole-class feedback stage at the end.",
        "tags": "ELT365, teacher training, ELT, productive skills, monitoring, feedback",
        "meta": "How and where to position yourself during speaking activities. ELT365 Day 190 micro-lesson for ELT teachers.",
    },
    {
        "day": 191, "title": "Error correction in speaking — delayed vs immediate",
        "idea": "Correct mid-fluency task: you interrupt flow and discourage risk-taking. Correct after the task: you address language without breaking communication. Immediate correction suits accuracy stages; delayed suits fluency stages.",
        "example": "During a role play (fluency), note 'She go to school yesterday' on your board. After the task, elicit the correct form from the class.",
        "try_task": "Choose one speaking activity you plan this week. Decide in advance: will you correct immediately or delay? Write it in your plan and explain why.",
        "tags": "ELT365, teacher training, ELT, productive skills, error correction, speaking",
        "meta": "When to correct errors in speaking tasks — delayed vs immediate. ELT365 Day 191 micro-lesson.",
    },
    {
        "day": 192, "title": "Reformulation — correction by restatement",
        "idea": "Reformulation means you restate what a learner said — correctly — without explicitly flagging the error. It is low-threat. Research suggests learners who notice the reformulation acquire the form faster than those who hear an explicit correction.",
        "example": "Learner: 'I goed to the market.' Teacher: 'Oh, you went to the market — what did you buy?' The correct form is provided naturally; communication continues.",
        "try_task": "In your next conversation-based lesson, recast at least five learner errors using reformulation only. After class: did any learner self-correct on the next attempt?",
        "tags": "ELT365, teacher training, ELT, productive skills, error correction, reformulation",
        "meta": "Reformulation corrects errors by restating correctly without interrupting. ELT365 Day 192 teacher training micro-lesson.",
    },
    {
        "day": 193, "title": "Elicitation — prompting self-correction",
        "idea": "Elicitation is prompting a learner to produce the correct form themselves rather than supplying it. A raised eyebrow, a repeated word with rising intonation, or a direct prompt all work. Self-correction is more memorable than teacher correction.",
        "example": "Learner: 'She don't like it.' Teacher (eyebrows raised): 'She…?' Learner: 'She doesn't like it.' Teacher: 'Yes, exactly.'",
        "try_task": "This week, replace three explicit corrections with elicitations. Use only a question word, a rising tone, or a gesture. Note how often learners self-correct correctly.",
        "tags": "ELT365, teacher training, ELT, productive skills, error correction, elicitation",
        "meta": "Eliciting self-correction builds language awareness and retention. ELT365 Day 193 — 5-minute micro-lesson.",
    },
    {
        "day": 194, "title": "Writing as process, not product",
        "idea": "Process writing treats the written text as the result of stages: brainstorm → plan → draft → revise → edit. Focusing only on the final product skips the thinking that produces good writing.",
        "example": "A product approach marks the essay. A process approach gives feedback on the plan, then the draft, then the final version. Learners improve between stages.",
        "try_task": "Add a planning stage to your next writing task. Give learners 5 minutes to write a bullet-point plan before drafting. Collect the plan, not the essay, for a first feedback round.",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, process writing",
        "meta": "Process writing trains thinking through drafting stages, not just final output. ELT365 Day 194 teacher micro-lesson.",
    },
    {
        "day": 195, "title": "Controlled writing — copying and gap-fill",
        "idea": "Controlled writing tasks limit what learners can write: copy a model, complete gaps in a text, unscramble sentences. They build accuracy and familiarity with form before free production is expected.",
        "example": "Learners read a model email of complaint and rewrite it changing name, date, and product. They focus on structure and phrases, not content invention.",
        "try_task": "Write a 6-sentence model paragraph in the genre your class is practising. Design a gap-fill version with five key phrases removed. Use it before any free writing task.",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, controlled practice",
        "meta": "Controlled writing builds accuracy with forms and phrases before free production. ELT365 Day 195 micro-lesson.",
    },
    {
        "day": 196, "title": "Guided writing — sentence frames and models",
        "idea": "Guided writing sits between controlled and free. Sentence frames, partial texts, and model analysis give learners structural support while allowing some choice of content. It works well at A2–B1.",
        "example": "'I am writing to complain about… On [date], I… I would like you to…' The frame is given; the learner fills in the specifics.",
        "try_task": "Write three sentence frames for a writing type your class needs (email, report, story). Share the frames on the board. Learners complete them with their own content. Compare outputs.",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, guided writing",
        "meta": "Guided writing frames support structure while allowing content choice. ELT365 Day 196 — five-minute ELT lesson.",
    },
    {
        "day": 197, "title": "Free writing — generating fluency",
        "idea": "Free writing gives learners a topic and minimal constraints. It is the writing equivalent of a fluency task: quantity over accuracy, ideas over form. Timed free writing removes the blank-page paralysis many learners feel.",
        "example": "'Write everything you know about your favourite place for 5 minutes. Don't stop. Don't correct. Just write.' Learners are often surprised by how much they produce.",
        "try_task": "Try a 3-minute timed free write with your class on a topic they know well. No correction, no stopping. Read one or two aloud without identifying the author. Debrief: what ideas came out?",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, fluency",
        "meta": "Free writing builds writing fluency and overcomes blank-page paralysis. ELT365 Day 197 teacher training.",
    },
    {
        "day": 198, "title": "Writing for a purpose and audience",
        "idea": "Every real piece of writing has a writer, a reader, a purpose, and a context. Classroom writing tasks that specify all four produce more purposeful, better-organised work than open prompts.",
        "example": "'Write a letter to your city council asking for a new cycle lane on your street' is more generative than 'Write about transport.'",
        "try_task": "Take your next writing task prompt. Add: who is writing, who is reading, and what the writer wants. Check whether this changes how learners approach and organise their text.",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, task design",
        "meta": "Specifying audience and purpose produces more purposeful writing tasks. ELT365 Day 198 micro-lesson.",
    },
    {
        "day": 199, "title": "Paragraph structure — topic sentence and support",
        "idea": "A paragraph in academic or formal writing typically opens with a topic sentence (the main idea), followed by supporting sentences (evidence, example, detail). Teaching this pattern explicitly reduces disorganised writing.",
        "example": "'Urban cycling reduces congestion.' (topic) 'A 2024 study of 12 European cities found a 15% drop in rush-hour traffic after cycle lanes were added.' (support).",
        "try_task": "Give learners three topic sentences. Ask them to write two supporting sentences for each. Mark only coherence, not grammar. Discuss: does each sentence genuinely support the claim?",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, paragraph structure",
        "meta": "Topic sentence plus support is the building block of academic paragraphs. ELT365 Day 199.",
    },
    {
        "day": 200, "title": "Cohesion and coherence in writing",
        "idea": "Cohesion is the surface-level linking of sentences (pronouns, connectors, lexical chains). Coherence is the underlying logical flow of ideas. Both are needed; you can have cohesion without coherence.",
        "example": "Cohesive but not coherent: 'I like swimming. Moreover, the sky is blue. Therefore, fish are wet.' Each connector is used correctly; the paragraph makes no sense.",
        "try_task": "Take a learner paragraph (anonymised). Underline all cohesive devices. Then ask: does the argument flow logically? Where does coherence break down? Feed back on both.",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, cohesion, coherence",
        "meta": "Cohesion links sentences; coherence makes ideas flow logically. ELT365 Day 200 — teacher training micro-lesson.",
    },
    {
        "day": 201, "title": "Linking words and discourse markers",
        "idea": "Linking words (however, therefore, in addition) signal logical relationships between ideas. Discourse markers (right, anyway, so) organise speech. Both are often memorised incorrectly — learners need meaning, not just a word list.",
        "example": "'Although' signals contrast within one sentence; 'However' contrasts two sentences. They cannot be swapped. Learners who memorise both as 'contrast words' often misuse them.",
        "try_task": "Test whether your learners know the difference between 'although' and 'however' by giving both sentence positions. If confusion exists, teach the grammar, not just the word.",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, grammar, connectors",
        "meta": "Linking words need meaning taught, not just lists memorised. ELT365 Day 201 teacher training micro-lesson.",
    },
    {
        "day": 202, "title": "Peer editing in writing tasks",
        "idea": "Peer editing asks learners to review each other's drafts before a final version. It develops critical reading, reduces teacher correction load, and gives writers a real audience. It needs training to work well.",
        "example": "First time: give learners two specific things to look for — topic sentence and one linking word. Don't ask for general 'comments'; learners don't yet know what good writing looks like.",
        "try_task": "Design a peer-editing checklist with exactly three items for a writing type your class just practised. Items should be binary: yes/no, not 'is the writing good?'",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, peer feedback",
        "meta": "Peer editing gives writers a real audience and trains critical reading. ELT365 Day 202 micro-lesson.",
    },
    {
        "day": 203, "title": "Teacher written feedback — minimal marking",
        "idea": "Minimal marking uses codes in the margin (sp = spelling, gr = grammar, ww = wrong word) rather than rewriting learners' sentences. It requires learners to locate and correct errors themselves, which is more memorable.",
        "example": "Teacher writes 'gr' beside 'She don't like.' Learner finds the error, identifies it as subject-verb agreement, corrects it. One minute of engagement versus one second of reading a correction.",
        "try_task": "Choose four marking codes. Introduce them to learners before the next writing task. Use only those codes on their drafts. Set 10 minutes in class for learners to find and correct their errors.",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, feedback, marking",
        "meta": "Minimal marking codes make learners work to find and fix their own errors. ELT365 Day 203 micro-lesson.",
    },
    {
        "day": 204, "title": "The writing conference — one-to-one feedback",
        "idea": "A writing conference is a brief (3–5 minute) one-to-one conversation between teacher and learner about a draft. The teacher asks questions rather than supplies answers. Talking about writing often unlocks what the learner meant to say.",
        "example": "Teacher: 'What are you trying to say in this paragraph?' Learner explains clearly. Teacher: 'Can you write that? It's better than what you have.'",
        "try_task": "In your next writing lesson, conference with three learners for 3 minutes each while the rest continue drafting. Ask only questions; do not correct. Note what happens.",
        "tags": "ELT365, teacher training, ELT, productive skills, writing, feedback",
        "meta": "Writing conferences use questions to unlock what learners meant to write. ELT365 Day 204 teacher training.",
    },
    {
        "day": 205, "title": "Speaking sub-skills — stress and intonation",
        "idea": "Stress and intonation carry meaning in spoken English. A sentence stressed differently changes its meaning or politeness level. Teaching these explicitly improves both production and listening comprehension.",
        "example": "'I didn't say she stole the money.' Stress each word in turn and the implied meaning shifts with each repetition. Seven words; seven meanings.",
        "try_task": "Write one sentence with at least six words. Read it aloud with the stress on a different word each time. Ask learners to say what changes. They'll remember stress for the rest of the course.",
        "tags": "ELT365, teacher training, ELT, productive skills, speaking, pronunciation, stress",
        "meta": "Sentence stress shifts meaning and politeness. How to teach it. ELT365 Day 205 — 5-minute teacher training.",
    },
    {
        "day": 206, "title": "Fluency activities — anecdote and storytelling",
        "idea": "Anecdote tasks ask learners to tell a personal story in 2–3 minutes. They are highly motivating, language-rich, and generate natural spoken grammar — ellipsis, discourse markers, backchannelling. Minimal teacher input required.",
        "example": "'Tell your partner about a time things went wrong on a journey.' No grammar target. No vocabulary list. Just a human story that everyone has.",
        "try_task": "Run a 3-minute anecdote task this week. While learners talk, listen for good language and one shared error. Run a 2-minute language feedback using examples from what you heard.",
        "tags": "ELT365, teacher training, ELT, productive skills, speaking, fluency, storytelling",
        "meta": "Anecdote tasks generate natural spoken grammar and high learner motivation. ELT365 Day 206 micro-lesson.",
    },
    {
        "day": 207, "title": "Task-Based Learning in productive skills",
        "idea": "In Task-Based Learning (Willis), learners complete a communicative task first; language work comes second. The task creates real communicative need; the language feedback addresses what they needed to do it better.",
        "example": "Task: plan a class event (date, venue, menu, budget). Learners negotiate in English. Post-task: teacher highlights useful language from what she heard during monitoring.",
        "try_task": "Design a TBL speaking task: a decision with a real outcome your class cares about. Run the task with no pre-teaching. Note what language they attempt. Feed that back after.",
        "tags": "ELT365, teacher training, ELT, productive skills, speaking, TBL, task-based learning",
        "meta": "Task-Based Learning makes communication drive the lesson, language follows. ELT365 Day 207 micro-lesson.",
    },
    {
        "day": 208, "title": "The four-stage production model",
        "idea": "A full productive lesson moves through four stages: exposure to model language → focus on form and meaning → controlled practice → free production. Skipping stages is common; each skip costs accuracy or confidence.",
        "example": "Skipping the model (stage 1) means learners write free essays without knowing what good writing looks like. Skipping controlled practice means free production is too hard too fast.",
        "try_task": "Map your last writing or speaking lesson against these four stages. Which did you include? Which did you skip? Would adding the missing stage have changed the output?",
        "tags": "ELT365, teacher training, ELT, productive skills, lesson planning, PPP",
        "meta": "The four-stage productive lesson: model, form, controlled, free. ELT365 Day 208 teacher micro-lesson.",
    },
    {
        "day": 209, "title": "Integrating skills — speaking leads to writing",
        "idea": "Skills rarely operate in isolation in the real world. Lessons that move from speaking to writing (or reading to speaking) better reflect authentic language use and give learners content and language for the next stage.",
        "example": "Learners discuss opinions on remote working (speaking). Notes from the discussion become the plan for a written argument (writing). The speaking generated content; the writing organised it.",
        "try_task": "Chain two skills in your next lesson: a 5-minute speaking task feeds directly into a 10-minute writing task on the same topic. Compare the writing quality to standalone tasks.",
        "tags": "ELT365, teacher training, ELT, productive skills, skills integration, speaking, writing",
        "meta": "Integrating speaking and writing mirrors real-world language use. ELT365 Day 209 teacher training micro-lesson.",
    },
    {
        "day": 210, "title": "Assessing productive skills formatively",
        "idea": "Formative assessment in productive skills captures evidence of progress during learning, not just at the end. Observation, self-assessment, and peer feedback all serve this purpose without requiring formal tests.",
        "example": "A speaking checklist learners complete after a role play: 'Did I use three linking words? Did I ask at least two questions?' takes 2 minutes and builds metacognitive awareness.",
        "try_task": "Write a three-item self-assessment checklist for a speaking or writing task you plan this week. Give it to learners after the task. Read their responses before the next lesson.",
        "tags": "ELT365, teacher training, ELT, productive skills, assessment, formative assessment",
        "meta": "Formative assessment in speaking and writing tracks progress without tests. ELT365 Day 210 micro-lesson.",
    },
    {
        "day": 211, "title": "The productive classroom — STT over TTT",
        "idea": "Student Talking Time (STT) and Student Writing Time should dominate a productive-skills lesson. If the teacher is talking for more than 30% of the time, learners are not practising the skill the lesson is meant to teach.",
        "example": "A 60-minute speaking lesson: 10 minutes setup/feedback (TTT), 50 minutes pair and group speaking (STT). That ratio is achievable. Many classrooms invert it.",
        "try_task": "Set a timer for your next lesson. Every 10 minutes, note: who was talking — teacher or learners? If TTT exceeds 40%, redesign the delivery stage as a peer task instead.",
        "tags": "ELT365, teacher training, ELT, productive skills, classroom management, STT, TTT",
        "meta": "Student talking time should dominate any productive skills lesson. ELT365 Day 211 teacher training.",
    },
    {
        "day": 212, "title": "Month 7 review — productive skills",
        "idea": "This month covered: accuracy vs fluency · controlled/free practice · drilling · pairwork · role play · information gap · error correction strategies · writing as process · paragraph structure · cohesion · TBL · skills integration. Central principle: learners improve by producing, not by watching.",
        "example": "A learner who writes three drafts improves more than one who reads three model essays. A learner who speaks for 20 minutes improves more than one who listens to perfect examples for 20 minutes.",
        "try_task": "Choose one technique from this month you have not tried before. Commit to using it in the next two lessons. Note what happened. That is your professional development.",
        "tags": "ELT365, teacher training, ELT, productive skills, review",
        "meta": "Month 7 review of ELT365 productive skills lessons D182–D211. Key principles for speaking and writing teachers.",
    },
]

DISCLAIMER_TEXT = ("<hr><p><em>Independent project; not affiliated with, endorsed by, "
                   "or accredited by Cambridge University Press &amp; Assessment. "
                   "Confers no qualification.</em></p>")

def build_html(lesson):
    return (
        f'<p><strong>Idea —</strong> {lesson["idea"]}</p>'
        f'<p><strong>Example —</strong> {lesson["example"]}</p>'
        f'<p><strong>Try —</strong> {lesson["try_task"]}</p>'
        + DISCLAIMER_TEXT
    )

def wp_post(lesson):
    day = lesson["day"]
    title_full = f"ELT365 · Day {day:03d} — {lesson['title']}"
    seo_title  = f"{lesson['title']} | ELT365 Day {day:03d} | Sourov Deb"[:70]
    payload = {
        "title":            title_full,
        "content":          build_html(lesson),
        "status":           "draft",
        "category":         "English Teaching",
        "tags":             lesson["tags"],
        "meta_description": lesson["meta"][:155],
        "seo_title":        seo_title,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        WP_ENDPOINT,
        data=data,
        headers={
            "X-Sourov-Key":  WP_KEY,
            "Content-Type":  "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as exc:
        return 0, str(exc)

def main():
    print(f"Publishing {len(LESSONS)} ELT365 lessons as drafts ...\n")
    results = []
    for i, lesson in enumerate(LESSONS, 1):
        status, body = wp_post(lesson)
        ok = "OK" if status in (200, 201) else "FAIL"
        print(f"[{i:02d}/{len(LESSONS)}] D{lesson['day']:03d} {ok} HTTP {status} — {lesson['title']}")
        results.append({"day": lesson["day"], "title": lesson["title"], "http": status, "response": body})
        if i < len(LESSONS):
            time.sleep(1.2)

    ok_count   = sum(1 for r in results if r["http"] in (200, 201))
    fail_count = len(results) - ok_count
    print(f"\n{ok_count} published as drafts  {fail_count} failed")

if __name__ == "__main__":
    main()
