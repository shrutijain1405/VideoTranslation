#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Setting up env for translation"
conda create --name vidTrans python=3.10
conda activate vidTrans

# Install Python packages
echo "Installing packages..."
sudo apt-get update
sudo apt-get install -y espeak-ng
sudo apt install rubberband-cli
pip install ffmpeg-python
pip install pysrt
pip install -U transformers
pip install torch torchvision torchaudio
pip install accelerate
pip install soundfile
pip install coqui-tts
pip install sentencepiece
pip install pyrubberband
pip install moviepy==1.0.3
pip install numpy==1.24.4
sudo apt-get install -y ffmpeg

echo "cloning into LatentSync"
git clone https://github.com/bytedance/LatentSync.git
cd LatentSync

echo "Setting up env for LatentSync"
source setup_env.sh

echo "Setup complete!!"