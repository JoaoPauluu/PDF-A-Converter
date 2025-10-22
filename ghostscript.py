import os
import subprocess
import logging


from aux_func import current_dir_at

class Ghostscript():
    gs_path:str
    logger:logging.Logger

    def __init__(self):
        self._set_logger()
        self._set_gs_path()
        pass

    def run(self, input_file:str, output_file:str, *gs_parameters:str) -> tuple[bool, subprocess.CompletedProcess] :
        command = list(gs_parameters)
        command.insert(0, self.gs_path)
        command.append(f"-o{output_file}")
        command.append(input_file)

        self.logger.debug(f"Running GS with {command}")

        complete_process = None
        try:
            complete_process = subprocess.run(command, check=True, capture_output=True, text=True) # SHOULD ADD LOGGING
            self.logger.debug(complete_process.stdout)
        except subprocess.CalledProcessError as e:
            self.logger.debug(e.stderr)
            return False, complete_process
        return True, complete_process

    def raster_file(self, input_file:str, output_file:str, downscale_factor:int=2) -> tuple[bool, subprocess.CompletedProcess]:
        params = ("-dNOPAUSE",
                    "-dBATCH",
                    "-sDEVICE=pdfimage24",
                    "-r400",
                    f"-dDownScaleFactor={downscale_factor}",)
        return self.run(input_file, output_file, *params)

    def to_pdfa2b(self, input_file:str, output_file:str) -> tuple[bool, subprocess.CompletedProcess]:
        params = ("-sDEVICE=pdfwrite",
                "-dPDFA=2",
                "-dPDFACompatibilityPolicy=1",
                "-sColorConversionStrategy=UseDeviceIndependentColor",)
        return self.run(input_file, output_file, *params)

    def _set_logger(self, logger:logging.Logger=None):
        from datetime import datetime
        from pathlib import Path
        from rich.logging import RichHandler


        if logger:
            self.logger = logger
            return
        
        logfile_path = Path(current_dir_at("logs", datetime.now().strftime("%Y-%m-%d -- %H-%M-%S") + ".txt"))

        logger = logging.getLogger('GHOSTSCRIPT')
        file_handler = logging.FileHandler(logfile_path)
        console_handler = RichHandler()
        formatter = logging.Formatter('[%(name)s] - [%(levelname)s] => %(message)s')

        logger.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.INFO)

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        self.logger = logger

    def _set_gs_path(self, path=None):
        if path:
            self.gs_path = path
            return
        if os.path.exists(current_dir_at('ghostscript', 'bin', 'gswin64c.exe')):
            gs_path = current_dir_at('ghostscript', 'bin', 'gswin64c.exe')
            self.logger.info(f"Instalação local do Ghostscript detectada!")
            self.gs_path = gs_path
        if not os.path.exists(current_dir_at('ghostscript', 'bin', 'gswin64c.exe')):
            gs_path = 'gswin64c'
            self.logger.warning("Instalação local do Ghostscript não detectada! Tentando utilizar instalação do sistema. Erros podem ocorrer!")
            self.gs_path = gs_path
