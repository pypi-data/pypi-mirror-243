import typer
import uvicorn

from .server import app as webapp

app = typer.Typer()


@app.command()
def run(host: str = "0.0.0.0", port: int = 8080):
    uvicorn.run(webapp, host=host, port=port, log_level="info")
