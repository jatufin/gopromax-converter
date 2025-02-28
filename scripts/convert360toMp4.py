import argparse
import os
import subprocess

CONCAT_FILE = "concat.txt"
CONCAT_FILE_COMMENT = "# This is a temporary file and can be deleted"

def validate_filetype(file_list, extension):
    """ Validate that the files have given extension.
    """
    if isinstance(file_list, str):
        file_list = [file_list]

    for filename in file_list:
        if not filename.lower().endswith(f".{extension.lower()}"):
            return False
    
    return True

def ffmpeg_convert(input_file, output_file=None):
    """ Converts the given 360 file into mp4
    
    Returns the output file name
    """
    if not output_file:
        output_file = f"{input_file[:-3]}mp4"

    input_dir = os.path.dirname(os.path.abspath(input_file))
    input_filename = os.path.basename(input_file)
    output_dir = os.path.dirname(os.path.abspath(output_file))
    output_filename = os.path.basename(output_file)

    # TODO: Remove debug
    print(f"Input dir: {input_dir} Filename: {input_filename}")
    
    docker_command = [
        "docker", "run", "--gpus", "device=0",
            "-v", f"{input_dir}:/input" ,
            "-v", f"{output_dir}:/output",
        "gopro-ffmpeg", "-hwaccel", "opencl", "-v", "verbose",
            "-i", f"/input/{input_filename}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-map_metadata", "0", "-map", "0:a", "-map", "0:3",
            "-filter_complex",
                "[0:0]format=yuv420p,hwupload[a],[0:5]format=yuv420p,hwupload[b],[a][b]gopromax_opencl,hwdownload,format=yuv420p",
            f"/output/{output_filename}"
    ]

    try:
        print(f"Converting: {input_file} --> {output_file}...", end="")
        subprocess.run(docker_command, check=True)
        print("OK")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

    return output_file

def ffmpeg_concatenate(file_list, output_file): # TODO: Test
    """ Concatenates file_list files into one output_file
    MP4 file format is assumed.

    Returns output file name if succesfull
    """
    if len(file_list) == 0:
        print("File list is empty")
        return

    input_dir = os.path.dirname(os.path.abspath(file_list[0]))

    concat_file = f"{input_dir}/concat.txt"
        
    with open(concat_file, "w") as f:
        for filename in file_list:
            dir = os.path.dirname(os.path.abspath(filename))
        
            if dir != input_dir:
                print("Files must be in the same directory")
                return

            line = f"file '{os.path.basename(filename)}'\n"
            f.write(line)

    input_dir = os.path.dirname(os.path.abspath(concat_file))
    input_filename = os.path.basename(concat_file)

    output_dir = os.path.dirname(os.path.abspath(output_file))
    output_filename = os.path.basename(output_file)

    docker_command = [
        "docker", "run", "--gpus", "device=0",
            "-v", f"{input_dir}:/input",
            "-v", f"{output_dir}:/output",
        "gopro-ffmpeg", "-hwaccel", "opencl", "-v", "verbose",
            "-f", "concat",
            "-i", f"/input/{input_filename}",
            "-c", "copy",
            "-strict", "unofficial",
            f"/output/{output_filename}"            
    ]

    try:
        print(f"Concatenating: {concat_file} --> {output_file}...", end="")
        subprocess.run(docker_command, check=True)
        print("OK")
    except subprocess.CalledProcessError as e:
        print(f"Error during concatenation: {e}")
        # TODO: activate cleanup
        #os.remove(concat_file)
        return

    # TODO: activate cleanup
    #os.remove(concat_file)
    
    return output_file


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