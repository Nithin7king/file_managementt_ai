@echo off
title SEFS Neural Interface — EXE Builder
color 0A

echo.
echo ============================================================
echo   SEFS — Building Windows .exe Package
echo ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.11 first.
    pause
    exit /b 1
)

:: Install PyInstaller if not present
echo [1/4] Installing PyInstaller...
pip install pyinstaller --quiet

echo.
echo [2/4] Installing project dependencies...
pip install -r requirements.txt --quiet

echo.
echo [3/4] Building SEFS.exe — This may take 5-10 minutes...
echo       (Packaging ML models and dependencies...)
echo.

pyinstaller ^
  --onefile ^
  --windowed ^
  --name "SEFS_Neural_Interface" ^
  --add-data "frontend;frontend" ^
  --add-data "graph_data.json;." ^
  --add-data "security_registry.json;." ^
  --hidden-import="fastembed" ^
  --hidden-import="onnxruntime" ^
  --hidden-import="hdbscan" ^
  --hidden-import="sklearn" ^
  --hidden-import="sumy" ^
  --hidden-import="PyPDF2" ^
  --hidden-import="docx" ^
  --hidden-import="pptx" ^
  --hidden-import="pytesseract" ^
  --hidden-import="flask" ^
  --hidden-import="watchdog" ^
  --hidden-import="tqdm" ^
  --collect-all="fastembed" ^
  --collect-all="onnxruntime" ^
  --collect-all="sumy" ^
  launcher.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed. Check output above for details.
    pause
    exit /b 1
)

echo.
echo [4/4] Packaging complete!
echo ============================================================
echo   Your .exe is at: dist\SEFS_Neural_Interface.exe
echo.
echo   HOW TO DISTRIBUTE:
echo   1. Copy dist\SEFS_Neural_Interface.exe to any Windows PC
echo   2. Double-click to run — browser opens automatically
echo   3. The user does NOT need Python installed
echo ============================================================
echo.
pause
