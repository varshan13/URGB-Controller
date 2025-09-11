"""
3D Models and representations for gaming peripherals and components
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Vector3D:
    x: float
    y: float
    z: float
    
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)


@dataclass
class DeviceModel3D:
    name: str
    device_type: str
    position: Vector3D
    rotation: Vector3D
    scale: Vector3D
    color: Tuple[int, int, int]
    vertices: List[Tuple[float, float, float]]
    faces: List[Tuple[int, int, int]]
    rgb_zones: List[Dict]
    category: str  # 'external' or 'internal'


class Device3DModels:
    """3D models for gaming peripherals and components"""
    
    @staticmethod
    def get_keyboard_model() -> DeviceModel3D:
        """Create 3D model for gaming keyboard"""
        # Simple rectangular keyboard with raised keys
        vertices = [
            # Base plate
            (-8.0, -3.0, 0.0), (8.0, -3.0, 0.0), (8.0, 3.0, 0.0), (-8.0, 3.0, 0.0),
            (-8.0, -3.0, 0.5), (8.0, -3.0, 0.5), (8.0, 3.0, 0.5), (-8.0, 3.0, 0.5),
            # Key area (raised)
            (-7.5, -2.5, 0.5), (7.5, -2.5, 0.5), (7.5, 2.5, 0.5), (-7.5, 2.5, 0.5),
            (-7.5, -2.5, 0.8), (7.5, -2.5, 0.8), (7.5, 2.5, 0.8), (-7.5, 2.5, 0.8)
        ]
        
        faces = [
            # Base faces
            (0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7),
            (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
            (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7),
            # Key area faces
            (8, 9, 10), (8, 10, 11), (12, 13, 14), (12, 14, 15),
            (8, 9, 13), (8, 13, 12), (9, 10, 14), (9, 14, 13),
            (10, 11, 15), (10, 15, 14), (11, 8, 12), (11, 12, 15)
        ]
        
        rgb_zones = [
            {'name': 'Backlight', 'position': (0, 0, 0.6), 'led_count': 104},
            {'name': 'Edge Left', 'position': (-7.5, 0, 0.4), 'led_count': 8},
            {'name': 'Edge Right', 'position': (7.5, 0, 0.4), 'led_count': 8},
            {'name': 'Logo', 'position': (0, 2.0, 0.4), 'led_count': 1}
        ]
        
        return DeviceModel3D(
            name="Gaming Keyboard",
            device_type="keyboard",
            position=Vector3D(0, -5, 0),
            rotation=Vector3D(0, 0, 0),
            scale=Vector3D(1, 1, 1),
            color=(50, 50, 50),
            vertices=vertices,
            faces=faces,
            rgb_zones=rgb_zones,
            category="external"
        )
    
    @staticmethod
    def get_mouse_model() -> DeviceModel3D:
        """Create 3D model for gaming mouse"""
        # Ergonomic mouse shape
        vertices = [
            # Base
            (-1.5, -2.5, 0.0), (1.5, -2.5, 0.0), (1.8, 1.5, 0.0), (-1.8, 1.5, 0.0),
            # Top curve
            (-1.2, -2.0, 1.0), (1.2, -2.0, 1.0), (1.5, 1.0, 1.2), (-1.5, 1.0, 1.2),
            # Scroll wheel area
            (-0.3, 0.5, 1.3), (0.3, 0.5, 1.3), (0.3, 1.0, 1.3), (-0.3, 1.0, 1.3)
        ]
        
        faces = [
            (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
            (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7),
            (4, 5, 6), (4, 6, 7), (8, 9, 10), (8, 10, 11)
        ]
        
        rgb_zones = [
            {'name': 'Logo', 'position': (0, -1.0, 0.8), 'led_count': 1},
            {'name': 'Scroll Wheel', 'position': (0, 0.75, 1.3), 'led_count': 4},
            {'name': 'Side Left', 'position': (-1.6, 0, 0.5), 'led_count': 3},
            {'name': 'Side Right', 'position': (1.6, 0, 0.5), 'led_count': 3}
        ]
        
        return DeviceModel3D(
            name="Gaming Mouse",
            device_type="mouse",
            position=Vector3D(6, -2, 0),
            rotation=Vector3D(0, 0, 0),
            scale=Vector3D(1, 1, 1),
            color=(30, 30, 30),
            vertices=vertices,
            faces=faces,
            rgb_zones=rgb_zones,
            category="external"
        )
    
    @staticmethod
    def get_monitor_model() -> DeviceModel3D:
        """Create 3D model for gaming monitor"""
        vertices = [
            # Screen
            (-12, 0, 0), (12, 0, 0), (12, 0, 8), (-12, 0, 8),
            # Frame
            (-12.5, -0.5, -0.5), (12.5, -0.5, -0.5), (12.5, -0.5, 8.5), (-12.5, -0.5, 8.5),
            # Stand base
            (-3, -2, -1), (3, -2, -1), (3, -1, -1), (-3, -1, -1),
            # Stand post
            (-0.5, -1.5, -1), (0.5, -1.5, -1), (0.5, -0.5, 3), (-0.5, -0.5, 3)
        ]
        
        faces = [
            # Screen and frame
            (0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7),
            (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
            # Stand
            (8, 9, 10), (8, 10, 11), (12, 13, 14), (12, 14, 15)
        ]
        
        rgb_zones = [
            {'name': 'Back Panel', 'position': (0, -0.5, 4), 'led_count': 20},
            {'name': 'Bottom Strip', 'position': (0, -0.3, 0), 'led_count': 15},
            {'name': 'Logo', 'position': (0, -0.3, 6), 'led_count': 1}
        ]
        
        return DeviceModel3D(
            name="Gaming Monitor",
            device_type="monitor",
            position=Vector3D(0, 5, 2),
            rotation=Vector3D(0, 0, 0),
            scale=Vector3D(1, 1, 1),
            color=(20, 20, 20),
            vertices=vertices,
            faces=faces,
            rgb_zones=rgb_zones,
            category="external"
        )
    
    @staticmethod
    def get_pc_case_model() -> DeviceModel3D:
        """Create 3D model for PC case/cabinet"""
        vertices = [
            # Main case body
            (-10, -5, 0), (10, -5, 0), (10, 5, 0), (-10, 5, 0),
            (-10, -5, 20), (10, -5, 20), (10, 5, 20), (-10, 5, 20),
            # Front panel
            (-9.5, 5, 1), (9.5, 5, 1), (9.5, 5, 19), (-9.5, 5, 19),
            # Side panel window
            (10, -4, 2), (10, 4, 2), (10, 4, 18), (10, -4, 18)
        ]
        
        faces = [
            # Main body
            (0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7),
            (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
            (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7),
            # Front and side panels
            (8, 9, 10), (8, 10, 11), (12, 13, 14), (12, 14, 15)
        ]
        
        rgb_zones = [
            {'name': 'Front Strip', 'position': (0, 5, 10), 'led_count': 30},
            {'name': 'Side Window', 'position': (10, 0, 10), 'led_count': 25},
            {'name': 'Top Edge', 'position': (0, 0, 20), 'led_count': 20},
            {'name': 'Bottom Edge', 'position': (0, 0, 0.5), 'led_count': 20}
        ]
        
        return DeviceModel3D(
            name="PC Case",
            device_type="case",
            position=Vector3D(-15, 0, 0),
            rotation=Vector3D(0, 0, 0),
            scale=Vector3D(1, 1, 1),
            color=(40, 40, 40),
            vertices=vertices,
            faces=faces,
            rgb_zones=rgb_zones,
            category="external"
        )
    
    @staticmethod
    def get_ram_model() -> DeviceModel3D:
        """Create 3D model for RAM stick"""
        vertices = [
            # RAM stick body
            (-0.5, -6, 0), (0.5, -6, 0), (0.5, 6, 0), (-0.5, 6, 0),
            (-0.5, -6, 1.5), (0.5, -6, 1.5), (0.5, 6, 1.5), (-0.5, 6, 1.5),
            # Heat spreader
            (-0.7, -5.5, 0.2), (0.7, -5.5, 0.2), (0.7, 5.5, 0.2), (-0.7, 5.5, 0.2),
            (-0.7, -5.5, 1.3), (0.7, -5.5, 1.3), (0.7, 5.5, 1.3), (-0.7, 5.5, 1.3)
        ]
        
        faces = [
            (0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7),
            (8, 9, 10), (8, 10, 11), (12, 13, 14), (12, 14, 15)
        ]
        
        rgb_zones = [
            {'name': 'Top Strip', 'position': (0, 0, 1.5), 'led_count': 8},
            {'name': 'Side Left', 'position': (-0.7, 0, 0.75), 'led_count': 4},
            {'name': 'Side Right', 'position': (0.7, 0, 0.75), 'led_count': 4}
        ]
        
        return DeviceModel3D(
            name="RGB RAM",
            device_type="ram",
            position=Vector3D(-2, 2, 0.5),
            rotation=Vector3D(0, 0, 90),
            scale=Vector3D(1, 1, 1),
            color=(0, 100, 0),
            vertices=vertices,
            faces=faces,
            rgb_zones=rgb_zones,
            category="internal"
        )
    
    @staticmethod
    def get_gpu_model() -> DeviceModel3D:
        """Create 3D model for graphics card"""
        vertices = [
            # GPU card body
            (-6, -1, 0), (6, -1, 0), (6, 1, 0), (-6, 1, 0),
            (-6, -1, 2), (6, -1, 2), (6, 1, 2), (-6, 1, 2),
            # Cooler shroud
            (-5.5, -0.8, 2), (5.5, -0.8, 2), (5.5, 0.8, 2), (-5.5, 0.8, 2),
            (-5.5, -0.8, 3.5), (5.5, -0.8, 3.5), (5.5, 0.8, 3.5), (-5.5, 0.8, 3.5)
        ]
        
        faces = [
            (0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7),
            (8, 9, 10), (8, 10, 11), (12, 13, 14), (12, 14, 15)
        ]
        
        rgb_zones = [
            {'name': 'Logo', 'position': (0, 0, 3.5), 'led_count': 1},
            {'name': 'Edge Strip', 'position': (0, 1, 1), 'led_count': 12},
            {'name': 'Backplate', 'position': (0, -1, 1), 'led_count': 8}
        ]
        
        return DeviceModel3D(
            name="Graphics Card",
            device_type="gpu",
            position=Vector3D(0, -2, 0.5),
            rotation=Vector3D(0, 0, 0),
            scale=Vector3D(1, 1, 1),
            color=(100, 0, 0),
            vertices=vertices,
            faces=faces,
            rgb_zones=rgb_zones,
            category="internal"
        )
    
    @staticmethod
    def get_fan_model() -> DeviceModel3D:
        """Create 3D model for case fan"""
        vertices = []
        faces = []
        
        # Generate circular fan frame
        segments = 12
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = 1.2 * math.cos(angle)
            y = 1.2 * math.sin(angle)
            vertices.extend([(x, y, 0), (x, y, 0.5)])
        
        # Fan blades (simplified)
        for i in range(4):
            angle = 2 * math.pi * i / 4
            x1, y1 = 0.3 * math.cos(angle), 0.3 * math.sin(angle)
            x2, y2 = 1.0 * math.cos(angle + 0.5), 1.0 * math.sin(angle + 0.5)
            vertices.extend([(x1, y1, 0.25), (x2, y2, 0.25)])
        
        rgb_zones = [
            {'name': 'Ring', 'position': (0, 0, 0.25), 'led_count': 16},
            {'name': 'Center', 'position': (0, 0, 0.25), 'led_count': 1}
        ]
        
        return DeviceModel3D(
            name="RGB Fan",
            device_type="fan",
            position=Vector3D(4, 4, 8),
            rotation=Vector3D(0, 0, 0),
            scale=Vector3D(1, 1, 1),
            color=(60, 60, 60),
            vertices=vertices,
            faces=faces,
            rgb_zones=rgb_zones,
            category="internal"
        )
    
    @staticmethod
    def get_aio_model() -> DeviceModel3D:
        """Create 3D model for AIO cooler"""
        vertices = [
            # Radiator
            (-6, 0, 8), (6, 0, 8), (6, 0.5, 8), (-6, 0.5, 8),
            (-6, 0, 12), (6, 0, 12), (6, 0.5, 12), (-6, 0.5, 12),
            # CPU block
            (-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
        ]
        
        faces = [
            (0, 1, 2), (0, 2, 3), (4, 5, 6), (4, 6, 7),
            (8, 9, 10), (8, 10, 11), (12, 13, 14), (12, 14, 15)
        ]
        
        rgb_zones = [
            {'name': 'CPU Block', 'position': (0, 0, 1), 'led_count': 8},
            {'name': 'Radiator', 'position': (0, 0.25, 10), 'led_count': 12}
        ]
        
        return DeviceModel3D(
            name="AIO Cooler",
            device_type="aio",
            position=Vector3D(0, 0, 0),
            rotation=Vector3D(0, 0, 0),
            scale=Vector3D(1, 1, 1),
            color=(0, 0, 100),
            vertices=vertices,
            faces=faces,
            rgb_zones=rgb_zones,
            category="internal"
        )
    
    @staticmethod
    def get_strimmer_cable_model() -> DeviceModel3D:
        """Create 3D model for Lian Li Strimmer cable"""
        vertices = []
        faces = []
        
        # Generate cable path with LED segments
        cable_length = 20
        segments = 24
        
        for i in range(segments):
            t = i / segments
            x = -8 + 16 * t  # Straight cable from PSU to motherboard
            y = -1 + 0.5 * math.sin(t * math.pi * 4)  # Slight curve
            z = 0.5
            
            # Each segment has width and height
            vertices.extend([
                (x - 0.2, y - 0.1, z), (x + 0.2, y - 0.1, z),
                (x + 0.2, y + 0.1, z), (x - 0.2, y + 0.1, z),
                (x - 0.2, y - 0.1, z + 0.2), (x + 0.2, y - 0.1, z + 0.2),
                (x + 0.2, y + 0.1, z + 0.2), (x - 0.2, y + 0.1, z + 0.2)
            ])
        
        rgb_zones = [
            {'name': f'Segment {i+1}', 'position': (-8 + 16 * i / 24, 0, 0.6), 'led_count': 1}
            for i in range(24)
        ]
        
        return DeviceModel3D(
            name="Strimmer Cable",
            device_type="strimmer",
            position=Vector3D(0, -1, 0),
            rotation=Vector3D(0, 0, 0),
            scale=Vector3D(1, 1, 1),
            color=(255, 255, 255),
            vertices=vertices,
            faces=faces,
            rgb_zones=rgb_zones,
            category="internal"
        )
    
    @staticmethod
    def get_all_external_models() -> List[DeviceModel3D]:
        """Get all external peripheral models"""
        return [
            Device3DModels.get_keyboard_model(),
            Device3DModels.get_mouse_model(),
            Device3DModels.get_monitor_model(),
            Device3DModels.get_pc_case_model()
        ]
    
    @staticmethod
    def get_all_internal_models() -> List[DeviceModel3D]:
        """Get all internal component models"""
        return [
            Device3DModels.get_ram_model(),
            Device3DModels.get_gpu_model(),
            Device3DModels.get_fan_model(),
            Device3DModels.get_aio_model(),
            Device3DModels.get_strimmer_cable_model()
        ]