# Plugin Architecture for Effects System

## Overview
Create a modular plugin system that allows anyone to easily add new effects with their own sliders, controls, and UI components. This will make the application extensible and maintainable.

## Core Plugin Architecture

### 1. Plugin Base Classes
```python
# Base classes that all effects must inherit from
- EffectPlugin (base class for all effects)
- EffectUI (base class for UI components)
- EffectParameter (base class for parameters)
```

### 2. Plugin Discovery System
```python
# Automatic plugin discovery and loading
- PluginRegistry (manages all loaded plugins)
- PluginLoader (loads plugins from directories)
- PluginValidator (validates plugin structure)
```

### 3. Plugin Interface
```python
# Standard interface that all plugins must implement
- apply_effect(frame, parameters) -> frame
- get_parameters() -> list of parameters
- get_ui_components() -> list of UI widgets
- get_metadata() -> plugin info
```

## Plugin Structure

### Directory Structure
```
plugins/
├── effects/
│   ├── artistic/
│   │   ├── cartoon_effect/
│   │   │   ├── __init__.py
│   │   │   ├── effect.py
│   │   │   ├── ui.py
│   │   │   └── metadata.json
│   │   └── sketch_effect/
│   ├── adjustments/
│   │   ├── brightness_effect/
│   │   └── contrast_effect/
│   └── filters/
│       ├── blur_effect/
│       └── sharpen_effect/
├── ui_components/
│   ├── custom_sliders/
│   ├── color_pickers/
│   └── parameter_widgets/
└── utils/
    ├── parameter_types.py
    └── ui_helpers.py
```

### Plugin Metadata (metadata.json)
```json
{
    "name": "Cartoon Effect",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "Converts video to cartoon style",
    "category": "artistic",
    "tags": ["cartoon", "artistic", "stylized"],
    "parameters": [
        {
            "name": "edge_strength",
            "type": "slider",
            "min": 0.0,
            "max": 2.0,
            "default": 1.0,
            "step": 0.1,
            "label": "Edge Strength"
        },
        {
            "name": "color_reduction",
            "type": "slider",
            "min": 2,
            "max": 32,
            "default": 8,
            "step": 1,
            "label": "Color Reduction"
        }
    ],
    "ui_components": [
        {
            "type": "slider_group",
            "parameters": ["edge_strength", "color_reduction"]
        }
    ]
}
```

## Implementation Plan

### Phase 1: Core Plugin System
1. **Create base classes**
   - EffectPlugin base class
   - Parameter system
   - UI component system

2. **Plugin registry and loader**
   - Automatic plugin discovery
   - Plugin validation
   - Plugin management

3. **Basic plugin interface**
   - Standard apply method
   - Parameter definition
   - UI component definition

### Phase 2: UI Integration
1. **Dynamic UI generation**
   - Auto-generate sliders from parameters
   - Custom UI component support
   - Parameter validation

2. **Effect management**
   - Effect selection and application
   - Parameter persistence
   - Real-time parameter updates

### Phase 3: Advanced Features
1. **Plugin marketplace**
   - Plugin distribution system
   - Version management
   - Dependency handling

2. **Advanced UI components**
   - Custom widgets
   - Parameter presets
   - Effect chains

## Plugin Development Guide

### Creating a New Effect Plugin

#### 1. Basic Effect Plugin
```python
# plugins/effects/artistic/my_effect/effect.py
from core.plugin_base import EffectPlugin
import cv2
import numpy as np

class MyEffectPlugin(EffectPlugin):
    def __init__(self):
        super().__init__()
        self.name = "My Custom Effect"
        self.description = "A custom effect I created"
        self.category = "artistic"
        
    def apply_effect(self, frame, parameters):
        """Apply the effect to the frame."""
        # Get parameters
        intensity = parameters.get('intensity', 1.0)
        
        # Apply effect
        result = cv2.convertScaleAbs(frame, alpha=intensity, beta=0)
        
        return result
        
    def get_parameters(self):
        """Define the parameters for this effect."""
        return [
            {
                'name': 'intensity',
                'type': 'slider',
                'min': 0.1,
                'max': 3.0,
                'default': 1.0,
                'step': 0.1,
                'label': 'Intensity'
            }
        ]
```

#### 2. Custom UI Components
```python
# plugins/effects/artistic/my_effect/ui.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from core.ui_base import EffectUI

class MyEffectUI(EffectUI):
    def __init__(self, effect_plugin):
        super().__init__(effect_plugin)
        
    def create_ui_components(self):
        """Create custom UI components."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Create intensity slider
        intensity_slider = QSlider()
        intensity_slider.setRange(10, 300)  # 0.1 to 3.0 * 100
        intensity_slider.setValue(100)  # Default 1.0
        
        intensity_label = QLabel("Intensity: 1.0")
        
        # Connect slider to parameter update
        intensity_slider.valueChanged.connect(
            lambda value: self.update_parameter('intensity', value / 100.0)
        )
        
        layout.addWidget(intensity_label)
        layout.addWidget(intensity_slider)
        widget.setLayout(layout)
        
        return widget
```

#### 3. Plugin Registration
```python
# plugins/effects/artistic/my_effect/__init__.py
from .effect import MyEffectPlugin
from .ui import MyEffectUI

def register_plugin(registry):
    """Register this plugin with the registry."""
    plugin = MyEffectPlugin()
    ui = MyEffectUI(plugin)
    registry.register_plugin(plugin, ui)
```

## Integration with Main Application

### 1. Plugin Manager Integration
```python
# In main window
class ProfessionalV2MainWindow(QMainWindow):
    def __init__(self):
        # ... existing code ...
        
        # Initialize plugin system
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        
        # Create effect UI from plugins
        self.effect_ui_manager = EffectUIManager(self.plugin_manager)
        self.effect_ui_manager.create_effect_buttons()
```

### 2. Dynamic Effect Application
```python
# In preview manager
def apply_current_effect(self, frame):
    """Apply the currently selected effect."""
    if hasattr(self.main_window, 'current_effect_plugin'):
        plugin = self.main_window.current_effect_plugin
        parameters = self.main_window.current_effect_parameters
        
        if plugin:
            return plugin.apply_effect(frame, parameters)
    
    return frame
```

## Benefits of This Architecture

### 1. **Extensibility**
- Anyone can create new effects without modifying core code
- Plugins can be distributed independently
- Easy to add new parameter types and UI components

### 2. **Maintainability**
- Clear separation between effects and core application
- Standardized interface makes debugging easier
- Version control for individual plugins

### 3. **User Experience**
- Dynamic UI generation based on effect parameters
- Consistent interface across all effects
- Easy parameter adjustment and real-time preview

### 4. **Developer Experience**
- Simple plugin creation process
- Rich documentation and examples
- Built-in validation and error handling

## Migration Strategy

### Phase 1: Create Plugin Infrastructure
1. Create base classes and plugin system
2. Convert 2-3 existing effects to plugin format
3. Test plugin loading and application

### Phase 2: UI Integration
1. Create dynamic UI generation system
2. Integrate with existing effect manager
3. Test parameter updates and real-time preview

### Phase 3: Full Migration
1. Convert all existing effects to plugins
2. Remove old effect system
3. Add advanced plugin features

This architecture will make your application much more powerful and user-friendly, while also making it easy for the community to contribute new effects! 