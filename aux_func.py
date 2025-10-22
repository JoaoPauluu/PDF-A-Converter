from rich.console import Console
from rich.logging import RichHandler
import os
import sys


def print_welcome(console: Console | None = None) -> None:
    if not console:
        console = Console()

    console.print("\n\n")
    console.print("Conversor de PDF para PDF/A-2b", style="bold green")
    console.print("Script feito por:", style="bold") 
    console.print("João Paulo Chiari de Gasperi", style="bold green")
    console.print("\n")

def current_dir():
    if getattr(sys, 'frozen', False):  # running as compiled .exe
        return os.path.dirname(sys.executable)
    else:  # running as a normal .py script
        return os.path.dirname(os.path.abspath(__file__))

def current_dir_at(*args) -> str:
    return_str = current_dir()
    for item in args:
        return_str = os.path.join(return_str, item)
    return return_str


def get_all_pdfs(folder: str) -> list[str]:
    all_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".pdf"):  # Only convert PDFs
                all_files.append(os.path.join(root, file))
    return all_files

def create_folders_cwd(*folders) -> None:
    for folder in folders:
        full_path = current_dir_at(folder)
        if not os.path.exists(full_path):
            os.mkdir(full_path)
