# Equids - Project Description
Visual identification of equids (horses, donkeys, mules) pre-registered individuals.

## Overview
This repository contains code, initial training data and documentation for a visual identification model for equids.

The system leverages computer vision and machine learning techniques to identify individual equids based on images of their faces.

## Motivation
The current method of identifying equids relies on microchips, which can be invasive and sometimes unreliable. By developing a visual identification system, we aim to provide a non-invasive, efficient, and scalable solution for equid identification.

Numerous rural communities in Costa Rica depend on equids for transportation and agricultural work. Proper identification is crucial for managing health records, ownership, and welfare of these animals. A visual identification system can significantly enhance the ability to monitor and care for equids in these communities.

## General Objectives
Identify equids by their faces to progressively replace the use of chips, achieving a less invasive and more efficient alternative.

## Specific Objectives
The system to be built must be capable of
- identifying equids from images taken in various conditions, including different lighting, angles, and backgrounds.
- handling a growing database of equid individuals as more animals are registered over time
- being user-friendly for non-technical users, such as farmers and veterinarians.
- operating on mobile devices to facilitate field use.
- operate in offline mode, considering that rural areas may have limited internet connectivity.
- scaling to accommodate a large number of equids as the system is adopted more widely.
- being adaptable to different equid species, including horses, donkeys, and mules.
- being open-source to encourage community contributions and improvements.
- providing comprehensive documentation to assist users in setup and operation.
- ensuring data privacy and security, especially regarding ownership information.

## Features
- Image preprocessing and augmentation
- Feature extraction using deep learning models
- Individual identification and classification
- Addition of new individuals to the database
- Performance evaluation metrics
- User-friendly interface for uploading and identifying equid images
- Support for multiple equid species
- Open-source and customizable codebase
- Scalability for large datasets
- Extensive documentation and examples

## Context: Number of Equids to Identify
Currently, as of 2025, around **850** equids have been identified nationwide. The intention is for this system to scale and also be used outside of Costa Rica.

## Available Data or Data Sources
To get started, we could rely on datasets available on the web or, ideally, coordinate photo sampling sessions at one of the locations we previously visited, ensuring the quality and consistency of the images.

## Performance Requirements
The ideal would be to maximize the model's accuracy, as the ultimate goal is to replace the chip-based identification method.

## Operational Requirements
Identification would be via a mobile device, like a mobile phone.

## Evaluation Metrics
### Key Performance Indicators (KPIs)
- Accuracy: Percentage of correctly identified equids.
- Precision and Recall: To evaluate the model's performance in identifying individual equids.
- F1 Score: To balance precision and recall.
- Inference Time: Time taken to identify an equid from an image.
- User Satisfaction: Feedback from end-users regarding the usability of the system.
- Offline Functionality: Effectiveness of the system when used without internet connectivity.
- Adaptability: Ease of adding new equid species or individuals to the system.

### Complementary Metrics
- Scalability: Ability to handle an increasing number of equids in the database without significant performance degradation.
- Robustness: Performance under varying conditions such as lighting, angle, and occlusions.
- Documentation Quality: Clarity and comprehensiveness of the provided documentation for users and developers.
- Security: Measures in place to protect ownership and identification data.

## System Architecture
See [docs/system_architecture.md](docs/system_architecture.md) for details on the system architecture.

## References
See [docs/references.md](docs/references.md) for a list of relevant references and resources.

