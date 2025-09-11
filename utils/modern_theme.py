"""
Modern Theme and Styling for RGB Control Center
"""

import tkinter as tk
from tkinter import ttk


class ModernTheme:
    """Modern dark theme configuration"""
    
    # Color Palette
    COLORS = {
        'bg_primary': '#1a1a1a',      # Main background
        'bg_secondary': '#2d2d2d',    # Secondary backgrounds
        'bg_tertiary': '#3d3d3d',     # Card backgrounds
        'bg_hover': '#4d4d4d',        # Hover states
        'accent_primary': '#00d4ff',   # Primary accent (cyan)
        'accent_secondary': '#ff6b6b', # Secondary accent (red)
        'accent_success': '#51cf66',   # Success green
        'accent_warning': '#ffd43b',   # Warning yellow
        'text_primary': '#ffffff',     # Primary text
        'text_secondary': '#b8b8b8',   # Secondary text
        'text_muted': '#6c757d',       # Muted text
        'border': '#404040',           # Borders
        'shadow': '#000000',           # Shadows
        'rgb_red': '#ff4757',
        'rgb_green': '#2ed573',
        'rgb_blue': '#5352ed',
        'rgb_purple': '#a55eea',
        'rgb_orange': '#ffa502',
        'rgb_pink': '#ff3838'
    }
    
    # Typography
    FONTS = {
        'heading': ('Segoe UI', 16, 'bold'),
        'subheading': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'body_bold': ('Segoe UI', 10, 'bold'),
        'small': ('Segoe UI', 8),
        'mono': ('Consolas', 9)
    }
    
    # Dimensions
    DIMENSIONS = {
        'padding_large': 20,
        'padding_medium': 15,
        'padding_small': 10,
        'padding_tiny': 5,
        'border_radius': 8,
        'button_height': 35,
        'frame_relief': 'flat'
    }


def configure_modern_style():
    """Configure ttk styles for modern appearance"""
    style = ttk.Style()
    
    # Configure theme
    style.theme_use('clam')
    
    # Configure colors
    colors = ModernTheme.COLORS
    
    # Configure default styles
    style.configure('.',
                   background=colors['bg_primary'],
                   foreground=colors['text_primary'],
                   borderwidth=0,
                   focuscolor='none')
    
    # Modern Button Style
    style.configure('Modern.TButton',
                   background=colors['accent_primary'],
                   foreground=colors['text_primary'],
                   borderwidth=0,
                   focuscolor='none',
                   font=ModernTheme.FONTS['body_bold'],
                   padding=(15, 8))
    
    style.map('Modern.TButton',
             background=[('active', colors['bg_hover']),
                        ('pressed', colors['accent_secondary'])])
    
    # Secondary Button Style
    style.configure('Secondary.TButton',
                   background=colors['bg_secondary'],
                   foreground=colors['text_primary'],
                   borderwidth=1,
                   relief='solid',
                   bordercolor=colors['border'],
                   font=ModernTheme.FONTS['body'],
                   padding=(12, 6))
    
    style.map('Secondary.TButton',
             background=[('active', colors['bg_hover']),
                        ('pressed', colors['bg_primary'])])
    
    # Success Button Style
    style.configure('Success.TButton',
                   background=colors['accent_success'],
                   foreground=colors['text_primary'],
                   borderwidth=0,
                   font=ModernTheme.FONTS['body_bold'],
                   padding=(12, 6))
    
    # Warning Button Style
    style.configure('Warning.TButton',
                   background=colors['accent_warning'],
                   foreground=colors['bg_primary'],
                   borderwidth=0,
                   font=ModernTheme.FONTS['body_bold'],
                   padding=(12, 6))
    
    # Modern Frame Style
    style.layout('Modern.TLabelFrame', [
        ('Labelframe.border', {'sticky': 'nswe'}),
        ('Labelframe.label', {'sticky': 'ew'})
    ])
    
    style.configure('Modern.TLabelFrame',
                   background=colors['bg_secondary'],
                   foreground=colors['text_primary'],
                   borderwidth=1,
                   relief='solid',
                   bordercolor=colors['border'])
    
    style.configure('Modern.TLabelFrame.Label',
                   background=colors['bg_secondary'],
                   foreground=colors['accent_primary'],
                   font=ModernTheme.FONTS['subheading'])
    
    # Card Frame Style
    style.configure('Card.TFrame',
                   background=colors['bg_tertiary'],
                   borderwidth=1,
                   relief='solid',
                   bordercolor=colors['border'])
    
    # Modern Checkbutton Style
    style.configure('Modern.TCheckbutton',
                   background=colors['bg_secondary'],
                   foreground=colors['text_primary'],
                   focuscolor='none',
                   font=ModernTheme.FONTS['body'])
    
    style.map('Modern.TCheckbutton',
             background=[('active', colors['bg_hover'])])
    
    # Modern Scale Style - use default scale with color modifications
    style.configure('TScale',
                   background=colors['bg_secondary'],
                   troughcolor=colors['bg_primary'],
                   borderwidth=0)
    
    style.map('TScale',
             background=[('active', colors['accent_primary'])])
    
    # Modern Combobox Style
    style.configure('Modern.TCombobox',
                   background=colors['bg_tertiary'],
                   foreground=colors['text_primary'],
                   fieldbackground=colors['bg_tertiary'],
                   borderwidth=1,
                   bordercolor=colors['border'],
                   font=ModernTheme.FONTS['body'])
    
    # Modern Notebook Style
    style.configure('Modern.TNotebook',
                   background=colors['bg_primary'],
                   borderwidth=0)
    
    style.configure('Modern.TNotebook.Tab',
                   background=colors['bg_secondary'],
                   foreground=colors['text_secondary'],
                   padding=(20, 10),
                   font=ModernTheme.FONTS['body'])
    
    style.map('Modern.TNotebook.Tab',
             background=[('selected', colors['accent_primary']),
                        ('active', colors['bg_hover'])],
             foreground=[('selected', colors['text_primary'])])
    
    # Modern Treeview Style
    style.configure('Modern.Treeview',
                   background=colors['bg_tertiary'],
                   foreground=colors['text_primary'],
                   fieldbackground=colors['bg_tertiary'],
                   borderwidth=0,
                   font=ModernTheme.FONTS['body'])
    
    style.configure('Modern.Treeview.Heading',
                   background=colors['bg_secondary'],
                   foreground=colors['text_primary'],
                   font=ModernTheme.FONTS['body_bold'])
    
    # Progressbar Style
    style.configure('RGB.TProgressbar',
                   background=colors['accent_primary'],
                   troughcolor=colors['bg_primary'],
                   borderwidth=0,
                   lightcolor=colors['accent_primary'],
                   darkcolor=colors['accent_primary'])


def create_modern_button(parent, text, command=None, style='Modern.TButton', **kwargs):
    """Create a modern styled button"""
    return ttk.Button(parent, text=text, command=command, style=style, **kwargs)


def create_modern_frame(parent, title=None, style='Modern.TLabelFrame', **kwargs):
    """Create a modern styled frame"""
    try:
        if title:
            return ttk.LabelFrame(parent, text=title, style=style, **kwargs)
        else:
            return ttk.Frame(parent, style='Card.TFrame', **kwargs)
    except tk.TclError:
        # Fallback to standard styling if modern style fails
        if title:
            frame = ttk.LabelFrame(parent, text=title, **kwargs)
            frame.configure(background=ModernTheme.COLORS['bg_secondary'])
            return frame
        else:
            frame = ttk.Frame(parent, **kwargs)
            frame.configure(background=ModernTheme.COLORS['bg_tertiary'])
            return frame


def create_gradient_canvas(parent, width, height, color1, color2, direction='horizontal'):
    """Create a gradient background canvas"""
    canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
    
    if direction == 'horizontal':
        for i in range(width):
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * i / width)
            g = int(g1 + (g2 - g1) * i / width)
            b = int(b1 + (b2 - b1) * i / width)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(i, 0, i, height, fill=color, width=1)
    
    return canvas


def add_hover_effect(widget, enter_color, leave_color):
    """Add hover effect to widgets"""
    def on_enter(event):
        widget.configure(background=enter_color)
    
    def on_leave(event):
        widget.configure(background=leave_color)
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


def create_rgb_indicator(parent, color=(255, 0, 0), size=20):
    """Create an RGB color indicator"""
    canvas = tk.Canvas(parent, width=size, height=size, highlightthickness=0)
    hex_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
    canvas.create_oval(2, 2, size-2, size-2, fill=hex_color, outline=ModernTheme.COLORS['border'])
    return canvas