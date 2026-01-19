#!/bin/bash
set -e  

INPUT_VIDEO="$1"
INPUT_SRT="$2"
OUTPUT_DIR="$3"

echo "Input video: $INPUT_VIDEO"
echo "Input srt:   $INPUT_SRT"
echo "Output dir:  $OUTPUT_DIR"


# Run translation pipeline
conda activate vidTrans
mkdir -p "$OUTPUT_DIR"
python main.py \
  --input_video "$INPUT_VIDEO" \
  --input_srt_file "$INPUT_SRT" \
  --output_dir "$OUTPUT_DIR"

# Run LatentSync
conda activate latentsync
cd LatentSync
python -m scripts.inference \
    --unet_config_path "configs/unet/stage2_512.yaml" \
    --inference_ckpt_path "checkpoints/latentsync_unet.pt" \
    --inference_steps 20 \
    --guidance_scale 1.5 \
    --enable_deepcache \
    --video_path "$INPUT_VIDEO" \
    --audio_path "$OUTPUT_DIR/output_audio.wav" \
    --video_out_path "$OUTPUT_DIR/output_video_lipsync.mp4"
