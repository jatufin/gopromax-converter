#!/bin/bash
set -e # Exit if error

echo "THIS SCRIPT HAS NOT BEEN TESTED" # TODO: TEST

echo "Automatic configure:"
echo "- Install Docker"
echo "- Install and configure the NVIDIA GPU support for Docker"
echo "- Build FFmpeg with GoProMAX support into a Docker container "


# ***********************************
# docker
echo "Install docker..."
sudo apt install docker.io
echo "OK Docker installed"

echo

# ***********************************
# NVIDIA Container Toolkit
echo "Install and configure NVIDIA Container Toolkit..."
echo "    Add the repository..."
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
echo "    OK Repository added"

echo "    Install the package"
sudo apt update
sudo apt install nvidia-container-toolkit
echo "    OK Package installed"

echo "    Configure the container runtime"
echo "    Modifying /etc/docker/daemon.json"
sudo nvidia-ctk runtime configure --runtime=docker
echo "    OK runtime configured"

echo "    Restart the Docker daemon"
sudo systemctl restart docker
echo "    OK daemon restarted"

echo "OK NVIDIA Container Toolkit installed and configured"

echo 

# ***********************************
# Build FFMpeg
echo "Build FFmpeg in a Docker container"
echo " In the case of ERROR: Permission denied"
echo " The user account must be in docker group:"
echo "      sudo usermod -aG docker \$USER"
echo " The change takes effect after next login."

docker build -t gopro-ffmpeg .
echo "OK FFmpeg container built"

echo

# ***********************************
# Test
echo "Test running FFmpeg in the container"
docker run --gpus device=0 gopro-ffmpeg -version
echo "OK"

