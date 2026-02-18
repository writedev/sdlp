import typer
from ..utils.format import VideoFormat
from ..utils.progress_hook import progress_downloading, spinner_postprocess
from typing import Annotated
from rich.prompt import Prompt, Confirm
from rich.console import Console
from yt_dlp import YoutubeDL
import random

app = typer.Typer()
console = Console()


@app.command()
def video(
    format: VideoFormat,
    file_name: Annotated[
        str,
        typer.Option(
            help="Choose file folder name (default is the title of the video)"
        ),
    ] = "%(title)s",
    worst: Annotated[bool, typer.Option(help="Get the worst quality video")] = False,
    random_number: Annotated[
        bool,
        typer.Option(
            help="Remove the random number in the end folder name (exemple: |[000])"
        ),
    ] = True,
    verbose: Annotated[bool, typer.Option(help="See every logs of yt-dlp")] = False,
    url: Annotated[str, typer.Option(help="Give the URL")] = "",
):
    if not url:
        url = Prompt.ask("[b]Give the url 🔗 [/b]")

    if not url.startswith("https://"):
        console.print(
            "[bold red]Please retry the command with a direct url.[/bold red]"
        )
        raise typer.Exit()

    if worst:
        # quality opts (worst quality)

        format_opts = {
            "format": "worstvideo*+worstaudio/worst",
            "merge_output_format": format.value,
        }
    else:
        # quality opts (best quality)

        format_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": format.value,
        }

    if format.value in ["mkv", "mov"]:
        format_confirmation = Confirm.ask(
            "[bold red] This is a format who take time and performance. Are you sure to continue ?"
        )

        if not format_confirmation:
            console.print("Good decision.")
            raise typer.Exit()

        # Re encode opts

        format_opts = format_opts | {
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": format.value,
                }
            ]
        }

    # The opts for the title like ""

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

    # For the progress bar and spinner (downloading and postprocessing)

    if verbose:
        hook_opts = {"verbose": True}

    else:
        hook_opts = {
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "progress_hooks": [progress_downloading],
            "postprocessor_hooks": [spinner_postprocess],
        }

    ydl_opts = hook_opts | title_opts | format_opts

    with YoutubeDL(ydl_opts) as ydl:  # type: ignore
        ydl.download(url)

    console.print("[green]The downloading is finished ✨")
