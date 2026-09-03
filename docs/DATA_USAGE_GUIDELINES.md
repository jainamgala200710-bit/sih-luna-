# Data Usage Guidelines: LunaAlign AI

## 1. Internal Project Use
All data stored in the `data/` directory is intended strictly for the LunaAlign AI project (SIH26166) development, testing, and evaluation.

## 2. Storage and Push Policy
- **NO RAW DATA IN VERSION CONTROL**: Do not commit raw, processed, or synthetic images to Git. The `.gitignore` must exclude these files to prevent repository bloat.
- **METADATA ONLY**: Only metadata files (e.g., CSV inventories, YAML schemas, ground truth mapping JSONs) should be pushed to the repository.

## 3. Data Integrity
- Do not manually edit the original raw images. All preprocessing must be done via scripts in `src/preprocessing/` and saved to `data/processed/`.
- Ensure that the original file names from data sources (ISRO, NASA) are retained or mapped carefully in the inventory system to prevent loss of lineage.

## 4. Ground Truth Integrity
- Synthetic ground truth must not be altered manually.
- If an image pair is deemed poor quality, flag it in the inventory (`pair_quality_score`) rather than deleting it, to allow algorithms to be tested on failure cases.

## 5. Security & Access
- Maintain local backups of the `data/` directory structure.
- Adhere to the terms of service of the respective space agencies (ISRO ISSDC, NASA PDS) regarding the redistribution of data.
