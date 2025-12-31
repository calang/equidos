# Data Preparation Scripts

This directory contains scripts for preparing equid face image data for training.

## Scripts

### 1. `prep_data.py` - Split Data into Train/Validation/Test Sets

This script takes images from `data/TunHorseDB2015G/Croped Images/` and splits them
into three sets while ensuring that each individual equid (subdirectory) has images
in all three sets with no overlap.

#### Features
- Splits images by individual equid (not randomly across all images)
- Maintains subdirectory structure for each individual
- Fixed random seed for reproducibility
- Creates organized output directories

#### Split Ratios
- Training: 70%
- Validation: 15%
- Testing: 15%

#### Prerequisites
Ensure the source data exists at: `data/TunHorseDB2015G/Croped Images/`

#### Usage
```bash
python src/scripts/prep_data.py
```

Or make it executable and run directly:
```bash
chmod +x src/scripts/prep_data.py
./src/scripts/prep_data.py
```

#### Output
The script creates three directories with subdirectories for each individual:
- `data/THGtraining/` - Training set (70% of images per individual)
- `data/THGvalidation/` - Validation set (15% of images per individual)
- `data/THGtest/` - Test set (15% of images per individual)

#### Expected Output
```
2025-12-31 10:00:00 - INFO - Created directory: data/THGtraining
2025-12-31 10:00:00 - INFO - Created directory: data/THGvalidation
2025-12-31 10:00:00 - INFO - Created directory: data/THGtest
2025-12-31 10:00:00 - INFO - Found 47 individual equids
2025-12-31 10:00:00 - INFO - Processing individual: Part01_Base01
2025-12-31 10:00:00 - INFO -   Found 10 images
2025-12-31 10:00:00 - INFO -   Split: 7 train, 2 val, 1 test
...
============================================================
2025-12-31 10:00:05 - INFO - Data preparation completed successfully!
2025-12-31 10:00:05 - INFO - Total training images: 2450
2025-12-31 10:00:05 - INFO - Total validation images: 525
2025-12-31 10:00:05 - INFO - Total test images: 525
2025-12-31 10:00:05 - INFO - Total images: 3500
============================================================
```

---

### 2. `xbasefaces.py` - Extract Base Face Images

This script extracts base face images from the dataset.

#### Usage
```bash
python src/scripts/xbasefaces.py
```

Or make it executable and run directly:
```bash
chmod +x src/scripts/xbasefaces.py
./src/scripts/xbasefaces.py
```

---

### 3. `xcropfaces.py` - Crop Face Images

This script crops face images from larger images, likely using face detection.

#### Usage
```bash
python src/scripts/xcropfaces.py
```

Or make it executable and run directly:
```bash
chmod +x src/scripts/xcropfaces.py
./src/scripts/xcropfaces.py
```

---

## Training Scripts

For model training, prediction, and visualization scripts, see:
- **`experiments/ResNet50-47/`** - Contains training pipeline scripts:
  - `train_model.py` - Train the equid identification model
  - `predict.py` - Make predictions with a trained model
  - `visualize_training.py` - Visualize training metrics and plots
  - `quickstart.py` - Interactive workflow guide
  - See `experiments/ResNet50-47/README.md` for details

---

## Requirements

Python packages (see `env.yml`):
- Python >= 3.11
- Standard library only for `prep_data.py`
- Additional packages may be needed for `xbasefaces.py` and `xcropfaces.py`

---

## Troubleshooting

**Error: "Source directory not found"**
- Ensure `data/TunHorseDB2015G/Croped Images/` exists
- Check that the source data has been downloaded/extracted

**No images found for an individual**
- Some subdirectories may be empty or contain non-image files
- The script will log warnings but continue processing

**Unexpected split ratios**
- For individuals with few images, integer rounding affects exact ratios
- Example: An individual with 5 images → 3 train, 1 val, 1 test (60%/20%/20%)

---

## Next Steps

After preparing data with these scripts:
1. Verify the output directories have the expected structure
2. Check that all individuals have images in all three sets
3. Proceed to model training in `experiments/ResNet50-47/`
4. See `experiments/ResNet50-47/README.md` for training instructions
