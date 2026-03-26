# Selfwrite Summary — BC Crime README Rewrite

## Score Trajectory

| Version | Factual Accuracy | Structure | Analytical Depth | Register | Audience | Evidence | Composite | Status |
|---------|-----------------|-----------|-----------------|----------|----------|----------|-----------|--------|
| v0 | 4 | 6 | 6 | 5 | 5 | 5 | 5.15 | baseline |
| v1 | 5 | 7 | 6 | 6 | 6 | 6 | 5.95 | kept |
| v2 | 6 | 7 | 6 | 6 | 6 | 6 | 6.20 | kept |
| v3 | 6 | 7 | 7 | 6 | 6 | 6 | 6.40 | kept |

## Metrics

- **Iterations:** 3 attempted, 3 kept, 0 reverted
- **Starting composite:** 5.15 → **Final composite:** 6.40 (delta: +1.25, 24% improvement)
- **Duration:** ~15 minutes (iteration loop)
- **Review agents deployed:** Reader (8 annotations), Voice Auditor (6 patterns), Synonym (15 proposals, 13 accepted)
- **Mode:** Simple rewrite (no RESEARCH phase)

## Key Learnings

1. **Fabricated derived values are the highest-risk error.** I computed 83.5 from partial data and had to revert it in iteration 2. Never compute absolute values from year-over-year changes applied to distant baselines.

2. **"Is consistent with" is the strongest AI signal in analytical writing.** Four uses in 2,400 words was flagged as the #1 detection risk by the Voice Auditor. Each instance needed a distinct replacement.

3. **Multi-dimension comprehensive revision yields the steepest gains.** Iteration 1 improved all 6 dimensions by +0.80 composite. Iterations 2-3 targeting single dimensions gained only +0.25 and +0.20.

## What Worked

- **Full agent review on iteration 1:** Reader/Voice Auditor/Synonym agents running in parallel caught issues across all dimensions simultaneously, enabling a comprehensive revision
- **Synonym substitutions at register 2:** "Posted" for "recorded," "corroborates" for "confirms," "decoupled" for "diverged" -- each more analytically precise and less predictable
- **Breaking five-factor parallelism:** Giving each factor a distinct heading and varied internal structure eliminated the strongest list-then-elaborate AI signal

## What Remains

- All dimensions at 6+ but none above 7 (except Structure at 7 and Analytical Depth at 7)
- Child exploitation "82 per 100,000" figure carries forward from original -- may be questionable but cannot be verified in simple rewrite mode
- Paragraph opener variety improved but still tends toward "The [noun]..." in Sections 2-3
- Enumerated pre-announcements reduced from 4 to 2 but could be further varied
