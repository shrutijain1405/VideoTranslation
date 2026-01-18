import ffmpeg
from TTS.api import TTS
from moviepy.editor import AudioFileClip
import os

def extract_audio(video_path, output_audio_path, sample_rate):
    (
        ffmpeg
        .input(video_path)
        .output(
            output_audio_path,
            ac=1,
            ar=sample_rate
        )
        .global_args('-loglevel', 'error')
        .overwrite_output()
        .run()
    )

def tts(trans_sentences, input_audio, output_dir, sample_rate):

    tts = TTS("tts_models/de/thorsten/tacotron2-DDC")

    i=0
    for sentence in trans_sentences:
        filename = f"{output_dir}/trans_segment_{i+1}.wav"
        if os.path.exists(filename):
            print(f"{filename} exists")
            continue
        print(f"Writing to {filename}")
        tts.tts_with_vc_to_file(
            sentence,
            speaker_wav=f"{output_dir}/input_audio.wav",
            file_path= filename
        )
        i += 1

def break_audio(audio_path, output_dir, sample_rate, sentences):

    audio_clip = AudioFileClip(audio_path)

    for i, segment in enumerate(sentences):
        filename = os.path.join(output_dir, f"input_segment_{i+1}.wav")
        if os.path.exists(filename):
            print(f"{filename} exists")
            continue
        start_time = segment["start"] 
        end_time = min(segment["end"], audio_clip.duration - 1e-3)

        seg_clip = audio_clip.subclip(start_time, end_time)

        seg_clip.write_audiofile(filename, fps=sample_rate)
    try:
        seg_clip.close()  
    except:
        pass
    audio_clip.close()

def merge_video_audio(out_dir, video_path):
    output_path = f"{out_dir}/output_video.mp4"
    # Load video and audio streams
    video_stream = ffmpeg.input(video_path)
    audio_stream = ffmpeg.input(f"{out_dir}/output_audio.wav")

    # Merge them
    ffmpeg_out = ffmpeg.output(
        video_stream.video,
        audio_stream.audio,
        output_path,
        vcodec='copy',
        acodec='aac',
    ).global_args('-loglevel', 'error')

    # Run the ffmpeg process
    ffmpeg_out.run(overwrite_output=True)
    print(f"Merged video saved to {output_path}")

    
