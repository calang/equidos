# Find Models

Is there some model in Hugging Face (https://huggingface.co/) that can be used to identify individual horses based on their face or muzzle?

---

## Recalling Relevant Concepts

Yes, while there isn't a single, famous "foundation model" specifically pre-trained solely for horse face identification out-of-the-box like there is for human faces, there are several approaches and specific datasets on Hugging Face that you can use to build or fine-tune such a system.

Here are the most relevant resources and models you can find on Hugging Face:

## 1. Fine-tuning General Vision Models

The most common approach is to take a strong vision backbone and fine-tune it on a horse identification dataset.

**ResNet**, **EfficientNet**, or **Vision Transformers (ViT)**: You can use models like `google/vit-base-patch16-224` or `microsoft/resnet-50`. These are excellent feature extractors. You would train them using a metric learning approach (like Triplet Loss) to distinguish between individual horses.

## 2. Specific Datasets

To train these models, you need data. There are datasets available on Hugging Face or linked through it that are relevant:

**AnimalWeb**: Contains various animal faces.
**Horse2Zebra**: While used for style transfer, it contains many horse images that can be used for pre-training.

## 3. Zero-Shot Object Detection (for locating the face)

Before identifying the individual, you usually need to crop the face or muzzle.

**OWL-ViT (google/owlvit-base-patch32)**: This is a zero-shot text-conditioned object detection model. You can prompt it with "horse face" or "horse muzzle," and it will likely locate those specific parts without specific training.

## Recommended Pipeline

Since a "plug-and-play" model for specific horse ID is rare, the standard solution is a two-step pipeline:

1. **Detection**: Use a detector to crop the face.
    - Model: ultralytics/yolov8 (fine-tuned on horse faces) or google/owlvit-base-patch32.

2. **Identification (Embedding)**: Pass the crop through an embedding model to get a unique "fingerprint" for the horse.
    - Model: A Vision Transformer (ViT) or ResNet fine-tuned using a library like pytorch-metric-learning.

Example: Using OWL-ViT to find horse faces
You can try this code to see if you can isolate the face first: `scripts/sandbag/try_face.py`

Note: execution output:

```plaintext
(equids) main calang@calang-xps:equidos$ time src/sandbag/try_face.py
/home/calang/installed/miniforge3/envs/equids/lib/python3.13/site-packages/transformers/models/owlvit/processing_owlvit.py:217: FutureWarning: `post_process_object_detection` method is deprecated for OwlVitProcessor and will be removed in v5. Use `post_process_grounded_object_detection` instead.
  warnings.warn(
Detected a photo of a horse face with confidence 0.146 at location [254.96, 34.35, 475.37, 454.83]
Detected a photo of a horse face with confidence 0.139 at location [270.74, 48.28, 469.58, 457.94]

real    0m7.754s
user    0m4.666s
sys     0m0.574s
```