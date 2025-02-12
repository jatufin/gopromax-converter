# GoPro MAX Converter Frontend

Convert native GoProMAX 360 files into standard MP4 files to be used in different platforms, such as VR headsets and video streaming services.


### Acknowledgements

The current version of FFmpeg doesn't natively support GoPro's `360` file format. A fork from a previous version with GoProMAX filter is used. Big thanks to people who have done great job:

- David G. of Treckview: [Using ffmpeg to Process Raw GoPro MAX .360's into Equirectangular Projections](https://www.trekview.org/blog/using-ffmpeg-process-gopro-max-360/)
- `gmat`'s goproMax-FFmpeg-v5 FFMpeg fork:
[https://github.com/gmat/goproMax-ffmpeg-v5]
- `zepadovani`'s GPU enabled Dockerfile:
[https://github.com/zepadovani/docker_goproMax-ffmpeg-v5/tree/main]

## Target

- Application that can be run on desktop linux
- GPU support
- Convert with minimal quality loss
- Simple editing abilities: Cutting and concatenation
- Clean graphical user interface

## Selected technologies

- Python
- Poetry environment
- PyQl GUI libraries
- FFMpeg running in Docker container

## Status

The project is currently in very early phase:
- The correct FFmpeg binary can be built using Docker
- NVIDIA GPUs are supported
- Simple conversion with CLI works

# Compiling FFmpeg in a Docker container

Debian based Linux distribution assumed.

## Prerequisities

Docker and NVIDIA container toolkit is needed.
Currently only NVIDIA GPU's are supported.

1. Install Docker
2. Install NVIDIA Container Toolkit
3. Configure Docker to use NVIDIA
4. Build FFjpeg
5. Test


### 1. Install Docker

Install `docker.io`:

```
sudo apt install docker.io
```

### 2. Install NVIDIA container tookit

Below are the instructions for Debian based host system.
If needed, refer to documentation:
[https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html]

**Add the repository**
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

**Install the package:**

```
$ sudo apt update
$ sudo apt install nvidia-container-toolkit
```

### 3. Configure Docker to use NVIDIA

Configure the container runtime. This modifyis `/etc/docker/daemon.json` or creates it, if the file doesn't exist:
```
sudo nvidia-ctk runtime configure --runtime=docker
```

Reststart the Docker daemon:
```
sudo systemctl restart docker
```

### 4. Build FFmpeg

Run the script in the project root:

```
./docker_build_ffmpeg.sh
```

**ERROR: Permission denied**

The script runs Docker with user privileges. If you get a Permission Denied
error, your user is probably not in the `docker` group. Join the user to
the group: (you must relogin to the system)

```
sudo usermod -aG docker $USER
```

### 5. Test the FFmpeg binary

```
docker run --gpus device=0 gopro-ffmpeg -version
```

## Running the app

### Converting a single file using command line

After building the FFmpeg container the conversion
should work by running in the project root:

```
./scripts/convert.sh infile.360 outfile.mp4
```

## Notes

### The file 360 format

GoPro documentation:

[https://gopro.com/en/us/news/max-tech-specs-stitching-resolution?srsltid=AfmBOopvUFb7gRgx74Uk7Rq9gQzmGIPFYdtl_4sfL8fI6HV6a_O8enwA]

### Concatenation

The `input.txt` file:
```
file 'file01.mp4'
file 'file02.mp4'
file 'file03.mp4'
```

Concatenate preserving the metadata:

```
ffmpeg -f concat -i input.txt -c copy -strict unofficial output.mp4
```
