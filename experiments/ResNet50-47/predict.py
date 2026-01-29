#!/usr/bin/env python3
"""
Make predictions using a trained equid identification model.

This script loads a trained model and makes predictions on new images,
returning the predicted equid identity and confidence score.
"""

import argparse
import logging
from pathlib import Path
from typing import Tuple

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
    Model for equid identification using ResNet50 backbone with embedding layer.
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

    def get_embedding(self, x: torch.Tensor) -> torch.Tensor:
        """
        Get embedding vector for an input image.

        Args:
            x: Input tensor of images

        Returns:
            Embedding tensor
        """
        features = self.backbone(x)
        embeddings = self.embedding(features)
        return embeddings


def load_model(model_path: Path, device: torch.device) -> Tuple[nn.Module, dict]:
    """
    Load a trained model from file.

    Args:
        model_path: Path to the model file
        device: Device to load the model on

    Returns:
        Tuple of (model, metadata)
    """
    logger.info(f"Loading model from: {model_path}")
    checkpoint = torch.load(model_path, map_location=device)

    num_classes = checkpoint['num_classes']
    embedding_dim = checkpoint['embedding_dim']

    model = EquidIdentificationModel(num_classes=num_classes, embedding_dim=embedding_dim)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()

    logger.info(f"Model loaded successfully (classes: {num_classes}, embedding_dim: {embedding_dim})")

    return model, checkpoint


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


def predict(model: nn.Module,
            image_tensor: torch.Tensor,
            device: torch.device) -> Tuple[int, float, torch.Tensor]:
    """
    Make a prediction on an image.

    Args:
        model: The trained model
        image_tensor: Preprocessed image tensor
        device: Device to run inference on

    Returns:
        Tuple of (predicted_class, confidence, embedding)
    """
    image_tensor = image_tensor.to(device)

    with torch.no_grad():
        embeddings, logits = model(image_tensor)
        probabilities = torch.nn.functional.softmax(logits, dim=1)
        confidence, predicted_class = torch.max(probabilities, 1)

    return predicted_class.item(), confidence.item(), embeddings


def main():
    """Main function to make predictions."""
    parser = argparse.ArgumentParser(description='Make predictions with trained equid identification model')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    parser.add_argument('--model', type=str, default='models/best_model.pth',
                        help='Path to the model file (default: models/best_model.pth)')
    parser.add_argument('--show-embedding', action='store_true',
                        help='Show the embedding vector')

    args = parser.parse_args()

    # Setup
    image_path = Path(args.image_path)
    model_path = Path(args.model)

    if not image_path.exists():
        logger.error(f"Image file not found: {image_path}")
        return

    if not model_path.exists():
        logger.error(f"Model file not found: {model_path}")
        return

    # Check for GPU availability
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    # Load model
    model, metadata = load_model(model_path, device)

    # Get class names if available
    class_names = metadata.get('class_names', None)

    # Preprocess image
    logger.info(f"Processing image: {image_path}")
    image_tensor = preprocess_image(image_path)

    # Make prediction
    predicted_class, confidence, embedding = predict(model, image_tensor, device)

    # Display results
    logger.info("=" * 60)
    logger.info("PREDICTION RESULTS")
    logger.info("=" * 60)
    logger.info(f"Predicted Class ID: {predicted_class}")
    if class_names and predicted_class < len(class_names):
        logger.info(f"Predicted Class Name: {class_names[predicted_class]}")
    logger.info(f"Confidence: {confidence * 100:.2f}%")

    if args.show_embedding:
        logger.info(f"Embedding vector shape: {embedding.shape}")
        logger.info(f"Embedding vector: {embedding.cpu().numpy()}")

    logger.info("=" * 60)


if __name__ == "__main__":
    main()

