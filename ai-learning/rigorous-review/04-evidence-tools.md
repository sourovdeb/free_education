# Make the evidence inspectable before adding tools

## The suggestion

You could begin with a small evidence packet before connecting a large Library. Give each record a stable ID such as `E1` and retain its title, origin, date/version, precise locator, relevant passage and source family.

**Why:** an ID traces the claim to a passage. A source family distinguishes copies from independent evidence. A coverage record identifies material not examined.

## Storage is not retrieval

![Files, Libraries and Upload file](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-05-files-libraries.png)

You could test access with a distinctive passage. Uploading a file is not proof that an Agent can retrieve it; successful retrieval is not proof that the whole archive was examined.

## Add function

The supplied example is `read_evidence_record`, whose argument is `evidence_id`. The exact schema is `schemas/read_evidence_record.parameters.json`; the wrapper is separate.

The annotated function screenshot in the downloadable guide identifies 1 Name, 2 Description, 3 Strict, 4 Parameters and 5 Confirm. This describes a callable operation, not the code that executes it.

The implementation still needs to receive the ID, run the lookup and return the actual result. The included read-only helper uses the supplied packet; it is not a Drive, Library or Mistral connector.

## Keep three contracts separate

Function arguments describe the call. The evidence packet holds the material. The report schema describes the final answer. This distinction helps avoid pasting the report schema into a function-argument box.

The report's exact keys are `bottom_line`, `basis`, `main_uncertainty`, `confidence`, `next_action` and `reconsider_when`.

## The limits of checking

The v2 schema rejects empty or whitespace-only required text. The checker detects selected ID, locator and completion-state problems. However, a real reference can still accompany a false claim. The tests deliberately retain that limitation.

Matching an ID or quotation does not prove source support or authenticity. You could test a known ID, an unknown ID and a real-but-irrelevant reference, inspecting returned content rather than only a success message.

## Video walkthrough — to be added

Reserved for my demonstration, transcript and chapter notes. No video is embedded.

## Materials and basis

[Reader PDF with all six annotated screenshots](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-suggestions-and-why-reader-v1.pdf) · [Schemas, packet and helpers](https://sourovdeb.com/wp-content/uploads/2026/10/rigorous-review-complete-session-v2.zip)

Basis: companion sections 14–17 and 21, `templates/evidence_packet.json`, `schemas/` and `tools/` in the v2 archive. No live tool integration is claimed.
