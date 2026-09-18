# Failure and retry policy

Use one of these reason codes:

| Code | Meaning |
|---|---|
| `BASE_BUILD_FAILED` | updated `main` does not compile before the feature branch |
| `WORKTREE_DIRTY` | unrelated local changes prevent safe execution |
| `REMOTE_DIVERGED` | local and remote feature branch do not share the expected HEAD |
| `DISCOVERY_BUDGET_EXHAUSTED` | bounded discovery reached its configured limit before closing a relevant gap |
| `EVIDENCE_INSUFFICIENT` | available knowledge/source evidence cannot support a reliable AS-IS conclusion |
| `KNOWLEDGE_STALE` | persisted knowledge is known or strongly indicated to be outdated for the requested area |
| `HANDOFF_MISSING` | a story refinement needs AS-IS context and no related `SPECKIT_HANDOFF` exists |
| `HUMAN_DECISION_REQUIRED` | a business/intent ambiguity cannot be answered by story, knowledge or code |
| `STORY_CONFLICTS_WITH_AS_IS` | the story contradicts an observed behavior or compatibility constraint without saying it changes |
| `PLAN_INVALID` | SPEC/DESIGN/TASKS or traceability is incomplete |
| `PLAN_CHANGED` | an approved plan digest differs from the execution baseline |
| `UNIT_TEST_FAILED` | required focused unit test failed |
| `SOLUTION_BUILD_FAILED` | full solution build failed after a TASK |
| `ENVIRONMENT_BLOCKED` | SDK, service, credential, network, or runner prevented a conclusive gate |
| `PUSH_BLOCKED` | validated commit could not be published |
| `REGRESSION_FAILED` | complete regression found a reproducible failure |
| `REGRESSION_UNSTABLE` | failure passed on the single diagnostic rerun |

Implementation uses at most two focused correction attempts total per TASK, shared across unit test and solution build. Regression permits one diagnostic rerun without changes. Git synchronization never authorizes force, reset, automatic merge, or unbounded retries. Push is allowed only after gates pass and with skill-generated artifacts excluded from publication.

Every block records: code, first relevant error, commands, attempts, changed files, current branch/HEAD, and the smallest human action needed to resume.
