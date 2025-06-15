#!/usr/bin/env python3
"""
Onset detection class using Librosa for feature extraction and onset detection
"""

import json
import numpy as np
import librosa
from pathlib import Path


class OnsetDetector:
    def __init__(self, audio_file):
        """
        Initialize the onset detector

        Args:
            audio_file: Path to audio file
        """
        self.audio_file = audio_file
        self.y = None
        self.sr = None
        self.onset_frames = None
        self.onset_times = None
        self.tempo = None
        self.beats = None

    def load_audio(self):
        """Load audio file using librosa"""
        self.y, self.sr = librosa.load(self.audio_file)
        print(f"Loaded audio: {self.audio_file}")
        print(f"Sample rate: {self.sr} Hz")
        print(f"Duration: {len(self.y) / self.sr:.2f} seconds")

    def detect_onsets(self):
        """Detect onsets using librosa's onset detection"""
        # Compute onset envelope
        onset_envelope = librosa.onset.onset_strength(y=self.y, sr=self.sr)

        # Detect onset frames
        self.onset_frames = librosa.onset.onset_detect(
            onset_envelope=onset_envelope,
            sr=self.sr,
            backtrack=True
        )

        # Convert frames to time
        self.onset_times = librosa.frames_to_time(self.onset_frames, sr=self.sr)

        print(f"Detected {len(self.onset_times)} onsets")

    def detect_tempo_and_beats(self):
        """Detect tempo and beat positions"""
        # Estimate tempo
        self.tempo, self.beats = librosa.beat.beat_track(y=self.y, sr=self.sr)

        print(f"Estimatd tempo: {self.tempo} BPM")
        print(f"Detected {len(self.beats)} beats")

    def extract_pitch_info(self):
        """Extract pitch information at onset points"""
        pitch_info = []

        # Compute chromagram
        chroma = librosa.feature.chroma_stft(y=self.y, sr=self.sr)

        for i, onset_frame in enumerate(self.onset_frames):
            # Get the dominant pitch class at this onset
            chroma_vector = chroma[:, onset_frame]
            dominant_pitch_class = np.argmax(chroma_vector)

            # Convert to pitch name
            pitch_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            pitch_name = pitch_names[dominant_pitch_class]

            pitch_info.append({
                'time': float(self.onset_times[i]),
                'pitch': pitch_name,
                'confidence': float(chroma_vector[dominant_pitch_class])
            })

        return pitch_info

    def generate_timemap(self):
        """Generate a timemap with onset, beat, and pitch information"""
        # Load and analyze audio
        self.load_audio()
        self.detect_onsets()
        self.detect_tempo_and_beats()

        # Extract pitch information
        pitch_info = self.extract_pitch_info()

        # Convert beat frames to times
        beat_times = librosa.frames_to_time(self.beats, sr=self.sr)

        # Create timemap
        timemap = {
            'metadata': {
                'audio_file': str(self.audio_file),
                'duration': float(len(self.y) / self.sr),
                'sample_rate': int(self.sr),
                'tempo': float(self.tempo)
            },
            'onsets': [float(t) for t in self.onset_times],
            'beats': [float(t) for t in beat_times],
            'pitch_info': pitch_info
        }

        return timemap

    def save_timemap(self, output_file):
        """Save timemap to JSON file"""
        timemap = self.generate_timemap()

        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save to JSON
        with open(output_file, 'w') as f:
            json.dump(timemap, f, indent=2)

        print(f"Timemap saved to {output_file}")
