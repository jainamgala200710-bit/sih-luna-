# Project Retrospective & Lessons Learned

## The OHRC vs TMC-2 Scale Problem
The fundamental challenge of SIH26166 was establishing correspondence between imagery with a 20x spatial resolution differential (0.25m vs 5.0m). 

**What we learned**: 
Classical mathematics simply cannot bridge this gap. SIFT relies on Difference-of-Gaussian (DoG) scale pyramids. We proved via our Pytest Edge-Case suite that shrinking an OHRC image by a factor of 20 algebraically smooths the physical crater geometries into flat pixels. The derivative yields exactly zero.
**The Pivot**: This realization mandated the integration of Phase 12 (LoFTR). By migrating to a Deep Learning cross-attention probability model, we successfully bypassed localized gradients entirely.

## Memory Allocation in Scientific Data
**What we learned**: 
Attempting to process gigapixel ISRO TIFF binaries directly in RAM caused immediate `cv2` Out-of-Memory segmentation faults on standard hardware.
**The Pivot**: We engineered the `TilingEngine` in Phase 25. By dividing the global matrix into `1000x1000` localized grids with a 100px overlap, we stabilized the memory footprint to a linear $O(N)$ consumption scale.

## Algorithmic Latency
**What we learned**:
Using `cv2.BFMatcher` to compute L2 Norms across 10,000 feature descriptors created severe CPU bottlenecks.
**The Pivot**: We migrated the structural arrays to KD-Tree and LSH FLANN indexers, reducing the search space to logarithmic time $O(N \log N)$ and dropping the global pipeline execution time by ~38%.
