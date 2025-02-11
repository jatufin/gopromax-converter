# GoPro MAX Converter Frontend

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

## Notes

Concatenation

The `input.txt` file:
```
file 'file01.mp4'
file 'file02.mp4'
file 'file03.mp4'
```

```
ffmpeg -f concat -i input.txt -c copy -strict unofficial output.mp4
```

Stitching from top-bottom to side-by-side: (not working with Max's 360 format, which is not top-bottom)

```
ffmpeg -i input.video -filter_complex "[0:v:0][0:v:5]hstack=inputs=2[v]" -map "[v]" -c:v libx264 output.mp4
```

## The file 360 format

GoPro MAX saves video in `*.360` videos.


(Reverse engineering)[https://www.trekview.org/blog/reverse-engineering-gopro-360-file-format-part-1/]

- Top & Bottom videos: 2 x 4032x1344
- Max shoots on 6k but the resulting video is 5.6k

How to convert:
[https://www.trekview.org/blog/using-ffmpeg-process-gopro-max-360/]


From GoPro documentation:

[https://gopro.com/en/us/news/max-tech-specs-stitching-resolution?srsltid=AfmBOopvUFb7gRgx74Uk7Rq9gQzmGIPFYdtl_4sfL8fI6HV6a_O8enwA]

## GoproMAX FFmpeg

(https://github.com/gmat/goproMax-ffmpeg-v5)