import typer

app = typer.Typer()


@app.command()
def hey():
    print("hey")


@app.command()
def bye():
    print("bye")
