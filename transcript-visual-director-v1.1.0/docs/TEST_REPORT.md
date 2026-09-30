# Test report

Candidate: 1.1.0
Source baseline: 1.0.0
Checked: 30 September 2026.

## Historical source evidence

The source report states:
33 tests passed.
No tests were skipped.
Linux used Python 3.13.
The PNG pipeline ran.
Resolve dry-run passed.

Those tests predate 1.1.0.
They do not validate changes.

## Candidate static checks

Reviewed during this upgrade:
- original package contents;
- manual fallback patch;
- source preservation rules;
- browser planner source;
- TypeSafe documentation;
- Manim documentation.

## Candidate runtime tests

Command:
`python3 -m unittest discover -s tests -v`

Result:
35 passed.
1 skipped.
0 failed.

The skipped test is:
`test_still_pipeline_with_mock_typesafe`

Reason:
`psutil` is unavailable here.
The candidate requires psutil.
No dependency installation was attempted.

Added tests cover:
- manual offline approval;
- truthful provider status;
- REVIEW bypass rejection.

## Still untested

Windows PowerShell execution.
Windows drive audit.
Manim animation rendering.
Live TypeSafe authentication.
Resolve media import.
Browser planner execution.
Target agent loading.

## Validation status

validation: OFFLINE_TESTS_PASS_WITH_SKIP
approval: NOT_REQUESTED
deployment: NOT_DEPLOYED

This is offline validation.
It does not test Windows.
It does not test Manim.
It does not test TypeSafe.
It does not test Resolve.
