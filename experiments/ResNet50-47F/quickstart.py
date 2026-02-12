#!/usr/bin/env python3
"""
Quick start guide for training an equid identification model.

This script provides a checklist and commands for the complete workflow.

This experiment uses data from data/TunHorseDB2015F (face pictures only).
"""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def check_directory(path: Path, description: str) -> bool:
    """Check if a directory exists."""
    exists = path.exists() and path.is_dir()
    status = "✓" if exists else "✗"
    logger.info(f"{status} {description}: {path}")
    return exists


def check_file(path: Path, description: str) -> bool:
    """Check if a file exists."""
    exists = path.exists() and path.is_file()
    status = "✓" if exists else "✗"
    logger.info(f"{status} {description}: {path}")
    return exists


def main():
    """Check prerequisites and display workflow."""
    logger.info("=" * 70)
    logger.info("EQUID IDENTIFICATION MODEL - TRAINING WORKFLOW (Face Pictures Only)")
    logger.info("=" * 70)

    # Check source data
    logger.info("\n1. Check Source Data:")
    source_exists = check_directory(
        Path("data/TunHorseDB2015F/Croped Images"),
        "Source images directory"
    )

    # Check prepared data
    logger.info("\n2. Check Prepared Data:")
    train_exists = check_directory(Path("data/THFtraining"), "Training data")
    val_exists = check_directory(Path("data/THFvalidation"), "Validation data")
    test_exists = check_directory(Path("data/THFtest"), "Test data")

    data_prepared = train_exists and val_exists and test_exists

    # Check trained models
    logger.info("\n3. Check Trained Models:")
    model_dir_exists = check_directory(Path("models"), "Models directory")
    best_model_exists = check_file(Path("experiments/ResNet50-47F/models/best_model.pth"), "Best model")
    final_model_exists = check_file(Path("experiments/ResNet50-47F/models/final_model.pth"), "Final model")

    model_trained = best_model_exists or final_model_exists

    # Display workflow
    logger.info("\n" + "=" * 70)
    logger.info("WORKFLOW STEPS")
    logger.info("=" * 70)

    # Step 1
    if not data_prepared:
        logger.info("\nSTEP 1: Prepare Data")
        logger.info("  Run the data preparation script to split images:")
        logger.info("  $ ./experiments/ResNet50-47F/prep_data.py")
        logger.info("  or")
        logger.info("  $ python experiments/ResNet50-47F/prep_data.py")
    else:
        logger.info("\n✓ STEP 1: Data already prepared")

    # Step 2
    if not model_trained:
        logger.info("\nSTEP 2: Train Model")
        logger.info("  Run the training script:")
        logger.info("  $ ./experiments/ResNet50-47F/train_model.py")
        logger.info("  or")
        logger.info("  $ python experiments/ResNet50-47F/train_model.py")
        logger.info("\n  Note: Training may take several hours depending on:")
        logger.info("  - Hardware (GPU recommended)")
        logger.info("  - Dataset size")
        logger.info("  - Number of epochs (default: 50)")
    else:
        logger.info("\n✓ STEP 2: Model already trained")

    # Step 3
    logger.info("\nSTEP 3: Visualize Training Results (optional)")
    logger.info("  View training metrics and plots:")
    logger.info("  $ ./experiments/ResNet50-47F/visualize_training.py --plot")
    logger.info("  or save plots:")
    logger.info("  $ ./experiments/ResNet50-47F/visualize_training.py --save-plot results.png")

    # Step 4
    logger.info("\nSTEP 4: Evaluate Model on Test Set")
    logger.info("  Run the test script to evaluate on all test images:")
    logger.info("  $ ./experiments/ResNet50-47F/test_model.py")
    logger.info("  or with custom paths:")
    logger.info("  $ ./experiments/ResNet50-47F/test_model.py --test-dir data/THFtest --output experiments/ResNet50-47F/test_results.csv")

    # Step 5
    logger.info("\nSTEP 5: Make Predictions on Individual Images")
    logger.info("  Test the model on new images:")
    logger.info("  $ ./experiments/ResNet50-47F/predict.py <image_path>")
    logger.info("  Example:")
    logger.info("  $ ./experiments/ResNet50-47F/predict.py data/horsefacecrop/Part01_Base01_F01.jpg")

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("SUMMARY")
    logger.info("=" * 70)

    if not source_exists:
        logger.warning("⚠ Source data not found. Check data directory.")
    elif not data_prepared:
        logger.info("→ Next step: Run prep_data.py to prepare training data")
    elif not model_trained:
        logger.info("→ Next step: Run train_model.py to train the model")
    else:
        logger.info("✓ All steps complete! You can now:")
        logger.info("  - Evaluate on test set with test_model.py")
        logger.info("  - Make predictions with predict.py")
        logger.info("  - Visualize results with visualize_training.py")
        logger.info("  - Experiment with different hyperparameters")
        logger.info("  - Try different model architectures")

    logger.info("\n" + "=" * 70)
    logger.info("For detailed documentation, see: src/scripts/README.md")
    logger.info("=" * 70 + "\n")


if __name__ == "__main__":
    main()

