import os
import ctypes
from rich.console import Console

#from dotenv import load_dotenv


def current_dir_at(*args):
    return_str = os.getcwd()
    for item in args:
        return_str = os.path.join(return_str, item)

    return return_str


def main() -> None:
    os.environ['GHOSTSCRIPT_DLL'] = current_dir_at('ghostscript', 'bin', 'gsdll64.dll')
    import ghostscript

    console = Console()

    #Bem-vindo
    console.print("\n\n")
    console.print("Conversor de PDF para PDF/A-2b", style="bold green")
    console.print("Script feito por:", style="bold") 
    console.print("João Paulo Chiari de Gasperi", style="bold green")
    console.print("\n\n")

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

    pda_def_file = current_dir_at("PDFA_def.ps")
    color_file = current_dir_at("AdobeRGB1998.icc")
    for file in nomes_input:
        input_file = current_dir_at('input', file)
        output_file = current_dir_at('output', file)
        args = [
            "gs",
            "-dPDFA=2",
            #"-dBATCH",
            #"-dNOPAUSE",
            "-sDEVICE=pdfwrite",
            #"-sProcessColorModel=DeviceRGB",
            "-sColorConversionStrategy=RGB",
            "-sPDFACompatibilityPolicy=1",
            f'-sOutputFile={output_file}',
            f"--permit-file-read={color_file}"
            f'{pda_def_file}',
            f'{input_file}'
        ]

        console.print(input_file)
        console.print(output_file)
        #command_string = ' '.join(args).encode('utf-8')
        #console.print(command_string)
        try:
            ghostscript.Ghostscript(*args)
            console.print(file + " -> Sucesso", style="green")
        except:
            console.print(file + " -> Algo deu errado", style="red")
            


if __name__ == '__main__':
    main()