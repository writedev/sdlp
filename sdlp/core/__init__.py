from .video import app as core_video_app
from .audio import app as core_audio_app
import typer

app = typer.Typer()

app.add_typer(core_video_app)
app.add_typer(core_audio_app)
