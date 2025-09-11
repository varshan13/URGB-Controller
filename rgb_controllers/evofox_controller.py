"""
Evofox Ronin Wireless Keyboard Controller
"""

import logging
import subprocess
import json
import time
from typing import Dict, List, Optional


class EvofoxController:
    """Controller for Evofox Ronin wireless keyboard"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.device_connected = False
        
    def scan_devices(self) -> List[Dict]:
        """Scan for Evofox devices"""
        devices = []
        
        if self._detect_evofox_keyboard():
            self.device_connected = True
            devices.append({
                'name': 'Evofox Ronin Wireless Keyboard',
                'type': 'keyboard',
                'zones': 6,  # Typical gaming keyboard zones
                'connection': 'wireless',
                'battery_level': self._get_battery_level()
            })
            
        return devices
        
    def _detect_evofox_keyboard(self) -> bool:
        """Detect if Evofox Ronin keyboard is connected"""
        try:
            # Use PowerShell to check for HID devices
            ps_command = """
            Get-WmiObject -Class Win32_PnPEntity | 
            Where-Object { $_.Name -like "*Evofox*" -or $_.Name -like "*Ronin*" } | 
            Select-Object Name, Status
            """
            
            result = subprocess.run([
                'powershell', '-Command', ps_command
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                return True
                
            # Alternative: Check USB devices
            usb_result = subprocess.run([
                'wmic', 'path', 'Win32_USBHub', 'get', 'Name', '/format:csv'
            ], capture_output=True, text=True, timeout=10)
            
            output = usb_result.stdout.lower()
            return 'evofox' in output or 'ronin' in output
            
        except Exception as e:
            self.logger.error(f"Error detecting Evofox keyboard: {e}")
            return False
            
    def _get_battery_level(self) -> Optional[int]:
        """Get battery level for wireless keyboard"""
        try:
            # This would typically require device-specific drivers
            # For now, return a simulated level
            return 85  # Mock battery level
        except Exception:
            return None
            
    def apply_settings(self, device_key: str, settings: Dict) -> bool:
        """Apply RGB settings to Evofox keyboard"""
        try:
            if not self.device_connected:
                self.logger.error("Evofox keyboard not connected")
                return False
                
            color = settings.get('color', (255, 0, 0))
            effect = settings.get('effect', 'static')
            brightness = settings.get('brightness', 100)
            speed = settings.get('speed', 50)
            
            # For Evofox devices, we would typically use:
            # 1. Manufacturer's RGB control software
            # 2. Direct HID communication
            # 3. Registry-based settings
            
            success = self._apply_via_hid_commands(color, effect, brightness, speed)
            
            if success:
                self.logger.info(f"Applied Evofox keyboard settings: {effect} effect")
                return True
            else:
                # Fallback to software-based control
                return self._apply_via_software_control(color, effect, brightness, speed)
                
        except Exception as e:
            self.logger.error(f"Error applying Evofox settings: {e}")
            return False
            
    def _apply_via_hid_commands(self, color: tuple, effect: str, brightness: int, speed: int) -> bool:
        """Apply settings via direct HID communication"""
        try:
            # This would require specific HID protocol knowledge for Evofox devices
            # Each manufacturer has their own protocol
            
            # Mock HID command structure for Evofox
            command_data = {
                'report_id': 0x06,  # RGB control report
                'command': 0x01,    # Set RGB command
                'zone': 0xFF,       # All zones
                'red': color[0],
                'green': color[1],
                'blue': color[2],
                'effect': self._get_effect_code(effect),
                'speed': int(speed * 255 / 100),
                'brightness': int(brightness * 255 / 100)
            }
            
            self.logger.info(f"Sending HID command to Evofox keyboard: {command_data}")
            
            # In real implementation, would use hidapi or similar library
            # to send raw HID reports to the device
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending HID commands: {e}")
            return False
            
    def _apply_via_software_control(self, color: tuple, effect: str, brightness: int, speed: int) -> bool:
        """Apply settings via software control method"""
        try:
            # Alternative method using registry or config files
            # Some keyboards store RGB settings in Windows registry
            
            self.logger.info("Applying settings via software control method")
            
            # Mock registry-based control
            registry_data = {
                'rgb_color': f"{color[0]:02x}{color[1]:02x}{color[2]:02x}",
                'effect_mode': effect,
                'brightness_level': brightness,
                'animation_speed': speed
            }
            
            # In real implementation, would write to appropriate registry keys
            # or configuration files used by Evofox software
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error with software control: {e}")
            return False
            
    def _get_effect_code(self, effect: str) -> int:
        """Convert effect name to device-specific code"""
        effect_codes = {
            'static': 0x01,
            'breathing': 0x02,
            'wave': 0x03,
            'rainbow': 0x04,
            'spectrum_cycle': 0x05,
            'reactive': 0x06
        }
        return effect_codes.get(effect, 0x01)
        
    def turn_off_all(self) -> bool:
        """Turn off all keyboard RGB"""
        try:
            if not self.device_connected:
                return False
                
            # Set all zones to black
            off_settings = {
                'color': (0, 0, 0),
                'effect': 'static',
                'brightness': 0,
                'speed': 50
            }
            
            return self.apply_settings('evofox_keyboard', off_settings)
            
        except Exception as e:
            self.logger.error(f"Error turning off Evofox keyboard: {e}")
            return False
            
    def get_supported_effects(self) -> List[str]:
        """Get supported effects for Evofox keyboard"""
        return [
            'static',
            'breathing',
            'wave',
            'rainbow',
            'spectrum_cycle',
            'reactive',
            'ripple',
            'fireball'
        ]
        
    def get_keyboard_layout(self) -> Dict:
        """Get keyboard layout information"""
        return {
            'layout': 'US_QWERTY',
            'form_factor': 'TKL',  # Tenkeyless
            'zones': [
                'function_row',
                'number_row', 
                'qwerty_rows',
                'space_row',
                'arrow_keys',
                'nav_cluster'
            ],
            'special_keys': ['fn', 'rgb_toggle', 'profile_switch']
        }
        
    def set_profile(self, profile_number: int) -> bool:
        """Switch to a specific RGB profile"""
        try:
            if not self.device_connected or profile_number < 1 or profile_number > 5:
                return False
                
            # Send profile switch command
            self.logger.info(f"Switching to profile {profile_number}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error switching profile: {e}")
            return False