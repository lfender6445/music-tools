
# Variables
PYTHON = python3
MP3_DIR = mp3
OUTPUT_DIR = output
SAMPLE_FILE = $(MP3_DIR)/variation-1.mp3
SAMPLE_OUTPUT = $(OUTPUT_DIR)/sample-5s.mp3
TIMEMAP_OUTPUT = $(OUTPUT_DIR)/timemap.json
PLOT_OUTPUT = $(OUTPUT_DIR)/waveform_pitch_plot.png

# Create output directory if it doesn't exist
$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

# Extract first 30 seconds of MP3
sample: $(OUTPUT_DIR)
	$(PYTHON) extract_sample.py $(SAMPLE_FILE) $(SAMPLE_OUTPUT) 5

# Generate timemap from sample file
timemap: sample
	$(PYTHON) generate_timemap.py $(SAMPLE_OUTPUT) $(TIMEMAP_OUTPUT)

# Generate timemap and plot with pitch markers
timemap:plot: timemap
	$(PYTHON) plot_timemap.py $(SAMPLE_OUTPUT) $(TIMEMAP_OUTPUT) $(PLOT_OUTPUT)

# Run both commands
all: sample timemap

# Clean generated files
clean:
	rm -rf $(OUTPUT_DIR)

.PHONY: sample timemap timemap:plot all clean
