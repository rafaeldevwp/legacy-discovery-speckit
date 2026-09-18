# Idempotent Git workflow

Read `.github/skill-contracts/{lifecycle,handoffs,failure-policy}.md`. Never stash, discard, reset, merge, rebase, or force without a separate human decision.

## Determine first run versus resume

- **First run:** `EXECUTION-FIX-NNNN.md` does not exist and there is no `[TASK-*]` commit for this FIX.
- **Resume:** the execution ledger exists or the feature branch contains commits for this FIX.
- If signals conflict, stop with `PLAN_INVALID`; do not guess.

## First run: establish a clean baseline

1. Verify the worktree is clean and `origin` matches the intended remote.
2. Confirm local and remote `main` exist.
3. Run:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
```

4. Execute the exact full-solution `build_command` from approved DESIGN **on updated main before creating the feature branch**.
5. If baseline build fails, create no branch and block with `BASE_BUILD_FAILED`.
6. Derive `feature/mmYYYY/descricao-curta`, confirm it does not exist locally/remotely, then create it from the validated main.
7. Create `EXECUTION-FIX-NNNN.md` with `base_commit`, `base_build`, `branch`, and `remote_url`.

The FIX keeps this base for its lifetime. Never refresh or merge `main` between TASKS.

## Resume

1. Verify the worktree is clean.
2. Read branch, base, and remote from `EXECUTION-FIX-NNNN.md`.
3. Run `git fetch origin`.
4. Switch to the recorded feature branch if necessary.
5. Verify local HEAD equals `origin/{feature-branch}` and the remote URL matches the recorded value.
6. Recompute SHA-256 for approved SPEC/DESIGN/TASKS and compare with `spec_digest`, `design_digest`, and `tasks_digest` from the ledger. Any difference blocks with `PLAN_CHANGED` and requires coordinated reapproval; never overwrite the baseline digests silently.

Any branch/remote divergence blocks with `REMOTE_DIVERGED`. Do not pull, merge, rebase, reset, or recreate the branch automatically.

## Publish one TASK

After gates pass and the TASK commit is created:

```bash
git push -u origin feature/mmYYYY/descricao-curta  # first published commit
git push origin feature/mmYYYY/descricao-curta     # later commits
```

Push only the recorded feature branch. Never push `main`, tags, or another branch. A failed push produces `PUSH_BLOCKED`; preserve the local commit and stop.
