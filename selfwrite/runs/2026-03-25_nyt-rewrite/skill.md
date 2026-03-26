# Data Journalism Rewrite Quality Guide

## Scoring Rubric

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Narrative Pull | 0.25 | Does it read like journalism? Opening hook, forward momentum, arc, closing payoff |
| Data Integration | 0.25 | Are charts introduced with context and commented on with findings? Do numbers land? |
| Audience Calibration | 0.20 | Would a non-specialist follow this? Jargon explained? Sentence rhythm varied? |
| Specificity | 0.15 | Every claim backed by a number. No vague quantifiers |
| Structure | 0.15 | Point-first paragraphs, scannable without losing narrative thread |

## Common Weaknesses and Fixes

### 1. Opening with abstract data instead of a scene
**Before:** "Ask British Columbians whether crime is getting worse, and 42% will say yes."
**After:** "In Chilliwack, a city of 100,000 in BC's Fraser Valley, residents are twice as likely to experience crime as their neighbours in Vancouver."
**Why it works:** Concrete scene-setting grounds the reader in a real place before introducing the paradox. The abstract data follows as evidence, not lede.

### 2. Mechanical chart introductions
**Before:** "Figure 12 ranks the largest absolute changes."
**After:** "The heatmap makes the shift visible at a glance: property violations cool from red to blue over time."
**Why it works:** Lead with the finding, point to the chart as evidence. The reader sees what to look for before looking.

### 3. Monotone sentence rhythm
**Before:** "The stability itself is the finding. Two decades of reforms, technology investment, and budget growth haven't moved the needle on property-crime resolution. This points to a structural constraint rather than a fixable capacity gap."
**After:** Add a short punch: "This isn't a capacity gap waiting to be filled. It's a design limitation of the system."
**Why it works:** Short sentences after long compounds create emphasis. They signal importance.

### 4. Jargon without natural-language alternates
**Before:** "The CSI dropped 46%... the CSI peaked... the CSI still sits above..."
**After:** "The crime severity index dropped... the index peaked... the severity score still sits..."
**Why it works:** Define the acronym once, then rotate through 2-3 natural-language forms. An NYT reader won't remember a definition from paragraph 2 by paragraph 20.

### 5. Recommendations in policy-memo format
**Before:** Five subheaded blocks with "Why now" and "Next steps" subsections (~350 words)
**After:** Five bold-numbered paragraphs integrating context and action (~250 words)
**Why it works:** Journalism integrates the so-what into the evidence. A separate recommendations section repeats findings the reader already absorbed.

## Expert Questions to Ask

1. "The opening hook creates a promise. Does the closing deliver on it, or does the piece trail off into methodology?"
2. "Which chart is introduced by pointing at it ('Figure X shows...') instead of pointing at the finding ('The gap is widening')?  Fix those."
3. "Where would the reader stop reading? That's where you need a short sentence and a new hook."
4. "How many times does the same number appear? Each mention should advance the argument, not repeat it."
5. "Is there a one-sentence paragraph in each section? If not, the rhythm is monotone."

## Anti-Patterns

- **"Figures X-Y spotlight..."** -- Never introduce charts by figure number first. The finding goes first.
- **Repeating the same statistic** -- If 46% appears three times in 200 words, two of those are redundant.
- **Policy-memo subheads in journalism** -- "Why now" and "Next steps" belong in a memo, not a feature.
- **Abstract opening** -- Starting with a survey statistic is weaker than starting with a place and a person.

## Convergence Notes

- No convergence signals fired in 4 iterations. All dimensions advanced from 5-6 to 6-7 range.
- Highest-leverage change: finding-first chart introductions (iteration 2, +0.45 delta).
- Structure compression (iteration 3) had the smallest delta (+0.15) but cleaned up the most word count.
- Scene-setting opening (iteration 4) had disproportionate impact on narrative pull relative to text changed.

## Revision Protocol (in order of impact)

1. **Rewrite the opening** -- Start with a concrete scene or person, not abstract data. The data follows as evidence.
2. **Fix chart introductions** -- Every chart introduction must lead with the finding. "The gap is widening (Figure 27)" not "Figure 27 shows the gap."
3. **Add sentence-rhythm variation** -- One short-punch paragraph per section. One short sentence after a long compound.
4. **Rotate jargon** -- Define acronyms once, then use 2-3 natural-language alternates.
5. **Make paragraphs point-first** -- Move the finding to the first sentence. Context comes second.
6. **Compress recommendations** -- Integrate context and action into numbered paragraphs. Cut "Why now" headers that repeat earlier findings.
