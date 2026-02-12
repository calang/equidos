# ResNet50-47

Train a model for equid identification using transfer learning, learning to identify the 47 individual equids in the dataset.

This script creates a model based on a pre-trained vision backbone (ResNet50),
adds classification layers, and trains it on the prepared dataset to identify
individual equids from face images.

## Model Details
- **Backbone**: ResNet50 pre-trained on ImageNet
- **Embedding Layer**: 512-dimensional vector for feature extraction
- **Classification Head**: Fully connected layer for 47 classes (individual equids)
- **Training**: Transfer learning with fine-tuning on the equid dataset
- **Data Augmentation**: Applied to training images for robustness
- **Validation Monitoring**: To prevent overfitting and save the best model
- **Output**: Saves the best model based on validation accuracy and final model
after training completion.
- **Training Epochs**: 50
- **Batch Size**: 32
- **Learning Rate**: 0.001
- **Learning Rate Decay**: Reduced by a factor of 10 every 15 epochs
- **Optimizer**: Adam
- **Loss Function**: Cross-Entropy Loss
- **Device**: Utilizes GPU if available for faster training
- **Logging**: Comprehensive logging of training progress and metrics
- **Model Saving**: Saves model state, performance metrics, and training history

## Scripts in this Directory

- `prep_data.py` - Script for preparing data (splitting into train/val/test sets)
- `train_model.py` - Script for training the model
- `test_model.py` - Script for evaluating model performance on the test dataset
- `predict.py` - Script for making predictions with the trained model
- `visualize_training.py` - Script for visualizing training progress
- `quickstart.py` - Interactive workflow guide
- `README.md` - This file

## Data Directory Structure

- `data/THGtraining/` - Training set (70% of images)
- `data/THGvalidation/` - Validation set (15% of images)
- `data/THGtest/` - Test set (15% of images)
- `models/` - Directory where trained models are saved

## Usage

See the README.md in each script or run with `--help` for detailed usage instructions.

**Train the model:**
```bash
./experiments/ResNet50-47/train_model.py
```

**Evaluate on test set:**
```bash
./experiments/ResNet50-47/test_model.py
# or with custom options:
./experiments/ResNet50-47/test_model.py --test-dir data/THGtest --output results.csv
```

**Make predictions:**
```bash
./experiments/ResNet50-47/predict.py <image_path>
```

**Visualize training:**
```bash
./experiments/ResNet50-47/visualize_training.py --plot
```

**Quick start guide:**
```bash
./experiments/ResNet50-47/quickstart.py
```

**Or**, use rules in the main `Makefile`

## References

- ResNet: [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)
- Transfer Learning: [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
