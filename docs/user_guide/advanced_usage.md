# Advanced Usage & Tuning

## Modifying Mathematical Thresholds
The classical engines (SIFT/ORB) are initialized in `src/matching/classical/feature_matching_pipeline.py`. 

### Adjusting SIFT Octaves
If you are matching high-resolution satellite imagery (e.g., OHRC 0.25m to OHRC 0.25m) with massive structural details, you can increase the `nOctaveLayers` parameter to extract finer geometries:
```python
# In src/matching/classical/sift_matcher.py
sift = cv2.SIFT_create(nfeatures=2000, nOctaveLayers=5) # Default is 3
```

### Tuning FLANN Indexers
By default, SIFT continuous vectors use `FLANN_INDEX_KDTREE`. If execution speed is critical and accuracy can be sacrificed, you can drop the number of trees:
```python
# Fewer trees = Faster search, lower precision
index_params = dict(algorithm=0, trees=2) # Default is 5
```

## Bypassing the Frontend
If you wish to integrate LunaAlign into an automated pipeline (e.g. Jenkins or a cron job processing hundreds of planetary orbits overnight), you can POST directly to the FastAPI layer, entirely bypassing the React UI.

```bash
curl -X POST "http://localhost:8000/api/v1/register" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "source_image=@/path/to/source.png" \
  -F "reference_image=@/path/to/reference.png"
```
The payload will synchronously return the Base64 visualization and mathematical JSON payload upon completion.
