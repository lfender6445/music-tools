#!/usr/bin/env python3
"""
Plot waveform with pitch markers from timemap
"""

import sys
import json
from pathlib import Path
from onset_detector import OnsetDetector


def main():
    if len(sys.argv) < 3:
        print("Usage: python plot_timemap.py <audio_file> <timemap_file> [output_image]")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    timemap_file = sys.argv[2]
    output_image = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Load timemap
    with open(timemap_file, 'r') as f:
        timemap = json.load(f)
    
    # Create detector and load audio
    detector = OnsetDetector(audio_file)
    detector.load_audio()
    
    # Plot with pitch markers
    detector.plot_waveform_with_pitch_markers(timemap, output_image)


if __name__ == "__main__":
    main()
