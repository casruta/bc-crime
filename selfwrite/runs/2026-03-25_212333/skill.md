# Data Analysis README Quality Guide

## Scoring Rubric

| Dimension | Weight | What to look for |
|-----------|--------|-----------------|
| Factual Accuracy | 0.25 | Every number traces to source. No fabricated values. Caveats stated. |
| Structure & Navigation | 0.20 | TOC, Key Terms, Reproducibility section. Point-first sections. |
| Analytical Depth | 0.20 | Every finding answers "so what?" Patterns explained, not just described. |
| Register Discipline | 0.15 | Stays in target register throughout. No editorial anti-patterns. |
| Audience Calibration | 0.10 | Key terms defined on first use. Accessible without dumbing down. |
| Evidence Integration | 0.10 | Charts are evidence for claims, not standalone exhibits. |

## Common Weaknesses and Fixes

### 1. Fabricated derived values
**Before:** "By 2024, the index had fallen to 83.5" (calculated by applying YoY change to a value from 10 years prior)
**After:** "...with a further 7.4% year-over-year decrease in 2024"
**Lesson:** Never compute absolute values from partial data. If the source doesn't state the number, don't state it.

### 2. "Is consistent with" template overuse
**Before:** Used 4x in 2,400 words. Strongest AI signal in the draft.
**After:** Varied to "points to," "aligns with," "tracks with," "suggests"
**Lesson:** Any hedging construction used 3+ times in a piece flags as AI-generated. Map all hedge phrases before revision.

### 3. Chart references without analysis
**Before:** "Figure 15 displays individual violation trajectories"
**After:** "The divergence in individual violation trajectories carries a policy implication: the offences driving the decline differ from those driving the increase"
**Lesson:** Every chart reference should lead with the finding or implication, not the figure number.

### 4. Missing dual-audience calibration
**Before:** CSI, clearance rate, indexed growth used without definition
**After:** Key Terms section defines all technical concepts; base-100 indexing explained
**Lesson:** A Key Terms section costs 5 lines and removes the largest barrier for non-expert readers.

### 5. Rigid parallelism in list sections
**Before:** Five factors, each with identical structure (bold claim → elaboration → italic corrective)
**After:** Each factor given a distinct heading and varied internal structure
**Lesson:** Parallel structure beyond 3 items reads as generated. Break the template after the third item.

## Expert Questions to Ask

1. "Is every number in this piece traceable to a specific source, or was any value computed by the author?"
2. "Where does the text tell the reader what a chart shows rather than what it means?"
3. "If I search for any phrase that appears 3+ times, which ones am I finding?"
4. "Which terms would a general reader need defined that aren't defined?"
5. "Does every paragraph open differently, or is there a dominant opener pattern?"
6. "For each 'the data suggests X' construction, what would a skeptic ask?"

## Anti-Patterns

| Pattern | Why it fails |
|---------|-------------|
| Fabricating values from partial data | Introduces errors that undermine all other claims |
| "The [noun] [verb]ed" opener on every paragraph | Creates mechanical cadence, flags as AI |
| Enumerated pre-announcements ("Five factors...", "Three questions...") | More than 2 per piece reads as templated |
| Redundant summary table after detailed narrative | Wastes reader attention; keep one or the other |
| "Is consistent with" as universal hedge | Signals AI caution rather than analytical judgment |

## Humanization Techniques

### Synonym Substitution Patterns
- Highest acceptance rate: adjectives and verbs (13/15 accepted)
- Register 2 direction: domain-specific over generic ("posted" over "recorded", "corroborates" over "confirms")
- Rejected: words that clash with existing terminology ("register" when geographic registers exist) or sound literary ("recede")

### Transition Diversity
- "The [noun]..." openers need breaking with subordinate clauses, prepositional phrases, or short punchy sentences
- Avoid cycling through "However/Moreover/Furthermore" -- better to use topic-noun repetition or contrastive pairs

### AI-Tell Elimination
- "Is consistent with" was the hardest pattern to eliminate (deeply embedded in analytical hedging)
- Solution: map all instances before revising, then apply different constructions to each

## Convergence Notes

Three iterations, all kept. Steepest gain in iteration 1 (+0.80) from multi-dimension comprehensive revision with full agent review. Diminishing returns in iterations 2-3 (+0.25, +0.20). No convergence signals fired. All dimensions at 6+ after iteration 1.

## Revision Protocol

1. Fix all factual errors first (highest-weight dimension)
2. Add structural elements (TOC, Key Terms, Reproducibility) before touching prose
3. Map all repeated phrases (search for 3+ occurrences) and vary each
4. Rewrite chart references: finding first, figure number second
5. Run Voice Auditor to detect remaining AI-tell patterns
6. Apply synonym substitutions at 1-3 per paragraph density
7. Check every paragraph opener for variety
