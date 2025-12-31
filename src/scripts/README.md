# Model Training and Prediction Scripts

This directory contains scripts for training and using equid identification models.

## Scripts

### 1. `train_model.py` - Train Equid Identification Model

This script creates and trains a deep learning model for identifying individual equids based on face images.

#### Features
- Uses ResNet50 as a pre-trained backbone
- Includes an embedding layer (512-dimensional vector) for feature extraction
- Transfer learning with fine-tuning
- Data augmentation for training robustness
- Validation monitoring to prevent overfitting
- Saves best model based on validation accuracy
- Comprehensive logging of training progress

#### Prerequisites
Ensure the data has been prepared by running `prep_data.py` first. This will create:
- `data/THGtraining/` - Training set (70% of images)
- `data/THGvalidation/` - Validation set (15% of images)
- `data/THGtest/` - Test set (15% of images)

#### Usage
```bash
./src/scripts/train_model.py 2>&1 | tee experiments/ResNet50-47/train_model_$(date +%Y%m%d_%H%M%S).log
```

Or with Python:
```bash
python src/scripts/train_model.py
```

#### Configuration
Key parameters can be modified at the top of the script:
- `BATCH_SIZE`: Number of images per batch (default: 32)
- `NUM_EPOCHS`: Number of training epochs (default: 50)
- `LEARNING_RATE`: Initial learning rate (default: 0.001)
- `EMBEDDING_DIM`: Dimension of embedding vector (default: 512)

#### Output
The script creates a `models/` directory with:
- `best_model.pth` - Model checkpoint with best validation accuracy
- `final_model.pth` - Final model with complete training history

Model files contain:
- Model weights (state_dict)
- Number of classes
- Embedding dimension
- Performance metrics
- Training history

#### Training Process
1. **Data Loading**: Loads images from prepared directories
2. **Model Creation**: Initializes ResNet50 backbone with custom classification head
3. **Training Loop**: 
   - Trains for specified number of epochs
   - Applies data augmentation to training images
   - Validates after each epoch
   - Saves model when validation accuracy improves
   - Adjusts learning rate every 15 epochs
4. **Final Evaluation**: Tests the best model on the test set
5. **Model Saving**: Saves both best and final models

#### Expected Output
```
2025-12-23 10:00:00 - INFO - Using device: cuda:0
2025-12-23 10:00:01 - INFO - Loading data...
2025-12-23 10:00:02 - INFO - Number of classes (individual equids): 45
2025-12-23 10:00:02 - INFO - Training samples: 2450
2025-12-23 10:00:02 - INFO - Validation samples: 525
2025-12-23 10:00:02 - INFO - Test samples: 525
2025-12-23 10:00:03 - INFO - Creating model...
============================================================
2025-12-23 10:00:05 - INFO - Starting training...
============================================================
2025-12-23 10:01:30 - INFO - Epoch [1/50] Train Loss: 2.3456 Train Acc: 35.67% Val Loss: 1.8932 Val Acc: 45.23% Time: 85.32s
2025-12-23 10:01:30 - INFO -   → Saved best model with validation accuracy: 45.23%
...
```

---

### 2. `predict.py` - Make Predictions with Trained Model

This script loads a trained model and makes predictions on new equid face images.

#### Features
- Loads trained model from file
- Preprocesses input images
- Returns predicted class and confidence score
- Optionally displays embedding vector
- GPU acceleration when available

#### Usage
```bash
./src/scripts/predict.py <image_path> [options]
```

#### Arguments
- `image_path` - Path to the image file to classify (required)
- `--model` - Path to the model file (default: `models/best_model.pth`)
- `--show-embedding` - Display the embedding vector

#### Examples

Basic prediction:
```bash
./src/scripts/predict.py data/horsefacecrop/Part01_Base01_F01.jpg
```

Using a specific model:
```bash
./src/scripts/predict.py data/test_image.jpg --model models/final_model.pth
```

Show embedding vector:
```bash
./src/scripts/predict.py data/test_image.jpg --show-embedding
```

#### Output
```
2025-12-23 10:30:00 - INFO - Using device: cuda:0
2025-12-23 10:30:01 - INFO - Loading model from: models/best_model.pth
2025-12-23 10:30:02 - INFO - Model loaded successfully (classes: 45, embedding_dim: 512)
2025-12-23 10:30:02 - INFO - Processing image: data/horsefacecrop/Part01_Base01_F01.jpg
============================================================
2025-12-23 10:30:02 - INFO - PREDICTION RESULTS
============================================================
2025-12-23 10:30:02 - INFO - Predicted Class ID: 12
2025-12-23 10:30:02 - INFO - Confidence: 87.45%
============================================================
```

---

### 3. `visualize_training.py` - Visualize Training Progress

This script loads a trained model and displays training metrics and plots.

#### Features
- Displays model information (classes, embedding dimension, etc.)
- Shows training summary statistics
- Plots loss and accuracy curves
- Can save plots to file

#### Usage
```bash
./src/scripts/visualize_training.py [options]
```

#### Arguments
- `--model` - Path to the model file (default: `models/final_model.pth`)
- `--plot` - Display training plots interactively
- `--save-plot` - Save plot to specified file path

#### Examples

View model information:
```bash
./src/scripts/visualize_training.py
```

Display training plots:
```bash
./src/scripts/visualize_training.py --plot
```

Save plots to file:
```bash
./src/scripts/visualize_training.py --save-plot training_history.png
```

Use specific model:
```bash
./src/scripts/visualize_training.py --model models/best_model.pth --plot
```

#### Output
```
2025-12-23 11:00:00 - INFO - Loading model from: models/final_model.pth
============================================================
2025-12-23 11:00:00 - INFO - MODEL INFORMATION
============================================================
2025-12-23 11:00:00 - INFO - Number of classes: 45
2025-12-23 11:00:00 - INFO - Embedding dimension: 512
2025-12-23 11:00:00 - INFO - Trained for 50 epochs
2025-12-23 11:00:00 - INFO - Test accuracy: 89.52%
2025-12-23 11:00:00 - INFO - Test loss: 0.3245
============================================================
2025-12-23 11:00:00 - INFO - TRAINING SUMMARY
============================================================
2025-12-23 11:00:00 - INFO - Total epochs: 50
2025-12-23 11:00:00 - INFO - Final training accuracy: 95.67%
2025-12-23 11:00:00 - INFO - Best training accuracy: 96.23%
2025-12-23 11:00:00 - INFO - Final validation accuracy: 91.43%
2025-12-23 11:00:00 - INFO - Best validation accuracy: 92.38% (epoch 42)
2025-12-23 11:00:00 - INFO - Final training loss: 0.1234
2025-12-23 11:00:00 - INFO - Best training loss: 0.1087
2025-12-23 11:00:00 - INFO - Final validation loss: 0.2987
2025-12-23 11:00:00 - INFO - Best validation loss: 0.2654
============================================================
```

---

## Model Architecture

The equid identification model consists of:

1. **Backbone**: ResNet50 pre-trained on ImageNet
   - Extracts visual features from horse face images
   - Layers are fine-tuned during training

2. **Embedding Layer**: Fully connected layer (2048 → 512)
   - Creates a compact representation of each equid's face
   - Used for similarity comparison
   - Includes batch normalization, ReLU, and dropout

3. **Classification Head**: Linear layer (512 → num_classes)
   - Maps embeddings to individual equid identities
   - Trained with cross-entropy loss

## Data Augmentation

Training images undergo the following augmentations:
- Random horizontal flip
- Random rotation (±10 degrees)
- Color jitter (brightness, contrast, saturation)
- Resize to 224×224 pixels
- Normalization using ImageNet statistics

Validation and test images are only resized and normalized.

## Training Strategy

1. **Transfer Learning**: Start with ResNet50 pre-trained on ImageNet
2. **Fine-tuning**: All layers are trainable to adapt to equid faces
3. **Learning Rate Schedule**: Reduce learning rate by 10× every 15 epochs
4. **Early Stopping**: Save model with best validation accuracy
5. **Regularization**: Dropout (0.5) to prevent overfitting

## Performance Monitoring

The training script logs:
- Training loss and accuracy per epoch
- Validation loss and accuracy per epoch
- Time per epoch
- Best validation accuracy achieved
- Final test set performance

## Requirements

Python packages (see `env.yml`):
- pytorch
- torchvision
- pillow
- python >= 3.11

GPU recommended for faster training (CUDA-compatible).

## Troubleshooting

**Error: "Data directory not found"**
- Run `prep_data.py` first to prepare the training data

**Error: "Model file not found"**
- Ensure `train_model.py` has completed successfully
- Check that `models/best_model.pth` exists

**Low accuracy**
- Increase number of epochs
- Try different learning rates
- Ensure sufficient training data per class
- Check image quality and preprocessing

**Out of memory**
- Reduce batch size
- Use CPU instead of GPU (slower but less memory)
- Close other applications

## Next Steps

After training a model:
1. Evaluate performance on test set
2. Analyze confusion matrix to identify difficult cases
3. Experiment with different architectures (Vision Transformer)
4. Implement similarity search using embeddings
5. Deploy model to mobile application
6. Collect more training data for underrepresented equids

## References

- ResNet: [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)
- Transfer Learning: [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

