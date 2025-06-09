.PHONY: help install clean test run-example chop-time chop-beat

# Default target
help:
	@echo "MP3 Chopper - Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make clean        - Clean output directory"
	@echo "  make test         - Run tests"
	@echo "  make run-example  - Run example with sample file"
	@echo "  make chop-time    - Chop MP3 by fixed time intervals"
	@echo "  make chop-beat    - Chop MP3 aligned to beats"

# Install dependencies
install:
	pip install -r requirements.txt

# Clean output directory
clean:
	rm -rf output/
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Run tests (placeholder for now)
test:
	@echo "No tests implemented yet"

# Example usage - replace example.mp3 with your file
run-example:
	@echo "Running example (time-based chopping)..."
	python app.py example.mp3 -o output -d 2.0

# Custom command: Chop by time
# Usage: make chop-time FILE=yourfile.mp3 DURATION=1.5
chop-time:
	@if [ -z "$(FILE)" ]; then \
		echo "Error: Please specify FILE=yourfile.mp3"; \
		exit 1; \
	fi
	python app.py $(FILE) -m time -d $(or $(DURATION),1.0) -o output_time

# Custom command: Chop by beats
# Usage: make chop-beat FILE=yourfile.mp3 BEATS=8
chop-beat:
	@if [ -z "$(FILE)" ]; then \
		echo "Error: Please specify FILE=yourfile.mp3"; \
		exit 1; \
	fi
	python app.py $(FILE) -m beat -b $(or $(BEATS),4) -o output_beat

# Development setup
dev-setup: install
	@echo "Development environment ready!"

# Check if dependencies are installed
check-deps:
	@python -c "import librosa; print('librosa version:', librosa.__version__)"
	@python -c "import numpy; print('numpy version:', numpy.__version__)"
	@python -c "import soundfile; print('soundfile version:', soundfile.__version__)"
