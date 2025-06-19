#!/usr/bin/env python3
"""
Extract a sample from an MP3 file using PyDub
"""

import sys
import subprocess
from pathlib import Path

from pydub.utils import which


def extract_sample(input_file, output_file, duration_seconds=30):
    """
    Extract a sample from an MP3 file, removing leading silence

    Args:
        input_file: Path to input MP3 file
        output_file: Path to output MP3 file
        duration_seconds: Duration to extract in seconds (default: 30)
    """
    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Try loading with explicit ffmpeg path
    cmd = [
        "ffmpeg",
        "-i",
        input_file,
        "-af",
        "silenceremove=start_periods=1:start_duration=0.1:start_threshold=-50dB",
        "-t",
        str(duration_seconds),
        "-acodec",
        "mp3",
        "-y",  # Overwrite output file
        output_file,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            raise Exception(f"FFmpeg failed with return code {result.returncode}")
        print(
            f"Extracted {duration_seconds} seconds from {input_file} to {output_file}"
        )
        return
    except Exception as ffmpeg_error:
        print(f"Direct ffmpeg also failed: {ffmpeg_error}")
        raise

def check_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error: ffmpeg is installed but not working properly")
            print(f"Error output: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error testing ffmpeg: {e}")
        return False

    return True


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(
            "Usage: python extract_sample.py <input_file> <output_file> [duration_seconds]"
        )
        print("       duration_seconds defaults to 30 if not specified")
        sys.exit(1)

    # Check if ffmpeg is available
    if not check_ffmpeg():
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    duration_seconds = int(sys.argv[3]) if len(sys.argv) == 4 else 30

    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)

    try:
        extract_sample(input_file, output_file, duration_seconds)
    except Exception as e:
        print(f"Error processing audio: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
