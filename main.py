#!/usr/bin/env python3
"""
Unified RGB Control Application
Controls RGB lighting for:
- Lian Li Strimmer cables
- ARGB fans (via motherboard)
- G.Skill AURA RGB RAM
- Evofox Ronin wireless keyboard
- Razer Basilisk mouse
- ASRock Phantom Gaming RX 7900XTX GPU
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, simpledialog
import threading
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from rgb_controllers.openrgb_controller import OpenRGBController
from rgb_controllers.razer_controller import RazerController
from rgb_controllers.lian_li_controller import LianLiController
from rgb_controllers.gskill_controller import GSkillController
from rgb_controllers.evofox_controller import EvofoxController
from rgb_controllers.asrock_controller import ASRockController
from rgb_controllers.msi_controller import MSIController
from utils.config_manager import ConfigManager
from utils.color_utils import ColorUtils
from utils.rgb_3d_interface import RGB3DInterface
from utils.modern_theme import ModernTheme, configure_modern_style, create_modern_button, create_modern_frame, create_rgb_indicator


class RGBControlApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("RGB Control Center")
        self.root.geometry("1200x800")
        self.root.configure(bg=ModernTheme.COLORS['bg_primary'])
        self.root.resizable(True, True)
        
        # Configure modern styling
        try:
            configure_modern_style()
        except Exception as e:
            print(f"Warning: Could not apply modern styling: {e}")
        
        # Set window icon and properties
        try:
            self.root.iconname("RGB Control Center")
        except:
            pass
        
        # Initialize configuration manager
        self.config_manager = ConfigManager()
        
        # Initialize device controllers
        self.controllers = {
            'openrgb': OpenRGBController(),
            'razer': RazerController(),
            'lian_li': LianLiController(),
            'gskill': GSkillController(),
            'evofox': EvofoxController(),
            'asrock': ASRockController(),
            'msi': MSIController()
        }
        
        # Current color state
        self.current_color = (255, 0, 0)  # Default to red
        self.current_effect = "static"
        
        # Device status tracking
        self.device_status = {}
        
        # Initialize 3D interface
        self.rgb_3d_interface = RGB3DInterface(self)
        
        self.setup_ui()
        self.scan_devices()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Create modern header
        self.create_header()
        
        # Create main container with modern layout
        self.create_main_container()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create content frames with modern styling
        self.create_device_frame()
        self.create_color_frame()
        self.create_effects_frame()
        self.create_control_frame()
        self.create_status_frame()
        
    def create_header(self):
        """Create modern header with app title and quick actions"""
        header_frame = tk.Frame(self.root, bg=ModernTheme.COLORS['bg_secondary'], height=60)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # App title and logo area
        title_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['bg_secondary'])
        title_frame.pack(side="left", fill="y", padx=20, pady=10)
        
        title_label = tk.Label(title_frame, 
                              text="RGB Control Center", 
                              font=ModernTheme.FONTS['heading'],
                              bg=ModernTheme.COLORS['bg_secondary'],
                              fg=ModernTheme.COLORS['accent_primary'])
        title_label.pack(side="left")
        
        subtitle_label = tk.Label(title_frame, 
                                 text="Unified Gaming Hardware RGB Control", 
                                 font=ModernTheme.FONTS['small'],
                                 bg=ModernTheme.COLORS['bg_secondary'],
                                 fg=ModernTheme.COLORS['text_secondary'])
        subtitle_label.pack(side="left", padx=(10, 0))
        
        # Quick action buttons in header
        actions_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['bg_secondary'])
        actions_frame.pack(side="right", fill="y", padx=20, pady=10)
        
        create_modern_button(actions_frame, "3D View", 
                           command=self.rgb_3d_interface.open_external_3d_view,
                           style='Secondary.TButton').pack(side="right", padx=(5, 0))
        
        create_modern_button(actions_frame, "Scan Devices", 
                           command=self.scan_devices,
                           style='Success.TButton').pack(side="right", padx=(5, 0))
    
    def create_main_container(self):
        """Create main content container with modern layout"""
        # Main container with padding
        self.main_container = tk.Frame(self.root, bg=ModernTheme.COLORS['bg_primary'])
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel for devices and controls
        self.left_panel = tk.Frame(self.main_container, bg=ModernTheme.COLORS['bg_primary'])
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Right panel for color and effects
        self.right_panel = tk.Frame(self.main_container, bg=ModernTheme.COLORS['bg_primary'])
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root, 
                         bg=ModernTheme.COLORS['bg_secondary'],
                         fg=ModernTheme.COLORS['text_primary'],
                         activebackground=ModernTheme.COLORS['accent_primary'],
                         activeforeground=ModernTheme.COLORS['text_primary'])
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0,
                           bg=ModernTheme.COLORS['bg_secondary'],
                           fg=ModernTheme.COLORS['text_primary'],
                           activebackground=ModernTheme.COLORS['accent_primary'])
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Profile", command=self.load_profile)
        file_menu.add_command(label="Save Profile", command=self.save_profile)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Devices menu
        devices_menu = tk.Menu(menubar, tearoff=0,
                              bg=ModernTheme.COLORS['bg_secondary'],
                              fg=ModernTheme.COLORS['text_primary'],
                              activebackground=ModernTheme.COLORS['accent_primary'])
        menubar.add_cascade(label="Devices", menu=devices_menu)
        devices_menu.add_command(label="Scan Devices", command=self.scan_devices)
        devices_menu.add_command(label="Device Settings", command=self.show_device_settings)
        
        # 3D View menu
        view_3d_menu = tk.Menu(menubar, tearoff=0,
                              bg=ModernTheme.COLORS['bg_secondary'],
                              fg=ModernTheme.COLORS['text_primary'],
                              activebackground=ModernTheme.COLORS['accent_primary'])
        menubar.add_cascade(label="3D View", menu=view_3d_menu)
        view_3d_menu.add_command(label="Gaming Peripherals", command=self.rgb_3d_interface.open_external_3d_view)
        view_3d_menu.add_command(label="Internal Components", command=self.rgb_3d_interface.open_internal_3d_view)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0,
                           bg=ModernTheme.COLORS['bg_secondary'],
                           fg=ModernTheme.COLORS['text_primary'],
                           activebackground=ModernTheme.COLORS['accent_primary'])
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_device_frame(self):
        """Create the device selection frame with modern design"""
        device_frame = create_modern_frame(self.left_panel, "Connected Devices")
        device_frame.pack(fill="x", pady=(0, 15))
        
        # Device list with modern cards
        devices_container = tk.Frame(device_frame, bg=ModernTheme.COLORS['bg_secondary'])
        devices_container.pack(fill="x", padx=15, pady=15)
        
        self.device_vars = {}
        self.device_status_indicators = {}
        
        devices = [
            ("ARGB Fans", "openrgb_fans", ModernTheme.COLORS['rgb_blue']),
            ("MSI Motherboard", "msi", ModernTheme.COLORS['rgb_red']),
            ("Lian Li Strimmer", "lian_li", ModernTheme.COLORS['rgb_purple']),
            ("G.Skill AURA RAM", "gskill", ModernTheme.COLORS['rgb_green']),
            ("Evofox Keyboard", "evofox", ModernTheme.COLORS['rgb_orange']),
            ("Razer Mouse", "razer", ModernTheme.COLORS['rgb_green']),
            ("ASRock GPU", "asrock", ModernTheme.COLORS['rgb_red'])
        ]
        
        for i, (device_name, device_key, color) in enumerate(devices):
            # Device card
            device_card = tk.Frame(devices_container, 
                                 bg=ModernTheme.COLORS['bg_tertiary'],
                                 relief='flat',
                                 bd=1)
            device_card.pack(fill="x", pady=2)
            
            # Status indicator
            indicator = create_rgb_indicator(device_card, size=12)
            indicator.pack(side="left", padx=(10, 8), pady=8)
            self.device_status_indicators[device_key] = indicator
            
            # Device checkbox with modern styling
            var = tk.BooleanVar()
            self.device_vars[device_key] = var
            
            cb = ttk.Checkbutton(device_card, text=device_name, variable=var,
                               style='Modern.TCheckbutton',
                               command=lambda key=device_key: self.update_device_status(key))
            cb.pack(side="left", pady=8)
            
            # Connection status
            status_label = tk.Label(device_card, 
                                  text="Disconnected",
                                  font=ModernTheme.FONTS['small'],
                                  bg=ModernTheme.COLORS['bg_tertiary'],
                                  fg=ModernTheme.COLORS['text_muted'])
            status_label.pack(side="right", padx=(0, 10), pady=8)
            
                
    def create_color_frame(self):
        """Create the color selection frame with modern design"""
        color_frame = create_modern_frame(self.right_panel, "Color Selection")
        color_frame.pack(fill="x", pady=(0, 15))
        
        # Color container
        color_container = tk.Frame(color_frame, bg=ModernTheme.COLORS['bg_secondary'])
        color_container.pack(fill="x", padx=15, pady=15)
        
        # Top row: Color display and picker
        top_row = tk.Frame(color_container, bg=ModernTheme.COLORS['bg_secondary'])
        top_row.pack(fill="x", pady=(0, 15))
        
        # Modern color display
        display_frame = tk.Frame(top_row, bg=ModernTheme.COLORS['bg_tertiary'], relief='flat', bd=1)
        display_frame.pack(side="left", padx=(0, 15))
        
        color_label = tk.Label(display_frame, text="Current Color", 
                              font=ModernTheme.FONTS['small'],
                              bg=ModernTheme.COLORS['bg_tertiary'],
                              fg=ModernTheme.COLORS['text_secondary'])
        color_label.pack(pady=(8, 2))
        
        self.color_display = tk.Canvas(display_frame, width=120, height=60, 
                                     bg="#FF0000", highlightthickness=0)
        self.color_display.pack(padx=10, pady=(0, 8))
        
        # Color picker button
        color_btn = create_modern_button(top_row, "Choose Color", 
                                        command=self.choose_color,
                                        style='Modern.TButton')
        color_btn.pack(side="left")
        
        # RGB Sliders with modern styling
        sliders_frame = tk.Frame(color_container, bg=ModernTheme.COLORS['bg_secondary'])
        sliders_frame.pack(fill="x")
        
        tk.Label(sliders_frame, text="RGB Values", 
                font=ModernTheme.FONTS['subheading'],
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['accent_primary']).pack(anchor="w", pady=(0, 10))
        
        self.rgb_vars = {"R": tk.IntVar(value=255), "G": tk.IntVar(value=0), "B": tk.IntVar(value=0)}
        colors_rgb = [("R", ModernTheme.COLORS['rgb_red']), 
                     ("G", ModernTheme.COLORS['rgb_green']), 
                     ("B", ModernTheme.COLORS['rgb_blue'])]
        
        for color, hex_color in colors_rgb:
            slider_row = tk.Frame(sliders_frame, bg=ModernTheme.COLORS['bg_secondary'])
            slider_row.pack(fill="x", pady=5)
            
            # Color indicator
            indicator = tk.Canvas(slider_row, width=20, height=20, highlightthickness=0)
            indicator.create_oval(2, 2, 18, 18, fill=hex_color, outline=ModernTheme.COLORS['border'])
            indicator.pack(side="left", padx=(0, 10))
            
            # Label
            tk.Label(slider_row, text=f"{color}:", 
                    font=ModernTheme.FONTS['body_bold'],
                    bg=ModernTheme.COLORS['bg_secondary'],
                    fg=ModernTheme.COLORS['text_primary'],
                    width=3).pack(side="left")
            
            # Slider
            var = self.rgb_vars[color]
            scale = ttk.Scale(slider_row, from_=0, to=255, variable=var, 
                            orient="horizontal", length=250)
            scale.pack(side="left", padx=10)
            scale.configure(command=self.on_rgb_change)
            
            # Value display
            value_frame = tk.Frame(slider_row, bg=ModernTheme.COLORS['bg_tertiary'],
                                 relief='flat', bd=1)
            value_frame.pack(side="left", padx=(10, 0))
            
            value_label = tk.Label(value_frame, textvariable=var, 
                                 font=ModernTheme.FONTS['mono'],
                                 bg=ModernTheme.COLORS['bg_tertiary'],
                                 fg=ModernTheme.COLORS['text_primary'],
                                 width=4)
            value_label.pack(padx=8, pady=4)
            
    def create_effects_frame(self):
        """Create the lighting effects frame with modern design"""
        effects_frame = create_modern_frame(self.right_panel, "Lighting Effects")
        effects_frame.pack(fill="x", pady=(0, 15))
        
        # Effects container
        effects_container = tk.Frame(effects_frame, bg=ModernTheme.COLORS['bg_secondary'])
        effects_container.pack(fill="x", padx=15, pady=15)
        
        # Effect selection with modern cards
        self.effect_var = tk.StringVar(value="static")
        effects = ["static", "breathing", "wave", "rainbow", "spectrum_cycle", "reactive"]
        
        tk.Label(effects_container, text="Effect Type", 
                font=ModernTheme.FONTS['subheading'],
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['accent_primary']).pack(anchor="w", pady=(0, 10))
        
        # Effects grid
        effects_grid = tk.Frame(effects_container, bg=ModernTheme.COLORS['bg_secondary'])
        effects_grid.pack(fill="x", pady=(0, 20))
        
        for i, effect in enumerate(effects):
            effect_card = tk.Frame(effects_grid, bg=ModernTheme.COLORS['bg_tertiary'],
                                 relief='flat', bd=1)
            effect_card.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
            
            radio = ttk.Radiobutton(effect_card, text=effect.replace("_", " ").title(),
                                  variable=self.effect_var, value=effect,
                                  style='Modern.TCheckbutton',
                                  command=self.on_effect_change)
            radio.pack(padx=15, pady=10)
        
        # Configure grid weights
        for i in range(3):
            effects_grid.columnconfigure(i, weight=1)
        
        # Parameters section
        params_frame = tk.Frame(effects_container, bg=ModernTheme.COLORS['bg_secondary'])
        params_frame.pack(fill="x")
        
        tk.Label(params_frame, text="Effect Parameters", 
                font=ModernTheme.FONTS['subheading'],
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['accent_primary']).pack(anchor="w", pady=(0, 10))
        
        # Speed control
        speed_row = tk.Frame(params_frame, bg=ModernTheme.COLORS['bg_secondary'])
        speed_row.pack(fill="x", pady=5)
        
        tk.Label(speed_row, text="Speed:", 
                font=ModernTheme.FONTS['body_bold'],
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_primary'],
                width=10).pack(side="left")
        
        self.speed_var = tk.IntVar(value=50)
        speed_scale = ttk.Scale(speed_row, from_=1, to=100, variable=self.speed_var,
                              orient="horizontal", length=250)
        speed_scale.pack(side="left", padx=10)
        
        speed_value = tk.Label(speed_row, textvariable=self.speed_var,
                             font=ModernTheme.FONTS['mono'],
                             bg=ModernTheme.COLORS['bg_tertiary'],
                             fg=ModernTheme.COLORS['text_primary'],
                             width=4, relief='flat', bd=1)
        speed_value.pack(side="left", padx=(10, 0))
        
        # Brightness control
        brightness_row = tk.Frame(params_frame, bg=ModernTheme.COLORS['bg_secondary'])
        brightness_row.pack(fill="x", pady=5)
        
        tk.Label(brightness_row, text="Brightness:", 
                font=ModernTheme.FONTS['body_bold'],
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_primary'],
                width=10).pack(side="left")
        
        self.brightness_var = tk.IntVar(value=100)
        brightness_scale = ttk.Scale(brightness_row, from_=0, to=100, variable=self.brightness_var,
                                   orient="horizontal", length=250)
        brightness_scale.pack(side="left", padx=10)
        
        brightness_value = tk.Label(brightness_row, textvariable=self.brightness_var,
                                   font=ModernTheme.FONTS['mono'],
                                   bg=ModernTheme.COLORS['bg_tertiary'],
                                   fg=ModernTheme.COLORS['text_primary'],
                                   width=4, relief='flat', bd=1)
        brightness_value.pack(side="left", padx=(10, 0))
        
    def create_control_frame(self):
        """Create the control buttons frame with modern design"""
        control_frame = create_modern_frame(self.left_panel, "Quick Actions")
        control_frame.pack(fill="x", pady=(0, 15))
        
        # Control container
        control_container = tk.Frame(control_frame, bg=ModernTheme.COLORS['bg_secondary'])
        control_container.pack(fill="x", padx=15, pady=15)
        
        # Primary actions
        primary_frame = tk.Frame(control_container, bg=ModernTheme.COLORS['bg_secondary'])
        primary_frame.pack(fill="x", pady=(0, 10))
        
        create_modern_button(primary_frame, "Apply to Selected", 
                           command=self.apply_to_selected,
                           style='Modern.TButton').pack(fill="x", pady=2)
        
        create_modern_button(primary_frame, "Apply to All", 
                           command=self.apply_to_all,
                           style='Success.TButton').pack(fill="x", pady=2)
        
        # Secondary actions
        secondary_frame = tk.Frame(control_container, bg=ModernTheme.COLORS['bg_secondary'])
        secondary_frame.pack(fill="x")
        
        buttons_row1 = tk.Frame(secondary_frame, bg=ModernTheme.COLORS['bg_secondary'])
        buttons_row1.pack(fill="x", pady=2)
        
        create_modern_button(buttons_row1, "Turn Off All", 
                           command=self.turn_off_all,
                           style='Warning.TButton').pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        create_modern_button(buttons_row1, "Sync All", 
                           command=self.sync_all,
                           style='Secondary.TButton').pack(side="left", padx=(5, 0), expand=True, fill="x")
        
    def create_status_frame(self):
        """Create the status display frame with modern design"""
        status_frame = create_modern_frame(self.main_container, "System Status")
        status_frame.pack(fill="both", expand=True, pady=(15, 0))
        
        # Status container
        status_container = tk.Frame(status_frame, bg=ModernTheme.COLORS['bg_secondary'])
        status_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Status header with clear button
        header_frame = tk.Frame(status_container, bg=ModernTheme.COLORS['bg_secondary'])
        header_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(header_frame, text="Activity Log", 
                font=ModernTheme.FONTS['subheading'],
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['accent_primary']).pack(side="left")
        
        create_modern_button(header_frame, "Clear Log", 
                           command=self.clear_status,
                           style='Secondary.TButton').pack(side="right")
        
        # Text widget container for border effect
        text_container = tk.Frame(status_container, 
                                bg=ModernTheme.COLORS['border'],
                                relief='flat', bd=1)
        text_container.pack(fill="both", expand=True)
        
        # Modern status text widget
        text_frame = tk.Frame(text_container, bg=ModernTheme.COLORS['bg_tertiary'])
        text_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.status_text = tk.Text(text_frame, 
                                  height=8, 
                                  bg=ModernTheme.COLORS['bg_tertiary'], 
                                  fg=ModernTheme.COLORS['text_primary'],
                                  font=ModernTheme.FONTS['mono'],
                                  insertbackground=ModernTheme.COLORS['accent_primary'],
                                  selectbackground=ModernTheme.COLORS['accent_primary'],
                                  selectforeground=ModernTheme.COLORS['text_primary'],
                                  borderwidth=0,
                                  highlightthickness=0,
                                  wrap=tk.WORD)
        
        # Modern scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", 
                                command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add some initial styled messages
        self.log_message("🚀 RGB Control Center initialized with modern interface")
        self.log_message("✨ Modern theme loaded successfully")
        self.log_message("🎮 Ready for RGB device control")
    
    def clear_status(self):
        """Clear the status log"""
        self.status_text.delete(1.0, tk.END)
        self.log_message("📝 Status log cleared")
        
    def choose_color(self):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(title="Choose RGB Color")
        if color[0]:
            self.current_color = tuple(int(c) for c in color[0])
            self.update_color_display()
            self.update_rgb_sliders()
            
    def on_rgb_change(self, event=None):
        """Handle RGB slider changes"""
        self.current_color = (self.rgb_vars["R"].get(), self.rgb_vars["G"].get(), self.rgb_vars["B"].get())
        self.update_color_display()
        
    def update_color_display(self):
        """Update the color display canvas"""
        hex_color = f"#{self.current_color[0]:02x}{self.current_color[1]:02x}{self.current_color[2]:02x}"
        self.color_display.configure(bg=hex_color)
        
    def update_rgb_sliders(self):
        """Update RGB slider values"""
        self.rgb_vars["R"].set(self.current_color[0])
        self.rgb_vars["G"].set(self.current_color[1])
        self.rgb_vars["B"].set(self.current_color[2])
        
    def on_effect_change(self):
        """Handle effect selection change"""
        self.current_effect = self.effect_var.get()
        self.log_message(f"Effect changed to: {self.current_effect}")
        
    def scan_devices(self):
        """Scan for connected RGB devices"""
        self.log_message("Scanning for RGB devices...")
        
        def scan_thread():
            try:
                # Scan each controller for devices
                for controller_name, controller in self.controllers.items():
                    devices = controller.scan_devices()
                    self.device_status[controller_name] = devices
                    if devices:
                        self.log_message(f"Found {len(devices)} {controller_name} device(s)")
                    else:
                        self.log_message(f"No {controller_name} devices found")
                        
                self.log_message("Device scan completed")
                
            except Exception as e:
                self.log_message(f"Error during device scan: {str(e)}")
                
        threading.Thread(target=scan_thread, daemon=True).start()
        
    def apply_to_selected(self):
        """Apply current settings to selected devices"""
        selected_devices = [device for device, var in self.device_vars.items() if var.get()]
        
        if not selected_devices:
            messagebox.showwarning("No Selection", "Please select at least one device")
            return
            
        self.log_message(f"Applying settings to selected devices: {', '.join(selected_devices)}")
        self._apply_settings(selected_devices)
        
    def apply_to_all(self):
        """Apply current settings to all available devices"""
        all_devices = list(self.device_vars.keys())
        self.log_message("Applying settings to all devices")
        self._apply_settings(all_devices)
        
    def _apply_settings(self, device_list: List[str]):
        """Apply current color and effect settings to specified devices"""
        def apply_thread():
            try:
                settings = {
                    'color': self.current_color,
                    'effect': self.current_effect,
                    'speed': self.speed_var.get(),
                    'brightness': self.brightness_var.get()
                }
                
                for device_key in device_list:
                    controller_name = self._get_controller_for_device(device_key)
                    if controller_name and controller_name in self.controllers:
                        controller = self.controllers[controller_name]
                        success = controller.apply_settings(device_key, settings)
                        if success:
                            self.log_message(f"✓ Applied settings to {device_key}")
                        else:
                            self.log_message(f"✗ Failed to apply settings to {device_key}")
                            
            except Exception as e:
                self.log_message(f"Error applying settings: {str(e)}")
                
        threading.Thread(target=apply_thread, daemon=True).start()
        
    def _get_controller_for_device(self, device_key: str) -> Optional[str]:
        """Map device key to controller name"""
        device_mapping = {
            'openrgb_fans': 'openrgb',
            'msi': 'msi',
            'lian_li': 'lian_li',
            'gskill': 'gskill',
            'evofox': 'evofox',
            'razer': 'razer',
            'asrock': 'asrock'
        }
        return device_mapping.get(device_key)
        
    def turn_off_all(self):
        """Turn off all RGB lighting"""
        self.log_message("Turning off all RGB lighting")
        
        def turn_off_thread():
            try:
                for controller in self.controllers.values():
                    controller.turn_off_all()
                self.log_message("All devices turned off")
            except Exception as e:
                self.log_message(f"Error turning off devices: {str(e)}")
                
        threading.Thread(target=turn_off_thread, daemon=True).start()
        
    def sync_all(self):
        """Synchronize all devices to current settings"""
        self.log_message("Synchronizing all devices")
        all_devices = list(self.device_vars.keys())
        self._apply_settings(all_devices)
        
    def save_profile(self):
        """Save current settings as a profile"""
        profile_name = tk.simpledialog.askstring("Save Profile", "Enter profile name:")
        if profile_name:
            profile_data = {
                'color': self.current_color,
                'effect': self.current_effect,
                'speed': self.speed_var.get(),
                'brightness': self.brightness_var.get(),
                'selected_devices': [device for device, var in self.device_vars.items() if var.get()]
            }
            
            if self.config_manager.save_profile(profile_name, profile_data):
                self.log_message(f"Profile '{profile_name}' saved successfully")
                messagebox.showinfo("Success", f"Profile '{profile_name}' saved")
            else:
                self.log_message(f"Failed to save profile '{profile_name}'")
                messagebox.showerror("Error", "Failed to save profile")
                
    def load_profile(self):
        """Load a saved profile"""
        profiles = self.config_manager.get_profiles()
        if not profiles:
            messagebox.showinfo("No Profiles", "No saved profiles found")
            return
            
        # Create profile selection dialog
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Load Profile")
        profile_window.geometry("300x200")
        
        tk.Label(profile_window, text="Select a profile to load:").pack(pady=10)
        
        profile_var = tk.StringVar()
        profile_listbox = tk.Listbox(profile_window)
        
        for profile_name in profiles:
            profile_listbox.insert(tk.END, profile_name)
            
        profile_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        def load_selected():
            selection = profile_listbox.curselection()
            if selection:
                profile_name = profile_listbox.get(selection[0])
                profile_data = self.config_manager.load_profile(profile_name)
                if profile_data:
                    self._apply_profile(profile_data)
                    self.log_message(f"Profile '{profile_name}' loaded")
                    profile_window.destroy()
                    
        ttk.Button(profile_window, text="Load", command=load_selected).pack(pady=10)
        
    def _apply_profile(self, profile_data: Dict):
        """Apply loaded profile data to UI"""
        # Set color
        self.current_color = tuple(profile_data.get('color', (255, 0, 0)))
        self.update_color_display()
        self.update_rgb_sliders()
        
        # Set effect
        self.effect_var.set(profile_data.get('effect', 'static'))
        self.current_effect = profile_data.get('effect', 'static')
        
        # Set parameters
        self.speed_var.set(profile_data.get('speed', 50))
        self.brightness_var.set(profile_data.get('brightness', 100))
        
        # Set selected devices
        for device, var in self.device_vars.items():
            var.set(device in profile_data.get('selected_devices', []))
            
    def show_device_settings(self):
        """Show device-specific settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Device Settings")
        settings_window.geometry("400x300")
        
        ttk.Label(settings_window, text="Device-specific settings will be implemented here").pack(pady=20)
        
    def show_about(self):
        """Show about dialog"""
        about_text = """
        Unified RGB Control Center
        
        Controls RGB lighting for:
        • ARGB Fans (via motherboard)
        • Lian Li Strimmer cables
        • G.Skill AURA RGB RAM
        • Evofox Ronin wireless keyboard
        • Razer Basilisk mouse
        • ASRock Phantom Gaming RX 7900XTX GPU
        
        Version 1.0
        """
        messagebox.showinfo("About", about_text)
        
    def log_message(self, message: str):
        """Add a message to the status log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.status_text.insert(tk.END, log_entry)
        self.status_text.see(tk.END)
        self.root.update_idletasks()


def main():
    """Main application entry point"""
    try:
        root = tk.Tk()
        app = RGBControlApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Failed to start RGB Control Center: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()