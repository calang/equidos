# ResNet50 Experiment

## Task
Develop an image classification model using ResNet50 to identify individual horses from images, with the dataset located at "/content/drive/MyDrive/equidos".

The project includes:
- Dataset preparation (organizing into training, validation, and test sets)
- Applying appropriate data transformations and normalization for ResNet
- Training the model with a validation loop
- Evaluating its performance using accuracy and a confusion matrix
- Creating a function to predict a horse from a new image

## Dataset link

[Dataset link](https://drive.google.com/drive/folders/1bjlwqtK-vFaOxL1ogbCCzbeuXp43tud0).

## Colab Link

[Colab Link](https://colab.research.google.com/drive/1PM58yQYGgp-jvzo5E0AJ0Zm8mhGRalYr?usp=sharing).


## Comments
This experiment uses **transfer learning** with the ResNet50 architecture, replacing or adding its final layers to identify individual horses from a given dataset of **5 possible classes**.

 Test data set consists of a total of **56** test images, distributed among the 5 classes: 16, 12, 10, 6, 12 images respectively.

### Pros
- Shared confusion matrix shows a perfect score, motivating further exploration of this architecture for horse identification.

### Cons
- This experiment assumes a fixed population of horses (5 classes).  Adding new horses would require retraining the model.
