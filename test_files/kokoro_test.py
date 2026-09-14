from kokoro import KPipeline
import soundfile as sf
import numpy as np

pipeline = KPipeline(
    lang_code="a",
    device="cuda"
)

with open ("story.txt", "r") as file:
    text = file.read()



generator = pipeline(
    text,
    voice="af_heart",
    speed=1
)

audio_chunks = []

for gs, ps, audio in generator:
    audio_chunks.append(audio)

final_audio = np.concatenate(audio_chunks)

sf.write(
    "kokoro_test.wav",
    final_audio,
    24000
)

print("Saved: kokoro_test.wav")