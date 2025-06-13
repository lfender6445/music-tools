#!/usr/bin/env python3
"""
Extract a sample from an MP3 file using PyDub
"""

import sys
import subprocess
from pathlib import Path
from pydub import AudioSegment
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
    
    try:
        # Try loading with explicit ffmpeg path
        audio = AudioSegment.from_file(input_file, format="mp3")
    except Exception as e:
        # If that fails, try using subprocess directly with ffmpeg
        print(f"PyDub failed with error: {e}")
        print("Attempting direct ffmpeg conversion...")
        
        # Use ffmpeg's silenceremove filter to remove leading silence
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-af", "silenceremove=start_periods=1:start_duration=0.1:start_threshold=-50dB",
            "-t", str(duration_seconds),
            "-acodec", "mp3",
            "-y",  # Overwrite output file
            output_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"FFmpeg error: {result.stderr}")
                raise Exception(f"FFmpeg failed with return code {result.returncode}")
            print(f"Extracted {duration_seconds} seconds from {input_file} to {output_file}")
            return
        except Exception as ffmpeg_error:
            print(f"Direct ffmpeg also failed: {ffmpeg_error}")
            raise
    
    # If PyDub worked, remove leading silence
    # Detect silence threshold (in dBFS)
    silence_threshold = audio.dBFS - 16  # 16 dB below average
    
    # Find the first non-silent chunk
    chunk_size = 10  # milliseconds
    non_silent_start = 0
    
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i+chunk_size]
        if chunk.dBFS > silence_threshold:
            non_silent_start = i
            break
    
    # Trim leading silence
    trimmed_audio = audio[non_silent_start:]
    
    # Extract exactly the specified duration (default 30 seconds)
    duration_ms = duration_seconds * 1000
    
    if len(trimmed_audio) < duration_ms:
        # If trimmed audio is shorter than requested duration, use what we have
        sample = trimmed_audio
        print(f"Warning: Audio after removing silence is only {len(trimmed_audio)/1000:.1f} seconds")
    else:
        # Extract the exact duration requested
        sample = trimmed_audio[:duration_ms]
    
    # Export the sample
    sample.export(output_file, format="mp3")
    print(f"Extracted {len(sample)/1000:.1f} seconds from {input_file} to {output_file}")
    print(f"Removed {non_silent_start/1000:.1f} seconds of leading silence")


def check_ffmpeg():
    """Check if ffmpeg is installed and accessible"""
    ffmpeg_path = which("ffmpeg")
    if ffmpeg_path is None:
        print("Error: ffmpeg is not installed or not in PATH")
        print("Please install ffmpeg:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        return False
    
    # Test if ffmpeg actually works
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: ffmpeg is installed but not working properly")
            print(f"Error output: {result.stderr}")
            return False
        print(f"Found working ffmpeg at: {ffmpeg_path}")
    except Exception as e:
        print(f"Error testing ffmpeg: {e}")
        return False
    
    return True


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python extract_sample.py <input_file> <output_file> [duration_seconds]")
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
