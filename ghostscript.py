import os
import subprocess
import logging

def current_dir_at(*args):
    return_str = os.getcwd()
    for item in args:
        return_str = os.path.join(return_str, item)
    return return_str

class Ghostscript():
    gs_path:str
    logger:logging.Logger

    def __init__(self):
        self._set_logger()
        self._set_gs_path()
        pass

    def run(self, input_file:str, output_file:str, *gs_parameters:str) -> subprocess.CompletedProcess:
        self.logger.debug(f"Running GS with {gs_parameters}")
        
        command = list(gs_parameters)
        command.insert(0, self.gs_path)
        command.append(f'-o {output_file}')
        command.append(input_file)

        return subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # SHOULD ADD LOGGING

    def raster_file(self, input_file:str, output_file:str, downscale_factor:int=2) -> subprocess.CompletedProcess:
        params = ("-dNOPAUSE",
                    "-dBATCH",
                    "-sDEVICE=pdfimage24",
                    "-r400",
                    f"-dDownScaleFactor={downscale_factor}",)
        return self.run(input_file, output_file, *params)

    def to_pdfa2b(self, input_file:str, output_file:str) -> subprocess.CompletedProcess:
        params = ("-sDEVICE=pdfwrite",
                "-dPDFA=2",
                "-dPDFACompatibilityPolicy=1",
                "-sColorConversionStrategy=UseDeviceIndependentColor",)
        return self.run(input_file, output_file, *params)

    def _set_logger(self, logger:logging.Logger=None):
        if logger:
            self.logger = logger
            return
        
        logger = logging.getLogger('GHOSTSCRIPT')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(name)s] - [%(levelname)s] => %(message)s')

        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger

    def _set_gs_path(self, path=None):
        if path:
            self.gs_path = path
            return
        if os.path.exists(current_dir_at('ghostscript', 'bin', 'gswin64c.exe')):
            gs_path = current_dir_at('ghostscript', 'bin', 'gswin64c.exe')
            self.logger.info(f"Instalação local do Ghostscript detectada! Utilizando: {gs_path}")
        if not os.path.exists(current_dir_at('ghostscript', 'bin', 'gswin64c.exe')):
            gs_path = 'gswin64c'
            self.logger.warning("Instalação local do Ghostscript não detectada. Tentando utilizar instalação do sistema...")