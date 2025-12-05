# Paper Summary

## A Methodology for Utilizing Vector Space to Improve the Performance of a Dog Face Identification Model, 2021.
### Summary
- Uses un-normalized vectors to store the feature embeddings of dog faces.
- Claims the the resulting accuracy of 97.33% for the proposed learning method is approximately 4% greater than that of the existing learning method.

## Cattle Recognition: A New Frontier in Visual Animal Biometrics Research, 2016.
### Summary
- Describes and summarizes different methods to identify cattle, from invasive to non-invasive.
- Visual cattle recognition system based on muzzle point image pattern uses geometric and texture features to identify individual cattle.

## Deep Transfer Learning-Based Animal Face Identification Model Empowered with Vision-Based Hybrid Approach, 2023.
### Summary
- Uses a Yolo (v7) object detector to automate the identification process.
- The proposed system consists of three stages:
  - detection of the animal’s face and muzzle
  - extraction of muzzle pattern features using the SIFT algorithm and
  - identification of the animal using the FLANN algorithm if the extracted features match those previously registered in the system.
- The Yolo (v7) object detector has mean average precision of 99.5% and 99.7% for face and muzzle point detection, respectively.
- The proposed system demonstrates the capability to accurately recognize animals using the FLANN algorithm and has the potential to be used for a range of applications, including animal security and health concerns, as well as livestock insurance.
- This study presents a promising approach for the real-time identification of livestock animals using muzzle patterns via a combination of automated detection and feature extraction algorithms.

### Notes and verbatim quotes
- Muzzle patterns are unique to each animal and can serve as a reliable means of identification [7]
- This study proposes a system using the biometrics of livestock animals, such as their muzzle patterns, for the automated, instant identification of livestock, utilizing deep transfer learning to **detect** the face and **the muzzle** point of the animal.
- **Any noise or image with motion blur is filtered out** in consideration of any movement by the animal, and only clear images of the nose are captured
- Images of the nose are captured, which are then used to **extract features using SIFT** (scale-invariant feature transform) [9] and then **stored in the database**
- Later on, the initial steps are the same when recognizing but, after the features are extracted, the system uses an approximate nearest neighbor search by applying FLANN (fast library for approximate nearest neighbor) matcher [10,11] to match SIFT-extracted features.
- The THDD dataset [12,13] was applied to train the Yolo object detector in this study
- The study by Kumar et al. [15] demonstrates the potential of using muzzle patterns for cattle identification and highlights the importance of considering the quality of the images used for identification.
- Li et al. [16] proposed a cattle identification approach based on deep learning techniques. The authors used **59 different deep learning models** to identify individual cattle **using their muzzle prints** and achieved **accuracy of 98.7%**.
- It is challenging to use still muzzle point images for identification when the animal is moving.
- Kumar et al. [18] proposed a **real-time system** for recognizing cattle using the distinctive patterns found on their muzzles or noses.
- Jarraya et al. [19] proposed a technique for horse identification using face biometrics, achieving accuracy of **99.89%**.

## When Language Model Guides Vision: Grounding DINO for Cattle Muzzle Detection, 2025
- Recently, automated methods using supervised models like YOLO have become popular for muzzle detection.
  - Although effective, these methods require extensive annotated datasets and tend to be trained data-dependent, limiting their performance on new or unseen cattle.
- This study proposes a zero-shot muzzle detection framework based on Grounding DINO, a vision-language model capable of detecting muzzles without any task-specific training or annotated data. 
- Our model achieves a **mean Average Precision** (mAP)@0.5 of **76.8%**, demonstrating promising performance without requiring annotated data.
- Publicly available datasets from UNE [26] and NUCES [1] were used.

### References of interest

## PetFace: A Large-Scale Dataset and Benchmark for Animal Identification, 2024.
- Comprehensive resource for animal face identification encompassing 257,484 unique individuals across 13 animal families and 319 breed categories: Cat, Chimpanzee, Chinchilla, Degus, Dog, Ferret, Guinea pig, Hamster, Hedgehog, Parakeet, Java sparrow, Pig, and Rabbit.

## Sparse Neural Network for horse face detection in a Smart Riding Club Biometric System, 2021 or later.
- The proposed HIR-FB for horse face recognition proved their performance by a recognition rate equal to **99.89%** on the THoDBRL’2015

