# main.py

import argparse
import torch

from src.audio_utils import extract_audio, tts, break_audio, merge_video_audio
from src.text_utils import read_srt_file
from src.text2text import get_translations
from src.audio_sync import sync_audios

def parse_args():
    parser = argparse.ArgumentParser("Video Translation Pipeline")

    parser.add_argument("--input_video", type=str, default="/home/shruti/projects/video_translation/inputs/Tanzania-2.mp4")
    parser.add_argument("--input_srt_file", type=str, default="/home/shruti/projects/video_translation/inputs/Tanzania-caption.srt")
    parser.add_argument("--output_dir", type=str, default="/home/shruti/projects/video_translation/outputs")

    parser.add_argument("--min_ratio", type=float, default=0.85)
    parser.add_argument("--max_ratio", type=float, default=1.2)

    return parser.parse_args()

def main():
    args = parse_args()
    sample_rate = 22050
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    sentence_grps = read_srt_file(args.input_srt_file)
    print("Transcripts: ")
    for i, s in enumerate(sentence_grps):
      t = s["text"]
      print(f"{i+1}: {t}")
    print()
    num_segs = len(sentence_grps)

    trans_sentence_grps = get_translations(sentence_grps, device)
    if(len(trans_sentence_grps) == 0):
        return  

    audio_path = f"{args.output_dir}/input_audio.wav"
    extract_audio(args.input_video, audio_path, sample_rate)
    break_audio(audio_path, args.output_dir, sample_rate,sentence_grps)
     
    
    tts(trans_sentence_grps, audio_path, args.output_dir, sample_rate)

    sync_audios(args.output_dir, args.min_ratio, args.max_ratio, num_segs)

    merge_video_audio(args.output_dir, args.input_video)

if __name__ == "__main__":
    main()
