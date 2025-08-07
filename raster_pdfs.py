import os
from rich.console import Console
import subprocess


def current_dir_at(*args):
    return_str = os.getcwd()
    for item in args:
        return_str = os.path.join(return_str, item)

    return return_str


def raster_pdfs(gs_path: str, logfile_path: str, input_folder: str, output_folder: str, console: Console) -> None:
    nomes_input = os.listdir(input_folder)
    if not nomes_input:
        console.print("[red]Nenhum arquivo encontrado na pasta [/red][bold purple]input")
        console.print("[red]Por favor, adicione arquivos PDF e rode o programa novamente.[/red]")
        input()
        return

    console.print("Arquivos detectados na pasta [bold purple]input")
    for file in nomes_input:
        console.print(file, style="yellow")

    console.print("\nPressione [bold]Enter[/bold] para rasterizar os documentos acima...")
    input()

    open(logfile_path, 'w').close() # Esvazia log antes de converter os pdfs

    with open(logfile_path, 'a') as logfile:
        successfully_converted = 0
        for index, file in enumerate(nomes_input):
            input_file = os.path.join(input_folder, file)
            output_file = os.path.join(output_folder, file)
            command = [
                f"{gs_path}",
                "-dNOPAUSE",
                "-dBATCH",
                "-sDEVICE=pdfimage24",
                "-r1200",
                "-dDownScaleFactor=2",
                f'-o{output_file}',
                f"{input_file}"
            ]

            counter_str = f"[{index + 1} / {len(nomes_input)}]"
            logfile.write(f"\n\n\n\nArquivo {counter_str} -> {file}\n\n\n\n")
            logfile.flush()

            try:
                #subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                subprocess.run(command, check=True, stdout=logfile, stderr=logfile, encoding="cp437")
                
                print_str = f"{counter_str} {file} -> Rasterizado com sucesso"
                console.print(print_str, style="green")
                successfully_converted += 1
            except:
                print_str = f"{counter_str} {file} -> Algo deu errado"
                console.print(print_str, style="red")


    console.print("\nConversão concluída!", style="green")
    if successfully_converted == len(nomes_input):
        console.print("Todos os arquivos foram rasterizados com sucesso!")
    else:
        console.print(f"{successfully_converted} arquivo(s) rasterizado(s) com sucesso, de um total de {len(nomes_input)} arquivo(s)")
    console.print(f"Consultar {logfile_path} para mais detalhes")
    input()
