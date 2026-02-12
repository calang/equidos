#!/usr/bin/env python3
"""
Test the trained equid identification model on the test dataset.

This script evaluates the model on all images in data/THFtest, compares
predictions against ground truth (directory names), and generates a report
with accuracy statistics.

This experiment uses data from data/TunHorseDB2015F (face pictures only).
"""

import argparse
import csv
import logging
from pathlib import Path
from typing import List, Tuple, Dict

import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms, models

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EquidIdentificationModel(nn.Module):
    """
    Model for equid identification using ResNet50 backbone with embedding.
    """

    def __init__(self, num_classes: int, embedding_dim: int = 512):
        """
        Initialize the model.

        Args:
            num_classes: Number of individual equids to identify
            embedding_dim: Dimension of the embedding vector
        """
        super(EquidIdentificationModel, self).__init__()

        # Load pre-trained ResNet50
        self.backbone = models.resnet50(weights=None)

        # Get the number of features from the backbone
        num_features = self.backbone.fc.in_features

        # Replace the final fully connected layer with an identity
        self.backbone.fc = nn.Identity()

        # Create embedding layer
        self.embedding = nn.Sequential(
            nn.Linear(num_features, embedding_dim),
            nn.BatchNorm1d(embedding_dim),
            nn.ReLU(),
            nn.Dropout(0.5)
        )

        # Create classification head
        self.classifier = nn.Linear(embedding_dim, num_classes)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass through the model.

        Args:
            x: Input tensor of images

        Returns:
            Tuple of (embeddings, class_logits)
        """
        # Extract features using backbone
        features = self.backbone(x)

        # Generate embeddings
        embeddings = self.embedding(features)

        # Get class predictions
        logits = self.classifier(embeddings)

        return embeddings, logits


def load_model(
    model_path: Path,
    device: torch.device
) -> Tuple[nn.Module, List[str]]:
    """
    Load a trained model from file.

    Args:
        model_path: Path to the model file
        device: Device to load the model on

    Returns:
        Tuple of (loaded model, class names list)
    """
    logger.info(f"Loading model from: {model_path}")
    checkpoint = torch.load(model_path, map_location=device)

    num_classes = checkpoint['num_classes']
    embedding_dim = checkpoint['embedding_dim']
    class_names = checkpoint.get(
        'class_names',
        [str(i) for i in range(num_classes)]
    )

    model = EquidIdentificationModel(
        num_classes=num_classes,
        embedding_dim=embedding_dim
    )
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()

    logger.info(
        f"Model loaded (classes: {num_classes}, "
        f"embedding_dim: {embedding_dim})"
    )
    logger.info(f"Class names: {class_names}")

    return model, class_names


def preprocess_image(image_path: Path) -> torch.Tensor:
    """
    Preprocess an image for model input.

    Args:
        image_path: Path to the image file

    Returns:
        Preprocessed image tensor
    """
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension

    return image_tensor


def predict(
    model: nn.Module,
    image_tensor: torch.Tensor,
    device: torch.device
) -> Tuple[int, float]:
    """
    Make a prediction on an image.

    Args:
        model: The trained model
        image_tensor: Preprocessed image tensor
        device: Device to run inference on

    Returns:
        Tuple of (predicted_class, confidence)
    """
    image_tensor = image_tensor.to(device)

    with torch.no_grad():
        embeddings, logits = model(image_tensor)
        probabilities = torch.nn.functional.softmax(logits, dim=1)
        confidence, predicted_class = torch.max(probabilities, 1)

    return predicted_class.item(), confidence.item()


def collect_test_images(test_dir: Path) -> List[Tuple[Path, int]]:
    """
    Collect all test images with their ground truth labels.

    Args:
        test_dir: Path to the test data directory

    Returns:
        List of (image_path, ground_truth_label) tuples
    """
    test_images = []

    # Iterate through subdirectories (each is a class)
    for class_dir in sorted(test_dir.iterdir()):
        if not class_dir.is_dir():
            continue

        # Get class ID from directory name
        try:
            class_id = int(class_dir.name)
        except ValueError:
            logger.warning(f"Skipping non-numeric directory: {class_dir.name}")
            continue

        # Collect all images in this class directory
        for image_path in class_dir.glob('*.jpg'):
            test_images.append((image_path, class_id))

    logger.info(f"Found {len(test_images)} test images")
    return test_images


def evaluate_model(
    model: nn.Module,
    test_images: List[Tuple[Path, int]],
    device: torch.device,
    class_names: List[str]
) -> List[Dict]:
    """
    Evaluate the model on all test images.

    Args:
        model: The trained model
        test_images: List of (image_path, ground_truth) tuples
        device: Device to run inference on
        class_names: List of class names corresponding to class IDs

    Returns:
        List of result dictionaries
    """
    results = []

    for i, (image_path, ground_truth) in enumerate(test_images, 1):
        try:
            # Preprocess and predict
            image_tensor = preprocess_image(image_path)
            predicted_class, confidence = predict(model, image_tensor, device)

            # Get class name for prediction
            predicted_name = int(class_names[predicted_class])

            # Determine if prediction is correct
            is_correct = (predicted_name == ground_truth)

            # Get relative path, handling both absolute and relative paths
            try:
                rel_path = image_path.relative_to(Path.cwd())
            except ValueError:
                # Path is already relative or not in cwd
                rel_path = image_path

            result = {
                'image_path': str(rel_path),
                'ground_truth': ground_truth,
                'predicted': predicted_class,
                'predicted_name': predicted_name,
                'confidence': confidence,
                'correct': is_correct
            }
            results.append(result)

            # Log progress
            if i % 10 == 0:
                logger.info(f"Processed {i}/{len(test_images)} images")

        except Exception as e:
            logger.error(f"Error processing {image_path}: {e}")

    return results


def save_results(results: List[Dict], output_path: Path):
    """
    Save test results to a CSV file.

    Args:
        results: List of result dictionaries
        output_path: Path to save the output CSV file
    """
    # Calculate accuracy
    correct_predictions = sum(1 for r in results if r['correct'])
    total_predictions = len(results)
    accuracy = (correct_predictions / total_predictions * 100
                if total_predictions > 0 else 0)

    logger.info(f"Saving results to: {output_path}")

    with open(output_path, 'w', newline='') as csvfile:
        # Write summary footer
        csvfile.write(f"# Test Results Summary\n")
        csvfile.write(f"# Total Images: {total_predictions}\n")
        csvfile.write(f"# Correct Predictions: {correct_predictions}\n")
        csvfile.write(
            f"# Incorrect Predictions: {total_predictions - correct_predictions}\n"
        )
        csvfile.write(f"# Accuracy: {accuracy:.2f}%\n")
        csvfile.write("#\n")

        # Write detailed results
        fieldnames = [
            'image_path',
            'ground_truth',
            'predicted',
            'predicted_name',
            'confidence',
            'result'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow({
                'image_path': result['image_path'],
                'ground_truth': result['ground_truth'],
                'predicted': result['predicted'],
                'predicted_name': result['predicted_name'],
                'confidence': f"{result['confidence']:.4f}",
                'result': 'HIT' if result['correct'] else 'MISS'
            })

    logger.info("Results saved successfully")


def main():
    """Main function to test the model."""
    parser = argparse.ArgumentParser(
        description='Test trained equid identification model'
    )
    parser.add_argument(
        '--test-dir',
        type=str,
        default='data/THFtest',
        help='Path to test data directory (default: data/THFtest)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='experiments/ResNet50-47F/models/best_model.pth',
        help='Path to model file (default: experiments/ResNet50-47F/models/best_model.pth)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='experiments/ResNet50-47F/test_results.csv',
        help='Output file path (default: experiments/ResNet50-47F/test_results.csv)'
    )

    args = parser.parse_args()

    # Setup paths
    test_dir = Path(args.test_dir)
    model_path = Path(args.model)
    output_path = Path(args.output)

    # Validate paths
    if not test_dir.exists():
        logger.error(f"Test directory not found: {test_dir}")
        return

    if not model_path.exists():
        logger.error(f"Model file not found: {model_path}")
        return

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Check for GPU availability
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    # Load model
    model, class_names = load_model(model_path, device)

    # Collect test images
    test_images = collect_test_images(test_dir)

    if not test_images:
        logger.error("No test images found")
        return

    # Run evaluation
    logger.info("Starting evaluation...")
    results = evaluate_model(model, test_images, device, class_names)

    # Save results
    save_results(results, output_path)

    # Display summary
    correct = sum(1 for r in results if r['correct'])
    total = len(results)
    accuracy = correct / total * 100 if total > 0 else 0

    logger.info("=" * 70)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Total images tested: {total}")
    logger.info(f"Correct predictions (HIT): {correct}")
    logger.info(f"Incorrect predictions (MISS): {total - correct}")
    logger.info(f"Accuracy: {accuracy:.2f}%")
    logger.info("=" * 70)
    logger.info(f"Detailed results saved to: {output_path}")


if __name__ == "__main__":
    main()

