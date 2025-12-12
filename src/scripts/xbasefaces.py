#!/usr/bin/env python3
"""
Script to copy and rename horse face base images.

This script copies files starting with 'F' from the "Base image" directories
under data/TunHorseDB2015 into a new directory called data/horsefacebase,
following a specific naming convention.
"""

import os
import shutil
from pathlib import Path


def main():
    """Main function to copy and rename base images."""
    # Define base paths
    base_dir = Path(__file__).parent.parent.parent
    source_base = base_dir / "data" / "TunHorseDB2015"
    dest_dir = base_dir / "data" / "horsefacebase"

    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created/verified destination directory: {dest_dir}")

    copied_count = 0

    # Iterate through all Part directories (Part1, Part2, etc.)
    for part_dir in sorted(source_base.glob("Part*")):
        if not part_dir.is_dir():
            continue

        # Extract part number (e.g., "Part1" -> 1)
        part_name = part_dir.name
        part_num = int(part_name.replace("Part", ""))

        # Path to "Base image" directory
        base_image_dir = part_dir / "Base image"
        if not base_image_dir.exists():
            continue

        # Iterate through all subdirectories (1, 2, 3, etc.)
        for subdir in sorted(base_image_dir.iterdir()):
            if not subdir.is_dir():
                continue

            # Extract directory number
            dir_num = int(subdir.name)

            # Find all files starting with 'F'
            for file_path in sorted(subdir.glob("F*")):
                if not file_path.is_file():
                    continue

                # Extract filename and extension
                original_filename = file_path.name
                name_without_ext = file_path.stem  # e.g., "F1"
                extension = file_path.suffix  # e.g., ".jpg"

                # Extract the number from the filename (e.g., "F1" -> 1)
                file_num_str = name_without_ext[1:]  # Remove 'F' prefix
                try:
                    file_num = int(file_num_str)
                except ValueError:
                    # If the filename after 'F' is not a number, skip
                    print(f"Skipping {original_filename}: cannot parse number")
                    continue

                # Create new filename following the convention:
                # PartP_BaseD_FN.jpg where P, D, N are 2-digit zero-padded integers
                new_filename = f"Part{part_num:02d}_Base{dir_num:02d}_F{file_num:02d}{extension}"
                dest_path = dest_dir / new_filename

                # Copy the file
                shutil.copy2(file_path, dest_path)
                copied_count += 1
                print(f"Copied: {file_path.relative_to(base_dir)} -> {dest_path.relative_to(base_dir)}")

    print(f"\nTotal files copied: {copied_count}")


if __name__ == "__main__":
    main()

