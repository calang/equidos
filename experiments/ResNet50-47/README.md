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
- Optimizer**: Adam
- **Loss Function**: Cross-Entropy Loss
- **Device**: Utilizes GPU if available for faster training
- **Logging**: Comprehensive logging of training progress and metrics
- **Model Saving**: Saves model state, performance metrics, and training history
- **Directory Structure**:
  - `data/THGtraining/`: Training set (70% of images)
  - `data/THGvalidation/`: Validation set (15% of images)
  - `data/THGtest/`: Test set (15% of images)
  - `models/`: Directory where trained models are saved
  - `logs/`: Directory for training logs
  - `src/scripts/train_model.py`: Script for training the model
  - `src/models/resnet_model.py`: Model architecture definition
  - `src/utils/data_utils.py`: Data loading and augmentation utilities
  - `src/utils/train_utils.py`: Training and evaluation utilities
  - `src/utils/logger.py`: Logging utilities
  - `src/utils/save_utils.py`: Model saving and loading utilities
  - `src/utils/config.py`: Configuration parameters
  - `src/visualize/plot_training.py`: Script for visualizing training progress
  - `src/predict/predict.py`: Script for making predictions with the trained model
