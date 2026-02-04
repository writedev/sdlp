from typer import Typer
import typer
from yt_dlp import YoutubeDL

app = Typer()


@app.command()
def main():
    pass


@app.command()
def download():
    url: str = typer.prompt("What is the url video ? ")
    if not url.startswith("https://"):
        raise typer.Exit()
    print(url)


if __name__ == "__main__":
    app()
