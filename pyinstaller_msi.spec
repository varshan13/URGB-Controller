# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file optimized for MSI packaging
# Creates one-folder distribution for easier MSI integration

import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        # Include any additional DLLs if needed
    ],
    datas=[
        ('rgb_controllers', 'rgb_controllers'),
        ('utils', 'utils'),
        ('config', 'config'),
        ('assets', 'assets'),  # If you have icons/images
    ],
    hiddenimports=[
        # Core GUI imports
        'tkinter',
        'tkinter.ttk',
        'tkinter.colorchooser',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        
        # Graphics and visualization
        'pygame',
        'pygame.locals',
        'pygame.constants',
        'OpenGL',
        'OpenGL.GL',
        'OpenGL.GLU',
        'OpenGL.arrays',
        'OpenGL_accelerate',
        'moderngl',
        'moderngl.context',
        
        # Image processing
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'Pillow',
        
        # Scientific computing
        'numpy',
        'numpy.core',
        'numpy.core.multiarray',
        
        # Network and API
        'requests',
        'requests.adapters',
        'urllib3',
        'http.client',
        'socket',
        
        # RGB Controller dependencies
        'colorama',
        'colorama.ansi',
        'colorama.win32',
        
        # System and utilities
        'threading',
        'json',
        'logging',
        'subprocess',
        'time',
        'math',
        'dataclasses',
        'typing',
        'datetime',
        'os',
        'sys',
        'pathlib',
        'platform',
        'ctypes',
        'ctypes.wintypes',
        
        # Windows-specific
        'winreg',
        'winsound',
        
        # Potential missing imports
        'pkg_resources',
        'pkg_resources.py2_warn',
        'encodings.idna',
        'encodings.utf_8',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary packages to reduce size
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'notebook',
        'qtpy',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx',
        'kivy',
        'django',
        'flask',
        'tornado',
        'twisted',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create ONE-FOLDER distribution (easier for MSI packaging)
exe = EXE(
    pyz,
    a.scripts,
    [],  # Empty - we want onedir, not onefile
    exclude_binaries=True,
    name='RGBControlCenter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Windows app, not console
    disable_windowed_traceback=False,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

# Collect all files into dist/RGBControlCenter/ folder
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RGBControlCenter',  # This creates dist/RGBControlCenter/ folder
)

# Add version info for Windows
version_info = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'RGB Gaming Solutions'),
            StringStruct(u'FileDescription', u'RGB Control Center'),
            StringStruct(u'FileVersion', u'1.0.0.0'),
            StringStruct(u'InternalName', u'RGBControlCenter'),
            StringStruct(u'LegalCopyright', u'Copyright (c) 2025 RGB Gaming Solutions'),
            StringStruct(u'OriginalFilename', u'RGBControlCenter.exe'),
            StringStruct(u'ProductName', u'RGB Control Center'),
            StringStruct(u'ProductVersion', u'1.0.0.0'),
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''

# Apply version info to executable
if hasattr(exe, 'version'):
    exe.version = version_info