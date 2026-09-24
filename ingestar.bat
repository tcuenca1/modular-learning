@echo off
setlocal
chcp 65001 >nul

echo =======================================================
echo  INGESTA INTELIGENTE DE MATERIAL DE ESTUDIO (GEMINI)
echo =======================================================

if "%~1"=="" (
    echo [ERROR] Por favor, arrastra un archivo PDF o documento sobre este archivo .bat.
    echo.
    pause
    exit /b 1
)

:: Forzar a la consola a usar la carpeta raíz del proyecto
cd /d "%~dp0"

:: Llamar al script de ingestión con el archivo arrastrado
python tools/ingestar_material.py "%~1"

echo.
pause
endlocal
