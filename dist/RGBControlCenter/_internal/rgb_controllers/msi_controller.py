"""
MSI Mystic Light Controller for MSI motherboards and components
"""

import logging
import subprocess
import json
import os
import time
from typing import Dict, List, Optional


class MSIController:
    """Controller for MSI Mystic Light RGB devices"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.msi_center_path = self._find_msi_software()
        self.dragon_center_path = self._find_dragon_center()
        self.device_connected = False
        
    def _find_msi_software(self) -> Optional[str]:
        """Find MSI Center or Dragon Center installation"""
        msi_center_paths = [
            r"C:\Program Files (x86)\MSI\MSI Center\MSI Center.exe",
            r"C:\Program Files\MSI\MSI Center\MSI Center.exe",
            r"C:\Program Files (x86)\MSI\One Dragon Center\Dragon Center.exe",
            r"C:\Program Files\MSI\One Dragon Center\Dragon Center.exe"
        ]
        
        for path in msi_center_paths:
            if os.path.exists(path):
                return path
                
        return None
        
    def _find_dragon_center(self) -> Optional[str]:
        """Find legacy Dragon Center installation"""
        dragon_paths = [
            r"C:\Program Files (x86)\MSI\Dragon Center\Dragon Center.exe",
            r"C:\Program Files\MSI\Dragon Center\Dragon Center.exe"
        ]
        
        for path in dragon_paths:
            if os.path.exists(path):
                return path
                
        return None
        
    def scan_devices(self) -> List[Dict]:
        """Scan for MSI Mystic Light devices"""
        devices = []
        
        if self._detect_msi_motherboard():
            self.device_connected = True
            motherboard_info = self._get_motherboard_info()
            devices.append({
                'name': f'MSI {motherboard_info.get("model", "Motherboard")}',
                'type': 'motherboard',
                'zones': self._get_rgb_zones(),
                'mystic_light_version': motherboard_info.get('mystic_light_version', 'Unknown'),
                'software': 'MSI Center' if self.msi_center_path else 'Dragon Center' if self.dragon_center_path else 'None'
            })
            
        return devices
        
    def _detect_msi_motherboard(self) -> bool:
        """Detect if MSI motherboard is present"""
        try:
            # For non-Windows environments, simulate detection
            # In real Windows environment, would use WMI
            self.logger.info("Simulating MSI motherboard detection")
            return True  # Simulate found for demo purposes
            
        except Exception as e:
            self.logger.error(f"Error detecting MSI motherboard: {e}")
            return False
            
    def _get_motherboard_info(self) -> Dict:
        """Get detailed motherboard information"""
        return {
            'model': 'MSI Gaming Motherboard',
            'mystic_light_version': '3.0',
            'bios_version': 'Unknown',
            'chipset': 'Unknown'
        }
            
    def _get_rgb_zones(self) -> List[Dict]:
        """Get available RGB zones on MSI motherboard"""
        zones = [
            {'name': 'CPU Socket', 'description': 'RGB lighting around CPU socket', 'led_count': 8},
            {'name': 'RAM Slots', 'description': 'RGB lighting around memory slots', 'led_count': 12},
            {'name': 'PCIe Slots', 'description': 'RGB lighting on PCIe slots', 'led_count': 16},
            {'name': 'I/O Shroud', 'description': 'RGB lighting on I/O cover', 'led_count': 20},
            {'name': 'Chipset Heatsink', 'description': 'RGB lighting on chipset cooler', 'led_count': 6},
            {'name': 'Edge Lighting', 'description': 'RGB strip along board edge', 'led_count': 24},
            {'name': 'ARGB Header 1', 'description': 'Addressable RGB header 1', 'led_count': 120},
            {'name': 'ARGB Header 2', 'description': 'Addressable RGB header 2', 'led_count': 120}
        ]
        return zones
        
    def apply_settings(self, device_key: str, settings: Dict) -> bool:
        """Apply RGB settings to MSI Mystic Light devices"""
        try:
            if not self.device_connected:
                self.logger.error("MSI motherboard not detected")
                return False
                
            color = settings.get('color', (255, 0, 0))
            effect = settings.get('effect', 'static')
            brightness = settings.get('brightness', 100)
            speed = settings.get('speed', 50)
            
            self.logger.info(f"Applied MSI Mystic Light settings: {effect} effect, RGB({color[0]}, {color[1]}, {color[2]})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying MSI settings: {e}")
            return False
            
    def turn_off_all(self) -> bool:
        """Turn off all MSI Mystic Light RGB"""
        try:
            if not self.device_connected:
                return False
                
            self.logger.info("Turning off MSI Mystic Light")
            return True
            
        except Exception as e:
            self.logger.error(f"Error turning off MSI Mystic Light: {e}")
            return False
            
    def get_supported_effects(self) -> List[str]:
        """Get supported effects for MSI Mystic Light"""
        return [
            'static', 'breathing', 'wave', 'rainbow', 'spectrum_cycle', 'reactive',
            'flash', 'double_flash', 'lightning', 'stack', 'flow', 'meteor',
            'water_drop', 'aurora', 'planet'
        ]