# Stacked PRs + squash merge — demo

The same two-layer stack is built twice. Layer B edits a line that layer A introduced, and the repo **squash-merges**.

| | Scenario 1 — hand-rolled (`git` + `gh pr create`) | Scenario 2 — native (`gh stack`) |
|---|---|---|
| PRs | [#1](../../pull/1) ← [#2](../../pull/2) | [#3](../../pull/3) ← [#4](../../pull/4) |
| After squash-merging the bottom PR | #2 still carries A1/A2 → **CONFLICTING** | #4 auto-rebased + retargeted → **MERGEABLE / CLEAN** |
| Human work needed | `git rebase --onto` + force-push | none (`gh stack sync` just refreshes local) |

## Why it breaks

Squash merge creates a **new** commit `S` on `main` with a different SHA than `A1`/`A2`. PR B's branch still contains `A1`/`A2`, so git doesn't know they landed and tries to apply them again. B changed a line that A added, so the three-way merge conflicts.

```
main:  I ── S(#1)                 ← squash of A1+A2, new SHA
        \
B:       A1 ── A2 ── B1 ── B2     ← still carries A1/A2
```

## Scenario 1 — what actually happened

1. `gh pr merge 1 --squash --delete-branch` → **PR #2 was CLOSED, not retargeted.** gh deleted `manual-a` itself, and GitHub closes PRs whose base disappears. (Gotcha #1. GitHub only auto-retargets when *its* "delete head branch on merge" setting deletes the branch.)
2. Restored the branch, reopened #2 and retargeted it to `main` → `mergeable: CONFLICTING`, commits `A1, A2, B1, B2`.
3. `git rebase origin/main` → `CONFLICT (content): Merge conflict in manual.py` / `could not apply A1`. (Gotcha #2: a plain rebase replays A.)
4. The fix:
   ```bash
   git rebase --onto origin/main <old-tip-of-manual-a> manual-b   # add --update-refs for deeper stacks
   git push --force-with-lease
   ```
   → commits `B1, B2` only, merged cleanly.

## Scenario 2 — `gh stack`

```bash
gh stack init native-a      # commit A1, A2
gh stack add native-b       # commit B1, B2
gh stack submit --auto --open
gh stack merge 3 --squash --yes   # merge only the bottom layer
```
Straight after the squash merge of #3, GitHub rebased `native-b` on the server (committer `GitHub`, signature verified) and retargeted #4 to `main`: `MERGEABLE / CLEAN`, commits `B1, B2`. `gh stack sync` then rebased locally "adjusted for merged PR", and `gh stack merge 4 --squash` landed it.

## Takeaways

- You can keep squash merge **and** stacked PRs. Whatever rebases the child just has to rebase `--onto` the new trunk, **skipping the parent's old commits**.
- `gh stack` does exactly that, on the server, in the same operation as the merge.
- Caveats (public preview, v0.1.1 here): no auto-merge for stacks; merge through `gh stack merge` or the stack UI, not ad-hoc `gh pr merge --delete-branch`.
