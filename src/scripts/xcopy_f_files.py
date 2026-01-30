#!/usr/bin/env python3
"""
Script to create a filtered copy of TunHorseDB2015G directory.

This script creates a new directory data/TunHorseDB2015F, which is a copy of
data/TunHorseDB2015G, but including only files whose basename starts with an 'F'.
"""

import logging
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def copy_f_files(source_dir: Path, dest_dir: Path) -> int:
    """
    Copy directory structure and files starting with 'F' from source to destination.

    Args:
        source_dir: Source directory path
        dest_dir: Destination directory path

    Returns:
        Number of files copied
    """
    copied_count = 0

    # Walk through all files in source directory
    for source_path in source_dir.rglob('*'):
        if not source_path.is_file():
            continue

        # Check if basename starts with 'F' (case-insensitive)
        if not source_path.name.lower().startswith('f'):
            continue

        # Calculate relative path from source_dir
        rel_path = source_path.relative_to(source_dir)
        dest_path = dest_dir / rel_path

        # Create parent directories if they don't exist
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file
        shutil.copy2(source_path, dest_path)
        copied_count += 1
        logger.info(f"Copied: {rel_path}")

    return copied_count


def main():
    """Main function to copy F-files from TunHorseDB2015G to TunHorseDB2015F."""
    # Define base paths
    base_dir = Path(__file__).parent.parent.parent
    source_dir = base_dir / "data" / "TunHorseDB2015G"
    dest_dir = base_dir / "data" / "TunHorseDB2015F"

    # Validate source directory exists
    if not source_dir.exists():
        logger.error(f"Source directory does not exist: {source_dir}")
        return

    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created/verified destination directory: {dest_dir}")

    # Copy files starting with 'F'
    logger.info(f"Copying files starting with 'F' from {source_dir} to {dest_dir}...")
    copied_count = copy_f_files(source_dir, dest_dir)

    logger.info(f"Total files copied: {copied_count}")


if __name__ == "__main__":
    main()
