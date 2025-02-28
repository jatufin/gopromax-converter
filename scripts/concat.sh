#!/bin/bash

## Concatenate mp4 files to a single file
## Input files are given in the first argument
## The output file is the second argument

## Example of 'input.txt':
#file 'file01.mp4'
#file 'file02.mp4'
#file 'file03.mp4'

## Command:
## $ concat.sh input.txt output.mp4

INFILE=$1
OUTFILE=$2

docker run --gpus device=0 \
    -v $PWD:/workdir \
    -w /workdir \
gopro-ffmpeg -hwaccel opencl -v verbose \
    -f concat \
    -i $INFILE \
    -c copy \
    -strict unofficial $OUTFILE


