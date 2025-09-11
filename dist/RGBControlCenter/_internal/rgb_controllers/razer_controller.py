"""
Razer Chroma Controller for Razer Basilisk mouse
"""

import logging
import requests
import json
from typing import Dict, List, Optional, Tuple


class RazerController:
    """Controller for Razer Chroma-compatible devices"""
    
    def __init__(self):
        self.base_url = "http://localhost:54235/razer/chromasdk"
        self.session_id = None
        self.logger = logging.getLogger(__name__)
        
    def connect(self) -> bool:
        """Initialize connection to Razer Chroma SDK"""
        try:
            # Initialize Chroma SDK session
            init_data = {
                "title": "RGB Control Center",
                "description": "Unified RGB Control Application",
                "author": {
                    "name": "RGB Control Center",
                    "contact": "support@rgbcontrol.com"
                },
                "device_supported": [
                    "keyboard",
                    "mouse", 
                    "headset",
                    "mousepad",
                    "keypad",
                    "chromalink"
                ],
                "category": "application"
            }
            
            response = requests.post(f"{self.base_url}", json=init_data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                if 'sessionid' in result:
                    self.session_id = result['sessionid']
                    self.logger.info("Connected to Razer Chroma SDK")
                    return True
                    
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to connect to Razer Chroma SDK: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error connecting to Razer: {e}")
            
        return False
        
    def disconnect(self):
        """Disconnect from Razer Chroma SDK"""
        if self.session_id:
            try:
                requests.delete(f"{self.base_url}/{self.session_id}", timeout=5)
                self.session_id = None
                self.logger.info("Disconnected from Razer Chroma SDK")
            except Exception as e:
                self.logger.error(f"Error disconnecting from Razer: {e}")
                
    def scan_devices(self) -> List[Dict]:
        """Scan for Razer devices"""
        devices = []
        
        if not self.session_id:
            if not self.connect():
                return devices
                
        # Razer SDK doesn't provide device enumeration
        # We'll assume common devices are available
        razer_devices = [
            {
                'name': 'Razer Basilisk Mouse',
                'type': 'mouse',
                'supported_effects': ['static', 'breathing', 'spectrum_cycle', 'reactive']
            }
        ]
        
        return razer_devices
        
    def apply_settings(self, device_key: str, settings: Dict) -> bool:
        """Apply RGB settings to Razer devices"""
        try:
            if not self.session_id:
                if not self.connect():
                    return False
                    
            color = settings.get('color', (255, 0, 0))
            effect = settings.get('effect', 'static')
            brightness = settings.get('brightness', 100)
            
            # Convert color with brightness
            rgb_color = [
                int(color[0] * brightness / 100),
                int(color[1] * brightness / 100),
                int(color[2] * brightness / 100)
            ]
            
            # Apply to mouse (Basilisk)
            return self._apply_mouse_effect(effect, rgb_color, settings)
            
        except Exception as e:
            self.logger.error(f"Error applying Razer settings: {e}")
            return False
            
    def _apply_mouse_effect(self, effect: str, color: List[int], settings: Dict) -> bool:
        """Apply effect to Razer mouse"""
        try:
            effect_data = None
            
            if effect == 'static':
                effect_data = {
                    "effect": "CHROMA_STATIC",
                    "param": {
                        "color": (color[0] << 16) | (color[1] << 8) | color[2]
                    }
                }
            elif effect == 'breathing':
                effect_data = {
                    "effect": "CHROMA_BREATHING", 
                    "param": {
                        "color": (color[0] << 16) | (color[1] << 8) | color[2]
                    }
                }
            elif effect == 'spectrum_cycle':
                effect_data = {
                    "effect": "CHROMA_SPECTRUM_CYCLING"
                }
            elif effect == 'reactive':
                effect_data = {
                    "effect": "CHROMA_REACTIVE",
                    "param": {
                        "color": (color[0] << 16) | (color[1] << 8) | color[2],
                        "duration": 2  # Medium duration
                    }
                }
            else:
                # Default to static
                effect_data = {
                    "effect": "CHROMA_STATIC",
                    "param": {
                        "color": (color[0] << 16) | (color[1] << 8) | color[2]
                    }
                }
                
            if effect_data:
                response = requests.put(
                    f"{self.base_url}/{self.session_id}/mouse",
                    json=effect_data,
                    timeout=5
                )
                
                return response.status_code == 200
                
        except Exception as e:
            self.logger.error(f"Error applying mouse effect: {e}")
            
        return False
        
    def turn_off_all(self) -> bool:
        """Turn off all Razer devices"""
        try:
            if not self.session_id:
                if not self.connect():
                    return False
                    
            # Turn off mouse
            off_data = {
                "effect": "CHROMA_NONE"
            }
            
            response = requests.put(
                f"{self.base_url}/{self.session_id}/mouse",
                json=off_data,
                timeout=5
            )
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Error turning off Razer devices: {e}")
            return False
            
    def get_device_capabilities(self) -> Dict:
        """Get Razer device capabilities"""
        return {
            'mouse': {
                'effects': ['static', 'breathing', 'spectrum_cycle', 'reactive'],
                'zones': ['logo', 'scroll_wheel', 'left_side', 'right_side']
            }
        }