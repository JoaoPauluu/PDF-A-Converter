import os
from rich.console import Console
import subprocess


def current_dir_at(*args):
    return_str = os.getcwd()
    for item in args:
        return_str = os.path.join(return_str, item)

    return return_str


def convert_pdfs(gs_path: str, logfile_path: str, input_folder: str, output_folder: str, console: Console) -> None:
# Collect all files recursively
    all_files = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".pdf"):  # Only convert PDFs
                all_files.append(os.path.join(root, file))

    if not all_files:
        console.print("[red]Nenhum arquivo PDF encontrado na pasta [/red][bold purple]rasters")
        console.print("[red]Por favor, adicione ou rasterize arquivos PDF e rode o programa novamente.[/red]")
        input()
        return

    console.print("Arquivos detectados na pasta [bold purple]input")
    for file in all_files:
        console.print(os.path.relpath(file, input_folder), style="yellow")

    console.print("\nPressione [bold]Enter[/bold] para converter os documentos acima...")
    input()

    # Empty logfile before converting
    open(logfile_path, 'w').close()

    with open(logfile_path, 'a', encoding="utf-8") as logfile:
        successfully_converted = 0
        for index, input_file in enumerate(all_files, start=1):
            # Preserve subfolder structure
            relative_path = os.path.relpath(input_file, input_folder)
            output_file = os.path.join(output_folder, relative_path)

            # Ensure output subfolder exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            command = [
                gs_path,
                "-sDEVICE=pdfwrite",
                "-dPDFA=2",
                "-dPDFACompatibilityPolicy=1",
                "-sColorConversionStrategy=UseDeviceIndependentColor",
                f'-o{output_file}',
                "-f",
                input_file
            ]

            counter_str = f"[{index} / {len(all_files)}]"
            logfile.write(f"\n\n\n\nArquivo {counter_str} -> {relative_path}\n\n\n\n")
            logfile.flush()

            try:
                subprocess.run(command, check=True, stdout=logfile, stderr=logfile, encoding="cp437")

                print_str = f"{counter_str} {relative_path} -> Convertido com sucesso"
                console.print(print_str, style="green")
                successfully_converted += 1
            except Exception as e:
                print_str = f"{counter_str} {relative_path} -> Algo deu errado"
                console.print(print_str, style="red")
                logfile.write(f"\nErro: {e}\n")

    console.print(f"\n[bold green]{successfully_converted}[/bold green] arquivos convertidos com sucesso de um total de {len(all_files)}.")
    console.print(f"Consultar {logfile_path} para mais detalhes")
    input()
