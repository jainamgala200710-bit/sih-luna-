# OHRC vs TMC-2 Failure Autopsy

## The Incident
During the execution of Phase 24 (Real Dataset Experiments), the proxy pair representing the extreme OHRC vs TMC-2 modality resulted in a critical pipeline halt:
`ERROR: Not enough matches to compute geometric transformation (minimum 4).`

## Mathematical Breakdown
The failure occurred specifically within the SIFT feature extractor mechanism prior to reaching the RANSAC algorithm.

1. **Scale Variance**: SIFT relies on Gaussian Difference pyramids to establish scale invariance. However, the theoretical 20x variance between TMC-2 and OHRC extends beyond the standard octave limits of the SIFT algorithm. The structural corners observed at 0.25m/px become smoothed indistinguishable blurs at the 5m/px level.
2. **Illumination Variance**: While SIFT descriptors normalize gradient vectors to survive moderate lighting changes, the simulated severe sun-angle gradient actively inverted shadow topologies within the crater mappings. The local gradient histograms were physically pointing in opposite directions, resulting in zero nearest-neighbor KNN matches.

## Remediation Strategy
This autopsy definitively confirms that classical descriptors cannot bridge the OHRC/TMC2 divide. 
To resolve this in a production deployment, the pipeline must dynamically route any payloads tagged with extreme scale differentials directly into the **Deep Learning Matching Integration** (Phase 12) utilizing Kornia's LoFTR architecture. LoFTR computes dense match probabilities at a macroscopic semantic level, completely bypassing the local gradient histogram dependency that shattered SIFT.
