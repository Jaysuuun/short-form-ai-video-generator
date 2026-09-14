from kokoro import KPipeline
import soundfile as sf
import numpy as np
import os
import re

pipline = KPipeline(lang_code="a", device="cuda")

def generate_ai_audio(txt_filepath, output_dir="tts_output_folder", voice="af_heart", speed=1):

    if not txt_filepath.lower().endswith('.txt'):
        raise ValueError(f"Input must be a txt file. Recieved {txt_filepath}")

    with open(txt_filepath, "r", encoding="utf-8") as file:
        text = file.read()

        first_line = text.split('\n')[0].strip()

        safe_filename = re.sub(r'[\\/*?:"<>|]', "", first_line)
        if not safe_filename:
            safe_filename = "unnamed_audio"

        os.makedirs(output_dir, exist_ok=True)

        output_wav_path = os.path.join(output_dir, f"{safe_filename}.wav")

        generator = pipline(text, voice=voice, speed=speed)
        audio_chunks = []

        for gs, ps, audio in generator:
            audio_chunks.append(audio)

        final_audio = np.concatenate(audio_chunks)
        sample_rate = 24000


    if output_wav_path:
        sf.write(output_wav_path, final_audio, sample_rate)
        print("Saved: {output_wav_path}")

    return output_wav_path, final_audio, sample_rate