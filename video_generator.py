import random
import subprocess
import os
from pathlib import Path

def create_video(audio_filepath, subtitle_filepath, bg_dir="bgvideos", output_dir="output"):
    bg_path = Path(bg_dir)
    audio_path = Path(audio_filepath)
    subtitle_path = Path(subtitle_filepath)
    out_dir = Path(output_dir)
    
    out_dir.mkdir(parents=True, exist_ok=True)

    if not bg_path.exists():
        raise FileNotFoundError(f"Background folder not found: {bg_path}")
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if not subtitle_path.exists():
        raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")

    backgrounds = list(bg_path.glob("*.mp4"))
    if not backgrounds:
        raise FileNotFoundError(f"No MP4 files found in {bg_path}")
    
    background = random.choice(backgrounds)
    print(f"Selected background: {background.name}")

    base_name = audio_path.stem
    output_file = out_dir / f"{base_name}.mp4"

    escaped_subtitle_path = str(subtitle_path.resolve()).replace("\\", "/").replace(":", "\\:")

    # Removed PrimaryColour so it defaults to white, allowing the yellow SRT highlight to work
    SUBTITLE_STYLE = (
        "force_style='"
        "FontName=Arial Bold,"
        "FontSize=16,"           
        "OutlineColour=&H00000000," 
        "BorderStyle=1,"         
        "Outline=2,"
        "Shadow=0,"
        "Alignment=10,"          
        "MarginV=0'"             
    )

    video_filter = (
        "scale=1080:1920:"
        "force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        f"subtitles='{escaped_subtitle_path}':{SUBTITLE_STYLE}"
    )

    command = [
        "ffmpeg",
        "-y",
        
        "-stream_loop", "-1",
        "-fflags", "+genpts",
        "-i", str(background),

        "-i", str(audio_path),

        "-vf", video_filter,
        "-r", "30", 

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

        str(output_file)
    ]

    print("\nStarting FFmpeg for word-highlighted video generation...\n")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("FFmpeg Error detected!")
        print(e.stderr)
        raise

    print("\n================================")
    print("Highlighted video generation complete!")
    print("================================")
    print(f"Output saved to: {output_file}")
    
    return str(output_file)