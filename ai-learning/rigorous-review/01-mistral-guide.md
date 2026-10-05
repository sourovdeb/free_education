# Start with one useful Mistral assistant

## A suggestion to start with

You could begin with one saved Prompt, one Agent and one small synthetic evidence packet. There is no need to build the whole automation system before finding out whether the review method helps.

**Why:** a small first version makes it easier to check the instructions, evidence and output separately.

In the supplied guide, the model generates the answer; a Prompt stores instructions; an Agent combines a model with instructions and available tools; a Skill packages a reusable method and supporting resources. A workflow describes the later sequence and recovery rules. Saving a prompt is not model training.

## Suggested click-through route

![Sidebar: 1 Prompts, 2 Skills, 3 Agents, 4 Knowledge, 5 Workflows](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-01-navigation.png)

You could begin with Prompts and Agents. The supplied screenshots show a particular interface; the visible menu names are more useful than assuming the surrounding headings never change.

![Prompt title, description, identifier, body and Create](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-02-prompt.png)

| Field | Suggested entry | Reason |
|---|---|---|
| Title | Rigorous Review — Core | Recognisable canonical text. |
| Description | Evidence-led review of claims and decisions; returns a defensible six-part answer. | Describes the task rather than promising exceptional intelligence. |
| Identifier | `rigorous-review-core` | A stable, readable identity. |
| Body | Complete `prompts/CORE_INSTRUCTIONS.txt` from the technical package | Preserves important qualifications. |

You could paste the same core into the Agent's actual Instructions field, choose an available model and save it as Rigorous Review. The Create Agent naming dialog does not replace the Instructions field. Metadata labels can wait until the first test works.

## A small check before adding more

Try T02 with the whole synthetic evidence packet. It asks whether one favourable lesson record settles an overall course decision. The supplied example distinguishes the lesson from the broader criterion and leaves the overall decision unresolved. This is a logic exercise, not a finding about a real institution.

A saved Prompt or Skill does not prove that an Agent loads it. A fresh test is where that assumption can be examined. Current permissions and model availability were not verified for this editorial edition.

**Next step to try:** save the core and run the synthetic packet before connecting private files or external services.

## Video walkthrough — to be added

This section is reserved for my video on setting up the assistant. No video is embedded yet. Its transcript and chapter notes can be added here when available.

## Materials and basis

[Reader PDF — all eight resources and six screenshots](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-suggestions-and-why-reader-v1.pdf)

[Preserved technical archive](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-complete-session-v2.zip)

Basis: the v2 companion, sections 2–3 and 6–13; canonical core; synthetic evidence packet. Source-derived editorial adaptation, not a new installation or model test.
