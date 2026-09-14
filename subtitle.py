import whisper
import torch
import os

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    device = "cuda"
else:
    print("Using CPU")
    device = "cpu"

MODEL = "small"
print(f"\nLoading whisper '{MODEL}' model...")
model = whisper.load_model(MODEL, device=device)

def get_timestamp(seconds):
    """Helper function to format seconds into SRT timestamp format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def transcribe_audio(audio_filepath, subtitle_output_dir="subtitle_output_folder"):
    print(f"Transcribing {audio_filepath} with word-level timestamps...")
    
    # CRITICAL CHANGE: word_timestamps=True added here
    result = model.transcribe(audio_filepath, fp16=False, word_timestamps=True)

    print("\n--- Transcription ---")
    print(result["text"])

    base_name = os.path.splitext(os.path.basename(audio_filepath))[0]
    os.makedirs(subtitle_output_dir, exist_ok=True)

    txt_path = os.path.join(subtitle_output_dir, f"{base_name}.txt")
    srt_path = os.path.join(subtitle_output_dir, f"{base_name}.srt")

    # Save plain text
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"].strip())

    # Save word-highlighted SRT
    with open(srt_path, "w", encoding="utf-8") as f:
        srt_index = 1
        
        for segment in result["segments"]:
            # Fallback if the model fails to generate word timestamps
            if "words" not in segment:
                continue
                
            words = segment["words"]
            
            for i, current_word_data in enumerate(words):
                start = current_word_data["start"]
                
                # Prevent text flickering by extending the end time to the start of the next word
                if i < len(words) - 1:
                    end = words[i+1]["start"]
                else:
                    end = segment["end"]

                # Reconstruct the sentence, highlighting only the current word
                display_text = ""
                for j, w_data in enumerate(words):
                    word_str = w_data["word"]
                    if i == j:
                        # Wrap the active word in yellow
                        display_text += f'<font color="#FFFF00">{word_str}</font>'
                    else:
                        display_text += word_str

                f.write(f"{srt_index}\n")
                f.write(f"{get_timestamp(start)} --> {get_timestamp(end)}\n")
                f.write(f"{display_text.strip()}\n\n")
                srt_index += 1
                
    print("\nSaved Word-Level Subtitles:")
    print(f"  {txt_path}")
    print(f"  {srt_path}")
    
    return txt_path, srt_path