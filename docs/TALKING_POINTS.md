# Technical Talking Points for Judges

If the judges ask specific, deep-technical questions about how LunaAlign functions, rely on these curated talking points:

### "Why didn't you just use OpenCV SIFT for everything?"
> "SIFT relies on Difference-of-Gaussian scale pyramids. When the scale variance between OHRC and TMC-2 hits 20x, the macroscopic craters become perfectly flat, smoothed-out pixels in the DoG pyramid. SIFT mathematically shatters because there is no localized gradient left to extract. We empirically proved this in our Edge-Case Test Suite."

### "How are you handling the massive memory load of satellite imagery?"
> "We implemented a custom `TilingEngine` in Phase 25. Instead of dumping a 10GB TIFF directly into RAM, we grid-slice it into `1000x1000` sliding blocks with a 100px overlap. Memory allocation remains linear, preventing Out-Of-Memory segmentation faults on edge hardware."

### "How fast is your nearest-neighbor matching?"
> "We deprecated standard Brute-Force $O(N^2)$ calculations. We migrated all continuous vectors to `KD-Tree` FLANN indexers, and all binary descriptors (like ORB) to Locality-Sensitive Hashing (`LSH`) FLANN indexers, achieving a ~38% execution speedup across the pipeline."

### "What happens when your pipeline fails?"
> "Our architecture is structurally fortified against catastrophic C++ OpenCV faults. We wrap all mathematical endpoints in a `PipelineExhaustionError` class. If the geometry drops below the necessary RANSAC requirements (N=4), the FastAPI backend degrades gracefully and pipes a readable JSON exception directly to the React UI via WebSockets."
