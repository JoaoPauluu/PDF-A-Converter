import os
from rich.console import Console
import subprocess


def current_dir_at(*args):
    return_str = os.getcwd()
    for item in args:
        return_str = os.path.join(return_str, item)

    return return_str


def main() -> None:
    console = Console()

    #Bem-vindo
    console.print("\n\n")
    console.print("Conversor de PDF para PDF/A-2b", style="bold green")
    console.print("Script feito por:", style="bold") 
    console.print("João Paulo Chiari de Gasperi", style="bold green")
    console.print("\n\n")

    gs_path = ''

    if os.path.exists(current_dir_at('ghostscript', 'bin', 'gswin64c.exe')):
        gs_path = current_dir_at('ghostscript', 'bin', 'gswin64c.exe')
        console.print(f"Instalação local do Ghostscript detectada! Utilizando: {gs_path}")
    if not os.path.exists(current_dir_at('ghostscript', 'bin', 'gswin64c.exe')):
        gs_path = 'gswin64c'
        console.print("Instalação local do Ghostscript não detectada. Tentando utilizar instalação do sistema...")


    input_folder = current_dir_at("input")
    output_folder = current_dir_at("output")

    #cria pastas
    if not os.path.exists(input_folder):
        os.mkdir(input_folder)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)


    nomes_input = os.listdir(input_folder)
    if not nomes_input:
        console.print("[red]Nenhum arquivo encontrado na pasta [/red][bold purple]input")
        console.print("[red]Por favor, adicione arquivos PDF e rode o programa novamente.[/red]")
        return

    console.print("Arquivos detectados na pasta [bold purple]input")
    for file in nomes_input:
        console.print(file, style="yellow")

    console.print("\nPressione [bold]Enter[/bold] para converter os documentos acima...")
    input()

    for file in nomes_input:
        input_file = current_dir_at('input', file)
        output_file = current_dir_at('output', file)
        command = [
            f"{gs_path}",
            "-sDEVICE=pdfwrite",
            "-dPDFA=2",
            "-dPDFACompatibilityPolicy=1",
            "-sColorConversionStrategy=UseDeviceIndependentColor",
            f'-o{output_file}',
            "-f",
            f"{input_file}"
        ]

        try:
            #console.print(command)
            subprocess.run(command, check=True)
            console.print(file + " -> Sucesso", style="green")
        except:
            console.print(file + " -> Algo deu errado", style="red")
            


if __name__ == '__main__':
    main()