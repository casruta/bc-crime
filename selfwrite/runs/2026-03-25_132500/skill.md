# Analytical Findings Summary — Quality Guide

## Scoring Rubric

| Dimension | Weight | What it measures |
|---|---|---|
| Specificity | 0.25 | Every claim backed by a number, source, or comparison |
| Structure | 0.20 | Point-first paragraphs, navigable hierarchy, executive summary |
| Analytical Depth | 0.25 | Causal reasoning, alternative explanations, bounded claims |
| Audience Calibration | 0.15 | Tone matches decision-maker readers; jargon explained; urgency proportional |
| Actionability | 0.15 | Specific next steps tied to findings; monitoring framework; pilot-then-scale |

## Common Weaknesses and Fixes

### 1. Vague quantifiers → specific numbers
- **Before:** "crime has risen modestly"
- **After:** "violent CSI climbed from X to Y since 2014, a Z% increase"
- **Impact:** +0.50 composite (largest single-iteration gain)

### 2. Flat finding lists → point-first sections
- **Before:** Section header "Crime Trends" → paragraph explaining context → finding buried in middle
- **After:** Section header IS the finding ("Crime Is Falling — but the Mix Is Getting Worse") → first sentence states the conclusion → evidence follows
- **Impact:** +0.45 composite

### 3. Generic recommendations → operational next steps with "why now"
- **Before:** "Resources should be redirected to interior communities"
- **After:** "Why now: Chilliwack (11,352/100k) faces 2x Vancouver's rate and the gap is widening. Next steps: Adopt composite ranking as allocation input. Pilot in top-5 ranked communities. Measure over 12 months before scaling."
- **Impact:** +0.40 composite

### 4. Unbounded claims → explicit limitations
- **Before:** Analysis implies it can explain everything it measures
- **After:** Dedicated "What This Analysis Cannot Answer" section; inline "what the data can't tell us" blocks
- **Impact:** +0.40 composite; also improved Structure as a bonus

## Expert Questions to Ask

When reviewing any analytical findings summary, ask:

1. "Which of these claims would survive if the data collection method changed?" (tests robustness to reporting-rate variability)
2. "What is the strongest alternative explanation for this trend that the author didn't address?" (tests analytical depth)
3. "If I only read the first sentence of each section, do I get the full story?" (tests point-first structure)
4. "What would a decision-maker do differently after reading this vs. before?" (tests actionability)
5. "Where does the author confuse detection change with prevalence change?" (tests analytical sophistication)

## Anti-Patterns

1. **Data dump structure:** Listing findings sequentially without editorial hierarchy. Fix: make section headings into findings.
2. **Implicit limitations:** Failing to state what the analysis can't answer. Fix: dedicated limitations section + inline caveats.
3. **Generic recommendations:** "More research needed" or "resources should be allocated." Fix: name the specific resource, the specific place, the specific timeline.
4. **Conflating trends:** Treating child exploitation (detection gain) and shoplifting (behavioural change) as the same kind of increase. Fix: always name the mechanism behind the number.

## Revision Protocol (in order of impact)

1. Replace every vague quantifier with a specific number
2. Rewrite section headings as findings
3. Move the conclusion to the first sentence of every paragraph
4. Add "why now" framing to every recommendation
5. Name confounders and alternative explanations inline
6. Add a "what this analysis cannot answer" section
7. Add a 10-second executive summary (blockquote at top)
8. Add a monitoring cadence table with trigger thresholds
