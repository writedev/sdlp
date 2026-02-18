from .video import app as core_video_part
import typer

app = typer.Typer()

app.add_typer(english_app)
app.add_typer(french_app)
