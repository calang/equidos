#!/usr/bin/env python3
"""
Prepare data for training by splitting images into train, validation, and test sets.

This script takes images from data/TunHorseDB2015G/Croped Images/ and splits them
into three sets while ensuring that each individual equid (subdirectory) has images
in all three sets with no overlap.

Split ratios:
- Training: 70%
- Validation: 15%
- Testing: 15%
"""

import logging
import os
import random
import shutil
from pathlib import Path
from typing import List, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
SOURCE_DIR = Path('data/TunHorseDB2015G/Croped Images')
TRAIN_DIR = Path('data/THGtraining')
VAL_DIR = Path('data/THGvalidation')
TEST_DIR = Path('data/THGtest')

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42


def get_image_files(directory: Path) -> List[Path]:
    """
    Get all image files from a directory.

    Args:
        directory: Path to the directory containing images

    Returns:
        List of Path objects for image files
    """
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    image_files = [
        f for f in directory.iterdir()
        if f.is_file() and f.suffix.lower() in valid_extensions
    ]
    return sorted(image_files)


def split_files(files: List[Path],
                train_ratio: float,
                val_ratio: float,
                test_ratio: float) -> Tuple[List[Path], List[Path], List[Path]]:
    """
    Split a list of files into train, validation, and test sets.

    Args:
        files: List of file paths to split
        train_ratio: Proportion for training set
        val_ratio: Proportion for validation set
        test_ratio: Proportion for test set

    Returns:
        Tuple of (train_files, val_files, test_files)
    """
    if not files:
        return [], [], []

    # Shuffle files with fixed seed for reproducibility
    shuffled_files = files.copy()
    random.shuffle(shuffled_files)

    n_total = len(shuffled_files)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)

    train_files = shuffled_files[:n_train]
    val_files = shuffled_files[n_train:n_train + n_val]
    test_files = shuffled_files[n_train + n_val:]

    return train_files, val_files, test_files


def copy_files(files: List[Path],
               dest_dir: Path,
               individual_id: str) -> None:
    """
    Copy files to destination directory, maintaining individual subdirectory structure.

    Args:
        files: List of file paths to copy
        dest_dir: Destination directory
        individual_id: ID of the individual (subdirectory name)
    """
    if not files:
        return

    # Create subdirectory for this individual
    individual_dest = dest_dir / individual_id
    individual_dest.mkdir(parents=True, exist_ok=True)

    # Copy each file
    for file_path in files:
        dest_path = individual_dest / file_path.name
        shutil.copy2(file_path, dest_path)


def prepare_data() -> None:
    """
    Main function to prepare and split data into train, validation, and test sets.
    """
    # Set random seed for reproducibility
    random.seed(RANDOM_SEED)

    # Check if source directory exists
    if not SOURCE_DIR.exists():
        logger.error(f"Source directory not found: {SOURCE_DIR}")
        raise FileNotFoundError(f"Source directory not found: {SOURCE_DIR}")

    # Create output directories
    for directory in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

    # Get all individual subdirectories
    individual_dirs = [
        d for d in SOURCE_DIR.iterdir()
        if d.is_dir()
    ]
    individual_dirs = sorted(individual_dirs, key=lambda x: x.name)

    logger.info(f"Found {len(individual_dirs)} individual equids")

    # Process each individual
    total_train = 0
    total_val = 0
    total_test = 0

    for individual_dir in individual_dirs:
        individual_id = individual_dir.name
        logger.info(f"Processing individual: {individual_id}")

        # Get all image files for this individual
        image_files = get_image_files(individual_dir)

        if not image_files:
            logger.warning(f"No images found for individual {individual_id}")
            continue

        logger.info(f"  Found {len(image_files)} images")

        # Split files
        train_files, val_files, test_files = split_files(
            image_files,
            TRAIN_RATIO,
            VAL_RATIO,
            TEST_RATIO
        )

        logger.info(f"  Split: {len(train_files)} train, "
                   f"{len(val_files)} val, {len(test_files)} test")

        # Copy files to respective directories
        copy_files(train_files, TRAIN_DIR, individual_id)
        copy_files(val_files, VAL_DIR, individual_id)
        copy_files(test_files, TEST_DIR, individual_id)

        total_train += len(train_files)
        total_val += len(val_files)
        total_test += len(test_files)

    # Summary
    logger.info("=" * 60)
    logger.info("Data preparation completed successfully!")
    logger.info(f"Total training images: {total_train}")
    logger.info(f"Total validation images: {total_val}")
    logger.info(f"Total test images: {total_test}")
    logger.info(f"Total images: {total_train + total_val + total_test}")
    logger.info("=" * 60)


if __name__ == "__main__":
    prepare_data()

