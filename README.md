# MP3 Chopper

A Python application that chops MP3 input files into time-based waveforms for alignment with the underlying beat.

## Features

- **Time-based chopping**: Split MP3 files into fixed-duration segments
- **Beat-aligned chopping**: Split MP3 files aligned to detected beats
- **Minimal dependencies**: Uses only librosa, numpy, and soundfile
- **WAV output**: Saves segments as high-quality WAV files
- **Makefile support**: Easy-to-use commands for common operations

## Installation

```bash
make install
```

## Usage

### Basic Usage

```bash
# Chop by fixed time intervals (default: 1 second)
python app.py input.mp3

# Chop by fixed time intervals (custom duration)
python app.py input.mp3 -d 2.5

# Chop aligned to beats
python app.py input.mp3 -m beat

# Specify output directory
python app.py input.mp3 -o my_output
```

### Using Makefile Commands

```bash
# Install dependencies
make install

# Clean output files
make clean

# Chop by time (1.5 second segments)
make chop-time FILE=song.mp3 DURATION=1.5

# Chop by beats (8 beats per segment)
make chop-beat FILE=song.mp3 BEATS=8

# Show help
make help
```

## Command Line Options

- `input`: Input MP3 file (required)
- `-o, --output`: Output directory (default: "output")
- `-d, --duration`: Segment duration in seconds for time mode (default: 1.0)
- `-m, --mode`: Chopping mode - "time" or "beat" (default: "time")
- `-b, --beats`: Beats per segment for beat mode (default: 4)

## Output

The application saves chopped segments as WAV files in the output directory:
- Time mode: `time_1.0s_0000.wav`, `time_1.0s_0001.wav`, etc.
- Beat mode: `beat_4_0000.wav`, `beat_4_0001.wav`, etc.

## Dependencies

- librosa >= 0.10.0 (for audio processing and beat detection)
- numpy >= 1.24.0 (for numerical operations)
- soundfile >= 0.12.0 (for saving WAV files)

## Examples

```bash
# Chop a song into 2-second segments
python app.py mysong.mp3 -d 2.0

# Chop a song into 4-beat segments (typical bar length)
python app.py mysong.mp3 -m beat -b 4

# Chop a song into 16-beat segments (4 bars)
python app.py mysong.mp3 -m beat -b 16
```


