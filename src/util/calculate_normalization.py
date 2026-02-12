#!/usr/bin/env python3
"""
Calculate mean and standard deviation of image datasets for normalization.

This script computes the channel-wise mean and standard deviation
of all images in a dataset directory, to be used for proper normalization
during training and inference.
"""

import argparse
import logging
from pathlib import Path

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


def get_image_files(directory: Path) -> list[Path]:
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


def calculate_mean_std(image_dir: Path, image_size: int = 224) -> tuple[list[float], list[float]]:
    """
    Calculate the mean and standard deviation of all images in a directory.

    Args:
        image_dir: Path to the directory containing images
        image_size: Size to resize images to before computing statistics

    Returns:
        Tuple of (mean, std) where each is a list of 3 floats for RGB channels
    """
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor()
    ])

    image_files = get_image_files(image_dir)
    logger.info(f"Found {len(image_files)} images in {image_dir}")

    if not image_files:
        logger.error("No images found!")
        return [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]

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
    logger.info(f"Calculated mean: {mean.tolist()}")

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
    logger.info(f"Calculated std: {std.tolist()}")

    return mean.tolist(), std.tolist()


def main():
    """Main function to calculate dataset statistics."""
    parser = argparse.ArgumentParser(
        description='Calculate mean and std of image dataset for normalization'
    )
    parser.add_argument(
        'image_dir',
        type=str,
        help='Path to the directory containing images'
    )
    parser.add_argument(
        '--image-size',
        type=int,
        default=224,
        help='Size to resize images to (default: 224)'
    )

    args = parser.parse_args()
    image_dir = Path(args.image_dir)

    if not image_dir.exists():
        logger.error(f"Directory not found: {image_dir}")
        return

    mean, std = calculate_mean_std(image_dir, args.image_size)

    print("\n" + "=" * 60)
    print("DATASET NORMALIZATION PARAMETERS")
    print("=" * 60)
    print(f"Directory: {image_dir}")
    print(f"Mean (RGB): {mean}")
    print(f"Std (RGB):  {std}")
    print("\nFor use in transforms.Normalize:")
    print(f"  transforms.Normalize({[round(m, 3) for m in mean]}, {[round(s, 3) for s in std]})")
    print("=" * 60)


if __name__ == "__main__":
    main()

