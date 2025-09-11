# Overview

This is a unified RGB control application built in Python that provides centralized control for various RGB-enabled gaming hardware components. The application supports multiple device categories including external peripherals (keyboard, mouse) and internal PC components (RAM, GPU, fans, cables). It features a Tkinter-based GUI with 3D visualization capabilities and comprehensive device management through various vendor-specific controllers.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **GUI Framework**: Tkinter for the main application interface with ttk components for modern styling
- **3D Visualization**: OpenGL-based 3D interface using pygame for device placement and RGB visualization
- **Color Management**: Custom color picker integration with HSV/RGB conversion utilities
- **Theme Support**: Dark theme implementation with configurable UI preferences

## Backend Architecture
- **Modular Controller Design**: Separate controller classes for each hardware vendor/protocol
  - OpenRGB for universal device support and ARGB fans
  - Razer Chroma SDK for Razer peripherals
  - Vendor-specific controllers for Lian Li, G.Skill, ASRock, MSI, and Evofox devices
- **Configuration Management**: JSON-based configuration system for profiles and application settings
- **Device Discovery**: Automatic device scanning and detection across multiple protocols
- **Profile System**: Save/load functionality for RGB lighting configurations

## Data Storage
- **Configuration Files**: JSON format for storing application settings and user profiles
- **File Structure**: 
  - `config/settings.json` - Application and device connection settings
  - `config/profiles.json` - User-created RGB lighting profiles
- **No Database**: Simple file-based storage for configuration persistence

## Device Communication Protocols
- **OpenRGB Protocol**: TCP connection (localhost:6742) for universal RGB device control
- **Razer Chroma SDK**: HTTP REST API (localhost:54235) for Razer device integration
- **Native Software Integration**: Detection and control through vendor software (L-Connect, MSI Center, etc.)
- **Windows Registry**: Used for software detection and device enumeration

## 3D Visualization System
- **OpenGL Rendering**: Real-time 3D visualization of device placements
- **Device Models**: Predefined 3D models for common gaming peripherals and PC components
- **Interactive Placement**: Drag-and-drop device positioning in 3D space
- **RGB Zone Mapping**: Visual representation of RGB zones on 3D models

# External Dependencies

## Core Dependencies
- **tkinter**: Built-in Python GUI framework for main application interface
- **pygame**: Game development library used for OpenGL context and input handling
- **OpenGL (PyOpenGL)**: 3D graphics rendering for device visualization
- **openrgb-python**: Python client library for OpenRGB server communication
- **requests**: HTTP client for Razer Chroma SDK REST API calls

## System Dependencies
- **OpenRGB Server**: Must be running locally for universal device control
- **Razer Synapse/Chroma SDK**: Required for Razer device support
- **Vendor Software**: Optional vendor-specific software for enhanced device support
  - Lian Li L-Connect for Strimmer cable control
  - MSI Center/Dragon Center for MSI motherboard RGB
  - ASUS Aura Sync for G.Skill RAM compatibility
  - ASRock Polychrome for GPU RGB control

## Platform Requirements
- **Windows**: Primary target platform with Windows Registry integration
- **Cross-platform Compatibility**: Core functionality designed to work on Linux/macOS with feature limitations
- **Hardware Requirements**: OpenGL-capable graphics for 3D visualization features

## Network Services
- **Local TCP Server**: OpenRGB server on localhost:6742
- **Local HTTP API**: Razer Chroma SDK on localhost:54235
- **No External Services**: All communication is local system-based