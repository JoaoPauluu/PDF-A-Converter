from rich.console import Console
import sys
import time
import os
from pathlib import Path

from ghostscript import Ghostscript
import aux_func



def convert_single_pdf(gs: Ghostscript, input_file_path: str, output_file_path: str, temp_folder_path:str) -> bool:
    # note that folder_path + name = file_path

    file_name = os.path.basename(input_file_path)
    temp_file_name = "TEMP - " + file_name
    temp_file_path = os.path.join(temp_folder_path, temp_file_name)

    raster_result = gs.raster_file(input_file_path, temp_file_path)

    if raster_result[0] is False:
        return False
        

    conversion_result = gs.to_pdfa2b(temp_file_path, output_file_path)

    os.remove(temp_file_path)
    if conversion_result[0] is False:
        return False
    
    return True



def main():
    aux_func.print_welcome()


    aux_func.create_folders_cwd("temp", "logs")
    gs = Ghostscript()
    logger = gs.logger



    if len(sys.argv) <= 1:
        logger.error("[bold]Arraste e solte algum arquivo pdf ou pasta contendo pdfs![/bold]")
        time.sleep(4)
        return

    

    temp_folder_path = aux_func.current_dir_at("temp")
    input_uncertain_path = sys.argv[1]

    # single pdf file is provided
    if input_uncertain_path.endswith('.pdf'):

        input_file_path = input_uncertain_path
        root_input_folder_path = os.path.dirname(input_file_path)
        file_name = os.path.basename(input_file_path)


        output_folder_path = root_input_folder_path
        output_file_path = os.path.join(output_folder_path, "CONV - " + file_name)


        logger.info("Convertendo arquivo " + input_file_path)
        logger.warning("Por favor, aguarde a conclusão!")

        if convert_single_pdf(gs, input_file_path, output_file_path, temp_folder_path):
            logger.info(f"[green]Arquivo convertido com sucesso[/green] => {output_file_path}")

        time.sleep(3)

    # folder with multiple pdf files is provided
    else:
        root_input_folder_path = input_uncertain_path
        pdfs_paths = aux_func.get_all_pdfs(root_input_folder_path)
        if not pdfs_paths:
            logger.critical("[bold red]Nenhum arquivo pdf encontrado![/bold red]")
            time.sleep(3)
            return


        logger.info("Pdfs encontrados:")
        for input_file_path in pdfs_paths:
            logger.info(os.path.relpath(input_file_path, root_input_folder_path))

        logger.warning("Precione enter para converter os pdfs acima!")
        input()

        root_input_folder_name = os.path.basename(root_input_folder_path)
        root_output_folder_name = "CONV - " + root_input_folder_name
        root_output_folder_path = os.path.join(os.path.dirname(root_input_folder_path), root_output_folder_name)

        logger.info("Convertendo arquivos:")
        for index, input_file_path in enumerate(pdfs_paths):
            input_file_path_relative = os.path.relpath(input_file_path, root_input_folder_path)
            output_file_path = os.path.join(root_output_folder_path, input_file_path_relative)
            output_folder_path = os.path.dirname(output_file_path)


            os.makedirs(output_folder_path, exist_ok=True)
            conversion_sucess = convert_single_pdf(gs, input_file_path, output_file_path, temp_folder_path)
            if conversion_sucess:
                logger.info(f"[{index + 1} / {len(pdfs_paths)}] {input_file_path_relative} [green]convertido com sucesso![/green]")
            else:
                logger.error(f"[{index + 1} / {len(pdfs_paths)}] {input_file_path_relative} [red]erro ao converter![/red]")

        logger.info(f"[green]Conversão concluída![/green] Arquivos convertidos salvos em {root_output_folder_path}")



if __name__ == "__main__":
    main()