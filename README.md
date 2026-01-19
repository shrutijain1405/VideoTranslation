
# Video Translation

## Project Overview

This project implements a **video translation pipeline** that takes an input Video, translates the Audio into a target language (German), and synchronizes the translated audio back with the original video with lip-syncing.

The focus is on:
- Accurate text to text translation
- Text-to-speech with voice cloning
- Temporal alignment between original and translated audio segments
- Lipsync the new audio to video
---

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/shrutijain1405/VideoTranslation.git
cd VideoTranslation
```

### Setup Environment
```bash
source setup.sh
```

---

## Running inference

First get the translated Audio. \
Note: Please change the input arguments in ```trans_audio_inference.sh``` before running.
```bash
conda activate vidTrans
sh trans_audio_inference.sh
```

Then get the Lip-synced video. \
Note: Please change the input arguments in ```inference.sh``` before running.
```bash
conda activate latentsync
cd LatentSync
sh ./inference.sh
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
7. **Lip-syncing**
    - use [LatentSync](https://github.com/bytedance/LatentSync) to synchronize the final output audio and the input video.


## Results

**Input Video**

https://github.com/user-attachments/assets/86d0ce65-9c1e-48ab-a62f-fe65b2a48b4d


**Input Audio Segment**

[input_segment_3.wav](https://github.com/user-attachments/files/24699310/input_segment_3.wav)


**Original Transcript Segment**

Over a million wildebeest, zebras, and gazelles travel vast distances in search of fresh grass, braving rivers filled with crocodiles.


**Translated Transcript Segment**

Über eine Million Wildebees, Zebras und Gazellen reisen weite Entfernungen auf der Suche nach frischem Gras, dürren Flüssen mit Krokodilen.


**Translated Audio Segment**

[trans_segment_3.wav](https://github.com/user-attachments/files/24699327/trans_segment_3.wav)


**Synced Translated Audio Segment**

[synced_segment_3.wav](https://github.com/user-attachments/files/24699333/synced_segment_3.wav)


**Output Without Lip Sync**

https://github.com/user-attachments/assets/ad7a9a98-8a80-422d-ae52-e6fb42e24b02


**Output With Lip Sync**

https://github.com/user-attachments/assets/811a7d62-b335-446d-8d76-d1f73f10b941


---

## Limitations

- Supports only English to German translation
- Audio may get distorted if translation lengths are very different

---

## Future Work

- Multi-speaker support
