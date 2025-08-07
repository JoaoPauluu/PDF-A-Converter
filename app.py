import os
from rich.console import Console
from convert_pdfs import convert_pdfs
from raster_pdfs import raster_pdfs



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
    console.print("\n")


    #Define a localização do ghostscript
    gs_path = ''
    if os.path.exists(current_dir_at('ghostscript', 'bin', 'gswin64c.exe')):
        gs_path = current_dir_at('ghostscript', 'bin', 'gswin64c.exe')
        console.print(f"Instalação local do Ghostscript detectada! Utilizando: {gs_path}")
    if not os.path.exists(current_dir_at('ghostscript', 'bin', 'gswin64c.exe')):
        gs_path = 'gswin64c'
        console.print("Instalação local do Ghostscript não detectada. Tentando utilizar instalação do sistema...")

    console.print("\n")
    pass


    input_folder = current_dir_at("input")
    rasters_folder = current_dir_at("rasters")
    output_folder = current_dir_at("output")

    #cria pastas
    if not os.path.exists(input_folder):
        os.mkdir(input_folder)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    if not os.path.exists(rasters_folder):
        os.mkdir(rasters_folder)

    console.print("Escolha o que deseja realizar:")
    console.print("[1] Rasterizar pdfs (input -> rasters)")
    console.print("[2] Converter pdfs rasterizados para pdf/a-2b (rasters -> output)")
    user_input = input()


    if user_input == "1":
        raster_pdfs(gs_path, "log_raster.txt", input_folder, rasters_folder, console)
    elif user_input == "2":
        convert_pdfs(gs_path, "log_conversion.txt", rasters_folder, output_folder, console)
    else:
        console.print("Input inválido!")

if __name__ == "__main__":
    main()