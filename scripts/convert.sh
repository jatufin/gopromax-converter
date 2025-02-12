#!/bin/bash

INFILE=$1
OUTFILE=$2

docker run --gpus device=0 \
    -v $PWD:/workdir \
    -w /workdir \
gopro-ffmpeg -hwaccel opencl -v verbose \
    -i $INFILE \
    -c:v libx264 -pix_fmt yuv420p -map_metadata 0 -map 0:a -map 0:3 \
    -filter_complex '[0:0]format=yuv420p,hwupload[a],[0:5]format=yuv420p,hwupload[b],[a][b]gopromax_opencl,hwdownload,format=yuv420p' $OUTFILE


