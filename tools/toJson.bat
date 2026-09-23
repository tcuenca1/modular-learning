@echo off
setlocal

echo INICIANDO EXTRACCION DE SILABO
echo ========================================

if "%~1"=="" (
    echo ERROR: Arrastra un archivo PDF del silabo sobre este .bat.
    echo.
    pause
    exit /b 1
)

:: Forzar a la consola a usar la carpeta donde esta guardado este .bat
cd /d "%~dp0"

:: Llamamos al script de Python pasandole el archivo arrastrado
py -3.14 extraer_silabo.py "%~1"

echo.
pause
endlocal