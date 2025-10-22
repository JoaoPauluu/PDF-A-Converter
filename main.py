from rich.console import Console
import sys
import time
import os

from ghostscript import Ghostscript
import aux_func



def main():
    aux_func.print_welcome()


    aux_func.create_folders_cwd("temp", "logs", "output")
    gs = Ghostscript()
    logger = gs.logger



    if len(sys.argv) <= 1:
        logger.error("Nenhum Argumento! Arraste e solte algum arquivo!")
        time.sleep(2)
        return

    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if input_path.endswith('.pdf'):
            # single file is provided
            logger.info("Convertendo arquivo " + input_path)
            gs.
            return


        pdfs_paths = aux_func.get_all_pdfs(input_path)
        if not pdfs_paths:
            logger.error("Nenhum arquivo pdf encontrado!")
        for pdf_path in pdfs_paths:
            logger.info(os.path.relpath(pdf_path, input_path))

    input()



if __name__ == "__main__":
    main()