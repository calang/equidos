# Quick Fix Guide: GPU Not Working

## TL;DR - What's Wrong?

✅ Your conda environment is **correctly configured**  
✅ PyTorch 2.5.1 + CUDA 12.1 is **installed**  
✅ TensorFlow 2.20.0 is **installed**  
❌ Your NVIDIA driver is **not loaded** (system issue)

## Quick Fix

### Step 1: Try Loading the Driver
```bash
sudo modprobe nvidia
nvidia-smi
```

If `nvidia-smi` now shows your GPU info, you're done! Test with:
```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### Step 2: If Step 1 Failed - Reinstall Driver
```bash
sudo apt-get install --reinstall nvidia-driver-580
sudo reboot
```

After reboot:
```bash
nvidia-smi  # Should show GPU info
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### Step 3: If Still Not Working - Use Stable Driver
```bash
sudo apt-get purge nvidia-driver-580
sudo apt-get install nvidia-driver-550  # LTS version
sudo reboot
```

## Verify Everything Works

Once `nvidia-smi` works:

```bash
# Enter project directory
cd /home/calang/proyects/calang/equidos

# Reload environment
source .bashrc

# Test PyTorch GPU
python -c "import torch; print('PyTorch CUDA available:', torch.cuda.is_available()); print('Device count:', torch.cuda.device_count())"

# Test TensorFlow GPU
python -c "import tensorflow as tf; print('TensorFlow GPUs:', tf.config.list_physical_devices('GPU'))"
```

Expected output:
```
PyTorch CUDA available: True
Device count: 1

TensorFlow GPUs: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

## What Was Already Fixed

The following files are now correctly configured for GPU support:
- ✅ `env.yml` - PyTorch with CUDA 12.1, TensorFlow via pip
- ✅ `requirements.txt` - TensorFlow 2.16-2.20
- ✅ `.bashrc` - CUDA environment variables
- ✅ `Makefile` - GPU support enabled

**You can run `make update-env` without errors now!**

## Need More Details?

See these files:
- `CONFIGURATION_UPDATE_SUMMARY.md` - What was changed
- `GPU_SETUP_VERIFICATION.md` - Detailed troubleshooting

