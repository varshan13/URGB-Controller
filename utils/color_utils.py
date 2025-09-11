"""
Color utility functions for RGB Control Application
"""

import colorsys
import math
from typing import Tuple, List, Union


class ColorUtils:
    """Utility class for color operations and conversions"""
    
    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex string"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex string to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        rgb_values = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        return (rgb_values[0], rgb_values[1], rgb_values[2])
        
    @staticmethod
    def rgb_to_hsv(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Convert RGB to HSV"""
        r, g, b = [x / 255.0 for x in rgb]
        return colorsys.rgb_to_hsv(r, g, b)
        
    @staticmethod
    def hsv_to_rgb(hsv: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """Convert HSV to RGB"""
        r, g, b = colorsys.hsv_to_rgb(*hsv)
        return (int(r * 255), int(g * 255), int(b * 255))
        
    @staticmethod
    def adjust_brightness(rgb: Tuple[int, int, int], brightness: float) -> Tuple[int, int, int]:
        """Adjust RGB color brightness (0.0 to 1.0)"""
        adjusted = [int(c * brightness) for c in rgb]
        return (adjusted[0], adjusted[1], adjusted[2])
        
    @staticmethod
    def blend_colors(color1: Tuple[int, int, int], color2: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
        """Blend two RGB colors with given ratio (0.0 to 1.0)"""
        blended = [
            int(c1 * (1 - ratio) + c2 * ratio)
            for c1, c2 in zip(color1, color2)
        ]
        return (blended[0], blended[1], blended[2])
        
    @staticmethod
    def generate_rainbow_colors(num_colors: int) -> List[Tuple[int, int, int]]:
        """Generate a list of rainbow colors"""
        colors = []
        for i in range(num_colors):
            hue = i / num_colors
            rgb = ColorUtils.hsv_to_rgb((hue, 1.0, 1.0))
            colors.append(rgb)
        return colors
        
    @staticmethod
    def generate_gradient(start_color: Tuple[int, int, int], end_color: Tuple[int, int, int], steps: int) -> List[Tuple[int, int, int]]:
        """Generate gradient between two colors"""
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1) if steps > 1 else 0
            color = ColorUtils.blend_colors(start_color, end_color, ratio)
            gradient.append(color)
        return gradient
        
    @staticmethod
    def get_complementary_color(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Get complementary color"""
        return (255 - rgb[0], 255 - rgb[1], 255 - rgb[2])
        
    @staticmethod
    def get_color_temperature(kelvin: int) -> Tuple[int, int, int]:
        """Convert color temperature in Kelvin to RGB"""
        # Simplified color temperature calculation
        temp = kelvin / 100.0
        
        if temp <= 66:
            red = 255
            green = temp
            green = 99.4708025861 * math.log(green) - 161.1195681661
            if temp >= 19:
                blue = temp - 10
                blue = 138.5177312231 * math.log(blue) - 305.0447927307
            else:
                blue = 0
        else:
            red = temp - 60
            red = 329.698727446 * (red ** -0.1332047592)
            green = temp - 60
            green = 288.1221695283 * (green ** -0.0755148492)
            blue = 255
            
        # Clamp values
        red = max(0, min(255, int(red)))
        green = max(0, min(255, int(green)))
        blue = max(0, min(255, int(blue)))
        
        return (red, green, blue)
        
    @staticmethod
    def analyze_color(rgb: Tuple[int, int, int]) -> dict:
        """Analyze color properties"""
        r, g, b = rgb
        
        # Calculate brightness (perceived luminance)
        brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        
        # Calculate saturation
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        saturation = (max_val - min_val) / max_val if max_val > 0 else 0
        
        # Determine dominant color
        if r >= g and r >= b:
            dominant = "Red"
        elif g >= r and g >= b:
            dominant = "Green"
        else:
            dominant = "Blue"
            
        # Determine if warm or cool
        if r + 50 > b:
            temperature = "Warm"
        else:
            temperature = "Cool"
            
        return {
            'brightness': brightness,
            'saturation': saturation,
            'dominant_color': dominant,
            'temperature': temperature,
            'hex': ColorUtils.rgb_to_hex(rgb),
            'hsv': ColorUtils.rgb_to_hsv(rgb)
        }
        
    @staticmethod
    def create_breathing_effect(base_color: Tuple[int, int, int], steps: int = 50) -> List[Tuple[int, int, int]]:
        """Create breathing effect color sequence"""
        colors = []
        
        # Fade in
        for i in range(steps // 2):
            brightness = i / (steps // 2)
            color = ColorUtils.adjust_brightness(base_color, brightness)
            colors.append(color)
            
        # Fade out
        for i in range(steps // 2, 0, -1):
            brightness = i / (steps // 2)
            color = ColorUtils.adjust_brightness(base_color, brightness)
            colors.append(color)
            
        return colors
        
    @staticmethod
    def create_wave_effect(colors: List[Tuple[int, int, int]], width: int, position: float) -> List[Tuple[int, int, int]]:
        """Create wave effect across a strip of LEDs"""
        result = []
        
        for i in range(width):
            # Calculate wave position
            wave_pos = (position + i / width) % 1.0
            color_index = int(wave_pos * len(colors))
            color_index = min(color_index, len(colors) - 1)
            
            result.append(colors[color_index])
            
        return result
        
    @staticmethod
    def validate_rgb(rgb: Union[Tuple, List]) -> bool:
        """Validate RGB color values"""
        try:
            if len(rgb) != 3:
                return False
                
            for value in rgb:
                if not isinstance(value, int) or value < 0 or value > 255:
                    return False
                    
            return True
            
        except Exception:
            return False
            
    @staticmethod
    def get_random_color() -> Tuple[int, int, int]:
        """Generate random RGB color"""
        import random
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        
    @staticmethod
    def get_predefined_colors() -> dict:
        """Get dictionary of predefined colors"""
        return {
            'Red': (255, 0, 0),
            'Green': (0, 255, 0),
            'Blue': (0, 0, 255),
            'Yellow': (255, 255, 0),
            'Cyan': (0, 255, 255),
            'Magenta': (255, 0, 255),
            'White': (255, 255, 255),
            'Orange': (255, 165, 0),
            'Purple': (128, 0, 128),
            'Pink': (255, 192, 203),
            'Lime': (0, 255, 0),
            'Teal': (0, 128, 128),
            'Navy': (0, 0, 128),
            'Maroon': (128, 0, 0),
            'Olive': (128, 128, 0),
            'Silver': (192, 192, 192),
            'Gray': (128, 128, 128),
            'Black': (0, 0, 0)
        }