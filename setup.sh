#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# 3. Install Python packages
echo "Installing Python packages..."
pip install ffmpeg-python
pip install pysrt
pip install -U transformers
pip install torch torchvision torchaudio
pip install accelerate
pip install soundfile
sudo apt-get install -y espeak-ng
pip install coqui-tts
pip install sentencepiece
pip install pyrubberband
pip install moviepy==1.0.3
pip install numpy==1.24.4
sudo apt install rubberband-cli