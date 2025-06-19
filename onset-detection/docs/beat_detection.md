## Challenges in Tempo Analysis of Piano Music
- Insufficient Duration
- 5 seconds provides very limited data for reliable tempo analysis
- Most tempo detection algorithms need at least 10-30 seconds to establish consistent beat patterns
- Short duration makes it difficult to distinguish between actual tempo and random rhythmic coincidences
- Piano notes have complex attack characteristics - not the sharp transients of drums

## Global Tempo Models vs PLDP
- Assume one tempo describes the entire piece
- Tempo changes must be gradual and systematic
- Work well for pop/electronic music with steady beats

For expressive classical music, however, these assumptions can be too rigid Bpm

Instead of global tempo assumptions, PLPDP uses local periodicity analysis

PLPDP particularly enhances the recall values at the cost of a lower precision, resulting in an overall improvement of F1-score for beat tracking in ASAP (from 0.473 to 0.493) and Maz-5 (from 0.595 to 0.838)

Why Better Recall?

Traditional PPTs: Miss many beats in expressive sections (low recall)
PLPDP: Finds more actual beats, including those in tempo-flexible sections
**PPTs** stands for **Post-Processing Trackers** - they're the final stage algorithms that convert raw beat detection signals into actual beat positions and tempo estimates.

## **The Beat Detection Pipeline**

Beat detection typically works in stages:

```
Audio Signal
    ↓
1. ONSET DETECTION (finds note starts)
    ↓
2. ACTIVATION FUNCTION (signal showing beat likelihood)
    ↓
3. POST-PROCESSING TRACKER (PPT) (finds actual beat positions)
    ↓
Final Beat Positions & BPM
```

## **What PPTs Do**

To model the periodicity of beats, state-of-the-art beat tracking systems use "post-processing trackers" (PPTs) that rely on several empirically determined global assumptions for tempo transition

PPTs take a **noisy activation function** (a signal indicating where beats might be) and clean it up to find the **actual beat sequence**. Think of it like:

- **Input**: "There might be beats at 0.1s, 0.12s, 0.48s, 0.51s, 0.89s, 0.95s..."
- **PPT Processing**: "These cluster around 0.1s, 0.5s, 0.9s - probably beats every 0.4s"
- **Output**: "Beats at 0.1s, 0.5s, 0.9s, 1.3s, 1.7s..." (120 BPM)

## **Common PPT Types**

### **1. Dynamic Programming (DP)**
- Uses optimization to find the most likely beat sequence
- Balances local evidence with global tempo consistency
- Penalizes sudden tempo changes

### **2. Hidden Markov Models (HMM)**
- Models tempo as a state that can transition gradually
- Grid search experiments are conducted to investigate the performance of HMM using tempo transition lambda from 0--100 with a step size of five
- The λ parameter controls how much tempo is allowed to change

### **3. Particle Filtering**
- Uses multiple "particles" representing different tempo hypotheses
- Particles with better evidence survive and reproduce
- Good for real-time applications

### **4. Simple Peak Picking (SPPK)**
- Basic approach: just pick the strongest peaks
- No temporal modeling
- Often used as baseline comparison

## **The Problem with Traditional PPTs**

Traditional PPTs make **global assumptions**:

### **Tempo Transition Constraints**
```python
# Typical PPT assumption
if current_tempo == 120:
    next_tempo_must_be_between(115, 125)  # Only small changes allowed
```

### **Global Tempo Models**
- Assume one tempo describes the entire piece
- Tempo changes must be gradual and systematic
- Work well for pop/electronic music with steady beats

For expressive classical music, however, these assumptions can be too rigid

## **Why PPTs Fail on Expressive Piano**

### **Rubato Challenges**
In Chopin's music, tempo might fluctuate like:
```
Measure 1: 120 BPM (steady)
Measure 2: 100 BPM (slowing for expression)
Measure 3: 140 BPM (speeding up dramatically)
Measure 4: 80 BPM (ritardando to cadence)
```

Traditional PPTs see this as "impossible" tempo variation and try to "correct" it to a steady tempo.

### **Lambda Parameter Problem**
From the different preference of lambda for ASAP and Maz-5 in real activation experiment, it can be seen that "adjust the lambda for the characteristics of the data" may be impractical in real use cases

The λ parameter controls tempo flexibility:
- **Low λ**: Allows rapid tempo changes (noisy results)
- **High λ**: Forces steady tempo (misses expressive timing)
- **Problem**: Optimal λ varies dramatically between pieces

## **How PLPDP Improves PPTs**

We propose a new local periodicity-based PPT, called predominant local pulse-based dynamic programming (PLPDP) tracking

Instead of global tempo assumptions, PLPDP uses **local periodicity analysis**:

### **Traditional PPT Logic**
```python
def traditional_ppt(activations):
    global_tempo = estimate_global_tempo(activations)
    beats = []
    for i, activation in enumerate(activations):
        expected_beat_time = i * (60.0 / global_tempo)
        if activation > threshold:
            beats.append(expected_beat_time)
    return beats
```

### **PLPDP Logic**
```python
def plpdp_ppt(activations):
    beats = []
    for window in local_windows(activations):
        # Find predominant local periodicity
        local_period = find_predominant_local_pulse(window)
        local_beats = extract_beats_with_period(window, local_period)
        beats.extend(local_beats)

    # Use DP to ensure global coherence
    return dynamic_programming_optimize(beats, activations)
```

## **Performance Comparison**

PLPDP particularly enhances the recall values at the cost of a lower precision, resulting in an overall improvement of F1-score for beat tracking in ASAP (from 0.473 to 0.493) and Maz-5 (from 0.595 to 0.838)

### **Why Better Recall?**
- **Traditional PPTs**: Miss many beats in expressive sections (low recall)
- **PLPDP**: Finds more actual beats, including those in tempo-flexible sections

### **Why Lower Precision?**
- **PLPDP**: Sometimes finds extra beats in ambiguous sections
- **Trade-off**: Better to find most real beats plus some false ones than miss many real beats

## **Summary**

**PPTs are the "decision-making" stage** of beat detection that converts uncertain evidence into definitive beat positions. Traditional PPTs assume global tempo consistency, which works well for most music but fails on expressive classical piano where tempo is deliberately and dramatically varied for artistic effect.

PLPDP represents a new PPT approach that respects the local musical logic of expressive performance while maintaining global coherence - making it much more effective for piano music analysis.

**λ** is the Greek letter **lambda** (lowercase).

In the context of the PLPDP research, **λ (lambda)** is a **hyperparameter** that controls **tempo transition flexibility** in Hidden Markov Model (HMM) beat trackers.

## **What Lambda Controls**

Grid search experiments are conducted to investigate the performance of HMM using tempo transition lambda from 0--100 with a step size of five

**Lambda values determine how much tempo is allowed to change between consecutive beats:**

- **λ = 0**: **Maximum flexibility** - tempo can change dramatically between any two beats
- **λ = 100**: **Maximum rigidity** - tempo must remain nearly constant
- **λ = 5-25**: **Moderate flexibility** - allows gradual tempo changes
- **λ = 50-90**: **Low flexibility** - enforces steady tempo with minimal variation

## **The Lambda Dilemma**

From the different preference of lambda for ASAP and Maz-5 in real activation experiment, it can be seen that "adjust the lambda for the characteristics of the data" may be impractical in real use cases

The research found that different piano datasets require completely different λ values:

- **Maz-5 dataset** (Chopin Mazurkas): λ = 5 works best (needs high flexibility for rubato)
- **ASAP dataset**: λ = 90 works best (needs more stability)

This reveals a fundamental problem: **you can't choose one λ value that works for all expressive piano music**.

## **Mathematical Meaning**

In HMM tempo tracking, lambda appears in the **transition probability model**:

```python
# Simplified concept
def tempo_transition_probability(current_tempo, next_tempo, lambda_param):
    """
    Higher lambda = lower probability of tempo changes
    Lower lambda = higher probability of tempo changes
    """
    tempo_change = abs(next_tempo - current_tempo)
    probability = exp(-lambda_param * tempo_change)
    return probability
```

**Higher λ** → **Lower probability** of tempo changes → **More rigid tracking**
**Lower λ** → **Higher probability** of tempo changes → **More flexible tracking**

## **Why This Matters for Piano**

The lambda parameter problem illustrates why traditional PPTs (Post-Processing Trackers) struggle with piano music:

1. **No single λ works universally** for expressive piano pieces
2. **Even within one piece**, different sections might need different λ values
3. **Manual tuning is impractical** for real-world applications

This is exactly why PLPDP was developed - to avoid the need for global tempo transition parameters like λ by using **local periodicity analysis** instead.

So **λ (lambda)** represents the fundamental trade-off in tempo tracking: **stability vs. expressiveness** - and PLPDP's innovation is finding a way to avoid this trade-off entirely.
