# GoPro MAX Converter

Convert native files into other file formats to be used in
different platforms, such as VR headsets and video streaming
services.

## Status

The project is currently in initial phase.

## Motivation

- The GoproPlayer native application can convert videos to
mp4 formats, but the resolution decreases from 5.7k to 4k
- The Player converts a single `.360` file as whole, and doesn't
allow cutting the file, or concatenating multiple files into one
- GoPo Player is not supported in Linux

## Aim

- Cross platform support (at least Windows and Linux)
- Convert with minimal quality loss
- Simple editing abilities: Cutting and concatenation
- Clean graphical user interface

## Selected technologies

- Python
- Poetry environment
- PyQl GUI libraries
- FFMpeg libraries for conversions and GPU support

## Running

### Prerequirements and initialization

You should have Python (minimum 3.12) and Poetry installed.
The dependencies should be installed in the project root:

```
poetry install
```

### Launching the app

In the project root:

```
poetry run python src/main.py
```
