from TTS import generate_ai_audio
from subtitle import transcribe_audio
from video_generator import create_video


def main():
    
    input_text_file = "story.txt"
    audio_folder = "tts_output_folder"
    subtitle_folder = "subtitle_output_folder"
    backgrounds_folder = "bgvideos"
    video_folder = "output"


    audio_path, audio_data, sample_rate = generate_ai_audio(
        txt_filepath=input_text_file,
        output_dir=audio_folder
    )

    print(f"Audio successfully created at: {audio_path}")

    txt_out, srt_path = transcribe_audio(
        audio_filepath= audio_path,
        subtitle_output_dir=subtitle_folder
    )

    final_video_path = create_video(
        audio_filepath=audio_path,
        subtitle_filepath=srt_path,
        bg_dir=backgrounds_folder,
        output_dir=video_folder
    )

    print("\nAll pipeline tasks finished successfully!")


if __name__ == "__main__":
    main()