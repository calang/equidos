#!/usr/bin/env python3
"""
Train a model for equid identification using transfer learning.

This script creates a model based on a pre-trained vision backbone (ResNet50),
adds classification layers, and trains it on the prepared dataset to identify
individual equids from face images.

This experiment uses data from data/TunHorseDB2015F (face pictures only).
"""

import argparse
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
TRAIN_DIR = Path('data/THFtraining')
VAL_DIR = Path('data/THFvalidation')
TEST_DIR = Path('data/THFtest')
NORMALIZATION_FILE = Path('data/THFtraining/normalization.json')
MODEL_DIR = Path('models')
EMBEDDING_DIM = 512
BATCH_SIZE = 32
NUM_EPOCHS = 50
LEARNING_RATE = 0.001
MOMENTUM = 0.9
RANDOM_SEED = 42


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
        self.backbone = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

        # Get the number of features from the backbone
        num_features = self.backbone.fc.in_features

        # Replace the final fully connected layer with an embedding layer
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


def load_normalization(normalization_file: Path) -> Tuple[List[float], List[float]]:
    """
    Load normalization values from JSON file.

    Args:
        normalization_file: Path to the normalization JSON file

    Returns:
        Tuple of (mean, std) lists

    Raises:
        FileNotFoundError: If normalization file doesn't exist
    """
    if not normalization_file.exists():
        raise FileNotFoundError(
            f"Normalization file not found: {normalization_file}\n"
            "Please run prep_data.py first to prepare the data and calculate normalization values."
        )

    with open(normalization_file, 'r') as f:
        data = json.load(f)

    mean = data['mean']
    std = data['std']
    logger.info(f"Loaded normalization values - Mean: {mean}, Std: {std}")

    return mean, std


def get_data_loaders(batch_size: int, mean: List[float], std: List[float]) -> Tuple[DataLoader, DataLoader, DataLoader, int, list[str]]:
    """
    Create data loaders for training, validation, and testing.

    Args:
        batch_size: Batch size for data loaders
        mean: Mean values for normalization (RGB)
        std: Standard deviation values for normalization (RGB)

    Returns:
        Tuple of (train_loader, val_loader, test_loader, num_classes, class_names)
    """
    # Data transforms with loaded normalization values
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])

    val_test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])

    # Load datasets
    train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=train_transform)
    val_dataset = datasets.ImageFolder(VAL_DIR, transform=val_test_transform)
    test_dataset = datasets.ImageFolder(TEST_DIR, transform=val_test_transform)

    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )

    num_classes = len(train_dataset.classes)
    class_names = train_dataset.classes
    logger.info(f"Number of classes (individual equids): {num_classes}")
    logger.info(f"Class names: {class_names}")
    logger.info(f"Training samples: {len(train_dataset)}")
    logger.info(f"Validation samples: {len(val_dataset)}")
    logger.info(f"Test samples: {len(test_dataset)}")

    return train_loader, val_loader, test_loader, num_classes, class_names


def train_epoch(model: nn.Module,
                train_loader: DataLoader,
                criterion: nn.Module,
                optimizer: optim.Optimizer,
                device: torch.device) -> Tuple[float, float]:
    """
    Train the model for one epoch.

    Args:
        model: The model to train
        train_loader: DataLoader for training data
        criterion: Loss function
        optimizer: Optimizer
        device: Device to train on (CPU or CUDA)

    Returns:
        Tuple of (average_loss, accuracy)
    """
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in train_loader:
        inputs = inputs.to(device)
        labels = labels.to(device)

        # Zero the parameter gradients
        optimizer.zero_grad()

        # Forward pass
        embeddings, logits = model(inputs)

        # Calculate loss
        loss = criterion(logits, labels)

        # Backward pass and optimize
        loss.backward()
        optimizer.step()

        # Statistics
        running_loss += loss.item() * inputs.size(0)
        _, predicted = torch.max(logits, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / total
    epoch_acc = 100.0 * correct / total

    return epoch_loss, epoch_acc


def validate(model: nn.Module,
             val_loader: DataLoader,
             criterion: nn.Module,
             device: torch.device) -> Tuple[float, float]:
    """
    Validate the model.

    Args:
        model: The model to validate
        val_loader: DataLoader for validation data
        criterion: Loss function
        device: Device to validate on (CPU or CUDA)

    Returns:
        Tuple of (average_loss, accuracy)
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            # Forward pass
            embeddings, logits = model(inputs)

            # Calculate loss
            loss = criterion(logits, labels)

            # Statistics
            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(logits, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    val_loss = running_loss / total
    val_acc = 100.0 * correct / total

    return val_loss, val_acc


def train_model(num_epochs: int = NUM_EPOCHS) -> None:
    """
    Main function to train the equid identification model.

    Args:
        num_epochs: Number of training epochs (default: 50)
    """
    # Set random seed for reproducibility
    torch.manual_seed(RANDOM_SEED)

    # Check if data directories exist
    for directory in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        if not directory.exists():
            logger.error(f"Data directory not found: {directory}")
            raise FileNotFoundError(f"Data directory not found: {directory}")

    # Create model directory
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Load normalization values
    logger.info("Loading normalization values...")
    mean, std = load_normalization(NORMALIZATION_FILE)

    # Check for GPU availability
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    # Load data
    logger.info("Loading data...")
    train_loader, val_loader, test_loader, num_classes, class_names = get_data_loaders(BATCH_SIZE, mean, std)

    # Create model
    logger.info("Creating model...")
    model = EquidIdentificationModel(num_classes=num_classes, embedding_dim=EMBEDDING_DIM)
    model = model.to(device)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE, momentum=MOMENTUM)

    # Learning rate scheduler
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=15, gamma=0.1)

    # Training loop
    logger.info("=" * 60)
    logger.info("Starting training...")
    logger.info(f"Number of epochs: {num_epochs}")
    logger.info("=" * 60)

    best_val_acc = 0.0
    best_model_path = MODEL_DIR / "best_model.pth"
    training_history: Dict[str, list] = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }

    start_time = time.time()

    for epoch in range(num_epochs):
        epoch_start = time.time()

        # Train for one epoch
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device
        )

        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion, device)

        # Update learning rate
        scheduler.step()

        # Save history
        training_history['train_loss'].append(train_loss)
        training_history['train_acc'].append(train_acc)
        training_history['val_loss'].append(val_loss)
        training_history['val_acc'].append(val_acc)

        epoch_time = time.time() - epoch_start

        # Log progress
        logger.info(
            f"Epoch [{epoch + 1}/{num_epochs}] "
            f"Train Loss: {train_loss:.4f} Train Acc: {train_acc:.2f}% "
            f"Val Loss: {val_loss:.4f} Val Acc: {val_acc:.2f}% "
            f"Time: {epoch_time:.2f}s"
        )

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch + 1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'val_loss': val_loss,
                'num_classes': num_classes,
                'embedding_dim': EMBEDDING_DIM,
                'class_names': class_names,
                'normalization': {'mean': mean, 'std': std}
            }, best_model_path)
            logger.info(f"  → Saved best model with validation accuracy: {val_acc:.2f}%")

    total_time = time.time() - start_time

    # Final evaluation on test set
    logger.info("=" * 60)
    logger.info("Training completed!")
    logger.info(f"Total training time: {total_time / 60:.2f} minutes")
    logger.info(f"Best validation accuracy: {best_val_acc:.2f}%")

    # Load best model and evaluate on test set
    logger.info("=" * 60)
    logger.info("Evaluating on test set...")
    checkpoint = torch.load(best_model_path)
    model.load_state_dict(checkpoint['model_state_dict'])

    test_loss, test_acc = validate(model, test_loader, criterion, device)
    logger.info(f"Test Loss: {test_loss:.4f}")
    logger.info(f"Test Accuracy: {test_acc:.2f}%")

    # Save final model
    final_model_path = MODEL_DIR / "final_model.pth"
    torch.save({
        'model_state_dict': model.state_dict(),
        'num_classes': num_classes,
        'embedding_dim': EMBEDDING_DIM,
        'test_acc': test_acc,
        'test_loss': test_loss,
        'training_history': training_history,
        'class_names': class_names,
        'normalization': {'mean': mean, 'std': std}
    }, final_model_path)
    logger.info(f"Saved final model to: {final_model_path}")

    logger.info("=" * 60)


def main():
    """Parse arguments and start training."""
    parser = argparse.ArgumentParser(
        description='Train equid identification model using transfer learning'
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=50,
        help='Number of training epochs (default: 50)'
    )

    args = parser.parse_args()

    # Start training
    train_model(num_epochs=args.epochs)


if __name__ == "__main__":
    main()

