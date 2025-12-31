# GPU Setup Verification Guide

## Current Status (December 25, 2025)

### ✅ Successfully Configured Files

1. **env.yml** - Conda environment with PyTorch CUDA support
2. **Makefile** - Build and environment variable configuration
3. **.bashrc** - Shell initialization with CUDA environment variables
4. **requirements.txt** - TensorFlow installed via pip

### ✅ Packages Successfully Installed

- **PyTorch**: 2.5.1 with CUDA 12.1 support (from pytorch channel)
- **TorchVision**: 0.20.1 with CUDA 12.1
- **TensorFlow**: 2.20.0 (installed via pip)
- **CUDA Runtime**: 12.1.0 (from conda)
- **pytorch-cuda**: 12.1

### ⚠️ Current Issue: GPU Not Detected

Both TensorFlow and PyTorch report no GPUs available. This appears to be a **system-level issue** with NVIDIA drivers, not a configuration issue with the conda environment.

**System Status:**
- NVIDIA Driver 580.95.05 is installed (confirmed via `dpkg -l`)
- `nvidia-smi` shows partial output but driver may not be properly loaded
- NVIDIA kernel modules may not be loaded for current kernel

## Files Updated

### env.yml
- Added `pytorch` channel for PyTorch packages
- PyTorch with CUDA 12.1: `pytorch::pytorch`, `pytorch::torchvision`, `pytorch::pytorch-cuda=12.1`
- TensorFlow installed via pip (requirements.txt) to avoid conda package conflicts
- CUDA toolkit and runtime installed via conda dependencies

### .bashrc
- Enabled CUDA environment variables using `${CONDA_PREFIX}` (dynamic path)
- Set `CUDA_DIR=${CONDA_PREFIX}`
- Set `XLA_FLAGS="--xla_gpu_cuda_data_dir=${CUDA_DIR}"`
- Set `LD_LIBRARY_PATH=${CUDA_DIR}/lib:${LD_LIBRARY_PATH}`
- Set `TF_ENABLE_ONEDNN_OPTS=0`

### Makefile
- Enabled GPU support variables
- Set `CUDA_DIR` to use `${CONDA_PREFIX}`
- Configured `XLA_FLAGS`, `LD_LIBRARY_PATH`, and `TF_ENABLE_ONEDNN_OPTS`
- Updated `show-vars` target to display all GPU-related variables

### requirements.txt
- TensorFlow 2.16-2.20 installed via pip for better compatibility

## Next Steps to Fix GPU Detection

### CRITICAL: Fix NVIDIA Driver Issue

The conda environment is correctly configured, but the **NVIDIA drivers are not properly loaded**. You need to fix this at the system level.

#### Step 1: Check NVIDIA Driver Status
```bash
# Check if driver is loaded
lsmod | grep nvidia

# Check driver version
cat /proc/driver/nvidia/version

# Check nvidia-smi
nvidia-smi
```

If these commands show nothing or errors, the driver is not loaded.

#### Step 2: Check Kernel Module Compatibility
```bash
# Check current kernel version
uname -r

# Check if NVIDIA modules exist for current kernel
ls /lib/modules/$(uname -r)/updates/dkms/nvidia*
```

NVIDIA driver 580.95.05 is installed, but may not be compiled for your current kernel.

#### Step 3: Reinstall/Rebuild NVIDIA Driver

**Option A: Reinstall driver for current kernel**
```bash
# Remove old driver modules
sudo apt-get purge nvidia-*
sudo apt-get autoremove

# Reinstall recommended driver
sudo ubuntu-drivers autoinstall

# Or install specific version
sudo apt-get install nvidia-driver-580

# Reboot
sudo reboot
```

**Option B: Rebuild DKMS modules**
```bash
# Check DKMS status
sudo dkms status

# If nvidia module is listed but not built:
sudo dkms install nvidia/580.95.05 -k $(uname -r)

# Load the module
sudo modprobe nvidia

# Verify
lsmod | grep nvidia
nvidia-smi
```

#### Step 4: After Driver is Fixed - Verify Environment

Once `nvidia-smi` works properly:

```bash
# 1. Reload shell configuration
source .bashrc

# 2. Verify environment variables
make show-vars
# Or manually:
echo $CUDA_DIR
echo $XLA_FLAGS
echo $LD_LIBRARY_PATH

# 3. Test TensorFlow GPU Detection
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__); print('GPU devices:', tf.config.list_physical_devices('GPU')); print('Num GPUs:', len(tf.config.list_physical_devices('GPU')))"

# 4. Test PyTorch GPU Detection
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('Number of GPUs:', torch.cuda.device_count())"
```

## Troubleshooting

### Current Diagnosis: NVIDIA Driver Not Loaded

**Symptoms:**
- ✅ NVIDIA driver packages are installed (580.95.05)
- ❌ NVIDIA kernel modules are NOT loaded (`lsmod | grep nvidia` returns nothing)
- ❌ `nvidia-smi` shows incomplete/N/A output
- ❌ TensorFlow reports: "Skipping registering GPU devices..."
- ❌ PyTorch cannot detect CUDA devices

**Root Cause:**
The NVIDIA kernel driver is not loaded into the running kernel. This is a **system-level issue**, not a Python/conda environment issue.

**Common Causes:**
1. **Kernel update**: Your kernel was recently updated, but NVIDIA DKMS modules weren't rebuilt
2. **Secure Boot**: Secure Boot may be blocking unsigned kernel modules
3. **Wrong driver version**: Driver 580 may not support your GPU or kernel
4. **Missing kernel headers**: DKMS couldn't compile modules for current kernel

### Solution: Fix NVIDIA Driver

Follow the steps in "Next Steps to Fix GPU Detection" above. The key is to:

1. Ensure NVIDIA kernel modules are compiled for your current kernel
2. Load the nvidia module: `sudo modprobe nvidia`
3. Verify with: `lsmod | grep nvidia` and `nvidia-smi`
4. If Secure Boot is enabled, either disable it or sign the kernel modules

### After Driver is Fixed

Once the NVIDIA driver is working (confirmed by `nvidia-smi` showing GPU info):

**The conda environment is already properly configured!** Just run:

```bash
# Reload environment
source .bashrc

# Test GPU detection
python -c "import torch; print('PyTorch CUDA:', torch.cuda.is_available())"
python -c "import tensorflow as tf; print('TensorFlow GPUs:', len(tf.config.list_physical_devices('GPU')))"
```

### If conda environment needs update:
```bash
make update-env
```

### Alternative: If Driver 580 Doesn't Work

If you continue to have issues with driver 580, try installing an older, more stable version:

```bash
# Remove driver 580
sudo apt-get purge nvidia-driver-580

# Install driver 550 (LTS)
sudo apt-get install nvidia-driver-550

# Reboot
sudo reboot

# Verify
nvidia-smi
```

### Checking Secure Boot Status

```bash
mokutil --sb-state
```

If Secure Boot is enabled, you may need to:
- Disable Secure Boot in BIOS/UEFI, OR
- Sign NVIDIA kernel modules (more complex)

### Check Kernel Headers

```bash
# Install kernel headers for current kernel
sudo apt-get install linux-headers-$(uname -r)
```

## Additional Notes

- The configuration now uses `${CONDA_PREFIX}` which automatically points to the active conda environment, making it portable across different systems
- All GPU-related settings are now enabled by default in both Makefile and .bashrc
- The `make jupl` command will now set GPU environment variables when launching Jupyter Lab
- Environment variables are set automatically when you run `source .bashrc` in the project directory

