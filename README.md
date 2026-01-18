
# Video Translation

## Project Overview

This project implements a **video translation pipeline** that takes an input Video, translates the Audio into a target language (German), and synchronizes the translated audio back with the original video.

The focus is on:
- Accurate text to text translation
- Text-to-speech with voice cloning
- Temporal alignment between original and translated audio segments

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/shrutijain1405/VideoTranslation.git
cd VideoTranslation
```

### 2. Create and Activate Conda Environment
```bash
conda create --name vidTrans python=3.9
conda activate vidTrans
```

### 3. Install Dependencies
```bash
sh setup.sh
```

---

## Running inference

Example:
```bash

python main.py \
  --input_video path/to/input.mp4 \
  --input_srt_file path/to/srt/file.srt \
  --output_dir path/to/output_dir/

```

---

## Project Description

**Pipeline:**

1. **Parsing the srt file to get transcripts and timesteps of the segments**
2. **Text to Text translation while keeping the text lengths same** 
    - Text to Text translation using [opus-mt-en-de](https://huggingface.co/Helsinki-NLP/opus-mt-en-de) model
    - Text length matching using [google/flan-t5-small](https://huggingface.co/google/flan-t5-small) model
        - prompt: "Rewrite the following sentence to be approximately {target_chars} characters long, keeping meaning intact: {translated_sentence}"
3. **Extracting input audio segemnts** 
    - extract input audio from input video using ```ffmpeg-python```
    - break the input audio into segments based on transcript segments
4. **Text-to-speech generation with voice cloning** 
    - using [coqui-tts](https://github.com/coqui-ai/TTS) ```tts_models/de/thorsten/tacotron2-DDC``` model
    - runs on each translated segment
5. **Audio time synchronization** 
    - synchronize each input audio and translated audio segment using ```librosa```
    - slow down or speed up the translated audio segment according to input audio segment within limits
    - if the translated audio is still short, match the length by appending silence
6. **Merging synced translated audios together** 
    - merge the synced audio segments
    - global syncing - to ensure final audio lengths are exactly the same, sync the merged audio with input audio again without limits
6. **Merging translated audio with original video**
    - using ```ffmpeg-python```


## Results



https://github.com/user-attachments/assets/ad7a9a98-8a80-422d-ae52-e6fb42e24b02


---

## Limitations

- Supports only English to German translation
- Audio may get distorted if translation lengths are very different

---

## Future Work

- LipSyncing
- Multi-speaker support
