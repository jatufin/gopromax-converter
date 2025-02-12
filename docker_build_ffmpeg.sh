#!/bin/bash
set -e # Exit if error

# Build the image
echo "Build the Docker image..."
docker build -t gopro-ffmpeg .
echo "OK"


# Test
echo "Test running FFmpeg in the container"
docker run --gpus device=0 gopro-ffmpeg -version
echo "OK"

