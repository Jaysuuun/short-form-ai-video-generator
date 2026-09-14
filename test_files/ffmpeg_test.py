import random
import subprocess
from pathlib import Path


# ==========================================
# PATHS
# ==========================================

BASE_DIR = Path(__file__).parent

BG_DIR = BASE_DIR / "bgvideos"
AUDIO_FILE = BASE_DIR / "kokoro_test.wav"
SUBTITLE_FILE = BASE_DIR / "whisper_test.srt"
OUTPUT_DIR = BASE_DIR / "video_test_output"

OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "test_final.mp4"


# ==========================================
# CHECK FILES
# ==========================================

if not BG_DIR.exists():
    raise FileNotFoundError(f"Background folder not found: {BG_DIR}")

if not AUDIO_FILE.exists():
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

if not SUBTITLE_FILE.exists():
    raise FileNotFoundError(f"Subtitle file not found: {SUBTITLE_FILE}")


# ==========================================
# RANDOM BACKGROUND
# ==========================================

backgrounds = list(BG_DIR.glob("*.mp4"))

if not backgrounds:
    raise FileNotFoundError(f"No MP4 files found in {BG_DIR}")

background = random.choice(backgrounds)

print(f"Selected background: {background.name}")


# ==========================================
# ESCAPE SUBTITLE PATH
# ==========================================

subtitle_path = str(SUBTITLE_FILE.resolve())

subtitle_path = (
    subtitle_path
    .replace("\\", "/")
    .replace(":", "\\:")
)


# ==========================================
# VIDEO FILTER
# ==========================================

video_filter = (
    "scale=1080:1920:"
    "force_original_aspect_ratio=increase,"
    "crop=1080:1920,"
    f"subtitles='{subtitle_path}':"
    "force_style="
    "'FontName=Arial,"
    "FontSize=20,"
    "PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H00000000,"
    "Outline=2,"
    "Shadow=0,"
    "Alignment=5,"
    "MarginV=0'"
)


# ==========================================
# FFMPEG COMMAND
# ==========================================

command = [
    "ffmpeg",
    "-y",

    # Background
    "-stream_loop", "-1",
    "-i", str(background),

    # Kokoro narration
    "-i", str(AUDIO_FILE),

    # Video filters
    "-vf", video_filter,

    # Output FPS
    "-r", "30",

    # IMPORTANT:
    # Only use the background VIDEO
    "-map", "0:v:0",

    # IMPORTANT:
    # Only use the Kokoro AUDIO
    "-map", "1:a:0",

    # Stop when narration ends
    "-shortest",

    # Video encoding
    "-c:v", "h264_nvenc",
    "-preset", "p4",
    "-cq", "23",

    # Audio encoding
    "-map", "0:v:0",
    "-map", "1:a:0",

    "-af", "volume=1.8",

    "-shortest",

    "-c:v", "h264_nvenc",
    "-preset", "p4",
    "-cq", "23",

    "-c:a", "aac",
    "-b:a", "192k",
    "-ar", "44100",
    # Output
    str(OUTPUT_FILE),
]


# ==========================================
# RUN
# ==========================================

print("\nStarting FFmpeg...\n")

subprocess.run(command, check=True)

print("\n================================")
print("Video generation complete!")
print("================================")
print(f"Background: {background.name}")
print(f"Output:     {OUTPUT_FILE}")
print("Resolution: 1080x1920")
print("FPS:        30")
print("Audio:      Kokoro narration")
print("Encoder:    NVIDIA NVENC")