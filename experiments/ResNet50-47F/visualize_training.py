#!/usr/bin/env python3
"""
Visualize training history and model performance.

This script loads a trained model and displays training metrics,
including loss curves and accuracy over epochs.

This experiment uses data from data/TunHorseDB2015F (face pictures only).
"""

import argparse
import logging
from pathlib import Path

import torch

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def plot_training_history(history: dict, output_path: Path = None) -> None:
    """
    Plot training and validation metrics.

    Args:
        history: Dictionary containing training history
        output_path: Optional path to save the plot
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.error("matplotlib is required for plotting. Install with: conda install matplotlib")
        return

    epochs = range(1, len(history['train_loss']) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Plot loss
    ax1.plot(epochs, history['train_loss'], 'b-', label='Training Loss')
    ax1.plot(epochs, history['val_loss'], 'r-', label='Validation Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.legend()
    ax1.grid(True)

    # Plot accuracy
    ax2.plot(epochs, history['train_acc'], 'b-', label='Training Accuracy')
    ax2.plot(epochs, history['val_acc'], 'r-', label='Validation Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_title('Training and Validation Accuracy')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Plot saved to: {output_path}")
    else:
        plt.show()


def display_model_info(checkpoint: dict) -> None:
    """
    Display model information and statistics.

    Args:
        checkpoint: Model checkpoint dictionary
    """
    logger.info("=" * 60)
    logger.info("MODEL INFORMATION")
    logger.info("=" * 60)

    if 'num_classes' in checkpoint:
        logger.info(f"Number of classes: {checkpoint['num_classes']}")

    if 'embedding_dim' in checkpoint:
        logger.info(f"Embedding dimension: {checkpoint['embedding_dim']}")

    if 'epoch' in checkpoint:
        logger.info(f"Trained for {checkpoint['epoch']} epochs")

    if 'val_acc' in checkpoint:
        logger.info(f"Best validation accuracy: {checkpoint['val_acc']:.2f}%")

    if 'val_loss' in checkpoint:
        logger.info(f"Best validation loss: {checkpoint['val_loss']:.4f}")

    if 'test_acc' in checkpoint:
        logger.info(f"Test accuracy: {checkpoint['test_acc']:.2f}%")

    if 'test_loss' in checkpoint:
        logger.info(f"Test loss: {checkpoint['test_loss']:.4f}")

    logger.info("=" * 60)


def display_training_summary(history: dict) -> None:
    """
    Display training summary statistics.

    Args:
        history: Dictionary containing training history
    """
    if not history:
        logger.warning("No training history available")
        return

    logger.info("=" * 60)
    logger.info("TRAINING SUMMARY")
    logger.info("=" * 60)

    num_epochs = len(history.get('train_loss', []))
    logger.info(f"Total epochs: {num_epochs}")

    if 'train_acc' in history and history['train_acc']:
        final_train_acc = history['train_acc'][-1]
        best_train_acc = max(history['train_acc'])
        logger.info(f"Final training accuracy: {final_train_acc:.2f}%")
        logger.info(f"Best training accuracy: {best_train_acc:.2f}%")

    if 'val_acc' in history and history['val_acc']:
        final_val_acc = history['val_acc'][-1]
        best_val_acc = max(history['val_acc'])
        best_epoch = history['val_acc'].index(best_val_acc) + 1
        logger.info(f"Final validation accuracy: {final_val_acc:.2f}%")
        logger.info(f"Best validation accuracy: {best_val_acc:.2f}% (epoch {best_epoch})")

    if 'train_loss' in history and history['train_loss']:
        final_train_loss = history['train_loss'][-1]
        best_train_loss = min(history['train_loss'])
        logger.info(f"Final training loss: {final_train_loss:.4f}")
        logger.info(f"Best training loss: {best_train_loss:.4f}")

    if 'val_loss' in history and history['val_loss']:
        final_val_loss = history['val_loss'][-1]
        best_val_loss = min(history['val_loss'])
        logger.info(f"Final validation loss: {final_val_loss:.4f}")
        logger.info(f"Best validation loss: {best_val_loss:.4f}")

    logger.info("=" * 60)


def main():
    """Main function to visualize model training."""
    parser = argparse.ArgumentParser(description='Visualize training history and model performance')
    parser.add_argument('--model', type=str, default='experiments/ResNet50-47F/models/final_model.pth',
                        help='Path to the model file (default: experiments/ResNet50-47F/models/final_model.pth)')
    parser.add_argument('--plot', action='store_true',
                        help='Show training plots')
    parser.add_argument('--save-plot', type=str,
                        help='Save plot to file instead of displaying')

    args = parser.parse_args()

    model_path = Path(args.model)

    if not model_path.exists():
        logger.error(f"Model file not found: {model_path}")
        return

    # Load checkpoint
    logger.info(f"Loading model from: {model_path}")
    checkpoint = torch.load(model_path, map_location='cpu')

    # Display model information
    display_model_info(checkpoint)

    # Display training summary if available
    if 'training_history' in checkpoint:
        history = checkpoint['training_history']
        display_training_summary(history)

        # Plot if requested
        if args.plot or args.save_plot:
            output_path = Path(args.save_plot) if args.save_plot else None
            plot_training_history(history, output_path)
    else:
        logger.warning("No training history found in this model file")


if __name__ == "__main__":
    main()

