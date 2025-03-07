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
