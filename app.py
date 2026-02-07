from typer import Typer
from enum import StrEnum
import typer
from yt_dlp import YoutubeDL, postprocessor
from typing import Annotated, Optional, Literal, Union
import random
from rich.prompt import Prompt, Confirm
from rich.console import Console

app = Typer()
console = Console()


class AudioFormat(StrEnum):
    MP3 = "mp3"
    WAV = "wav"
    m4a = "M4A"


class VideoFormat(StrEnum):
    MP4 = "mp4"
    MOV = "mov"
    MKV = "mkv"


class EveryFormat(StrEnum):
    # Audio Format
    MP3 = "mp3"
    WAV = "wav"
    M4A = "m4a"
    # Video Format
    MP4 = "mp4"
    MKV = "mkv"


@app.command()
def main():
    pass


@app.command()
def download(
    format: EveryFormat,
    worst: Annotated[bool, typer.Option(help="Get the worst quality video")] = False,
    random_number: Annotated[
        bool, typer.Option(help="Remove the random number in the end folder name")
    ] = True,
):
    url: str = Prompt.ask("[b]What is the url ? 🔗 [/b]")
    if not url.startswith("https://"):
        raise typer.Exit()

    if format.value in AudioFormat:
        format_opts = {
            # "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
            "format": "worstvideo+*bestaudio/best",
            "postprocessors": [
                {  # Extract audio using ffmpeg
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format.value,
                }
            ],
        }

    if format.value in VideoFormat:
        if worst:
            format_opts = {
                # "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
                "format": "worstvideo*+worstaudio/worst",
                "merge_output_format": format.value,
            }
        else:
            format_opts = {
                # "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
                # "format": "bv*[vcodec^=avc1]+ba[acodec^=mp4a]/b",
                "merge_output_format": format.value,
                "format": "bestvideo*+bestaudio/best",
            }

    if random_number:
        title_opts = {
            "outtmpl": f"./%(title)s |[{random.randint(1, 1000)}].%(ext)s",
            "download_archive": None,
            "force_overwrites": True,
        }
    else:
        title_opts = {
            "outtmpl": "./%(title)s.%(ext)s",
            "postprocessor_args": ["-loglevel", "error"],
        }

    ydl_opts = format_opts | title_opts

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


if __name__ == "__main__":
    app()
