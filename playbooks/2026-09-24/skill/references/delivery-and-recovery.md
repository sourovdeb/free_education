# Delivery and recovery

## Authority table

| Action | Required authorization |
|---|---|
| Inspect relevant account evidence | User task and available access |
| Create playbook and local fixes | Implied by the task |
| Email the user | Explicit email request |
| Contact employer or buyer | Separate recipient-directed authorization |
| Publish requested repository files | User's publication request |
| Pause existing automations | User's change instruction |
| Schedule requested review | User's future-work request |
| Submit applications or accept terms | Explicit action authorization |

Carry authorization across the session. Do not ask again without cause.

## Repository writes

Read repository instructions and visibility. Inspect the target branch and files. Preserve unrelated content and licenses. Follow required review workflows. Do not force push.

Add files to a scoped directory. Build from the current tree. Advance refs without forcing. If concurrent changes intervene, rebase safely. Read back expected file content. Record the verified commit privately.

Repository upload does not deploy Pages. A draft pull request remains unmerged. State that distinction in delivery.

## Email writes

Verify the user's account identity. Use existing authorization to send. Prefer HTML with accessible attachments. Avoid sandbox links inside email. Attach files or use recipient-accessible links.

Search exact subject before sending. Reuse completed delivery evidence. If send status is uncertain, inspect sent mail. Never immediately resend an uncertain action.

## Future review

Create a finite automation when requested. Verify each required app first. Supply timezone and artifact paths. Include source limits and privacy rules. Include exact completion and stopping criteria.

The prompt should ask for changes. Avoid recreating the whole project. If evidence is unchanged, say so. Send no duplicate report without purpose.

## Recovery record

Keep these fields privately:

- Artifact identity and current version.
- Repository branch, paths, commit.
- Email subject and send status.
- Automation identity and next execution.
- Remaining failure and next action.

If GitHub fails, preserve deliverables. Email the artifacts when authorized. Report the upload failure precisely.

If email fails, preserve repository work. Do not claim inbox delivery. Retry only after checking sent state.

If scheduling fails, deliver current work. State that future execution remains unset. Never imply a running background agent.
