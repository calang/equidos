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

Additionally, this script calculates the mean and standard deviation of the training
images for normalization purposes and saves them to a JSON file.
"""

import json
import logging
import random
import shutil
from pathlib import Path
from typing import List, Tuple

import torch
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

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
NORMALIZATION_FILE = Path('data/THGtraining/normalization.json')

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42
IMAGE_SIZE = 224


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


def get_all_image_files(directory: Path) -> List[Path]:
    """
    Recursively get all image files from a directory.

    Args:
        directory: Path to the directory containing images

    Returns:
        List of Path objects for image files
    """
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    image_files = []

    for ext in valid_extensions:
        image_files.extend(directory.rglob(f'*{ext}'))
        image_files.extend(directory.rglob(f'*{ext.upper()}'))

    return sorted(set(image_files))


def calculate_normalization(image_dir: Path) -> Tuple[List[float], List[float]]:
    """
    Calculate the mean and standard deviation of all images in a directory.

    Args:
        image_dir: Path to the directory containing images

    Returns:
        Tuple of (mean, std) where each is a list of 3 floats for RGB channels
    """
    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor()
    ])

    image_files = get_all_image_files(image_dir)
    logger.info(f"Calculating normalization from {len(image_files)} images...")

    if not image_files:
        logger.error("No images found for normalization calculation!")
        return [0.5, 0.5, 0.5], [0.5, 0.5, 0.5]

    # Initialize accumulators
    channel_sum = torch.zeros(3)
    channel_sum_sq = torch.zeros(3)
    pixel_count = 0

    # First pass: calculate mean
    for image_path in tqdm(image_files, desc="Calculating mean"):
        try:
            image = Image.open(image_path).convert('RGB')
            tensor = transform(image)  # Shape: (3, H, W)

            channel_sum += tensor.sum(dim=[1, 2])
            pixel_count += tensor.shape[1] * tensor.shape[2]
        except Exception as e:
            logger.warning(f"Error processing {image_path}: {e}")

    mean = channel_sum / pixel_count

    # Second pass: calculate standard deviation
    for image_path in tqdm(image_files, desc="Calculating std"):
        try:
            image = Image.open(image_path).convert('RGB')
            tensor = transform(image)  # Shape: (3, H, W)

            # Sum of squared differences from mean
            for c in range(3):
                channel_sum_sq[c] += ((tensor[c] - mean[c]) ** 2).sum()
        except Exception as e:
            logger.warning(f"Error processing {image_path}: {e}")

    std = torch.sqrt(channel_sum_sq / pixel_count)

    mean_list = [round(m, 4) for m in mean.tolist()]
    std_list = [round(s, 4) for s in std.tolist()]

    logger.info(f"Calculated mean: {mean_list}")
    logger.info(f"Calculated std: {std_list}")

    return mean_list, std_list


def save_normalization(mean: List[float], std: List[float], output_path: Path) -> None:
    """
    Save normalization values to a JSON file.

    Args:
        mean: List of mean values for RGB channels
        std: List of std values for RGB channels
        output_path: Path to save the JSON file
    """
    normalization_data = {
        'mean': mean,
        'std': std,
        'description': 'Normalization values calculated from training dataset'
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(normalization_data, f, indent=2)

    logger.info(f"Normalization values saved to: {output_path}")


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

    # Calculate normalization values from training set
    logger.info("=" * 60)
    logger.info("Calculating normalization values from training set...")
    mean, std = calculate_normalization(TRAIN_DIR)
    save_normalization(mean, std, NORMALIZATION_FILE)

    # Summary
    logger.info("=" * 60)
    logger.info("Data preparation completed successfully!")
    logger.info(f"Total training images: {total_train}")
    logger.info(f"Total validation images: {total_val}")
    logger.info(f"Total test images: {total_test}")
    logger.info(f"Total images: {total_train + total_val + total_test}")
    logger.info(f"Normalization - Mean: {mean}")
    logger.info(f"Normalization - Std: {std}")
    logger.info("=" * 60)


if __name__ == "__main__":
    prepare_data()

