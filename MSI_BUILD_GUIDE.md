# RGB Control Center - MSI Installer Build Guide

## Overview

This guide explains how to create a professional MSI installer for the RGB Control Center using PyInstaller and WiX Toolset. The MSI installer provides proper Windows integration with Start Menu shortcuts, desktop shortcuts, file associations, and clean uninstallation.

## Prerequisites

### Required Software

1. **Python 3.8+** with pip
   - Download from: https://python.org/downloads/
   - Ensure "Add Python to PATH" is checked during installation

2. **WiX Toolset v3.11** (for MSI creation)
   - Download from: https://wixtoolset.org/releases/
   - Install the main toolset and Visual Studio extension

3. **Visual Studio 2022** (Community Edition is fine)
   - Download from: https://visualstudio.microsoft.com/
   - Required for WiX project building

### Python Dependencies

Install all required packages:

```bash
pip install PyInstaller pygame Pillow numpy requests colorama PyOpenGL PyOpenGL-accelerate moderngl pyinstaller-hooks-contrib
```

## Build Process

### Automated Build (Recommended)

Run the automated build script:

```bash
python build_msi.py
```

This script will:
1. Clean previous builds
2. Check dependencies
3. Build executable with PyInstaller
4. Harvest files for WiX
5. Create MSI installer
6. Package distribution files

### Manual Build Steps

If you prefer manual control:

#### Step 1: Build Executable

```bash
pyinstaller --clean --noconfirm pyinstaller_msi.spec
```

This creates `dist/RGBControlCenter/` folder with the application.

#### Step 2: Generate WiX File List

```bash
cd "C:\Program Files (x86)\WiX Toolset v3.11\bin"
heat.exe dir "path\to\dist\RGBControlCenter" -cg RGBControlCenterFiles -gg -scom -sreg -sfrag -srd -dr INSTALLFOLDER -out "path\to\installer\RGBControlCenterFiles.wxs"
```

#### Step 3: Build MSI

```bash
cd installer
candle.exe *.wxs
light.exe *.wixobj -ext WixUIExtension -out ..\output\RGBControlCenter.msi
```

## File Structure

```
RGB-Control-Center/
├── main.py                          # Main application
├── rgb_controllers/                 # RGB controller modules
├── utils/                          # Utility modules
├── config/                         # Configuration files
├── assets/                         # Icons and images
│   └── icon.ico                    # Application icon
├── installer/                      # WiX installer project
│   ├── Product.wxs                 # Main installer definition
│   ├── RGBControlCenter.wixproj    # WiX project file
│   ├── License.rtf                 # License text
│   └── RGBControlCenterFiles.wxs   # Generated file list
├── pyinstaller_msi.spec           # PyInstaller configuration
├── build_msi.py                   # Automated build script
└── output/                        # Build output
    ├── RGBControlCenter.msi       # MSI installer
    ├── RGBControlCenter_Portable/ # Portable version
    └── INSTALLATION_INSTRUCTIONS.txt
```

## MSI Features

### Installation Features

- **Program Files Installation**: Installs to `C:\Program Files\RGB Control Center\`
- **Start Menu Integration**: Creates Start Menu folder with shortcuts
- **Desktop Shortcut**: Optional desktop shortcut during installation
- **File Associations**: Associates `.rgbprofile` files with the application
- **Registry Entries**: Proper software registration
- **Uninstall Support**: Clean uninstallation through Add/Remove Programs

### User Interface

- **Modern Installer Wizard**: Professional installation experience
- **License Agreement**: Shows license terms
- **Custom Installation Directory**: User can choose install location
- **Progress Indication**: Shows installation progress
- **Finish Options**: Launch application after installation

### System Integration

- **Windows Registry**: Proper application registration
- **Add/Remove Programs**: Shows in Windows program list
- **File Type Association**: Opens `.rgbprofile` files automatically
- **Administrator Rights**: Requests elevation for hardware access

## Troubleshooting

### Common Build Issues

**"WiX Toolset not found"**
- Install WiX Toolset v3.11 from the official website
- Ensure it's added to system PATH

**"PyInstaller import errors"**
- Install missing packages with pip
- Check the `hiddenimports` list in the spec file

**"Icon not found"**
- Place `icon.ico` in the `assets/` folder
- Ensure the icon is a valid ICO format

**"MSI build fails"**
- Check that all WXS files are valid XML
- Ensure no duplicate GUIDs in the installer files

### Runtime Issues

**"This app can't run on your PC"**
- The MSI was built for the correct architecture (x64)
- User has proper Windows version (10/11)

**"Access denied" errors**
- Run the installer as Administrator
- Check Windows Defender isn't blocking installation

**"Missing DLL" errors**
- Install Visual C++ Redistributable
- Check PyInstaller includes all dependencies

## Customization

### Branding

Edit `installer/Product.wxs` to customize:
- Company name and publisher
- Application version
- Product descriptions
- Help and support URLs

### Installation Behavior

Modify `installer/Product.wxs` for:
- Default installation directory
- Shortcut placement
- File associations
- Registry entries

### Application Assets

Replace files in `assets/` folder:
- `icon.ico` - Application icon
- Banner images for installer
- Additional resources

## Distribution

### Testing the MSI

Before distribution:
1. Test installation on clean Windows VM
2. Verify all shortcuts work
3. Test uninstallation is clean
4. Check hardware functionality

### Deployment Options

**Direct Distribution**
- Share the MSI file directly
- Users run as Administrator to install

**Software Distribution**
- Use Group Policy for enterprise deployment
- SCCM/Intune for managed environments

**Code Signing (Recommended)**
- Sign the MSI with a code certificate
- Prevents Windows security warnings
- Builds user trust

## Version Management

### Updating the Application

For new versions:
1. Update version numbers in `pyinstaller_msi.spec`
2. Update version in `installer/Product.wxs`
3. Update UpgradeCode for major versions
4. Rebuild MSI with new version

### Upgrade Behavior

The MSI supports:
- **Minor Updates**: Automatic upgrade installation
- **Major Versions**: Side-by-side or replace installation
- **Rollback**: Windows restore point support

## Security Considerations

### Code Signing

For production distribution:
1. Obtain code signing certificate
2. Sign the executable: `signtool sign /f cert.pfx RGBControlCenter.exe`
3. Sign the MSI: `signtool sign /f cert.pfx RGBControlCenter.msi`

### Hardware Access

The application requires:
- Administrator privileges for hardware control
- Windows security exclusions for RGB protocols
- Firewall exceptions for network RGB devices

## Support and Maintenance

### Log Files

Application logs are stored in:
- `%APPDATA%\RGB Control Center\logs\`
- Windows Event Log (for installer events)

### Common User Issues

**Hardware not detected**
- Install vendor software (MSI Center, Razer Synapse, etc.)
- Run as Administrator
- Check OpenRGB server is running

**Performance issues**
- Update graphics drivers
- Check system requirements
- Disable unnecessary RGB software

### Updates and Patches

For distributing updates:
1. Create patch MSI for minor fixes
2. Full MSI for feature updates
3. Auto-updater integration (future enhancement)

---

This MSI installer provides a professional installation experience for the RGB Control Center, ensuring proper Windows integration and user-friendly distribution.