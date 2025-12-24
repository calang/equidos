# Git LFS (Large File Storage) Guide

Git LFS (Large File Storage) is a Git extension that replaces large files in your repository with text pointers while storing the actual file contents on a remote server. This keeps your repository lightweight and fast.

## Why Use Git LFS?

- Handles large binary files (images, videos, datasets, models)
- Reduces repository clone/fetch times
- Maintains Git's versioning for large files
- Useful for machine learning projects with datasets or model weights

## How to Use Git LFS

**1. Install Git LFS:**

```bash
# On Ubuntu/Debian
sudo apt-get install git-lfs

# Or download from https://git-lfs.github.com/
```

**2. Initialize in your repository:**

```bash
cd /home/calang/proyects/calang/equidos
git lfs install
```

**3. Track file types:**

```bash
# Track specific file types
git lfs track "*.jpg"
git lfs track "*.png"
git lfs track "*.h5"  # Keras model files
git lfs track "*.pb"  # TensorFlow models
git lfs track "*.pth" # PyTorch models

# Track specific directories
git lfs track "data/**"
```

**4. Commit the `.gitattributes` file:**

```bash
git add .gitattributes
git commit -m "Configure Git LFS tracking"
```

**5. Add and commit files normally:**

```bash
git add data/horsefacebase/*.jpg
git commit -m "Add horse face images"
git push origin main
```

## Useful Commands

```bash
# Check tracked patterns
git lfs track

# List LFS files
git lfs ls-files

# Fetch LFS content
git lfs fetch

# Pull LFS content
git lfs pull
```

For your horse face recognition project, consider tracking your image datasets and trained model files with Git LFS.