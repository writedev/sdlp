import typer

app = typer.Typer()


@app.command()
def bonjours():
    print("bonjours")


@app.command()
def salut():
    print("salut")
