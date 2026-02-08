from typer import Typer
from enum import StrEnum
import typer
from yt_dlp import YoutubeDL
from typing import Annotated
import random
from rich.prompt import Prompt, Confirm
from rich.console import Console
from core.logger import SytdlpLogger
import logging
from core.hook import spinner_downloading, spinner_postprocess

app = Typer()
console = Console()


class AudioFormat(StrEnum):
    MP3 = "mp3"
    WAV = "wav"
    M4A = "m4a"


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
    MOV = "mov"
    MKV = "mkv"


@app.command()
def main():
    pass


@app.command()
def download(
    format: EveryFormat,
    file_name: Annotated[
        str,
        typer.Option(
            help="Choose file folder name (default is the title of the video)"
        ),
    ] = "%(title)s",
    worst: Annotated[bool, typer.Option(help="Get the worst quality video")] = False,
    random_number: Annotated[
        bool, typer.Option(help="Remove the random number in the end folder name")
    ] = True,
    verbose: Annotated[bool, typer.Option(help="See every logs of yt-dlp")] = False,
):

    url: str = Prompt.ask("[b]What is the url ? 🔗 [/b]")
    if not url.startswith("https://"):
        console.print(
            "[bold red]Please retry the command with a direct link.[/bold red]"
        )
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
        if not worst:
            format_opts = {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": format.value,
            }
        else:
            format_opts = {
                # "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
                "format": "worstvideo*+worstaudio/worst",
                "merge_output_format": format.value,
            }

        if format.value == "mov" or format.value == "mkv":
            format_confirmation = Confirm.ask(
                "[bold red] Are you sure you want to use mov or mkv because this will require re encored entire video and will take time and performance ? [/bold red]"
            )

            if not format_confirmation:
                console.print("Good decision to save time.")
                raise typer.Exit()

            format_opts = format_opts | {
                "postprocessors": [
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": format.value,
                    }
                ]
            }  # Add recoding options

    if random_number:
        title_opts = {
            "outtmpl": f"./{file_name} |[{random.randint(1, 1000)}].%(ext)s",
            "download_archive": None,
            "force_overwrites": True,
        }
    else:
        title_opts = {
            "outtmpl": f"./{file_name}.%(ext)s",
        }

    hook_opts = {}

    if verbose:
        hook_opts = hook_opts | {"logger": SytdlpLogger(), "verbose": True}
    else:
        hook_opts = hook_opts | {
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "progress_hooks": [spinner_downloading],
            "postprocessor_hooks": [spinner_postprocess],
        }

    ydl_opts = format_opts | title_opts | hook_opts  # type: ignore
    try:
        with YoutubeDL(ydl_opts) as ydl:  # type: ignore
            ydl.download(url)

    except Exception as e:
        logging.error(e)
        console.print(
            "There error report to https://github.com/writedev/simple-yt-dlp-cli/issues"
        )


if __name__ == "__main__":
    app()
