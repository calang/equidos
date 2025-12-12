#!/usr/bin/env python3
"""
Script to detect and crop horse faces from images.

This script uses the OWL-ViT model to detect horse faces in images from the
data/horsefacebase directory, crops the detected faces, and saves them to
data/horsefacecrop directory.
"""

import logging
from pathlib import Path
from PIL import Image
import torch
from transformers import OwlViTProcessor, OwlViTForObjectDetection


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def detect_horse_face(image, processor, model, threshold=0.1):
    """
    Detect horse face in an image using OWL-ViT model.

    Args:
        image: PIL Image object
        processor: OwlViTProcessor instance
        model: OwlViTForObjectDetection instance
        threshold: Confidence threshold for detection (default: 0.1)

    Returns:
        tuple: (box, score) of the best detection, or (None, None) if no
               detection found
    """
    # texts = [["a photo of a horse face", "a photo of a horse muzzle"]]
    texts = [["a photo of a horse face"]]

    inputs = processor(text=texts, images=image, return_tensors="pt")
    outputs = model(**inputs)

    # Target image sizes (height, width) to rescale box predictions
    target_sizes = torch.Tensor([image.size[::-1]])

    # Convert outputs (bounding boxes and class logits) to COCO API
    results = processor.post_process_grounded_object_detection(
        outputs=outputs,
        target_sizes=target_sizes,
        threshold=threshold
    )

    # Get predictions for the first image
    boxes = results[0]["boxes"]
    scores = results[0]["scores"]

    if len(boxes) == 0:
        return None, None

    # Return the detection with highest confidence
    best_idx = torch.argmax(scores)
    best_box = boxes[best_idx].tolist()
    best_score = scores[best_idx].item()

    return best_box, best_score


def crop_face(image, box):
    """
    Crop the face region from an image.

    Args:
        image: PIL Image object
        box: List of [x_min, y_min, x_max, y_max] coordinates

    Returns:
        PIL Image object of the cropped face
    """
    x_min, y_min, x_max, y_max = [int(coord) for coord in box]
    cropped = image.crop((x_min, y_min, x_max, y_max))
    return cropped


def main():
    """Main function to process all images in horsefacebase directory."""
    # Define base paths
    base_dir = Path(__file__).parent.parent.parent
    source_dir = base_dir / "data" / "horsefacebase"
    dest_dir = base_dir / "data" / "horsefacecrop"

    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created/verified destination directory: {dest_dir}")

    # Load the model and processor
    logger.info("Loading OWL-ViT model and processor...")
    processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
    model = OwlViTForObjectDetection.from_pretrained(
        "google/owlvit-base-patch32"
    )
    logger.info("Model loaded successfully")

    # Process all image files in source directory
    processed_count = 0
    failed_count = 0
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}

    for image_path in sorted(source_dir.iterdir()):
        if not image_path.is_file():
            continue

        if image_path.suffix.lower() not in image_extensions:
            continue

        try:
            # Load image
            image = Image.open(image_path)

            # Detect horse face
            box, score = detect_horse_face(image, processor, model)

            if box is None:
                logger.warning(
                    f"No horse face detected in {image_path.name}"
                )
                failed_count += 1
                continue

            # Crop the face
            cropped_face = crop_face(image, box)

            # Save the cropped face with "base" replaced by "crop" in filename
            new_filename = image_path.name.replace("Base", "Crop")
            dest_path = dest_dir / new_filename
            cropped_face.save(dest_path)

            processed_count += 1

        except Exception as e:
            logger.error(f"Error processing {image_path.name}: {e}")
            failed_count += 1

    # Print summary
    logger.info(f"\n{'=' * 50}")
    logger.info(f"Processing complete!")
    logger.info(f"Successfully processed: {processed_count}")
    logger.info(f"Failed: {failed_count}")
    logger.info(f"Total: {processed_count + failed_count}")
    logger.info(f"{'=' * 50}")


if __name__ == "__main__":
    main()

