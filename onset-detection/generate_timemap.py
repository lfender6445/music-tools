#!/usr/bin/env python3
"""
Generate timemap from audio file using onset detection
"""

import sys
from onset_detector import OnsetDetector


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_timemap.py <audio_file> <output_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Create onset detector and generate timemap
    detector = OnsetDetector(audio_file)
    detector.save_timemap(output_file)


if __name__ == "__main__":
    main()
