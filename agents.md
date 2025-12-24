# AI Coding Agent Instructions

## Project Description
See [Project_Description](Project_Description.md) for details, to understand the project context.

## Coding Standards
Follow the contents in all files under the `coding_standards/` directory.

## File formats and other references
Follow the contents in all files under the `agent_references/` directory.

## Project approach
Consider ideas described in  `agent_prompts/find_models_out.md`.

## Current approach
### Prepare data
  - Split image files within each subdirectory in `data/TunHorseDB2015G` in three sets: training, validation, and testing.
  - Ensure that each set has images from all individual equids, with no overlap between sets.
  - training set: 70% of images
  - validation set: 15% of images
  - testing set: 15% of images
### Build model
  - Use a pre-trained vision model as a backbone (e.g., Vision Transformer, ResNet).
  - Add layers on top of the backbone to create a classification head for identifying individual equids.
  - Use techniques like transfer learning and fine-tuning to adapt the model to the specific task.
  - The model is to include, as one of its layers a vector embedding from the face or muzzle image using a vision model.
### Train model
  - Use the training set to train the model.
  - Monitor performance on the validation set to tune hyperparameters and prevent overfitting.
### Evaluate model
  - Use the testing set to evaluate the final model's performance.
### Save model
  - Save the trained model to a file for later use in the mobile app.


