from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

console = Console()

spinner = Spinner("dots")
live = Live(spinner, refresh_per_second=20, console=Console(), transient=True)


def spinner_downloading(d):
    live.start()
    spinner.update(text="[b]Downloading...[/b]")
    if d["status"] == "downloading":
        current_progress = d["downloaded_bytes"] / d["total_bytes"] * 100
        spinner.update(text=f"[b]Downloading : {round(current_progress)}%[/b]")

    if d["status"] == "finished":
        live.stop()
        console.print("[green]The Downloading is finished ! [/green]")


def spinner_postprocess(d):
    live.start()
    spinner.update(text="[b]Postprocessing...")
    if d["status"] == "finished":
        live.stop()
        console.print("[green]The Postprocessing is finished ! [/green]")
