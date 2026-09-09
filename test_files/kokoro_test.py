from kokoro import KPipeline
import soundfile as sf
import numpy as np

pipeline = KPipeline(
    lang_code="a",
    device="cuda"
)

text = """
The Little Cloud Who Was Afraid to Rain

Once, high above a small village, lived a little cloud named Puffy. All the other clouds loved to rain, sending sparkling drops down to the flowers and fields below. But Puffy was scared. "What if I rain too hard? What if I make a mess?" she worried.

One day, the village grew dry. The flowers drooped. The garden turned brown. A little girl named Mia looked up at the sky and whispered, "Please, someone help our flowers."

Puffy heard her. Her heart pounded. She wanted to help, but she was still afraid.

Then an old wise cloud named Gus drifted beside her. "Puffy," he said gently, "rain isn't about being perfect. It's about giving what you have, even a little."

Puffy took a deep breath. She let go, just a few drops at first. Then a few more. Soon, gentle rain fell over the whole village. The flowers lifted their heads. The grass turned green again. Mia laughed and danced in the rain, arms wide open.

From that day on, Puffy wasn't afraid anymore. She learned that even small clouds can bring big joy, one little drop at a time.

The End.
"""

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