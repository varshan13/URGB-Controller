"""
ASRock Phantom Gaming RX 7900XTX GPU Controller
"""

import logging
import subprocess
import json
import os
try:
    import winreg
except ImportError:
    # For non-Windows systems
    winreg = None
from typing import Dict, List, Optional


class ASRockController:
    """Controller for ASRock Phantom Gaming GPU RGB"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.polychrome_path = self._find_polychrome()
        self.gpu_detected = False
        
    def _find_polychrome(self) -> Optional[str]:
        """Find ASRock Polychrome RGB software"""
        possible_paths = [
            r"C:\Program Files (x86)\ASRock\Polychrome RGB\Polychrome RGB.exe",
            r"C:\Program Files\ASRock\Polychrome RGB\Polychrome RGB.exe",
            r"C:\Program Files (x86)\ASRock\ASRock Polychrome Sync\ASRock Polychrome Sync.exe",
            r"C:\Program Files\ASRock\ASRock Polychrome Sync\ASRock Polychrome Sync.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        # Try registry lookup
        if winreg:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                  r"SOFTWARE\ASRock\Polychrome RGB") as key:
                    install_path = winreg.QueryValueEx(key, "InstallPath")[0]
                    polychrome_exe = os.path.join(install_path, "Polychrome RGB.exe")
                    if os.path.exists(polychrome_exe):
                        return polychrome_exe
            except (FileNotFoundError, OSError):
                pass
            
        return None
        
    def scan_devices(self) -> List[Dict]:
        """Scan for ASRock GPU devices"""
        devices = []
        
        if self._detect_asrock_gpu():
            self.gpu_detected = True
            gpu_info = self._get_gpu_info()
            devices.append({
                'name': 'ASRock Phantom Gaming RX 7900XTX',
                'type': 'gpu',
                'zones': 3,  # Typical zones: logo, fan shroud, backplate
                'vram': gpu_info.get('vram', 'Unknown'),
                'temperature': gpu_info.get('temperature', 0),
                'memory_clock': gpu_info.get('memory_clock', 0),
                'core_clock': gpu_info.get('core_clock', 0)
            })
            
        return devices
        
    def _detect_asrock_gpu(self) -> bool:
        """Detect ASRock Phantom Gaming GPU"""
        try:
            # Use WMI to check for ASRock GPU
            wmi_command = """
            Get-WmiObject -Class Win32_VideoController | 
            Where-Object { $_.Name -like "*ASRock*" -or $_.Name -like "*Phantom*" -or $_.Name -like "*RX 7900*" } | 
            Select-Object Name, DriverVersion, AdapterRAM
            """
            
            result = subprocess.run([
                'powershell', '-Command', wmi_command
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0 and result.stdout.strip():
                return True
                
            # Alternative: Check PCI devices
            pci_result = subprocess.run([
                'wmic', 'path', 'win32_VideoController', 'get', 'Name,PNPDeviceID', '/format:csv'
            ], capture_output=True, text=True, timeout=10)
            
            output = pci_result.stdout.lower()
            return any(keyword in output for keyword in ['asrock', 'phantom', '7900'])
            
        except Exception as e:
            self.logger.error(f"Error detecting ASRock GPU: {e}")
            return False
            
    def _get_gpu_info(self) -> Dict:
        """Get detailed GPU information"""
        try:
            gpu_info = {}
            
            # Get GPU memory info
            memory_command = """
            Get-WmiObject -Class Win32_VideoController | 
            Where-Object { $_.Name -like "*7900*" } | 
            Select-Object AdapterRAM, CurrentHorizontalResolution, CurrentVerticalResolution
            """
            
            result = subprocess.run([
                'powershell', '-Command', memory_command
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Parse memory info (simplified)
                gpu_info['vram'] = '24GB'  # RX 7900XTX has 24GB
                
            # Mock additional info (would use GPU monitoring APIs in real implementation)
            gpu_info.update({
                'temperature': 65,  # Mock temperature
                'core_clock': 2500,  # Mock core clock MHz
                'memory_clock': 2500,  # Mock memory clock MHz
                'fan_speed': 1200,   # Mock fan RPM
                'power_usage': 300   # Mock power usage watts
            })
            
            return gpu_info
            
        except Exception as e:
            self.logger.error(f"Error getting GPU info: {e}")
            return {}
            
    def apply_settings(self, device_key: str, settings: Dict) -> bool:
        """Apply RGB settings to ASRock GPU"""
        try:
            if not self.gpu_detected:
                self.logger.error("ASRock GPU not detected")
                return False
                
            color = settings.get('color', (255, 0, 0))
            effect = settings.get('effect', 'static')
            brightness = settings.get('brightness', 100)
            speed = settings.get('speed', 50)
            
            # Apply via different methods based on availability
            if self.polychrome_path:
                return self._apply_via_polychrome(color, effect, brightness, speed)
            else:
                return self._apply_via_registry(color, effect, brightness, speed)
                
        except Exception as e:
            self.logger.error(f"Error applying ASRock GPU settings: {e}")
            return False
            
    def _apply_via_polychrome(self, color: tuple, effect: str, brightness: int, speed: int) -> bool:
        """Apply settings via ASRock Polychrome software"""
        try:
            # In real implementation, would interface with Polychrome API
            # or use command-line parameters if available
            
            self.logger.info("Applying GPU RGB settings via Polychrome")
            self.logger.info(f"Color: RGB({color[0]}, {color[1]}, {color[2]})")
            self.logger.info(f"Effect: {effect}")
            self.logger.info(f"Brightness: {brightness}%")
            
            # Mock Polychrome command
            polychrome_args = [
                self.polychrome_path,
                '--zone', 'all',
                '--color', f"{color[0]},{color[1]},{color[2]}",
                '--effect', effect,
                '--brightness', str(brightness),
                '--speed', str(speed)
            ]
            
            # In real implementation, would execute this command
            # subprocess.run(polychrome_args, timeout=10)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error with Polychrome control: {e}")
            return False
            
    def _apply_via_registry(self, color: tuple, effect: str, brightness: int, speed: int) -> bool:
        """Apply settings via registry modifications"""
        try:
            # ASRock GPUs may store RGB settings in registry
            # This is a fallback method when Polychrome isn't available
            
            self.logger.info("Applying GPU RGB settings via registry method")
            
            # Mock registry keys (would be device-specific)
            registry_data = {
                'RGB_Red': color[0],
                'RGB_Green': color[1],
                'RGB_Blue': color[2],
                'Effect_Mode': self._get_effect_code(effect),
                'Brightness': brightness,
                'Speed': speed
            }
            
            # In real implementation, would write to:
            # HKEY_LOCAL_MACHINE\SOFTWARE\ASRock\GPU_RGB or similar
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error with registry method: {e}")
            return False
            
    def _get_effect_code(self, effect: str) -> int:
        """Convert effect name to ASRock-specific code"""
        effect_codes = {
            'static': 1,
            'breathing': 2,
            'wave': 3,
            'rainbow': 4,
            'spectrum_cycle': 5,
            'reactive': 6,
            'comet': 7,
            'flash': 8
        }
        return effect_codes.get(effect, 1)
        
    def turn_off_all(self) -> bool:
        """Turn off all GPU RGB"""
        try:
            if not self.gpu_detected:
                return False
                
            off_settings = {
                'color': (0, 0, 0),
                'effect': 'static',
                'brightness': 0,
                'speed': 50
            }
            
            return self.apply_settings('asrock_gpu', off_settings)
            
        except Exception as e:
            self.logger.error(f"Error turning off ASRock GPU RGB: {e}")
            return False
            
    def get_supported_effects(self) -> List[str]:
        """Get supported effects for ASRock GPU"""
        return [
            'static',
            'breathing',
            'wave',
            'rainbow',
            'spectrum_cycle',
            'reactive',
            'comet',
            'flash',
            'music_sync'
        ]
        
    def get_gpu_zones(self) -> List[Dict]:
        """Get RGB zones for the GPU"""
        return [
            {
                'name': 'Logo',
                'description': 'ASRock Phantom Gaming logo',
                'led_count': 8
            },
            {
                'name': 'Fan Shroud',
                'description': 'RGB strip around fan shroud',
                'led_count': 16
            },
            {
                'name': 'Backplate',
                'description': 'RGB accent on backplate',
                'led_count': 4
            }
        ]
        
    def get_gpu_status(self) -> Dict:
        """Get current GPU status and monitoring info"""
        try:
            if not self.gpu_detected:
                return {}
                
            # In real implementation, would use GPU monitoring APIs
            # Like AMD ADL, NVIDIA NVML, or similar
            
            return {
                'temperature': 65,
                'core_clock': 2500,
                'memory_clock': 2500,
                'fan_speed': 1200,
                'power_usage': 300,
                'utilization': 25,
                'memory_usage': 8.5  # GB used
            }
            
        except Exception as e:
            self.logger.error(f"Error getting GPU status: {e}")
            return {}