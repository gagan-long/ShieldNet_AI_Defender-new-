# Data Folder Overview

This folder contains datasets used for training, testing, and validating ShieldNet AI Defender components.

## Folder Breakdown

- **raw/**: Contains raw, unprocessed data such as phishing emails, videos, images, and query logs.
- **processed/**: Contains cleaned and feature-extracted datasets ready for model consumption.

## Notes

- Raw media files (videos, images) should be stored in their respective subfolders.
- Processed `.npy` files are generated by feature extraction scripts and should not be manually edited.
- Keep sensitive data secure and do not commit real confidential information to version control.

## Adding New Data

1. Place raw data in the appropriate `raw/` subfolder.
2. Run preprocessing scripts located in `scripts/` to generate processed datasets.
3. Store processed data in the `processed/` folder.

