# ISRO Pipeline Limitations Manual

## Classical Extractor Limitations (SIFT/ORB)
The Classical mathematical pipelines deployed in LunaAlign are robust, sub-second algorithms designed for **temporal or identical-sensor registration** (e.g. TMC-2 vs TMC-2). 

However, they **WILL** physically exhaust their mathematical capabilities and trigger a `PipelineExhaustionError` under the following orbital conditions:

1. **Scale Variance Exceeds 4x**: SIFT relies on Difference-of-Gaussian pyramids. Beyond 4 octaves (e.g., OHRC 0.25m vs TMC-2 5m), the physical layout of the macroscopic craters is entirely smoothed into flat grey pixels. There is no mathematical gradient left to extract.
2. **Inverted Shadow Topology**: If the temporal orbital passes occurred at drastically different sun-angles (e.g., morning terminator vs high-noon), the shadow gradients will point in opposite directions. The L2 norm of these histograms will reject all matches.

## Operator Protocol
When a `PipelineExhaustionError` is triggered, the LunaAlign backend degrades gracefully. The React UI will highlight a red block indicating that the physical limits of the classical math have been reached.

**At this threshold, operators MUST switch the UI toggles to the Deep Learning (Phase 12) LoFTR Engine.**

LoFTR computes dense probability fields at a coarse macroscopic level, completely bypassing the localized gradient histogram dependency that restricts classical SIFT. It is the only mathematical topology capable of bridging the SIH26166 OHRC-to-TMC2 requirement.
