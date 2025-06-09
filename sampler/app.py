#!/usr/bin/env python3
"""
MP3 Chopper - Chops MP3 files into time-based waveforms for beat alignment
"""

import argparse
import os
import sys
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path


class MP3Chopper:
    def __init__(self, input_file, output_dir="output", segment_duration=1.0):
        """
        Initialize MP3 chopper
        
        Args:
            input_file: Path to input MP3 file
            output_dir: Directory to save output files
            segment_duration: Duration of each segment in seconds
        """
        self.input_file = input_file
        self.output_dir = Path(output_dir)
        self.segment_duration = segment_duration
        self.output_dir.mkdir(exist_ok=True)
        
    def load_audio(self):
        """Load MP3 file and return audio data and sample rate"""
        print(f"Loading audio file: {self.input_file}")
        audio, sr = librosa.load(self.input_file, sr=None, mono=False)
        return audio, sr
    
    def detect_beats(self, audio, sr):
        """Detect beats in the audio for alignment"""
        # Convert to mono if stereo
        if audio.ndim > 1:
            audio_mono = librosa.to_mono(audio)
        else:
            audio_mono = audio
            
        # Detect tempo and beats
        tempo, beats = librosa.beat.beat_track(y=audio_mono, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        
        # Extract scalar tempo value if it's an array
        if isinstance(tempo, np.ndarray):
            tempo = tempo.item()
            
        print(f"Detected tempo: {tempo:.2f} BPM")
        print(f"Found {len(beats)} beats")
        
        return beat_times
    
    def chop_by_time(self, audio, sr):
        """Chop audio into fixed time segments"""
        total_duration = len(audio) / sr if audio.ndim == 1 else len(audio[0]) / sr
        num_segments = int(total_duration / self.segment_duration)
        
        print(f"Chopping into {num_segments} segments of {self.segment_duration}s each")
        
        segments = []
        for i in range(num_segments):
            start_sample = int(i * self.segment_duration * sr)
            end_sample = int((i + 1) * self.segment_duration * sr)
            
            if audio.ndim == 1:
                segment = audio[start_sample:end_sample]
            else:
                segment = audio[:, start_sample:end_sample]
                
            segments.append(segment)
            
        return segments
    
    def chop_by_beats(self, audio, sr, beat_times, beats_per_segment=4):
        """Chop audio aligned to beats"""
        segments = []
        
        for i in range(0, len(beat_times) - beats_per_segment, beats_per_segment):
            start_time = beat_times[i]
            end_time = beat_times[i + beats_per_segment]
            
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            
            if audio.ndim == 1:
                segment = audio[start_sample:end_sample]
            else:
                segment = audio[:, start_sample:end_sample]
                
            segments.append(segment)
            
        print(f"Created {len(segments)} beat-aligned segments")
        return segments
    
    def save_segments(self, segments, sr, prefix="segment"):
        """Save segments as WAV files"""
        for i, segment in enumerate(segments):
            output_file = self.output_dir / f"{prefix}_{i:04d}.wav"
            
            # Transpose if stereo (librosa uses shape (channels, samples))
            if segment.ndim > 1:
                segment = segment.T
                
            sf.write(output_file, segment, sr)
            print(f"Saved: {output_file}")
    
    def process(self, mode="time", beats_per_segment=4):
        """
        Process the MP3 file
        
        Args:
            mode: 'time' for fixed-time segments, 'beat' for beat-aligned segments
            beats_per_segment: Number of beats per segment (for beat mode)
        """
        # Load audio
        audio, sr = self.load_audio()
        
        # Chop based on mode
        if mode == "beat":
            beat_times = self.detect_beats(audio, sr)
            segments = self.chop_by_beats(audio, sr, beat_times, beats_per_segment)
            prefix = f"beat_{beats_per_segment}"
        else:
            segments = self.chop_by_time(audio, sr)
            prefix = f"time_{self.segment_duration}s"
        
        # Save segments
        self.save_segments(segments, sr, prefix)
        
        print(f"\nProcessing complete! Output saved to: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Chop MP3 files into time-based waveforms")
    parser.add_argument("input", help="Input MP3 file")
    parser.add_argument("-o", "--output", default="output", help="Output directory (default: output)")
    parser.add_argument("-d", "--duration", type=float, default=1.0, 
                        help="Segment duration in seconds for time mode (default: 1.0)")
    parser.add_argument("-m", "--mode", choices=["time", "beat"], default="time",
                        help="Chopping mode: 'time' or 'beat' (default: time)")
    parser.add_argument("-b", "--beats", type=int, default=4,
                        help="Beats per segment for beat mode (default: 4)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    chopper = MP3Chopper(args.input, args.output, args.duration)
    chopper.process(mode=args.mode, beats_per_segment=args.beats)


if __name__ == "__main__":
    main()
