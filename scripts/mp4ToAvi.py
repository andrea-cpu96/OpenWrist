import subprocess
import os
import math

def split_and_convert():
    # Ask user for input and output names
    input_file = input("Enter input .mp4 file path: ").strip()
    base_output = input("Enter base output name (no extension): ").strip()

    # Get total duration in seconds
    cmd_duration = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", input_file
    ]
    duration = float(subprocess.check_output(cmd_duration).decode().strip())
    total_minutes = math.ceil(duration / 60)

    for i in range(total_minutes):
        start_time = i * 60
        index = f"{i:03d}"  # zero‑padded index: 000, 001, 002...
        output_file = f"{base_output}{index}.avi"

        cmd_convert = [
            "ffmpeg",
            "-ss", str(start_time),
            "-i", input_file,
            "-t", "60",
            "-vf", "scale=240:240",
            "-an",                      # remove audio
            "-c:v", "mjpeg",            # high‑quality AVI codec
            "-q:v", "2",                # near‑lossless quality
            "-y",
            output_file
        ]

        print(f"Creating {output_file}...")
        subprocess.run(cmd_convert, check=True)

    print("All segments created successfully.")

# Run the function
if __name__ == "__main__":
    split_and_convert()
