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
        raise Exception("Something wrong occurred when rastering the file")
        

    conversion_result = gs.to_pdfa2b(temp_file_path, output_file_path)

    os.remove(temp_file_path)
    if conversion_result[0] is False:
        raise Exception("Something wrong occurred when converting the file")
    
    return True



def main():
    aux_func.print_welcome()


    aux_func.create_folders_cwd("temp", "logs", "output")
    gs = Ghostscript()
    logger = gs.logger



    if len(sys.argv) <= 1:
        logger.error("Arraste e solte algum arquivo pdf ou pasta contendo pdfs!")
        time.sleep(4)
        return

    
    if len(sys.argv) > 1:
        temp_folder_path = aux_func.current_dir_at("temp")

        input_uncertain_path = sys.argv[1]

        # single pdf file is provided
        if input_uncertain_path.endswith('.pdf'):

            input_file_path = input_uncertain_path
            input_folder_path = os.path.dirname(input_file_path)
            file_name = os.path.basename(input_file_path)


            output_folder_path = input_folder_path
            output_file_path = os.path.join(output_folder_path, "CONV - " + file_name)


            logger.info("Convertendo arquivo " + input_file_path)

            if convert_single_pdf(gs, input_file_path, output_file_path, temp_folder_path):
                logger.info(f"Arquivo convertido com sucesso => {output_file_path}")

            time.sleep(3)
            return



        # folder with multiple pdf files is provided
        pdfs_paths = aux_func.get_all_pdfs(input_uncertain_path)
        if not pdfs_paths:
            logger.error("Nenhum arquivo pdf encontrado!")
        for input_file_path in pdfs_paths:
            logger.info(os.path.relpath(input_file_path, input_uncertain_path))

    input()



if __name__ == "__main__":
    main()