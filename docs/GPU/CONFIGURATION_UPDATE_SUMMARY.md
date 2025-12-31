# Configuration Update Summary

## Date: December 25, 2025

## What Was Done

### 1. Fixed env.yml Configuration ✅

**Key Changes:**
- Added `pytorch` channel to channels list (required for PyTorch CUDA packages)
- Used channel-specific notation for PyTorch packages:
  - `pytorch::pytorch`
  - `pytorch::torchvision`
  - `pytorch::pytorch-cuda=12.1`
- Removed TensorFlow from conda dependencies (causes conflicts with PyTorch)
- TensorFlow now installed via pip in requirements.txt

**Result:** `make update-env` now works without errors!

### 2. Updated requirements.txt ✅

**Key Changes:**
- TensorFlow 2.16-2.20 installed via pip
- All conda-managed packages commented out
- Clear documentation of what should/shouldn't be in requirements.txt

**Why pip for TensorFlow?**
- TensorFlow 2.15 from conda-forge has import errors
- TensorFlow 2.15 not available via pip anymore
- TensorFlow 2.16+ from pip has better GPU support
- Avoids libabseil conflicts between TensorFlow and PyTorch

### 3. Updated .bashrc ✅

**Key Changes:**
- Uses `${CONDA_PREFIX}` instead of hardcoded path
- Sets all required CUDA environment variables
- Automatically activated when entering project directory

### 4. Updated Makefile ✅

**Key Changes:**
- Enabled GPU support variables by default
- Uses `${CONDA_PREFIX}` for portability
- Added `LD_LIBRARY_PATH` to `show-vars` target

## Packages Successfully Installed

```
pytorch                   2.5.1           py3.11_cuda12.1_cudnn9.1.0_0    pytorch
pytorch-cuda              12.1                 ha16c6d3_6    pytorch
torchvision               0.20.1              py311_cu121    pytorch
tensorflow                2.20.0                    (via pip)
cuda-runtime              12.1.0                      0    nvidia
```

## Current Issue: NVIDIA Driver Not Loaded ⚠️

### Status
- ✅ Conda environment configured correctly
- ✅ All packages installed successfully
- ❌ NVIDIA kernel driver not loaded
- ❌ GPU not detected by PyTorch or TensorFlow

### Diagnosis
This is a **system-level issue**, not a Python/conda configuration issue.

**Evidence:**
- `lsmod | grep nvidia` returns nothing (no kernel modules loaded)
- `nvidia-smi` shows incomplete output
- Driver 580.95.05 is installed but not active

### What You Need to Do

**Fix the NVIDIA driver first:**

1. **Check driver status:**
   ```bash
   lsmod | grep nvidia
   cat /proc/driver/nvidia/version
   nvidia-smi
   ```

2. **If driver not loaded, try:**
   ```bash
   sudo modprobe nvidia
   ```

3. **If that fails, rebuild DKMS modules:**
   ```bash
   sudo dkms status
   sudo dkms install nvidia/580.95.05 -k $(uname -r)
   ```

4. **If still failing, reinstall driver:**
   ```bash
   sudo apt-get install --reinstall nvidia-driver-580
   sudo reboot
   ```

5. **Or try older LTS driver:**
   ```bash
   sudo apt-get purge nvidia-driver-580
   sudo apt-get install nvidia-driver-550
   sudo reboot
   ```

**After driver is working, the conda environment is ready to use!**

Just verify:
```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
python -c "import tensorflow as tf; print('GPUs:', len(tf.config.list_physical_devices('GPU')))"
```

## Files Modified

1. `/home/calang/proyects/calang/equidos/env.yml`
2. `/home/calang/proyects/calang/equidos/requirements.txt`
3. `/home/calang/proyects/calang/equidos/.bashrc`
4. `/home/calang/proyects/calang/equidos/Makefile`
5. `/home/calang/proyects/calang/equidos/GPU_SETUP_VERIFICATION.md` (updated)

## References

See `GPU_SETUP_VERIFICATION.md` for detailed troubleshooting steps and verification procedures.

