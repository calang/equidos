# To install NVIDIA drivers on Linux
Follow these steps:
1. 
2. Check Your GPU
First, verify you have an NVIDIA GPU:
```
lspci | grep -i nvidia
```
2. Check Current Driver Status
```
nvidia-smi
```
If this works, drivers are already installed. If not, proceed with installation.
3. Installation Methods

4. Option A: Using Ubuntu/Debian Package Manager (Recommended)
```
# Update package list
sudo apt update

# Search for available drivers
ubuntu-drivers devices

# Install recommended driver automatically
# sudo ubuntu-drivers autoinstall

# Or install a specific version (e.g., 535)
sudo apt install nvidia-driver-580-open  # - distro non-free recommended

# Reboot
sudo reboot
```

4. Verify Installation
After rebooting:
```
nvidia-smi
```
You should see your GPU information, driver version, and CUDA version.
5. Test with TensorFlow
```
conda activate equids
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```
Note: The NVIDIA driver version must support the CUDA version required by TensorFlow. Check compatibility at https://docs.nvidia.com/deploy/cuda-compatibility/