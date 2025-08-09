# Plugin Integration Guide

This guide explains how to integrate the advanced plugin system with the main me-tuber application.

## Table of Contents

1. [Overview](#overview)
2. [Integration Architecture](#integration-architecture)
3. [Main Application Integration](#main-application-integration)
4. [Plugin Manager Integration](#plugin-manager-integration)
5. [UI Integration](#ui-integration)
6. [Real-time Processing](#real-time-processing)
7. [Performance Optimization](#performance-optimization)
8. [Testing Integration](#testing-integration)

## Overview

The plugin system integrates seamlessly with the main application through:

- **Plugin Manager**: Centralized plugin discovery and management
- **UI Integration**: Automatic parameter panel generation
- **Real-time Processing**: Live effect application to webcam feed
- **Professional Styling**: Consistent dark theme across all plugins
- **Performance Optimization**: Efficient parameter handling and caching

## Integration Architecture

```
Main Application
├── Plugin Manager
│   ├── Plugin Discovery
│   ├── Plugin Loading
│   └── Plugin Registry
├── UI Components
│   ├── Parameter Panel
│   ├── Effect Selector
│   └── Preview Area
└── Processing Pipeline
    ├── Webcam Capture
    ├── Effect Application
    └── Display Output
```

## Main Application Integration

### 1. Update Main Window

Update your main window to use the plugin system:

```python
# src/gui/v2_main_window.py
from src.plugins.plugin_manager import PluginManager
from src.plugins.plugin_base import EffectUI

class ProfessionalV2MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize plugin manager
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        
        # Setup UI
        self.setup_ui()
        self.setup_plugin_integration()
    
    def setup_plugin_integration(self):
        """Setup plugin integration with the main application."""
        # Create effect selector
        self.effect_selector = self.create_effect_selector()
        
        # Create parameter panel
        self.parameter_panel = self.create_parameter_panel()
        
        # Connect signals
        self.effect_selector.currentTextChanged.connect(self.on_effect_changed)
    
    def create_effect_selector(self):
        """Create dropdown for effect selection."""
        selector = QComboBox()
        selector.setObjectName("effectSelector")
        
        # Add "No Effect" option
        selector.addItem("No Effect")
        
        # Add all available effects
        plugins = self.plugin_manager.get_all_plugins()
        for plugin in plugins:
            selector.addItem(plugin.name)
        
        return selector
    
    def create_parameter_panel(self):
        """Create panel for effect parameters."""
        panel = QWidget()
        panel.setObjectName("parameterPanel")
        
        # Create scrollable layout
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Create container widget
        container = QWidget()
        self.parameter_layout = QVBoxLayout(container)
        self.parameter_layout.setContentsMargins(8, 8, 8, 8)
        self.parameter_layout.setSpacing(6)
        
        scroll.setWidget(container)
        
        # Add to panel
        panel_layout = QVBoxLayout(panel)
        panel_layout.addWidget(scroll)
        
        return panel
    
    def on_effect_changed(self, effect_name):
        """Handle effect selection change."""
        # Clear current parameter UI
        self.clear_parameter_ui()
        
        if effect_name == "No Effect":
            self.current_effect = None
            return
        
        # Get selected plugin
        plugin = self.plugin_manager.get_plugin_by_name(effect_name)
        if plugin:
            self.current_effect = plugin
            
            # Create and add parameter UI
            ui = self.plugin_manager.get_effect_ui(effect_name)
            if ui:
                self.parameter_layout.addWidget(ui)
                
                # Connect parameter changes
                ui.parameter_changed.connect(self.on_parameter_changed)
    
    def clear_parameter_ui(self):
        """Clear the parameter UI panel."""
        while self.parameter_layout.count():
            child = self.parameter_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def on_parameter_changed(self, param_name, value):
        """Handle parameter value changes."""
        if self.current_effect:
            # Update effect parameters
            self.current_effect.set_parameters({param_name: value})
            
            # Trigger preview update
            self.update_preview()
    
    def update_preview(self):
        """Update the preview with current effect and parameters."""
        if self.current_effect and self.current_frame is not None:
            # Apply effect to current frame
            parameters = self.current_effect.get_parameters()
            processed_frame = self.current_effect.apply(self.current_frame, parameters)
            
            # Update preview display
            self.update_preview_display(processed_frame)
```

### 2. Webcam Integration

Integrate plugins with the webcam processing pipeline:

```python
# src/services/webcam_service.py
from src.plugins.plugin_manager import PluginManager

class WebcamService:
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.current_effect = None
        self.effect_parameters = {}
    
    def set_effect(self, effect_name):
        """Set the current effect."""
        if effect_name == "No Effect":
            self.current_effect = None
        else:
            self.current_effect = self.plugin_manager.get_plugin_by_name(effect_name)
    
    def set_effect_parameters(self, parameters):
        """Set parameters for the current effect."""
        self.effect_parameters = parameters
    
    def process_frame(self, frame):
        """Process a frame with the current effect."""
        if self.current_effect and frame is not None:
            try:
                return self.current_effect.apply(frame, self.effect_parameters)
            except Exception as e:
                logging.error(f"Error applying effect: {e}")
                return frame
        return frame
```

## Plugin Manager Integration

### 1. Enhanced Plugin Manager

```python
# src/plugins/plugin_manager.py
class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.plugin_uis = {}
        self.loader = PluginLoader()
        self.registry = PluginRegistry()
    
    def load_plugins(self):
        """Load all available plugins."""
        plugin_paths = [
            "src/plugins/effects/artistic",
            "src/plugins/effects/adjustments",
            "src/plugins/effects/filters"
        ]
        
        for path in plugin_paths:
            self.loader.load_plugins_from_directory(path, self.registry)
        
        # Get all loaded plugins
        self.plugins = self.registry.get_all_plugins()
        
        # Create UI components
        self.create_plugin_uis()
    
    def create_plugin_uis(self):
        """Create UI components for all plugins."""
        for plugin_id, plugin in self.plugins.items():
            try:
                # Try to create custom UI
                ui = self.create_plugin_ui(plugin)
                if ui:
                    self.plugin_uis[plugin_id] = ui
                else:
                    # Fallback to default UI
                    from src.plugins.plugin_base import EffectUI
                    ui = EffectUI(plugin)
                    self.plugin_uis[plugin_id] = ui
            except Exception as e:
                logging.error(f"Failed to create UI for {plugin.name}: {e}")
    
    def create_plugin_ui(self, plugin):
        """Create custom UI for a plugin."""
        try:
            # Try to import custom UI class
            plugin_module = plugin.__class__.__module__
            ui_module_name = plugin_module.replace('.effect', '.ui')
            
            # Import UI module
            ui_module = __import__(ui_module_name, fromlist=[''])
            
            # Find UI class (convention: PluginName + "UI")
            ui_class_name = plugin.__class__.__name__.replace('Plugin', 'UI')
            ui_class = getattr(ui_module, ui_class_name, None)
            
            if ui_class:
                return ui_class(plugin)
        except Exception as e:
            logging.debug(f"No custom UI for {plugin.name}: {e}")
        
        return None
    
    def get_all_plugins(self):
        """Get all loaded plugins."""
        return list(self.plugins.values())
    
    def get_plugin_by_name(self, name):
        """Get plugin by name."""
        for plugin in self.plugins.values():
            if plugin.name == name:
                return plugin
        return None
    
    def get_effect_ui(self, effect_name):
        """Get UI component for an effect."""
        plugin = self.get_plugin_by_name(effect_name)
        if plugin:
            plugin_id = self.registry.get_plugin_id(plugin)
            return self.plugin_uis.get(plugin_id)
        return None
    
    def get_plugin_categories(self):
        """Get all plugin categories."""
        categories = set()
        for plugin in self.plugins.values():
            categories.add(plugin.category)
        return sorted(list(categories))
    
    def get_plugins_by_category(self, category):
        """Get plugins by category."""
        return [p for p in self.plugins.values() if p.category == category]
```

## UI Integration

### 1. Parameter Panel Styling

```python
# src/gui/components/parameter_panel.py
class ParameterPanel(QWidget):
    def __init__(self, plugin_manager):
        super().__init__()
        self.plugin_manager = plugin_manager
        self.current_ui = None
        
        self.setup_ui()
        self.apply_styling()
    
    def setup_ui(self):
        """Setup the parameter panel UI."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create container widget
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(8, 8, 8, 8)
        self.container_layout.setSpacing(6)
        
        self.scroll_area.setWidget(self.container)
        self.layout.addWidget(self.scroll_area)
    
    def apply_styling(self):
        """Apply professional styling to the parameter panel."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            
            QScrollArea {
                border: none;
                background-color: #2d2d2d;
            }
            
            QScrollBar:vertical {
                background-color: #444;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #666;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #888;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
    
    def set_effect(self, effect_name):
        """Set the current effect and display its parameters."""
        # Clear current UI
        self.clear_current_ui()
        
        if effect_name == "No Effect":
            self.show_no_effect_message()
            return
        
        # Get effect UI
        ui = self.plugin_manager.get_effect_ui(effect_name)
        if ui:
            self.current_ui = ui
            self.container_layout.addWidget(ui)
            
            # Connect parameter changes
            ui.parameter_changed.connect(self.on_parameter_changed)
        else:
            self.show_error_message(f"Failed to load UI for {effect_name}")
    
    def clear_current_ui(self):
        """Clear the current parameter UI."""
        if self.current_ui:
            self.current_ui.parameter_changed.disconnect()
            self.current_ui.deleteLater()
            self.current_ui = None
        
        # Clear container layout
        while self.container_layout.count():
            child = self.container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def show_no_effect_message(self):
        """Show message when no effect is selected."""
        message = QLabel("No effect selected")
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                color: #888;
                font-style: italic;
                padding: 20px;
            }
        """)
        self.container_layout.addWidget(message)
    
    def show_error_message(self, text):
        """Show error message."""
        message = QLabel(f"Error: {text}")
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                color: #ff6b6b;
                font-style: italic;
                padding: 20px;
            }
        """)
        self.container_layout.addWidget(message)
    
    def on_parameter_changed(self, param_name, value):
        """Handle parameter value changes."""
        # Emit signal to main application
        self.parameter_changed.emit(param_name, value)
```

### 2. Effect Selector Integration

```python
# src/gui/components/effect_selector.py
class EffectSelector(QWidget):
    def __init__(self, plugin_manager):
        super().__init__()
        self.plugin_manager = plugin_manager
        
        self.setup_ui()
        self.populate_effects()
    
    def setup_ui(self):
        """Setup the effect selector UI."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        
        # Title
        title = QLabel("Effects")
        title.setObjectName("effectSelectorTitle")
        self.layout.addWidget(title)
        
        # Effect combo box
        self.effect_combo = QComboBox()
        self.effect_combo.setObjectName("effectSelector")
        self.effect_combo.addItem("No Effect")
        self.layout.addWidget(self.effect_combo)
        
        # Category filter
        self.category_combo = QComboBox()
        self.category_combo.setObjectName("categoryFilter")
        self.category_combo.addItem("All Categories")
        self.layout.addWidget(self.category_combo)
        
        # Connect signals
        self.effect_combo.currentTextChanged.connect(self.on_effect_changed)
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
    
    def populate_effects(self):
        """Populate the effect selector with available effects."""
        # Get all categories
        categories = self.plugin_manager.get_plugin_categories()
        for category in categories:
            self.category_combo.addItem(category)
        
        # Populate effects
        self.populate_effects_by_category("All Categories")
    
    def populate_effects_by_category(self, category):
        """Populate effects for a specific category."""
        self.effect_combo.clear()
        self.effect_combo.addItem("No Effect")
        
        if category == "All Categories":
            plugins = self.plugin_manager.get_all_plugins()
        else:
            plugins = self.plugin_manager.get_plugins_by_category(category)
        
        for plugin in plugins:
            self.effect_combo.addItem(plugin.name)
    
    def on_effect_changed(self, effect_name):
        """Handle effect selection change."""
        self.effect_changed.emit(effect_name)
    
    def on_category_changed(self, category):
        """Handle category filter change."""
        self.populate_effects_by_category(category)
    
    def set_current_effect(self, effect_name):
        """Set the currently selected effect."""
        index = self.effect_combo.findText(effect_name)
        if index >= 0:
            self.effect_combo.setCurrentIndex(index)
```

## Real-time Processing

### 1. Frame Processing Pipeline

```python
# src/core/frame_processor.py
class FrameProcessor:
    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.current_effect = None
        self.effect_parameters = {}
        self.frame_cache = {}
    
    def set_effect(self, effect_name):
        """Set the current effect."""
        if effect_name == "No Effect":
            self.current_effect = None
        else:
            self.current_effect = self.plugin_manager.get_plugin_by_name(effect_name)
        
        # Clear cache when effect changes
        self.frame_cache.clear()
    
    def set_parameters(self, parameters):
        """Set effect parameters."""
        self.effect_parameters = parameters
        # Clear cache when parameters change
        self.frame_cache.clear()
    
    def process_frame(self, frame):
        """Process a frame with the current effect."""
        if not self.current_effect or frame is None:
            return frame
        
        try:
            # Check cache for performance
            cache_key = self.get_cache_key(frame, self.effect_parameters)
            if cache_key in self.frame_cache:
                return self.frame_cache[cache_key]
            
            # Apply effect
            result = self.current_effect.apply(frame, self.effect_parameters)
            
            # Cache result (limit cache size)
            if len(self.frame_cache) < 10:
                self.frame_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logging.error(f"Error processing frame: {e}")
            return frame
    
    def get_cache_key(self, frame, parameters):
        """Generate cache key for frame and parameters."""
        # Simple hash based on frame size and parameter values
        frame_hash = hash((frame.shape[0], frame.shape[1]))
        param_hash = hash(str(sorted(parameters.items())))
        return frame_hash ^ param_hash
```

### 2. Performance Optimization

```python
# src/core/performance_optimizer.py
class PerformanceOptimizer:
    def __init__(self):
        self.frame_times = []
        self.max_frame_time = 33  # 30 FPS target
    
    def should_skip_frame(self, frame_time):
        """Determine if frame should be skipped for performance."""
        self.frame_times.append(frame_time)
        
        # Keep only last 10 frame times
        if len(self.frame_times) > 10:
            self.frame_times.pop(0)
        
        # Calculate average frame time
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        
        return avg_frame_time > self.max_frame_time
    
    def get_optimized_parameters(self, plugin, original_params):
        """Get optimized parameters for better performance."""
        if not plugin:
            return original_params
        
        # Create copy of parameters
        optimized = original_params.copy()
        
        # Apply performance optimizations
        if 'quality' in optimized:
            optimized['quality'] = min(optimized['quality'], 0.7)
        
        if 'resolution' in optimized:
            optimized['resolution'] = 'medium'
        
        return optimized
```

## Testing Integration

### 1. Integration Test Script

```python
# test_plugin_integration.py
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication

from src.plugins.plugin_manager import PluginManager
from src.gui.components.parameter_panel import ParameterPanel
from src.gui.components.effect_selector import EffectSelector

def test_plugin_integration():
    """Test complete plugin integration."""
    app = QApplication(sys.argv)
    
    # Create plugin manager
    plugin_manager = PluginManager()
    plugin_manager.load_plugins()
    
    # Test plugin loading
    plugins = plugin_manager.get_all_plugins()
    print(f"Loaded {len(plugins)} plugins")
    
    # Test effect selector
    selector = EffectSelector(plugin_manager)
    selector.show()
    
    # Test parameter panel
    panel = ParameterPanel(plugin_manager)
    panel.show()
    
    # Test with a sample effect
    if plugins:
        sample_effect = plugins[0]
        selector.set_current_effect(sample_effect.name)
        panel.set_effect(sample_effect.name)
        
        print(f"Testing effect: {sample_effect.name}")
    
    return app.exec_()

if __name__ == "__main__":
    test_plugin_integration()
```

### 2. Performance Test

```python
# test_performance.py
import time
import cv2
import numpy as np

from src.plugins.plugin_manager import PluginManager
from src.core.frame_processor import FrameProcessor

def test_performance():
    """Test plugin performance with real-time processing."""
    # Create plugin manager and frame processor
    plugin_manager = PluginManager()
    plugin_manager.load_plugins()
    
    processor = FrameProcessor(plugin_manager)
    
    # Create test video capture
    cap = cv2.VideoCapture(0)
    
    # Test each plugin
    plugins = plugin_manager.get_all_plugins()
    
    for plugin in plugins[:3]:  # Test first 3 plugins
        print(f"\nTesting {plugin.name}...")
        
        processor.set_effect(plugin.name)
        
        # Process frames for 5 seconds
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < 5:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            processed = processor.process_frame(frame)
            
            frame_count += 1
            
            # Display result
            cv2.imshow('Test', processed)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Calculate FPS
        elapsed = time.time() - start_time
        fps = frame_count / elapsed
        print(f"  FPS: {fps:.1f}")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_performance()
```

## Summary

This integration guide provides a complete framework for integrating the advanced plugin system with your main application. The system offers:

- **Seamless Integration**: Plugins work naturally with the main application
- **Professional UI**: Consistent styling and user experience
- **Real-time Performance**: Optimized for live webcam processing
- **Extensible Architecture**: Easy to add new effects and features
- **Comprehensive Testing**: Tools to verify integration works correctly

The plugin system maintains the beautiful GUI while providing powerful extensibility for custom effects and advanced features. 