"""
Build script for creating RGB Control Center Windows executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_files():
    """Clean previous build files"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name} directory")
    
    for pattern in files_to_clean:
        for file_path in Path('.').glob(pattern):
            file_path.unlink()
            print(f"Cleaned {file_path}")

def create_spec_file():
    """Create PyInstaller spec file for RGB Control Center"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('rgb_controllers', 'rgb_controllers'),
        ('utils', 'utils'),
        ('config', 'config'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.colorchooser',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'pygame',
        'pygame.locals',
        'OpenGL',
        'OpenGL.GL',
        'OpenGL.GLU',
        'OpenGL_accelerate',
        'pkg_resources.py2_warn',
        'requests',
        'colorama',
        'numpy',
        'pillow',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'moderngl',
        'glcontext',
        'threading',
        'json',
        'logging',
        'subprocess',
        'socket',
        'time',
        'math',
        'dataclasses',
        'typing',
        'datetime',
        'os',
        'sys'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'IPython'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RGBControlCenter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    icon=None,  # Add icon path here if you have one
    version_file=None,
)
'''
    
    with open('RGBControlCenter.spec', 'w') as f:
        f.write(spec_content)
    print("Created RGBControlCenter.spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        print("\\nBuilding RGB Control Center executable...")
        print("This may take several minutes...")
        
        # Use the spec file for building
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'RGBControlCenter.spec'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("\\n✅ Build successful!")
            print("\\nExecutable location: dist/RGBControlCenter.exe")
            
            # Check file size
            exe_path = Path('dist/RGBControlCenter.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"Executable size: {size_mb:.1f} MB")
            
        else:
            print("\\n❌ Build failed!")
            print("\\nError output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"\\n❌ Build error: {e}")
        return False
    
    return True

def create_installer_info():
    """Create installation instructions"""
    instructions = '''
# RGB Control Center - Windows Installation

## What You Get
- RGBControlCenter.exe - Standalone executable (no Python required)
- Complete RGB control for gaming hardware
- 3D interface for device placement
- Profile management and lighting effects

## Installation Steps
1. Copy RGBControlCenter.exe to your desired location (e.g., C:\\Program Files\\RGB Control Center\\)
2. Create a desktop shortcut (optional)
3. Run as Administrator for full hardware access

## Requirements
- Windows 10/11 (64-bit)
- OpenRGB Server (for universal RGB control)
- Vendor software (MSI Center, Razer Synapse, etc.) for full hardware support

## Supported Hardware
- ARGB Fans (via OpenRGB)
- MSI Motherboards (Mystic Light)
- Lian Li Strimmer Cables
- G.Skill AURA RGB RAM
- Evofox Ronin Keyboard
- Razer Basilisk Mouse
- ASRock Phantom Gaming GPU

## First Run
1. Install OpenRGB and start the server
2. Install vendor software for your specific hardware
3. Run RGB Control Center as Administrator
4. Use "Scan Devices" to detect your hardware
5. Open 3D View to set up your device layout

## Troubleshooting
- Run as Administrator for device access
- Ensure OpenRGB server is running (localhost:6742)
- Check vendor software is installed and running
- Windows Defender may need exclusion for RGB control
'''
    
    with open('dist/INSTALLATION_GUIDE.txt', 'w') as f:
        f.write(instructions)
    print("Created installation guide")

def main():
    """Main build process"""
    print("🚀 RGB Control Center - Windows Executable Builder")
    print("=" * 50)
    
    # Step 1: Clean previous builds
    print("\\n1. Cleaning previous build files...")
    clean_build_files()
    
    # Step 2: Create spec file
    print("\\n2. Creating PyInstaller configuration...")
    create_spec_file()
    
    # Step 3: Build executable
    print("\\n3. Building executable...")
    if build_executable():
        # Step 4: Create installation guide
        print("\\n4. Creating installation guide...")
        create_installer_info()
        
        print("\\n" + "=" * 50)
        print("✅ RGB Control Center executable ready!")
        print("\\n📁 Output location: dist/RGBControlCenter.exe")
        print("📄 Installation guide: dist/INSTALLATION_GUIDE.txt")
        print("\\n🎮 Ready for Windows installation!")
        
    else:
        print("\\n❌ Build failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())