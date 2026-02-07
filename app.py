from typer import Typer
from enum import StrEnum
import typer
from yt_dlp import YoutubeDL
from typing import Annotated, Optional
from rich.prompt import Prompt

app = Typer()

class AudioFormat(StrEnum):
    mp3 = "MP3"
    wav = "WAV"
    m4a = "M4A"

class VideoFormat(StrEnum):
    mp4 = "MP4"
    mov = "MOV"

@app.command()
def main():
    pass


@app.command()
def download(
    mp4: Annotated[bool, typer.Option("--mp4")] = False,
    mp3: Annotated[bool, typer.Option("--mp3")] = False,
    wav : Annotated[bool, typer.Option("--wav")] = False,
    mov: Annotated[bool, typer.Option("--mov")] = False,
):
    url: str = Prompt.ask("[b]What is the url ? [/b]")
    if not url.startswith("https://"):
        raise typer.Exit()
    
    AUDIO_FORMAT : str | None = None

    VIDEO_FORMAT : str | None = None

    if mp3 or wav:
        
        

    if mp4:
        ydl_opts: any = {
            # "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
            "format": "bestvideo*+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": "./%(title)s.%(ext)s",
        }

        with YoutubeDL(ydl_opts) as ydl:
            file = ydl.download(url)

        return

    if mp3:
        ydl_opts = {
            # "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
            "format": "bestaudio/best",
            "postprocessors": [
                {  # Extract audio using ffmpeg
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }
            ],
            "converouttmpl": "./%(title)s.%(ext)s",
        }

        with YoutubeDL(ydl_opts) as ydl:
            file = ydl.download(url)


if __name__ == "__main__":
    app()
