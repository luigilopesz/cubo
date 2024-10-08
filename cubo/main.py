import cubo
import os
from pathlib import Path
from rich.console import Console
import typer

app = typer.Typer(no_args_is_help=True)
console = Console()

@app.command('info')
def print_info(custom_message : str = ""):
    """
    Print information about the module
    """
    console.print("Hello! I am cubo")
    console.print(f"Author: { cubo.__author__} / FELIPE MARIANO")
    console.print(f"Version: { cubo.__version__}")
    console.print("COMANDOS: W A S D para rotacionar")
    console.print("---")
    console.print("COMANDOS: Q E para aproximar e afastar")
    console.print("---")
    console.print("COMANDOS: C para ver o cubo")
    console.print("---")
    console.print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    console.print(">>>COMANDOS: V para ver a vaca<<<")
    console.print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    if custom_message != "":
        console.print(f"Custom message: {custom_message}")

@app.command() # Defines a default action
def run():
    """
    Probably run the main function of the module
    """
    print("Hello world!")
    cubo.run_aps4()
    script_path = Path(os.path.abspath(__file__))
    parent_path = script_path.parent
    print("Script path:", script_path)
    with open(parent_path / "assets/poetry.txt") as f:
        print(f.read())
    with open(parent_path / "assets/test_folder/test_something.txt") as f:
        print(f.read())

if __name__ == "__main__":
    app()