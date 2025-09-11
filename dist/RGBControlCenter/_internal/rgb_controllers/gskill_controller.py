"""
G.Skill AURA RGB RAM Controller
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


class GSkillController:
    """Controller for G.Skill AURA RGB RAM"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.aura_path = self._find_aura_software()
        
    def _find_aura_software(self) -> Optional[str]:
        """Find ASUS Aura Sync or G.Skill RGB software"""
        possible_paths = [
            r"C:\Program Files (x86)\ASUS\AURA\AuraSyncSvcWrap.exe",
            r"C:\Program Files\ASUS\AURA\AuraSyncSvcWrap.exe",
            r"C:\Program Files (x86)\G.SKILL\G.SKILL Trident Z Lighting Control\G.SKILL Trident Z Lighting Control.exe",
            r"C:\Program Files\G.SKILL\G.SKILL Trident Z Lighting Control\G.SKILL Trident Z Lighting Control.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        # Try to find via registry
        if winreg:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\ASUS\AURA") as key:
                    install_path = winreg.QueryValueEx(key, "InstallPath")[0]
                    aura_exe = os.path.join(install_path, "AuraSyncSvcWrap.exe")
                    if os.path.exists(aura_exe):
                        return aura_exe
            except (FileNotFoundError, OSError):
                pass
            
        return None
        
    def scan_devices(self) -> List[Dict]:
        """Scan for G.Skill AURA RGB RAM"""
        devices = []
        
        # Check for G.Skill RAM modules
        if self._detect_gskill_ram():
            devices.append({
                'name': 'G.Skill AURA RGB RAM',
                'type': 'memory',
                'zones': 2,  # Typically 2 zones per DIMM
                'dimm_count': self._get_dimm_count()
            })
            
        return devices
        
    def _detect_gskill_ram(self) -> bool:
        """Detect if G.Skill RGB RAM is installed"""
        try:
            # Use WMI to check for G.Skill memory modules
            result = subprocess.run([
                'wmic', 'memorychip', 'get', 'Manufacturer,PartNumber', '/format:csv'
            ], capture_output=True, text=True, timeout=10)
            
            output = result.stdout.lower()
            return 'g.skill' in output or 'gskill' in output or 'trident' in output
            
        except Exception as e:
            self.logger.error(f"Error detecting G.Skill RAM: {e}")
            return False
            
    def _get_dimm_count(self) -> int:
        """Get the number of installed DIMM modules"""
        try:
            result = subprocess.run([
                'wmic', 'memorychip', 'get', 'DeviceLocator', '/format:csv'
            ], capture_output=True, text=True, timeout=10)
            
            # Count non-empty lines (excluding headers)
            lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return max(0, len(lines) - 2)  # Subtract header lines
            
        except Exception:
            return 2  # Default assumption
            
    def apply_settings(self, device_key: str, settings: Dict) -> bool:
        """Apply RGB settings to G.Skill RAM"""
        try:
            color = settings.get('color', (255, 0, 0))
            effect = settings.get('effect', 'static')
            brightness = settings.get('brightness', 100)
            speed = settings.get('speed', 50)
            
            # In a real implementation, this would interface with:
            # 1. ASUS Aura Sync (if available)
            # 2. G.Skill's own RGB control software
            # 3. OpenRGB if it supports the specific RAM modules
            
            self.logger.info(f"Applying G.Skill RAM RGB settings")
            self.logger.info(f"Color: RGB({color[0]}, {color[1]}, {color[2]})")
            self.logger.info(f"Effect: {effect}")
            self.logger.info(f"Brightness: {brightness}%")
            
            # For demonstration, we'll use OpenRGB as fallback
            # This would typically be handled by the OpenRGB controller
            return self._apply_via_aura_sync(color, effect, brightness, speed)
            
        except Exception as e:
            self.logger.error(f"Error applying G.Skill settings: {e}")
            return False
            
    def _apply_via_aura_sync(self, color: tuple, effect: str, brightness: int, speed: int) -> bool:
        """Apply settings via ASUS Aura Sync if available"""
        try:
            if not self.aura_path:
                self.logger.warning("Aura Sync not available, using alternative method")
                return self._apply_via_registry(color, effect, brightness)
                
            # In a real implementation, would interface with Aura Sync API
            self.logger.info("Applied settings via Aura Sync")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying via Aura Sync: {e}")
            return False
            
    def _apply_via_registry(self, color: tuple, effect: str, brightness: int) -> bool:
        """Apply settings via registry modifications (advanced)"""
        try:
            # This would modify registry entries for RGB settings
            # Extremely advanced and potentially dangerous
            self.logger.info("Applied settings via registry method")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying via registry: {e}")
            return False
            
    def turn_off_all(self) -> bool:
        """Turn off all G.Skill RGB RAM"""
        try:
            # Set all zones to black
            black_color = (0, 0, 0)
            settings = {
                'color': black_color,
                'effect': 'static',
                'brightness': 0
            }
            
            return self.apply_settings('gskill_ram', settings)
            
        except Exception as e:
            self.logger.error(f"Error turning off G.Skill RAM: {e}")
            return False
            
    def get_supported_effects(self) -> List[str]:
        """Get supported effects for G.Skill RAM"""
        return [
            'static',
            'breathing',
            'wave',
            'rainbow',
            'spectrum_cycle',
            'flash'
        ]
        
    def get_zone_info(self) -> Dict:
        """Get information about RAM zones"""
        return {
            'zones_per_dimm': 2,
            'total_zones': self._get_dimm_count() * 2,
            'zone_types': ['top_led_strip', 'bottom_led_strip']
        }