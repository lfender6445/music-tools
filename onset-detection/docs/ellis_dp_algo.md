The algorithm used by `librosa.beat.beat_track()` is **Ellis Dynamic Programming Beat Tracker**, which is a classic onset-based beat tracking algorithm developed by Daniel Ellis.

## **Algorithm Details**

### **Core Approach**
1. **Onset Detection**: Detects note onsets using spectral flux
2. **Tempo Estimation**: Uses autocorrelation to find dominant periodicity
3. **Dynamic Programming**: Optimally places beats considering both local evidence and global tempo consistency

### **Technical Steps**

```python
def ellis_beat_tracker_simplified(y, sr):
    # 1. Onset strength detection
    onset_envelope = librosa.onset.onset_strength(y=y, sr=sr)

    # 2. Tempo estimation via autocorrelation
    tempo = librosa.beat.tempo(onset_envelope=onset_envelope, sr=sr)

    # 3. Dynamic programming beat tracking
    beats = librosa.beat.beat_track(
        onset_envelope=onset_envelope,
        sr=sr,
        start_bpm=tempo
    )

    return tempo, beats
```

## **Algorithm Classification**

This is a **traditional PPT (Post-Processing Tracker)** that uses:
- **Global tempo assumptions** (exactly what PLPDP was designed to improve upon)
- **Onset-based detection** (works well for percussive music, struggles with piano)
- **Dynamic programming optimization** (good for maintaining temporal consistency)

## **Performance Expectations for Piano**

Based on our earlier discussion, you can expect:
- **Electronic/Pop music**: 85-95% accuracy
- **Simple piano music**: 70-80% accuracy
- **Expressive classical piano**: 50-70% accuracy
- **Chopin-style rubato**: Potentially much lower

## **Why It Struggles with Piano**

1. **Onset detection issues**: Piano's sustained notes and pedal effects make onset detection unreliable
2. **Global tempo assumption**: Can't handle rubato and expressive timing variations
3. **Octave errors**: May detect tempo at half/double the actual rate

## **Librosa Parameters You Can Tune**

```python
tempo, beats = librosa.beat.beat_track(
    y=y,
    sr=sr,
    onset_envelope=None,    # Custom onset detection
    hop_length=512,         # Analysis frame size
    start_bpm=120.0,        # Initial tempo guess
    tightness=100,          # How strictly to enforce tempo consistency
    trim=True,              # Remove non-beat frames
    bpm=None,               # Force specific BPM if known
    units='time'            # Return beat times vs. frame indices
)
```

**For piano music, you might try:**
- **Lower tightness** (e.g., 50-80): Allows more tempo flexibility
- **Custom onset_envelope**: Use piano-optimized onset detection
- **Different start_bpm**: If you have rough tempo estimate

## **Comparison to PLPDP**

| Aspect | Ellis (librosa) | PLPDP |
|--------|----------------|-------|
| **Tempo Model** | Global | Local periodicity |
| **Piano Accuracy** | 50-70% | 75-85% |
| **Rubato Handling** | Poor | Excellent |
| **Ease of Use** | Very easy | More complex |
| **Availability** | Built into librosa | Research code |

## **Bottom Line**

`librosa.beat.beat_track()` uses a solid, well-established algorithm that works well for most music but has the exact limitations that motivated PLPDP's development. For quick BPM estimation it's fine, but for accurate piano analysis, especially expressive classical music, you'd want to consider the more sophisticated approaches we discussed earlier.
