"""
3D RGB Interface for placing and visualizing gaming peripherals and components
"""

import tkinter as tk
from tkinter import ttk
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import threading
from typing import Dict, List, Tuple, Optional
from utils.device_3d_models import Device3DModels, DeviceModel3D, Vector3D


class RGB3DInterface:
    """3D interface for placing and controlling RGB devices"""
    
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.external_window = None
        self.internal_window = None
        self.selected_device = None
        self.camera_rotation = [0, 0]
        self.camera_distance = 30
        self.mouse_dragging = False
        self.last_mouse_pos = (0, 0)
        
        # Device collections
        self.external_devices = Device3DModels.get_all_external_models()
        self.internal_devices = Device3DModels.get_all_internal_models()
        
        # Active device placements
        self.placed_external_devices = {}
        self.placed_internal_devices = {}
        
        # Initialize default placements
        self._initialize_default_placements()
        
    def _initialize_default_placements(self):
        """Set up default device placements"""
        for device in self.external_devices:
            self.placed_external_devices[device.name] = device
            
        for device in self.internal_devices:
            self.placed_internal_devices[device.name] = device
    
    def open_external_3d_view(self):
        """Open 3D view for external peripherals"""
        if self.external_window and self.external_window.winfo_exists():
            self.external_window.lift()
            return
            
        self.external_window = tk.Toplevel(self.parent_app.root)
        self.external_window.title("3D Setup - Gaming Peripherals")
        self.external_window.geometry("1000x700")
        
        # Create control panel
        control_frame = ttk.Frame(self.external_window)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ttk.Label(control_frame, text="Gaming Peripherals", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Device list
        device_frame = ttk.LabelFrame(control_frame, text="Devices", padding="5")
        device_frame.pack(fill="x", pady=5)
        
        self.external_device_vars = {}
        for device in self.external_devices:
            var = tk.BooleanVar(value=True)
            self.external_device_vars[device.name] = var
            
            cb = ttk.Checkbutton(device_frame, text=device.name, variable=var,
                               command=lambda d=device: self._toggle_device_visibility(d, 'external'))
            cb.pack(anchor="w")
        
        # Position controls
        pos_frame = ttk.LabelFrame(control_frame, text="Position", padding="5")
        pos_frame.pack(fill="x", pady=5)
        
        self.pos_vars = {'x': tk.DoubleVar(), 'y': tk.DoubleVar(), 'z': tk.DoubleVar()}
        for axis, var in self.pos_vars.items():
            ttk.Label(pos_frame, text=f"{axis.upper()}:").pack(anchor="w")
            scale = ttk.Scale(pos_frame, from_=-20, to=20, variable=var, orient="horizontal")
            scale.pack(fill="x", pady=2)
            scale.configure(command=lambda v, a=axis: self._update_device_position(a, v))
        
        # RGB Preview
        rgb_frame = ttk.LabelFrame(control_frame, text="RGB Preview", padding="5")
        rgb_frame.pack(fill="x", pady=5)
        
        ttk.Button(rgb_frame, text="Sync Current Color", 
                  command=self._sync_current_color).pack(fill="x", pady=2)
        ttk.Button(rgb_frame, text="Preview Effect", 
                  command=self._preview_effect).pack(fill="x", pady=2)
        
        # 3D View placeholder
        view_frame = ttk.Frame(self.external_window, relief="sunken", borderwidth=2)
        view_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(view_frame, bg="black", width=600, height=500)
        canvas.pack(fill="both", expand=True)
        
        # Instructions
        instructions = [
            "3D Gaming Setup View",
            "",
            "Mouse Controls:",
            "• Left click + drag: Rotate view",
            "• Scroll wheel: Zoom in/out",
            "• Right click: Select device",
            "",
            "Devices:",
            "• Keyboard: WASD area with RGB zones",
            "• Mouse: Side buttons and scroll wheel",
            "• Monitor: Back panel RGB strips",
            "• PC Case: Front, side, and edge lighting"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction == "3D Gaming Setup View":
                canvas.create_text(300, 50, text=instruction, fill="white", 
                                 font=("Arial", 16, "bold"))
            elif instruction.startswith("•"):
                canvas.create_text(300, 120 + i*20, text=instruction, fill="lightblue", 
                                 font=("Arial", 10))
            elif instruction.endswith(":"):
                canvas.create_text(300, 120 + i*20, text=instruction, fill="yellow", 
                                 font=("Arial", 12, "bold"))
            else:
                canvas.create_text(300, 120 + i*20, text=instruction, fill="white", 
                                 font=("Arial", 10))
        
        # Simulate 3D device layout
        self._draw_external_devices_2d(canvas)
        
        # Bind events
        canvas.bind("<Button-1>", lambda e: self._on_canvas_click(e, 'external'))
        canvas.bind("<B1-Motion>", lambda e: self._on_canvas_drag(e, 'external'))
        canvas.bind("<MouseWheel>", lambda e: self._on_canvas_scroll(e, 'external'))
        
    def open_internal_3d_view(self):
        """Open 3D view for internal components"""
        if self.internal_window and self.internal_window.winfo_exists():
            self.internal_window.lift()
            return
            
        self.internal_window = tk.Toplevel(self.parent_app.root)
        self.internal_window.title("3D Setup - Internal Components")
        self.internal_window.geometry("1000x700")
        
        # Create control panel
        control_frame = ttk.Frame(self.internal_window)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ttk.Label(control_frame, text="Internal Components", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Device list
        device_frame = ttk.LabelFrame(control_frame, text="Components", padding="5")
        device_frame.pack(fill="x", pady=5)
        
        self.internal_device_vars = {}
        for device in self.internal_devices:
            var = tk.BooleanVar(value=True)
            self.internal_device_vars[device.name] = var
            
            cb = ttk.Checkbutton(device_frame, text=device.name, variable=var,
                               command=lambda d=device: self._toggle_device_visibility(d, 'internal'))
            cb.pack(anchor="w")
        
        # Component-specific controls
        comp_frame = ttk.LabelFrame(control_frame, text="Component Settings", padding="5")
        comp_frame.pack(fill="x", pady=5)
        
        ttk.Button(comp_frame, text="Auto-Arrange", 
                  command=self._auto_arrange_components).pack(fill="x", pady=2)
        ttk.Button(comp_frame, text="Reset Positions", 
                  command=self._reset_component_positions).pack(fill="x", pady=2)
        
        # RGB Zones
        zones_frame = ttk.LabelFrame(control_frame, text="RGB Zones", padding="5")
        zones_frame.pack(fill="x", pady=5)
        
        self.zones_listbox = tk.Listbox(zones_frame, height=6)
        self.zones_listbox.pack(fill="x")
        
        ttk.Button(zones_frame, text="Control Selected Zone", 
                  command=self._control_selected_zone).pack(fill="x", pady=2)
        
        # 3D View placeholder
        view_frame = ttk.Frame(self.internal_window, relief="sunken", borderwidth=2)
        view_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(view_frame, bg="black", width=600, height=500)
        canvas.pack(fill="both", expand=True)
        
        # Instructions for internal components
        instructions = [
            "3D Internal Components View",
            "",
            "Components:",
            "• RAM: RGB strips on top and sides",
            "• GPU: Logo, edge strips, backplate",
            "• Fans: Ring lighting and center logo",
            "• AIO Cooler: CPU block and radiator",
            "• Strimmer Cables: Individual LED segments",
            "",
            "Controls:",
            "• Drag components to reposition",
            "• Select zones for individual control",
            "• Auto-arrange for optimal layout"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction == "3D Internal Components View":
                canvas.create_text(300, 50, text=instruction, fill="white", 
                                 font=("Arial", 16, "bold"))
            elif instruction.startswith("•"):
                canvas.create_text(300, 100 + i*20, text=instruction, fill="lightgreen", 
                                 font=("Arial", 10))
            elif instruction.endswith(":"):
                canvas.create_text(300, 100 + i*20, text=instruction, fill="yellow", 
                                 font=("Arial", 12, "bold"))
            else:
                canvas.create_text(300, 100 + i*20, text=instruction, fill="white", 
                                 font=("Arial", 10))
        
        # Simulate 3D component layout
        self._draw_internal_components_2d(canvas)
        
        # Bind events
        canvas.bind("<Button-1>", lambda e: self._on_canvas_click(e, 'internal'))
        canvas.bind("<B1-Motion>", lambda e: self._on_canvas_drag(e, 'internal'))
        canvas.bind("<MouseWheel>", lambda e: self._on_canvas_scroll(e, 'internal'))
        
        # Populate zones for first device
        self._update_zones_list()
    
    def _draw_external_devices_2d(self, canvas):
        """Draw 2D representation of external devices"""
        # Keyboard
        canvas.create_rectangle(200, 350, 400, 420, fill="gray20", outline="blue")
        canvas.create_text(300, 385, text="Gaming Keyboard", fill="white", font=("Arial", 10))
        
        # Mouse
        canvas.create_oval(450, 360, 490, 410, fill="gray30", outline="red")
        canvas.create_text(470, 385, text="Mouse", fill="white", font=("Arial", 8))
        
        # Monitor
        canvas.create_rectangle(150, 100, 450, 250, fill="gray10", outline="green")
        canvas.create_text(300, 175, text="Gaming Monitor", fill="white", font=("Arial", 12))
        
        # PC Case
        canvas.create_rectangle(50, 200, 120, 400, fill="gray25", outline="purple")
        canvas.create_text(85, 300, text="PC\nCase", fill="white", font=("Arial", 10))
        
        # RGB effect simulation
        self._animate_rgb_effects(canvas)
    
    def _draw_internal_components_2d(self, canvas):
        """Draw 2D representation of internal components"""
        # Motherboard outline
        canvas.create_rectangle(100, 100, 500, 400, fill="gray15", outline="white")
        
        # RAM slots
        for i in range(4):
            x = 150 + i * 30
            canvas.create_rectangle(x, 150, x+20, 220, fill="green", outline="lime")
            canvas.create_text(x+10, 185, text="RAM", fill="white", font=("Arial", 6), angle=90)
        
        # GPU
        canvas.create_rectangle(200, 300, 450, 350, fill="red", outline="orange")
        canvas.create_text(325, 325, text="Graphics Card", fill="white", font=("Arial", 10))
        
        # CPU/AIO area
        canvas.create_oval(300, 200, 350, 250, fill="blue", outline="cyan")
        canvas.create_text(325, 225, text="AIO", fill="white", font=("Arial", 8))
        
        # Fans
        positions = [(80, 80), (520, 80), (80, 420), (520, 420)]
        for i, (x, y) in enumerate(positions):
            canvas.create_oval(x-20, y-20, x+20, y+20, fill="gray40", outline="white")
            canvas.create_text(x, y, text="Fan", fill="white", font=("Arial", 7))
        
        # Strimmer cables
        canvas.create_line(150, 250, 300, 250, fill="white", width=3)
        canvas.create_text(225, 240, text="24-pin Strimmer", fill="white", font=("Arial", 8))
        
        canvas.create_line(350, 280, 450, 280, fill="white", width=3)
        canvas.create_text(400, 270, text="8-pin GPU", fill="white", font=("Arial", 8))
    
    def _animate_rgb_effects(self, canvas):
        """Animate RGB effects on devices"""
        def animate():
            colors = ["red", "green", "blue", "yellow", "purple", "cyan"]
            color_index = 0
            
            while True:
                try:
                    if not canvas.winfo_exists():
                        break
                        
                    color = colors[color_index % len(colors)]
                    
                    # Update device outlines with current RGB color
                    canvas.itemconfig("all", outline=color)
                    color_index += 1
                    
                    threading.Event().wait(0.5)  # 500ms delay
                    
                except tk.TclError:
                    break
        
        threading.Thread(target=animate, daemon=True).start()
    
    def _toggle_device_visibility(self, device: DeviceModel3D, category: str):
        """Toggle device visibility in 3D view"""
        var_dict = self.external_device_vars if category == 'external' else self.internal_device_vars
        
        if var_dict[device.name].get():
            self.parent_app.log_message(f"Showing {device.name} in 3D view")
        else:
            self.parent_app.log_message(f"Hiding {device.name} from 3D view")
    
    def _update_device_position(self, axis: str, value: str):
        """Update selected device position"""
        if self.selected_device:
            try:
                val = float(value)
                if axis == 'x':
                    self.selected_device.position.x = val
                elif axis == 'y':
                    self.selected_device.position.y = val
                elif axis == 'z':
                    self.selected_device.position.z = val
                    
                self.parent_app.log_message(f"Updated {self.selected_device.name} {axis}: {val}")
            except ValueError:
                pass
    
    def _sync_current_color(self):
        """Sync current RGB color to 3D preview"""
        color = self.parent_app.current_color
        self.parent_app.log_message(f"Syncing RGB color to 3D preview: RGB({color[0]}, {color[1]}, {color[2]})")
    
    def _preview_effect(self):
        """Preview current effect in 3D view"""
        effect = self.parent_app.current_effect
        self.parent_app.log_message(f"Previewing effect in 3D: {effect}")
    
    def _auto_arrange_components(self):
        """Auto-arrange internal components"""
        self.parent_app.log_message("Auto-arranging internal components for optimal RGB visibility")
        
        # Reset to optimal positions
        arrangements = {
            "RGB RAM": Vector3D(-2, 2, 0.5),
            "Graphics Card": Vector3D(0, -2, 0.5),
            "RGB Fan": Vector3D(4, 4, 8),
            "AIO Cooler": Vector3D(0, 0, 0),
            "Strimmer Cable": Vector3D(0, -1, 0)
        }
        
        for device in self.internal_devices:
            if device.name in arrangements:
                device.position = arrangements[device.name]
    
    def _reset_component_positions(self):
        """Reset all component positions to default"""
        self.parent_app.log_message("Resetting all component positions to default")
        self._initialize_default_placements()
    
    def _update_zones_list(self):
        """Update the RGB zones list"""
        if hasattr(self, 'zones_listbox'):
            self.zones_listbox.delete(0, tk.END)
            
            for device in self.internal_devices:
                for zone in device.rgb_zones:
                    self.zones_listbox.insert(tk.END, f"{device.name}: {zone['name']}")
    
    def _control_selected_zone(self):
        """Control the selected RGB zone"""
        selection = self.zones_listbox.curselection()
        if selection:
            zone_text = self.zones_listbox.get(selection[0])
            self.parent_app.log_message(f"Controlling RGB zone: {zone_text}")
    
    def _on_canvas_click(self, event, category: str):
        """Handle canvas click for device selection"""
        self.mouse_dragging = True
        self.last_mouse_pos = (event.x, event.y)
        
        # Simple device selection based on click position
        if category == 'external':
            devices = self.external_devices
        else:
            devices = self.internal_devices
            
        # Mock device selection
        if len(devices) > 0:
            self.selected_device = devices[0]  # Select first device for demo
            self.parent_app.log_message(f"Selected device: {self.selected_device.name}")
    
    def _on_canvas_drag(self, event, category: str):
        """Handle canvas drag for 3D navigation"""
        if self.mouse_dragging:
            dx = event.x - self.last_mouse_pos[0]
            dy = event.y - self.last_mouse_pos[1]
            
            self.camera_rotation[0] += dx * 0.5
            self.camera_rotation[1] += dy * 0.5
            
            self.last_mouse_pos = (event.x, event.y)
    
    def _on_canvas_scroll(self, event, category: str):
        """Handle canvas scroll for zoom"""
        if event.delta > 0:
            self.camera_distance *= 0.9
        else:
            self.camera_distance *= 1.1
            
        self.camera_distance = max(10, min(100, self.camera_distance))
    
    def apply_rgb_to_3d_devices(self, settings: Dict):
        """Apply RGB settings to 3D device visualization"""
        color = settings.get('color', (255, 0, 0))
        effect = settings.get('effect', 'static')
        
        self.parent_app.log_message(f"Applying RGB to 3D devices: {effect} effect, RGB({color[0]}, {color[1]}, {color[2]})")
        
        # Update device colors in 3D models
        for device in self.external_devices + self.internal_devices:
            device.color = color
    
    def get_device_positions(self) -> Dict:
        """Get current device positions for saving"""
        positions = {}
        
        for device in self.external_devices:
            positions[f"external_{device.name}"] = {
                'x': device.position.x,
                'y': device.position.y,
                'z': device.position.z
            }
            
        for device in self.internal_devices:
            positions[f"internal_{device.name}"] = {
                'x': device.position.x,
                'y': device.position.y,
                'z': device.position.z
            }
            
        return positions
    
    def load_device_positions(self, positions: Dict):
        """Load device positions from saved data"""
        for device in self.external_devices:
            key = f"external_{device.name}"
            if key in positions:
                pos = positions[key]
                device.position = Vector3D(pos['x'], pos['y'], pos['z'])
                
        for device in self.internal_devices:
            key = f"internal_{device.name}"
            if key in positions:
                pos = positions[key]
                device.position = Vector3D(pos['x'], pos['y'], pos['z'])
        
        self.parent_app.log_message("Loaded device positions from saved profile")