"""
RGB Control Center MSI Builder
Professional MSI installer creation using PyInstaller + WiX Toolset
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

class MSIBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / "dist"
        self.installer_dir = self.root_dir / "installer" 
        self.output_dir = self.root_dir / "output"
        
    def clean_previous_builds(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        
        dirs_to_clean = [
            self.dist_dir,
            self.installer_dir / "bin",
            self.installer_dir / "obj",
            self.output_dir
        ]
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   Cleaned {dir_path}")
        
        # Clean spec files
        for spec_file in self.root_dir.glob("*.spec"):
            if spec_file.name != "pyinstaller_msi.spec":
                spec_file.unlink()
                print(f"   Cleaned {spec_file}")
                
        print("✅ Cleanup complete")
    
    def check_dependencies(self):
        """Check for required tools"""
        print("🔍 Checking dependencies...")
        
        # Check Python packages with correct import names
        required_packages = [
            ("PyInstaller", "PyInstaller"), 
            ("pygame", "pygame"), 
            ("Pillow", "PIL"), 
            ("numpy", "numpy"), 
            ("requests", "requests"), 
            ("colorama", "colorama"), 
            ("PyOpenGL", "OpenGL"), 
            ("moderngl", "moderngl")
        ]
        
        missing_packages = []
        for package_name, import_name in required_packages:
            try:
                __import__(import_name)
                print(f"   ✅ {package_name}")
            except ImportError:
                missing_packages.append(package_name)
                print(f"   ❌ {package_name}")
        
        if missing_packages:
            print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
            print("Install with: pip install " + " ".join(missing_packages))
            return False
            
        # Check WiX Toolset (optional for MSI)
        wix_paths = [
            r"C:\Program Files (x86)\WiX Toolset v3.11\bin\candle.exe",
            r"C:\Program Files\WiX Toolset v3.11\bin\candle.exe",
            r"C:\Tools\WiX\bin\candle.exe"
        ]
        
        wix_found = False
        for path in wix_paths:
            if Path(path).exists():
                print(f"   ✅ WiX Toolset found at {path}")
                self.wix_path = Path(path).parent
                wix_found = True
                break
                
        if not wix_found:
            print("   ⚠️ WiX Toolset not found (optional for MSI creation)")
            print("   📥 Download from: https://wixtoolset.org/releases/")
            self.wix_path = None
        
        print("✅ Dependency check complete")
        return True
    
    def create_assets(self):
        """Create required assets for installer"""
        print("🎨 Creating installer assets...")
        
        assets_dir = self.root_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        # Create simple icon if none exists
        icon_path = assets_dir / "icon.ico"
        if not icon_path.exists():
            print("   Creating default icon...")
            # This would normally create an actual icon file
            # For now, we'll note it needs to be provided
            print("   ⚠️ Please provide icon.ico in assets/ folder")
        
        # Create installer images for WiX
        installer_assets = self.installer_dir / "assets"
        installer_assets.mkdir(exist_ok=True)
        
        if not (installer_assets / "icon.ico").exists() and icon_path.exists():
            shutil.copy2(icon_path, installer_assets / "icon.ico")
            
        print("✅ Assets created")
    
    def build_executable(self):
        """Build executable using PyInstaller"""
        print("🔨 Building executable with PyInstaller...")
        
        try:
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--clean",
                "--noconfirm", 
                "pyinstaller_msi.spec"
            ]
            
            print(f"   Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.root_dir)
            
            if result.returncode == 0:
                exe_path = self.dist_dir / "RGBControlCenter" / "RGBControlCenter.exe"
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    print(f"   ✅ Executable built successfully ({size_mb:.1f} MB)")
                    print(f"   📁 Location: {exe_path}")
                    return True
                else:
                    print("   ❌ Executable not found after build")
                    return False
            else:
                print("   ❌ PyInstaller build failed:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"   ❌ Build error: {e}")
            return False
    
    def harvest_files_for_wix(self):
        """Generate WiX file list using heat.exe"""
        if not self.wix_path:
            print("⚠️ Skipping WiX file harvesting (WiX not found)")
            return False
            
        print("📋 Harvesting files for WiX...")
        
        heat_exe = self.wix_path / "heat.exe"
        dist_folder = self.dist_dir / "RGBControlCenter"
        output_file = self.installer_dir / "RGBControlCenterFiles.wxs"
        
        if not dist_folder.exists():
            print(f"   ❌ Distribution folder not found: {dist_folder}")
            return False
        
        try:
            cmd = [
                str(heat_exe),
                "dir", str(dist_folder),
                "-cg", "RGBControlCenterFiles",
                "-gg",  # Generate GUIDs
                "-scom", "-sreg", "-sfrag", "-srd",  # Suppress various elements
                "-dr", "INSTALLFOLDER",
                "-out", str(output_file)
            ]
            
            print(f"   Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ Files harvested to {output_file}")
                return True
            else:
                print("   ❌ File harvesting failed:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"   ❌ Harvest error: {e}")
            return False
    
    def build_msi(self):
        """Build MSI installer using WiX"""
        if not self.wix_path:
            print("⚠️ Skipping MSI build (WiX not found)")
            return False
            
        print("📦 Building MSI installer...")
        
        candle_exe = self.wix_path / "candle.exe"
        light_exe = self.wix_path / "light.exe"
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
        
        try:
            # Step 1: Compile WiX source files
            print("   Compiling WiX sources...")
            
            wxs_files = list(self.installer_dir.glob("*.wxs"))
            if not wxs_files:
                print("   ❌ No WiX source files found")
                return False
            
            wixobj_files = []
            for wxs_file in wxs_files:
                wixobj_file = self.installer_dir / f"{wxs_file.stem}.wixobj"
                wixobj_files.append(str(wixobj_file))
                
                cmd = [
                    str(candle_exe),
                    str(wxs_file),
                    "-out", str(wixobj_file)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.installer_dir)
                
                if result.returncode != 0:
                    print(f"   ❌ Compilation failed for {wxs_file.name}:")
                    print(result.stderr)
                    return False
                    
            print("   ✅ WiX sources compiled")
            
            # Step 2: Link MSI
            print("   Linking MSI...")
            
            msi_output = self.output_dir / "RGBControlCenter.msi"
            
            cmd = [
                str(light_exe),
                *wixobj_files,
                "-ext", "WixUIExtension",
                "-out", str(msi_output)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.installer_dir)
            
            if result.returncode == 0:
                if msi_output.exists():
                    size_mb = msi_output.stat().st_size / (1024 * 1024)
                    print(f"   ✅ MSI created successfully ({size_mb:.1f} MB)")
                    print(f"   📁 Location: {msi_output}")
                    return True
                else:
                    print("   ❌ MSI file not found after build")
                    return False
            else:
                print("   ❌ MSI linking failed:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"   ❌ MSI build error: {e}")
            return False
    
    def create_distribution_package(self):
        """Create final distribution package"""
        print("📦 Creating distribution package...")
        
        # Copy executable to output
        exe_source = self.dist_dir / "RGBControlCenter"
        exe_dest = self.output_dir / "RGBControlCenter_Portable"
        
        if exe_source.exists():
            if exe_dest.exists():
                shutil.rmtree(exe_dest)
            shutil.copytree(exe_source, exe_dest)
            print(f"   ✅ Portable version: {exe_dest}")
        
        # Create installation instructions
        instructions = self.output_dir / "INSTALLATION_INSTRUCTIONS.txt"
        with open(instructions, 'w') as f:
            f.write("""RGB Control Center - Installation Instructions
==============================================

OPTION 1: MSI Installer (Recommended)
-------------------------------------
1. Run RGBControlCenter.msi as Administrator
2. Follow the installation wizard
3. Launch from Start Menu or Desktop shortcut

OPTION 2: Portable Version
-------------------------
1. Extract RGBControlCenter_Portable folder to desired location
2. Run RGBControlCenter.exe as Administrator

HARDWARE REQUIREMENTS
====================
• Windows 10/11 (64-bit)
• OpenRGB Server (for universal RGB control)
• Vendor software for specific hardware:
  - MSI Center (MSI motherboards)
  - Razer Synapse (Razer peripherals)
  - Vendor-specific software as needed

FIRST RUN SETUP
===============
1. Install and start OpenRGB server
2. Install vendor software for your hardware
3. Run RGB Control Center as Administrator
4. Use "Scan Devices" to detect your RGB hardware
5. Configure your 3D device layout

TROUBLESHOOTING
==============
• Run as Administrator for hardware access
• Ensure OpenRGB is running on localhost:6742
• Check vendor software is installed and running
• Windows Defender may require exclusions

SUPPORT
=======
For support and updates:
GitHub: https://github.com/rgbcontrolcenter

Enjoy your RGB Control Center! 🌈
""")
        
        print(f"   ✅ Instructions created: {instructions}")
        print("✅ Distribution package complete")
    
    def build_all(self):
        """Complete build process"""
        print("🚀 RGB Control Center MSI Builder")
        print("=" * 50)
        
        try:
            # Step 1: Clean previous builds
            self.clean_previous_builds()
            
            # Step 2: Check dependencies
            if not self.check_dependencies():
                return False
            
            # Step 3: Create assets
            self.create_assets()
            
            # Step 4: Build executable
            if not self.build_executable():
                return False
            
            # Step 5: Harvest files for WiX (if available)
            self.harvest_files_for_wix()
            
            # Step 6: Build MSI (if WiX available)
            self.build_msi()
            
            # Step 7: Create distribution package
            self.create_distribution_package()
            
            print("\n" + "=" * 50)
            print("✅ RGB Control Center build complete!")
            print(f"\n📁 Output location: {self.output_dir}")
            
            if (self.output_dir / "RGBControlCenter.msi").exists():
                print("🎯 MSI Installer: RGBControlCenter.msi")
            
            print("📦 Portable Version: RGBControlCenter_Portable/")
            print("📋 Instructions: INSTALLATION_INSTRUCTIONS.txt")
            
            print("\n🎮 Ready for Windows distribution!")
            return True
            
        except Exception as e:
            print(f"\n❌ Build failed: {e}")
            return False

def main():
    """Main entry point"""
    builder = MSIBuilder()
    success = builder.build_all()
    
    if not success:
        print("\n❌ Build failed. Check error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())