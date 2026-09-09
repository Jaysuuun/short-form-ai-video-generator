import whisper
import torch

AUDIO_FILE = "kokoro_test.wav"
MODEL = "small"

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    device = "cuda"
else:
    print("Using CPU")
    device = "cpu"

print(f"\nLoading Whisper '{MODEL}' model...")
model = whisper.load_model(MODEL, device=device)

print("Transcribing...")
result = model.transcribe(
    AUDIO_FILE,
    fp16=False
)

print("\n--- TRANSCRIPTION ---")
print(result["text"])

# Save plain text
with open("whisper_test.txt", "w", encoding="utf-8") as f:
    f.write(result["text"].strip())

# Save timestamped segments
with open("whisper_test.srt", "w", encoding="utf-8") as f:
    for i, segment in enumerate(result["segments"], start=1):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"].strip()

        def timestamp(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millis = int((seconds - int(seconds)) * 1000)

            return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

        f.write(f"{i}\n")
        f.write(f"{timestamp(start)} --> {timestamp(end)}\n")
        f.write(f"{text}\n\n")

print("\nSaved:")
print("  whisper_test.txt")
print("  whisper_test.srt")