@echo off

REM --- Set the path to your Ghostscript executable ---
set GS_EXE="./Ghostscript/bin/gswin64c.exe"

REM --- Set your input and output files ---
set INPUT_PDF="input.pdf"
set OUTPUT_PDF="output.pdf"
set PDFA_DEF="PDFA_def.ps"

REM --- Run the Ghostscript command ---
%GS_EXE% -dPDFA=2 -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=%OUTPUT_PDF% %PDFA_DEF% %INPUT_PDF%

echo.

pause