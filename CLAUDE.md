# BC Crime Data Analysis

## Overview

R Markdown analysis of crime trends across British Columbia, Canada (2018-2023).
Built with R: ggplot2, dplyr, tidyr, scales, knitr, glue. Data source: `bc_crime.csv`.

## Commands

- **Knit report**: Open `BC Crime Data/Data Sets/BC CRIME.Rmd` in RStudio and click **Knit** (HTML or PDF output)
- No npm/build system. No CI/CD pipeline.

## Architecture

```
BC-CRIME-/
  BC Crime Data/Data Sets/   # Rmd files, CSV data, custom CSS
    BC CRIME.Rmd             # Main analysis report
    BC CRIME Worksheet.Rmd   # Exploration worksheet
    bc_crime.csv             # Source dataset (not in repo)
    custom.css               # Report styling
  docs/                      # Planning and learning loop documents
  .claude/skills/            # Claude skill definitions
  CLAUDE.md                  # This file
  README.md
```

## Conventions

- Use the existing `theme_bc_crime()` function for all ggplot2 charts
- Use `safe_pct_change()` for percentage change calculations (handles Inf/NaN)
- Use `bc_palette` for consistent colour assignments across charts
- Follow existing R patterns: tidyverse verbs, pipe operator, kable for tables
- All packages are auto-installed via the setup chunk at the top of the Rmd
- Never modify `bc_crime.csv` source data

## File Boundaries

**Safe to edit:**
- `BC Crime Data/Data Sets/*.Rmd` — analysis files
- `docs/` — planning and learning loop documents
- `CLAUDE.md` — this file
- `README.md`
- `.claude/skills/` — skill definitions

**Never touch:**
- `bc_crime.csv` — source data (must remain unmodified)
- `.env` — environment secrets

---

# Autonomous Learning Loop

You are operating in **discovery-first development** mode. You do NOT jump
straight into coding. Every iteration begins with expert interrogation of
the codebase, then implementation informed by what you found, then reflection
that feeds the next iteration.

## Document System

You maintain four living documents in `docs/`. If the `docs/` directory or
any file below does not exist, create it using the templates at the bottom
of this file before doing anything else.

| File | Purpose | You Read It | You Write It |
|------|---------|:-----------:|:------------:|
| `docs/plan.md` | Feature backlog and task tracking | Every iteration | After completing or blocking a task |
| `docs/questions.md` | Expert-generated Q&A about the codebase | Every iteration | Every Phase 1 |
| `docs/learnings.md` | Accumulated project knowledge | Every iteration | Every Phase 3 |
| `docs/session-log.md` | Timestamped record of each iteration | On startup | Every Phase 3 |

---

## Phase 1 — DISCOVER

**Time budget: ~30% of iteration.**

Before touching any code, adopt each expert persona below IN ORDER. For each
persona, generate 2-3 hard questions that person would ask about the CURRENT
TASK and the existing codebase. Then INVESTIGATE the codebase to answer each
question. Write both Q and A to `docs/questions.md` under today's date and
iteration number.

### Expert Personas

**1. Senior Developer**
Ask about: existing patterns and conventions this codebase already uses that
you must follow; hidden dependencies between modules; what will break if you
get this wrong; current test coverage for the area you are about to touch;
whether a similar feature was attempted before and reverted.

**2. Security Engineer**
Ask about: attack surfaces this change exposes or widens; authentication and
authorization gaps; input validation and sanitization; how secrets, tokens,
and credentials are handled; what happens with malicious, oversized, or
malformed input; OWASP-relevant concerns for this stack.

**3. Product Manager**
Ask about: whether the feature as scoped actually matches what a user needs;
edge cases a real user would hit in the first five minutes; whether you are
overbuilding or underbuilding; what the simplest version that ships looks
like; acceptance criteria that would let you call this done.

**4. Code Reviewer**
Ask about: whether the planned approach is idiomatic for this stack and
framework; naming consistency with the rest of the codebase; duplication
that should be extracted; readability for the next developer who touches
this; whether the abstractions are at the right level.

**5. DevOps / Ops Engineer**
Ask about: how this change affects deployment, build, or CI; new environment
variables or configuration required; behavior at scale or under load; failure
modes in production and how you would detect them; logging and observability
for the new code path.

**6. End User**
Ask about: whether the feature is intuitive without documentation; what
would confuse or frustrate you on first use; what is missing that you would
immediately ask for; whether error messages actually help you fix the problem;
accessibility and performance from the user's perspective.

### Rules for Phase 1

- Read the actual code BEFORE generating questions. Generic questions are
  worthless. Reference specific file names, function names, and line numbers.
- If a previous iteration already answered a question about the same area,
  do not re-ask it — read `docs/questions.md` and build on what is there.
- If you discover something urgent (a bug, a security hole, a broken test)
  that is NOT your current task, log it in `docs/plan.md` as a new task
  rather than fixing it now — stay focused.

---

## Phase 2 — IMPLEMENT

**Time budget: ~50% of iteration.**

1. Read `docs/plan.md` — pick the highest-priority incomplete task.
2. Read `docs/learnings.md` — apply accumulated knowledge from all
   previous iterations.
3. Read your Phase 1 answers from this iteration — use them to guide
   every implementation decision.
4. Write code following existing patterns discovered in Phase 1.
5. Run tests after every meaningful change.
6. On test pass → commit with a descriptive message.
7. On test fail → fix and re-run (max 3 attempts before declaring blocked).

### Rules for Phase 2

- Never start coding until Phase 1 is complete and written to
  `docs/questions.md`.
- If your Phase 1 Security Engineer persona raised a concern, address it
  in the implementation — do not defer it.
- If your Phase 1 Code Reviewer persona found naming inconsistencies in
  existing code, follow the EXISTING convention even if it is not ideal.
  Log the inconsistency in `docs/learnings.md` for the human to decide.
- Keep commits small and focused. One logical change per commit.

---

## Phase 3 — REFLECT

**Time budget: ~20% of iteration.**

Update all three output documents:

### 1. Append to `docs/learnings.md`

Add entries under the appropriate heading:

- **Patterns Discovered** — conventions, idioms, or architectural choices
  you found in the codebase that are not documented anywhere.
- **Gotchas & Pitfalls** — things that tripped you up; save the next
  iteration from the same mistake.
- **Architecture Decisions** — the inferred "why" behind code structures.
- **Missing Documentation** — things that should be documented but are not.
- **Dependencies & Relationships** — non-obvious connections between
  parts of the codebase.

If an entry is important enough to belong in CLAUDE.md permanently, tag it
with `[CLAUDE.MD-CANDIDATE]` so the human can promote it later.

### 2. Update `docs/plan.md`

- Mark completed tasks as `- [x]` and move them to the Completed section
  with today's date.
- Mark blocked tasks as `- [!]` and move them to the Blocked section with
  a note explaining the blocker.
- If you discovered new tasks during Phase 1 (bugs, tech debt, missing
  features), add them at the appropriate priority level.

### 3. Append to `docs/session-log.md`

Add an entry with:
- Iteration number and timestamp
- Which task you worked on
- What you discovered in Phase 1 (summary, not full Q&A)
- What you implemented in Phase 2
- Outcome: done, partial, or blocked
- Anything the human should review

---

## Time-Boxed Execution

When given a time budget (e.g., "work for 2 hours"):

- Each full iteration (discover + implement + reflect) = 1 task.
- If running low on time, finish the current task cleanly rather than
  starting a new one half-done.
- Always leave time for Phase 3 — knowledge that is not written down is
  lost between context windows.
- The last iteration should be a "wrap-up" that ensures all docs are
  current and the session log has a clear summary.

---

## Exit Conditions

Output `COMPLETE` (and stop) ONLY when:
- All tasks in `docs/plan.md` are marked done, OR
- Time budget is exhausted (do a final Phase 3 first), OR
- You hit a blocker you cannot resolve (document it fully).

Output `CONTINUE` if tasks remain and time remains.

Output `BLOCKED` if you cannot proceed (document the blocker in both
`docs/session-log.md` and `docs/plan.md`).

NEVER output `COMPLETE` if there are unfinished tasks and time remains.

---

## Quality Gates

Before marking ANY task as done, verify all of these:

- [ ] Tests pass
- [ ] No lint errors
- [ ] Changes committed to git with a descriptive message
- [ ] `docs/questions.md` has this iteration's expert Q&A
- [ ] `docs/learnings.md` is updated with anything new
- [ ] `docs/session-log.md` has this iteration's entry

---

## Bootstrapping

If `docs/plan.md` exists but the other files do not, create them using
the templates below. If `docs/plan.md` does not exist, create it with
the placeholder template and STOP — tell the human they need to fill in
the plan before the loop can run.

### Template: docs/plan.md

```markdown
# Feature Plan

> The human must fill this in before the loop can run.
> Use `- [ ]` for incomplete, `- [x]` for done, `- [!]` for blocked.

## Priority 1: [Feature Name]
> Description of what this feature does and why.

- [ ] Task 1
- [ ] Task 2
- [ ] Write/update tests

## Priority 2: [Feature Name]
> Description.

- [ ] Task 1
- [ ] Task 2

## Blocked

## Completed
```

### Template: docs/questions.md

```markdown
# Expert Review Questions & Answers

> Each iteration, Claude adopts expert personas and generates hard questions
> about the codebase, then investigates to answer them. Grouped by date and
> iteration number. Reference specific files, functions, and line numbers.

---
```

### Template: docs/learnings.md

```markdown
# Project Learnings

> Accumulated knowledge discovered through the learning loop. Read at the
> start of every iteration so knowledge persists across context windows.
> Tag entries with [CLAUDE.MD-CANDIDATE] if they should be promoted to
> CLAUDE.md by the human.

---

## Patterns Discovered

## Gotchas & Pitfalls

## Architecture Decisions

## Missing Documentation

## Dependencies & Relationships
```

### Template: docs/session-log.md

```markdown
# Session Log

> Timestamped record of each iteration. Helps the human see what happened
> and helps Claude pick up where it left off if context resets.

---
```

---

## Running the Loop

### Option A: Native `/loop` (inside Claude Code)

```
/loop 15m Follow the Autonomous Learning Loop instructions in CLAUDE.md.
Execute one full iteration: Phase 1 (discover), Phase 2 (implement),
Phase 3 (reflect). End with COMPLETE, CONTINUE, or BLOCKED.
```

### Option B: Shell script (from terminal)

```bash
#!/bin/bash
# Save as run-loop.sh — chmod +x run-loop.sh
MAX_ITERATIONS=20
PROMPT='Follow the Autonomous Learning Loop instructions in CLAUDE.md.
Execute one full iteration: Phase 1 (discover), Phase 2 (implement),
Phase 3 (reflect). End with COMPLETE, CONTINUE, or BLOCKED.'

git checkout -b "auto/loop-$(date +%Y%m%d-%H%M%S)" 2>/dev/null

for i in $(seq 1 $MAX_ITERATIONS); do
    echo "=== Iteration $i / $MAX_ITERATIONS ==="
    output=$(claude --print --dangerously-skip-permissions "$PROMPT" 2>&1) || true
    echo "$output"
    echo "$output" | grep -q "COMPLETE" && echo "All tasks done." && exit 0
    echo "$output" | grep -q "BLOCKED" && echo "Blocked. See docs/session-log.md" && exit 1
    sleep 3
done
echo "Max iterations reached. See docs/ for progress."
```

Run inside tmux so it survives terminal close:
```bash
tmux new -s loop
./run-loop.sh
# Ctrl+B, D to detach — tmux attach -t loop to come back
```

### Option C: One-shot (manual in Claude Code)

Open Claude Code in the project and say:

> Follow the Autonomous Learning Loop in CLAUDE.md. You have 90 minutes. Go.

---

## When You Come Back

Check these in order:

1. **`docs/session-log.md`** — what happened, what got done, any blockers
2. **`docs/plan.md`** — what is checked off, what remains
3. **`docs/learnings.md`** — search for `[CLAUDE.MD-CANDIDATE]` and promote
   good entries into the Conventions section at the top of this file
4. **`docs/questions.md`** — the accumulated expert Q&A about your codebase
5. **`git log --oneline`** — review commits on the feature branch
