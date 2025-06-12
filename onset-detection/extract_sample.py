#!/usr/bin/env python3
"""
Extract a sample from an MP3 file using PyDub
"""

import sys
from pathlib import Path
from pydub import AudioSegment


def extract_sample(input_file, output_file, duration_seconds):
    """
    Extract the first N seconds from an MP3 file
    
    Args:
        input_file: Path to input MP3 file
        output_file: Path to output MP3 file
        duration_seconds: Duration to extract in seconds
    """
    # Load the audio file
    audio = AudioSegment.from_mp3(input_file)
    
    # Extract the first N seconds (convert to milliseconds)
    duration_ms = duration_seconds * 1000
    sample = audio[:duration_ms]
    
    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Export the sample
    sample.export(output_file, format="mp3")
    print(f"Extracted {duration_seconds} seconds from {input_file} to {output_file}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python extract_sample.py <input_file> <output_file> <duration_seconds>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    duration_seconds = int(sys.argv[3])
    
    extract_sample(input_file, output_file, duration_seconds)


if __name__ == "__main__":
    main()
