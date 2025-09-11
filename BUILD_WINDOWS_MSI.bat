@echo off
title RGB Control Center - MSI Builder
echo ================================================================
echo RGB Control Center - Professional MSI Builder
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if required packages are installed
echo.
echo 📦 Checking Python packages...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyInstaller not found
    echo Installing required packages...
    python -m pip install --upgrade pip
    python -m pip install PyInstaller pyinstaller-hooks-contrib pygame Pillow numpy requests colorama PyOpenGL PyOpenGL-accelerate moderngl
    if errorlevel 1 (
        echo ❌ Failed to install packages
        pause
        exit /b 1
    )
    echo ✅ Packages installed
) else (
    echo ✅ PyInstaller found
)

REM Check for WiX Toolset
echo.
echo 🔍 Checking for WiX Toolset...
set "WIX_FOUND=0"
if exist "C:\Program Files (x86)\WiX Toolset v3.11\bin\candle.exe" (
    set "WIX_PATH=C:\Program Files (x86)\WiX Toolset v3.11\bin"
    set "WIX_FOUND=1"
    echo ✅ WiX Toolset found at: !WIX_PATH!
) else if exist "C:\Program Files\WiX Toolset v3.11\bin\candle.exe" (
    set "WIX_PATH=C:\Program Files\WiX Toolset v3.11\bin"
    set "WIX_FOUND=1"
    echo ✅ WiX Toolset found at: !WIX_PATH!
) else (
    echo ⚠️ WiX Toolset not found
    echo.
    echo WiX Toolset is required for MSI creation.
    echo Download from: https://wixtoolset.org/releases/
    echo.
    echo Continuing with executable build only...
)

echo.
echo ================================================================
echo Starting Build Process
echo ================================================================

REM Run the Python build script
echo.
echo 🚀 Running automated build script...
python build_msi.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed! Check the error messages above.
    echo.
    echo Common solutions:
    echo • Install missing Python packages
    echo • Install WiX Toolset for MSI creation
    echo • Run as Administrator
    echo • Check that all source files are present
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo Build Complete!
echo ================================================================

REM Check what was created
if exist "output\RGBControlCenter.msi" (
    echo ✅ MSI Installer: output\RGBControlCenter.msi
    for %%I in ("output\RGBControlCenter.msi") do echo    Size: %%~zI bytes
)

if exist "output\RGBControlCenter_Portable" (
    echo ✅ Portable Version: output\RGBControlCenter_Portable\
)

if exist "output\INSTALLATION_INSTRUCTIONS.txt" (
    echo ✅ Instructions: output\INSTALLATION_INSTRUCTIONS.txt
)

echo.
echo 📁 All output files are in the 'output' folder
echo.
echo 🎮 Your RGB Control Center is ready for Windows distribution!
echo.

REM Offer to open output folder
echo.
set /p OPEN_FOLDER="Open output folder? (y/n): "
if /i "%OPEN_FOLDER%"=="y" (
    if exist "output" (
        explorer "output"
    )
)

echo.
echo Press any key to exit...
pause >nul