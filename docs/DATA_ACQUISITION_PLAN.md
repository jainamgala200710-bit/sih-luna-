# Data Acquisition Plan for LunaAlign AI

## Overview
This document outlines the data acquisition strategy for the LunaAlign AI project, which aims to develop a multi-modal, illumination-invariant lunar image correspondence and registration system.

## Data Sources
We plan to utilize the following lunar image datasets:

1. **Chandrayaan-2 Orbiter**
   - TMC-2 (Terrain Mapping Camera-2): Panchromatic images with 5m spatial resolution
   - OHRC (Orbiter High Resolution Camera): Very high resolution images (0.25m-0.5m)

2. **Lunar Reconnaissance Orbiter (LRO)**
   - LROC NAC (Narrow Angle Camera): 0.5m/pixel
   - LROC WAC (Wide Angle Camera): 100m/pixel (UV/VIS) and 400m/pixel (UV)

3. **SELENE (Kaguya)**
   - TC (Terrain Camera): 10m/pixel
   - MI (Multiband Imager): Various bands with 20m/pixel (visible) and 60m/pixel (near-infrared)

## Data Access Procedures
- Publicly available datasets will be downloaded from official planetary data archives:
  - ISRO Science Data Archive (ISDA) for Chandrayaan-2
  - NASA Planetary Data System (PDS) for LRO
  - JAXA Data Archives for SELENE
- Data will be downloaded in their native formats (IMG, PDS, etc.) and stored in the `data/raw/` directory.
- Metadata will be extracted and stored alongside the images.

## Inventory System
We will implement a CSV-based inventory system initially, with plans to migrate to a lightweight SQLite database if needed.

The inventory will track:
- Image identifier (unique ID)
- Mission and instrument
- Acquisition date and time
- Spatial resolution
- Band/wavelength information
- Georeferencing information (if available)
- File path and format
- Processing level
- Quality indicators
- Associated pairs (for registration experiments)

## Metadata Schema
A standardized metadata schema will be defined in YAML format to capture essential information for each image pair.

## Data Storage Organization
- `data/raw/`: Original downloaded files
- `data/processed/`: Preprocessed images (normalized, etc.)
- `data/synthetic/`: Synthetically generated image pairs for testing
- `data/pairs/`: Curated image pairs for registration experiments
- `data/metadata/`: Extracted metadata and inventory files
- `data/splits/`: Train/test/validation splits for machine learning components

## Data Validation
- Format validation: Ensure files are readable and not corrupted
- Metadata validation: Check for required fields and plausible values
- Duplicate detection: Avoid processing the same image multiple times
- Quality checks: Assess basic image properties (e.g., not blank, reasonable intensity range)

## Data Usage Guidelines
See `DATA_USAGE_GUIDELINES.md` for detailed policies on data handling, sharing, and usage.

## Implementation Timeline
This phase focuses on setting up the infrastructure for data management. Actual data downloading will occur in later phases after the inventory system is validated.

## Risks and Mitigation
- **Large dataset sizes**: Implement tiling and streaming approaches for processing
- **Inconsistent metadata**: Develop flexible metadata extractors for each format
- **Data access issues**: Prioritize publicly available datasets and establish backup sources