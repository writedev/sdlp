from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress
from rich.progress import (
    TransferSpeedColumn,
    BarColumn,
    TextColumn,
    SpinnerColumn,
    TimeElapsedColumn,
    ProgressColumn,
    DownloadColumn,
    TimeRemainingColumn,
)

console = Console()

spinner = Spinner("dots")
live = Live(spinner, refresh_per_second=20, console=Console(), transient=True)

progress = Progress(
    SpinnerColumn("dots"),
    TextColumn("{task.description}"),
    BarColumn(),
    DownloadColumn(),
    TimeElapsedColumn(),
    transient=True,
    console=console,
    expand=True,
)

task_1 = progress.add_task("[bold]Downloading...[/bold]")


def progress_downloading(d: dict):
    progress.start()
    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate")

        downloaded = d.get("downloaded_bytes")

        progress.update(
            task_1,
            total=total,
            completed=downloaded,
        )
    if d["status"] == "finished":
        progress.stop()
        console.print("[green]The Downloading is finished ! [/green]")


def spinner_postprocess(d):
    live.start()
    spinner.update(text="[b]Postprocessing...")
    if d["status"] == "finished":
        live.stop()
        console.print("[green]The Postprocessing is finished ! [/green]")
