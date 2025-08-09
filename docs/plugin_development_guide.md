# Plugin Development Guide

This guide explains how to create plugins for the me-tuber application using the advanced plugin system.

## Table of Contents

1. [Overview](#overview)
2. [Plugin Structure](#plugin-structure)
3. [Creating an Effect Plugin](#creating-an-effect-plugin)
4. [Parameter Types](#parameter-types)
5. [Creating UI Components](#creating-ui-components)
6. [Dynamic Dependencies](#dynamic-dependencies)
7. [Professional Styling](#professional-styling)
8. [Best practice-projects-projectss](#best-practice-projects-projectss)
9. [Testing Your Plugin](#testing-your-plugin)

## Overview

The plugin system provides a comprehensive framework for creating effects with:
- **Multiple Parameter Types**: int, float, bool, str, file, color
- **Dynamic UI**: Show/hide logic for dependent parameters
- **Professional Styling**: Automatic dark theme inheritance
- **Grouped Parameters**: Organized by category
- **File Integration**: Texture overlays and file pickers
- **Color Customization**: Advanced color pickers with RGB controls

## Plugin Structure

Each plugin should have the following structure:

```
src/plugins/effects/[category]/[plugin_name]/
├── __init__.py          # Plugin registration
├── effect.py            # Effect implementation
└── ui.py               # UI component (optional)
```

## Creating an Effect Plugin

### Basic Plugin Template

```python
from src.plugins.plugin_base import EffectPlugin
from typing import Dict, Any, Optional
import cv2
import numpy as np

class MyEffectPlugin(EffectPlugin):
    """My custom effect plugin."""
    
    def __init__(self):
        super().__init__(
            name="My Effect",
            category="Artistic",
            description="Description of my effect"
        )
        
        # Define parameters
        self.parameters = {
            'intensity': {
                'type': 'int',
                'default': 50,
                'min': 0,
                'max': 100,
                'step': 5,
                'label': 'Effect Intensity',
                'description': 'Overall strength of the effect',
                'category': 'Basic'
            }
        }
    
    def apply(self, frame, parameters: Optional[Dict[str, Any]] = None):
        """Apply the effect to a frame."""
        if parameters is None:
            parameters = self.parameters
        
        # Extract parameters
        intensity = parameters.get('intensity', 50) / 100.0
        
        # Apply effect logic here
        result = self._apply_effect(frame, intensity)
        
        return result
    
    def _apply_effect(self, frame, intensity):
        """Apply the core effect logic."""
        # Your effect implementation here
        return frame
```

## Parameter Types

### Integer Sliders

```python
'intensity': {
    'type': 'int',
    'default': 50,
    'min': 0,
    'max': 100,
    'step': 5,
    'label': 'Effect Intensity',
    'description': 'Overall strength of the effect',
    'category': 'Basic'
}
```

### Float Controls (Slider + Spinbox)

```python
'smoothness': {
    'type': 'float',
    'default': 0.7,
    'min': 0.1,
    'max': 1.0,
    'step': 0.05,
    'decimals': 2,
    'label': 'Smoothness',
    'description': 'Smoothing level',
    'category': 'Basic'
}
```

### Boolean Checkboxes

```python
'enable_feature': {
    'type': 'bool',
    'default': False,
    'label': 'Enable Feature',
    'description': 'Enable advanced feature',
    'category': 'Advanced'
}
```

### String Dropdowns

```python
'color_mode': {
    'type': 'str',
    'default': 'Auto',
    'options': ['Auto', 'Custom', 'Monochrome'],
    'label': 'Color Mode',
    'description': 'Color processing mode',
    'category': 'Color'
}
```

### File Pickers

```python
'texture_file': {
    'type': 'file',
    'default': '',
    'label': 'Texture File',
    'description': 'Select texture image file',
    'file_filter': 'Image Files (*.png *.jpg *.jpeg *.bmp)',
    'category': 'Advanced'
}
```

### Color Pickers

```python
'custom_color': {
    'type': 'color',
    'default': {'r': 255, 'g': 200, 'b': 150},
    'label': 'Custom Color',
    'description': 'Custom color for the effect',
    'category': 'Color'
}
```

## Creating UI Components

### Basic UI Template

```python
from src.plugins.plugin_base import EffectUI
from .effect import MyEffectPlugin

class MyEffectUI(EffectUI):
    """UI for My Effect Plugin."""
    
    def __init__(self, plugin: MyEffectPlugin):
        super().__init__(plugin)
        
        # Setup dynamic dependencies
        self.setup_dependencies()
    
    def setup_dependencies(self):
        """Setup dynamic parameter dependencies."""
        # Show texture file picker only when texture is enabled
        self.add_dependency("enable_texture", "texture_file", {"type": "is_true"})
        
        # Show custom color picker only when color mode is "Custom"
        self.add_dependency("color_mode", "custom_color", {"type": "equals", "value": "Custom"})
```

### Custom Styling

```python
def init_ui(self):
    """Initialize the UI with custom layout."""
    super().init_ui()
    
    # Add custom styling
    self.setObjectName("myEffectUI")
    self.setStyleSheet(self.styleSheet() + """
        #myEffectUI {
            background-color: #2a2a2a;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 8px;
        }
    """)
```

## Dynamic Dependencies

The plugin system supports dynamic show/hide logic for parameters based on other parameter values.

### Dependency Types

```python
# Show when parameter is true
self.add_dependency("enable_feature", "feature_param", {"type": "is_true"})

# Show when parameter equals specific value
self.add_dependency("color_mode", "custom_color", {"type": "equals", "value": "Custom"})

# Show when parameter is not equal to value
self.add_dependency("color_mode", "saturation", {"type": "not_equals", "value": "Monochrome"})

# Show when parameter is greater than value
self.add_dependency("intensity", "advanced_param", {"type": "greater_than", "value": 50})

# Show when parameter is less than value
self.add_dependency("intensity", "basic_param", {"type": "less_than", "value": 30})

# Show when parameter contains text
self.add_dependency("text_param", "related_param", {"type": "contains", "value": "special"})
```

### Condition Types

- `is_true`: Show when boolean parameter is True
- `is_false`: Show when boolean parameter is False
- `equals`: Show when parameter equals specific value
- `not_equals`: Show when parameter is not equal to value
- `contains`: Show when string parameter contains text
- `greater_than`: Show when numeric parameter is greater than value
- `less_than`: Show when numeric parameter is less than value

## Professional Styling

All plugins automatically inherit professional dark theme styling:

- **Dark Background**: `#2d2d2d` main background
- **Accent Color**: `#0096ff` blue accent
- **Professional Controls**: Styled sliders, buttons, dropdowns
- **Hover Effects**: Visual feedback on interaction
- **Consistent Spacing**: Proper margins and padding

### Custom Styling

You can add custom styling to your plugin:

```python
def apply_custom_styling(self):
    """Apply custom styling to the plugin."""
    self.setStyleSheet("""
        QGroupBox {
            background-color: #333;
            border: 1px solid #555;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            color: #0096ff;
            font-weight: bold;
            font-size: 10pt;
        }
    """)
```

## Best practice-projects-projectss

### 1. Parameter Organization

Group parameters by category for better organization:

```python
self.parameters = {
    # Basic Parameters
    'intensity': {'category': 'Basic', ...},
    'smoothness': {'category': 'Basic', ...},
    
    # Advanced Parameters
    'enable_feature': {'category': 'Advanced', ...},
    'advanced_param': {'category': 'Advanced', ...},
    
    # Color Parameters
    'color_mode': {'category': 'Color', ...},
    'custom_color': {'category': 'Color', ...},
}
```

### 2. Error Handling

Always include proper error handling in your effect:

```python
def apply(self, frame, parameters=None):
    """Apply the effect to a frame."""
    try:
        # Your effect logic here
        return result
    except Exception as e:
        self.logger.error(f"Error applying effect: {e}")
        return frame  # Return original frame on error
```

### 3. Performance Optimization

- Use efficient OpenCV operations
- Avoid unnecessary array copies
- Cache expensive computations
- Use appropriate data types

### 4. Documentation

- Provide clear parameter descriptions
- Include usage examples
- Document any special requirements
- Add comments to complex logic

## Testing Your Plugin

### 1. Create a Test Script

```python
# test_my_plugin.py
import sys
import cv2
import numpy as np

# Add project root to path
sys.path.insert(0, '.')

from src.plugins.effects.artistic.my_effect.effect import MyEffectPlugin

def test_plugin():
    """Test the plugin with a sample image."""
    # Create plugin
    plugin = MyEffectPlugin()
    
    # Create test image
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Test with default parameters
    result = plugin.apply(test_image)
    
    print(f"Plugin '{plugin.name}' loaded successfully")
    print(f"Parameters: {plugin.parameters}")
    print(f"Result shape: {result.shape}")
    
    return True

if __name__ == "__main__":
    test_plugin()
```

### 2. Test UI Components

```python
# test_ui.py
import sys
from PyQt5.QtWidgets import QApplication

from src.plugins.effects.artistic.my_effect.effect import MyEffectPlugin
from src.plugins.effects.artistic.my_effect.ui import MyEffectUI

def test_ui():
    """Test the plugin UI."""
    app = QApplication(sys.argv)
    
    # Create plugin and UI
    plugin = MyEffectPlugin()
    ui = MyEffectUI(plugin)
    
    # Show UI
    ui.show()
    
    return app.exec_()

if __name__ == "__main__":
    test_ui()
```

### 3. Integration Testing

Test your plugin with the main application:

```python
# test_integration.py
from src.plugins.plugin_manager import PluginManager

def test_integration():
    """Test plugin integration with main application."""
    manager = PluginManager()
    
    # Load all plugins
    plugins = manager.get_all_plugins()
    
    # Find your plugin
    my_plugin = None
    for plugin in plugins:
        if plugin.name == "My Effect":
            my_plugin = plugin
            break
    
    if my_plugin:
        print(f"Plugin '{my_plugin.name}' loaded successfully")
        
        # Test UI creation
        ui = manager.get_effect_ui(my_plugin.name)
        if ui:
            print("UI created successfully")
        else:
            print("Failed to create UI")
    else:
        print("Plugin not found")

if __name__ == "__main__":
    test_integration()
```

## Plugin Registration

Create an `__init__.py` file to register your plugin:

```python
"""
My Effect Plugin Registration
"""

from .effect import MyEffectPlugin
from .ui import MyEffectUI

def register_plugin():
    """Register the my effect plugin."""
    plugin = MyEffectPlugin()
    return plugin
```

## Advanced Features

### 1. Custom Parameter Validation

```python
def validate_parameters(self, parameters):
    """Validate parameter values."""
    if 'intensity' in parameters:
        if not 0 <= parameters['intensity'] <= 100:
            raise ValueError("Intensity must be between 0 and 100")
    return parameters
```

### 2. Parameter Presets

```python
def get_presets(self):
    """Get predefined parameter presets."""
    return {
        'subtle': {'intensity': 25, 'smoothness': 0.5},
        'normal': {'intensity': 50, 'smoothness': 0.7},
        'strong': {'intensity': 75, 'smoothness': 0.9}
    }
```

### 3. Real-time Preview

```python
def get_preview_parameters(self):
    """Get parameters optimized for real-time preview."""
    return {
        'intensity': 30,  # Lower for performance
        'smoothness': 0.5,
        'enable_feature': False  # Disable heavy features
    }
```

This guide provides everything you need to create professional plugins for the me-tuber application. The plugin system is designed to be flexible, powerful, and easy to use while maintaining the beautiful GUI that makes the application stand out. 