import argparse

from src.converter.max_converter import *

def main():
    # Command line arguments
    parser = argparse.ArgumentParser(
        description="Convert GoPro 360 video to equirectangular MP4"
    )

    # Optional
    parser.add_argument("-i", "--input",
                        nargs="+",
                        required=False,
                        help="Input filename (one or more)")
    parser.add_argument("-o", "--output",
                        required=False,
                        help="Output filename (optional)")
    
    # Positional
    parser.add_argument("input_positional",
                        nargs="*",
                        help="Input filename (positional)",
                        default=None
    )

    args = parser.parse_args()

    input_files = args.input if args.input is not None \
        else args.input_positional

    if not input_files:
        parser.error("Provide at least one input file")

    if isinstance(input_files, str):
        input_files = [input_files]

    if not validate_filetype(input_files, "360"):
        parser.error("Input files should have .360 extension")

    if args.output:
        output_file = args.output if validate_filetype(args.output, "mp4") \
            else f"{args.output}.mp4"
    else:
        output_file = None

    if len(input_files) == 1:
        ffmpeg_convert(input_files[0], output_file)
    else:
        converted_files = []
        for input_file in input_files:
            mp4_file = ffmpeg_convert(input_file)
            converted_files.append(mp4_file)

        ffmpeg_concatenate(converted_files, output_file)

if __name__ == "__main__":
    main()