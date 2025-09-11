"""
OpenRGB Controller for ARGB fans and universal RGB device support
"""

import logging
from typing import Dict, List, Optional, Tuple
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType


class OpenRGBController:
    """Controller for OpenRGB-compatible devices including ARGB fans"""
    
    def __init__(self, host: str = "localhost", port: int = 6742):
        self.host = host
        self.port = port
        self.client = None
        self.connected_devices = []
        self.logger = logging.getLogger(__name__)
        
    def connect(self) -> bool:
        """Connect to OpenRGB server"""
        try:
            self.client = OpenRGBClient(self.host, self.port)
            self.logger.info(f"Connected to OpenRGB server at {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to OpenRGB server: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from OpenRGB server"""
        if self.client:
            self.client.disconnect()
            self.client = None
            
    def scan_devices(self) -> List[Dict]:
        """Scan for available OpenRGB devices"""
        devices = []
        
        try:
            if not self.client:
                if not self.connect():
                    return devices
                    
            if self.client:
                self.connected_devices = self.client.devices
            
            for device in self.connected_devices:
                device_info = {
                    'name': device.name,
                    'type': device.type.name if hasattr(device.type, 'name') else str(device.type),
                    'modes': [mode.name for mode in device.modes],
                    'zones': len(device.zones),
                    'leds': len(device.leds)
                }
                devices.append(device_info)
                
        except Exception as e:
            self.logger.error(f"Error scanning OpenRGB devices: {e}")
            
        return devices
        
    def apply_settings(self, device_key: str, settings: Dict) -> bool:
        """Apply RGB settings to OpenRGB devices"""
        try:
            if not self.client:
                if not self.connect():
                    return False
                    
            color = settings.get('color', (255, 0, 0))
            effect = settings.get('effect', 'static')
            brightness = settings.get('brightness', 100)
            
            # Convert RGB tuple to OpenRGB color
            rgb_color = RGBColor(
                red=int(color[0] * brightness / 100),
                green=int(color[1] * brightness / 100), 
                blue=int(color[2] * brightness / 100)
            )
            
            success_count = 0
            
            for device in self.connected_devices:
                try:
                    # Apply to ARGB fans and motherboard RGB headers
                    if any(keyword in device.name.lower() for keyword in ['fan', 'argb', 'rgb', 'motherboard', 'header']):
                        
                        # Find appropriate mode
                        mode_index = self._get_mode_index(device, effect)
                        if mode_index is not None:
                            device.set_mode(mode_index)
                            
                        # Set colors
                        device.set_color(rgb_color)
                        success_count += 1
                        
                except Exception as e:
                    self.logger.error(f"Error setting RGB for device {device.name}: {e}")
                    
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Error applying OpenRGB settings: {e}")
            return False
            
    def _get_mode_index(self, device, effect: str) -> Optional[int]:
        """Get the mode index for the specified effect"""
        effect_mapping = {
            'static': ['static', 'direct'],
            'breathing': ['breathing', 'breath'],
            'wave': ['wave', 'rainbow wave'],
            'rainbow': ['rainbow', 'spectrum cycle'],
            'spectrum_cycle': ['spectrum cycle', 'rainbow'],
            'reactive': ['reactive', 'key reactive']
        }
        
        effect_names = effect_mapping.get(effect, [effect])
        
        for i, mode in enumerate(device.modes):
            if any(effect_name.lower() in mode.name.lower() for effect_name in effect_names):
                return i
                
        # Default to first mode if no match found
        return 0 if device.modes else None
        
    def turn_off_all(self) -> bool:
        """Turn off all OpenRGB devices"""
        try:
            if not self.client:
                if not self.connect():
                    return False
                    
            black_color = RGBColor(0, 0, 0)
            
            for device in self.connected_devices:
                try:
                    device.set_color(black_color)
                except Exception as e:
                    self.logger.error(f"Error turning off device {device.name}: {e}")
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error turning off OpenRGB devices: {e}")
            return False
            
    def get_device_info(self, device_name: str) -> Optional[Dict]:
        """Get detailed information about a specific device"""
        try:
            if not self.client:
                if not self.connect():
                    return None
                    
            for device in self.connected_devices:
                if device.name == device_name:
                    return {
                        'name': device.name,
                        'type': device.type.name if hasattr(device.type, 'name') else str(device.type),
                        'description': getattr(device, 'description', ''),
                        'version': getattr(device, 'version', ''),
                        'serial': getattr(device, 'serial', ''),
                        'location': getattr(device, 'location', ''),
                        'modes': [{'name': mode.name, 'value': mode.value} for mode in device.modes],
                        'zones': [{'name': zone.name, 'type': zone.type} for zone in device.zones],
                        'led_count': len(device.leds)
                    }
                    
        except Exception as e:
            self.logger.error(f"Error getting device info: {e}")
            
        return None