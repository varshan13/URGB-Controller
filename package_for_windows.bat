@echo off
echo RGB Control Center - Windows Packaging Script
echo ============================================

echo.
echo Installing PyInstaller and dependencies...
python -m pip install --upgrade pip
python -m pip install pyinstaller pyinstaller-hooks-contrib

echo.
echo Building Windows executable...
python build_exe.py

echo.
echo Build complete! Check the dist folder for RGBControlCenter.exe
pause