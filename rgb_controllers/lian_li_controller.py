"""
Lian Li Controller for Strimmer cables via L-Connect software
"""

import logging
import subprocess
import json
import os
from typing import Dict, List, Optional


class LianLiController:
    """Controller for Lian Li Strimmer cables via L-Connect"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.l_connect_path = self._find_l_connect()
        
    def _find_l_connect(self) -> Optional[str]:
        """Find L-Connect installation path"""
        possible_paths = [
            r"C:\Program Files (x86)\Lian Li\L-Connect 3\L-Connect 3.exe",
            r"C:\Program Files\Lian Li\L-Connect 3\L-Connect 3.exe",
            r"C:\Program Files (x86)\Lian Li\L-Connect\L-Connect.exe",
            r"C:\Program Files\Lian Li\L-Connect\L-Connect.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        return None
        
    def scan_devices(self) -> List[Dict]:
        """Scan for Lian Li devices"""
        devices = []
        
        if not self.l_connect_path:
            self.logger.warning("L-Connect software not found")
            return devices
            
        # Mock Lian Li devices for now
        # In a real implementation, this would interface with L-Connect API
        lian_li_devices = [
            {
                'name': 'Lian Li Strimmer Plus 24-Pin',
                'type': 'cable',
                'zones': 1,
                'leds': 24
            },
            {
                'name': 'Lian Li Strimmer Plus 8-Pin PCIe',
                'type': 'cable', 
                'zones': 1,
                'leds': 8
            }
        ]
        
        # Check if L-Connect is running
        if self._is_l_connect_running():
            devices.extend(lian_li_devices)
            
        return devices
        
    def _is_l_connect_running(self) -> bool:
        """Check if L-Connect software is running"""
        try:
            # Check if L-Connect process is running
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq L-Connect*'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return 'L-Connect' in result.stdout
        except Exception:
            return False
            
    def apply_settings(self, device_key: str, settings: Dict) -> bool:
        """Apply RGB settings to Lian Li devices"""
        try:
            if not self.l_connect_path:
                self.logger.error("L-Connect software not available")
                return False
                
            color = settings.get('color', (255, 0, 0))
            effect = settings.get('effect', 'static')
            brightness = settings.get('brightness', 100)
            speed = settings.get('speed', 50)
            
            # In a real implementation, this would use L-Connect's API or CLI
            # For now, we'll simulate the command
            command_data = {
                'device': 'strimmer',
                'color': {
                    'r': color[0],
                    'g': color[1], 
                    'b': color[2]
                },
                'effect': effect,
                'brightness': brightness,
                'speed': speed
            }
            
            self.logger.info(f"Applying Lian Li settings: {command_data}")
            
            # Simulate successful application
            # In real implementation, would execute L-Connect commands
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying Lian Li settings: {e}")
            return False
            
    def turn_off_all(self) -> bool:
        """Turn off all Lian Li devices"""
        try:
            if not self.l_connect_path:
                return False
                
            # In real implementation, would send turn-off command to L-Connect
            self.logger.info("Turning off Lian Li devices")
            return True
            
        except Exception as e:
            self.logger.error(f"Error turning off Lian Li devices: {e}")
            return False
            
    def get_supported_effects(self) -> List[str]:
        """Get supported effects for Lian Li devices"""
        return [
            'static',
            'breathing',
            'rainbow',
            'wave',
            'spectrum_cycle',
            'chase',
            'twinkle'
        ]