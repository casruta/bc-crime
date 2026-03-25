# Chart Embedding Selfwrite Summary

**Task:** Embed all 42 charts into the bc-crime README
**Duration:** 15 minutes
**Iterations:** 3 attempted, 3 kept, 0 reverted

## Score Trajectory

| Version | Completeness | Visual Integration | Caption Quality | Scannability | Narrative Flow | Composite |
|---------|-------------|-------------------|-----------------|-------------|---------------|-----------|
| v0 | 6 | 4 | 5 | 5 | 4 | 4.85 |
| v1 | 6 | 5 | 6 | 5 | 5 | 5.45 |
| v2 | 7 | 5 | 6 | 6 | 5 | 5.85 |
| v3 | 7 | 5 | 7 | 6 | 6 | 6.30 |

## Key Learnings

1. **Interleaving beats dumping.** Moving charts next to the prose that references their data (+0.60) was the largest single gain. Image dumps kill reading flow.

2. **Point-first captions are alt text with a purpose.** Captions that state the finding ("Property violations cool from red to blue") serve screen readers, GitHub preview, and the scanning eye simultaneously.

3. **TOC with chart counts aids navigation.** A section-level table of contents with figure ranges lets readers jump to the right section without scrolling through 42 images.

## Final Metrics
- 42 PNG images embedded with point-first captions
- 1 HTML interactive map linked
- Table of contents with section anchors and chart counts
- All prose references figures by number before they appear
