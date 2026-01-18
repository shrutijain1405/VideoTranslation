import os
import numpy as np
import librosa
import soundfile as sf
import ffmpeg

def sync(output_dir, min_ratio, max_ratio, num_segments):
    """
    Syncs translated audio segments to match input segment durations using librosa.
    Saves output segments as WAV files.
    """
    sample_rate = 48000
    for i in range(num_segments):
        input_path = f"{output_dir}/input_segment_{i+1}.wav"
        trans_path = f"{output_dir}/trans_segment_{i+1}.wav"
        out_path = f"{output_dir}/synced_segment_{i+1}.wav"

        print(f"Writing to {out_path}")
        if os.path.exists(out_path):
            print(f"{out_path} exists, skipping.")
            continue

        input_seg, _ = librosa.load(input_path, sr=sample_rate, mono=True)
        trans_seg, _ = librosa.load(trans_path, sr=sample_rate, mono=True)

        ratio = trans_seg.shape[0] / input_seg.shape[0]
        ratio = max(min_ratio, min(max_ratio, ratio))
        
        stretched = librosa.effects.time_stretch(trans_seg, rate=ratio)

        if len(stretched) < input_seg.shape[0]:
            pad_len = input_seg.shape[0] - len(stretched)
            stretched = np.concatenate([stretched, np.zeros(pad_len, dtype=stretched.dtype)])

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        sf.write(out_path, stretched, samplerate=sample_rate)
        

def merge_segments(output_dir, num_segments):
    """
    Reads a list of WAV files, concatenates them, and saves the result.

    Args:
        file_list (list of str): List of file paths to WAV files.
        output_path (str): Path to save concatenated WAV.
        sample_rate (int): Target sample rate.
        mono (bool): Whether to convert audio to mono.
    """
    sample_rate = 48000
    all_audio = []
    input_audio_path =  f"{output_dir}/input_audio.wav"
    output_audio_path =  f"{output_dir}/output_audio.wav"
    input_audio, _ = librosa.load(input_audio_path, sr=sample_rate, mono=True)

    for i in range(num_segments):
        sync_path = f"{output_dir}/synced_segment_{i+1}.wav"
        audio, sr = librosa.load(sync_path, sr=sample_rate, mono=True)
        all_audio.append(audio)

    # Concatenate along time axis
    merged_audio = np.concatenate(all_audio)
    ratio = merged_audio.shape[0] / input_audio.shape[0]
    stretched = librosa.effects.time_stretch(merged_audio, rate=ratio)

    # Save concatenated audio
    sf.write(output_audio_path, stretched, samplerate=sample_rate)
    print(f"Saved concatenated audio to {output_audio_path}")


def sync_audios(output_dir, min_ratio, max_ratio, num_segments):

    sync(output_dir, min_ratio, max_ratio, num_segments)
    merge_segments(output_dir, num_segments)
    
