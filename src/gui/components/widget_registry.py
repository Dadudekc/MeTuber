#!/usr/bin/env python3
"""
Widget Registry System
Manages the lifecycle, positioning, and filter associations of draggable widgets.
"""

import json
import os
from typing import Dict, List, Optional, Any
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QObject, pyqtSignal, QPoint, QSize, QRect
from .draggable_widget import DraggableWidget
import logging


class WidgetRegistry(QObject):
    """
    Registry system for managing all draggable filter widgets.
    Handles creation, positioning, persistence, and coordination.
    """
    
    # Signals
    widget_created = pyqtSignal(str, object)  # filter_name, widget
    widget_activated = pyqtSignal(str, object)  # filter_name, widget  
    widget_deactivated = pyqtSignal(str, object)  # filter_name, widget
    layout_changed = pyqtSignal()  # Emitted when widget layout changes
    
    def __init__(self, parent_widget: QWidget):
        super().__init__()
        
        self.logger = logging.getLogger(__name__)
        self.parent_widget = parent_widget
        
        # Widget storage
        self.active_widgets: Dict[str, DraggableWidget] = {}
        self.widget_configs: Dict[str, Dict] = {}
        self.dock_zones: Dict[str, List[DraggableWidget]] = {
            "left": [],
            "right": [],
            "top": [],
            "bottom": [],
            "floating": []
        }
        
        # Layout persistence
        self.layout_file = "widget_layouts.json"
        self.load_layout_config()
        
        # Default dock positions
        self.default_positions = {
            "left": {"x": 10, "y": 100, "width": 280, "height": 400},
            "right": {"x": -300, "y": 100, "width": 280, "height": 400},
            "bottom": {"x": 200, "y": -200, "width": 400, "height": 180},
            "floating": {"x": 300, "y": 200, "width": 300, "height": 350}
        }
        
    def create_widget_for_filter(self, filter_name: str, parameters: List[Dict]) -> DraggableWidget:
        """
        Create a new draggable widget for the specified filter.
        
        Args:
            filter_name: Name of the filter
            parameters: List of parameter definitions
            
        Returns:
            DraggableWidget: The created widget
        """
        # Check if widget already exists
        if filter_name in self.active_widgets:
            existing_widget = self.active_widgets[filter_name]
            existing_widget.show_widget()
            existing_widget.load_filter_parameters(filter_name, parameters)
            return existing_widget
            
        # Create new widget
        widget = DraggableWidget(f"{filter_name}", self.parent_widget)
        
        # Load filter parameters
        widget.load_filter_parameters(filter_name, parameters)
        
        # Connect signals
        self.connect_widget_signals(widget, filter_name)
        
        # Position widget
        self.position_widget(widget, filter_name)
        
        # Register widget
        self.active_widgets[filter_name] = widget
        self.dock_zones["floating"].append(widget)
        
        # Show widget
        widget.show_widget()
        
        # Emit signal
        self.widget_created.emit(filter_name, widget)
        
        self.logger.info(f"Created widget for filter: {filter_name}")
        return widget
        
    def connect_widget_signals(self, widget: DraggableWidget, filter_name: str):
        """Connect widget signals to registry handlers."""
        widget.widget_closed.connect(lambda w: self.on_widget_closed(filter_name, w))
        widget.widget_docked.connect(lambda w, zone: self.on_widget_docked(filter_name, w, zone))
        widget.widget_undocked.connect(lambda w: self.on_widget_undocked(filter_name, w))
        widget.parameters_changed.connect(lambda params: self.on_parameters_changed(filter_name, params))
        
    def position_widget(self, widget: DraggableWidget, filter_name: str):
        """Position widget based on saved layout or defaults."""
        # Check for saved position
        if filter_name in self.widget_configs:
            config = self.widget_configs[filter_name]
            
            # Restore geometry
            if "geometry" in config:
                geom = config["geometry"]
                widget.setGeometry(QRect(geom["x"], geom["y"], geom["width"], geom["height"]))
            
            # Restore dock state
            if config.get("is_docked", False):
                dock_zone = config.get("dock_zone", "right")
                widget.dock_to_zone(dock_zone)
            
            # Restore minimized state
            if config.get("is_minimized", False):
                widget.minimize()
                
        else:
            # Use default position
            self.position_widget_default(widget)
            
    def position_widget_default(self, widget: DraggableWidget):
        """Position widget using default smart positioning."""
        # Calculate next available position
        zone = "floating"
        existing_count = len([w for w in self.active_widgets.values() if not w.is_docked])
        
        # Get default position for zone
        default_pos = self.default_positions[zone].copy()
        
        # Offset for multiple widgets
        offset = existing_count * 30
        default_pos["x"] += offset
        default_pos["y"] += offset
        
        # Ensure widget stays within parent bounds
        parent_rect = self.parent_widget.rect()
        if default_pos["x"] + default_pos["width"] > parent_rect.width():
            default_pos["x"] = parent_rect.width() - default_pos["width"] - 20
        if default_pos["y"] + default_pos["height"] > parent_rect.height():
            default_pos["y"] = parent_rect.height() - default_pos["height"] - 20
            
        # Apply position
        widget.setGeometry(QRect(
            default_pos["x"], default_pos["y"], 
            default_pos["width"], default_pos["height"]
        ))
        
    def activate_filter_widget(self, filter_name: str, parameters: List[Dict]) -> DraggableWidget:
        """
        Activate widget for filter (create if doesn't exist, show if hidden).
        
        Args:
            filter_name: Name of the filter to activate
            parameters: Parameter definitions for the filter
            
        Returns:
            DraggableWidget: The activated widget
        """
        widget = self.create_widget_for_filter(filter_name, parameters)
        self.widget_activated.emit(filter_name, widget)
        return widget
        
    def deactivate_filter_widget(self, filter_name: str):
        """
        Deactivate widget for filter (hide but don't destroy).
        
        Args:
            filter_name: Name of the filter to deactivate
        """
        if filter_name in self.active_widgets:
            widget = self.active_widgets[filter_name]
            widget.hide()
            self.widget_deactivated.emit(filter_name, widget)
            self.logger.info(f"Deactivated widget for filter: {filter_name}")
            
    def remove_filter_widget(self, filter_name: str):
        """
        Completely remove widget for filter.
        
        Args:
            filter_name: Name of the filter widget to remove
        """
        if filter_name in self.active_widgets:
            widget = self.active_widgets[filter_name]
            
            # Remove from dock zones
            for zone_widgets in self.dock_zones.values():
                if widget in zone_widgets:
                    zone_widgets.remove(widget)
                    
            # Close widget
            widget.close_widget()
            
            # Remove from active widgets
            del self.active_widgets[filter_name]
            
            self.logger.info(f"Removed widget for filter: {filter_name}")
            
    def get_widget_for_filter(self, filter_name: str) -> Optional[DraggableWidget]:
        """
        Get widget for specific filter.
        
        Args:
            filter_name: Name of the filter
            
        Returns:
            Optional[DraggableWidget]: Widget if exists, None otherwise
        """
        return self.active_widgets.get(filter_name)
        
    def get_active_widgets(self) -> Dict[str, DraggableWidget]:
        """Get all currently active widgets."""
        return self.active_widgets.copy()
        
    def get_docked_widgets(self, zone: str) -> List[DraggableWidget]:
        """
        Get all widgets docked to specific zone.
        
        Args:
            zone: Dock zone name ("left", "right", "top", "bottom")
            
        Returns:
            List[DraggableWidget]: Widgets in the zone
        """
        return self.dock_zones.get(zone, []).copy()
        
    def arrange_docked_widgets(self, zone: str):
        """
        Arrange docked widgets in the specified zone.
        
        Args:
            zone: Dock zone to arrange ("left", "right", "top", "bottom")
        """
        widgets = self.dock_zones.get(zone, [])
        if not widgets:
            return
            
        parent_rect = self.parent_widget.rect()
        widget_spacing = 5
        
        if zone in ["left", "right"]:
            # Vertical arrangement
            total_height = sum(w.height() for w in widgets) + (len(widgets) - 1) * widget_spacing
            start_y = max(50, (parent_rect.height() - total_height) // 2)
            
            current_y = start_y
            for widget in widgets:
                if zone == "left":
                    x = 10
                else:  # right
                    x = parent_rect.width() - widget.width() - 10
                    
                widget.move(x, current_y)
                current_y += widget.height() + widget_spacing
                
        elif zone in ["top", "bottom"]:
            # Horizontal arrangement
            total_width = sum(w.width() for w in widgets) + (len(widgets) - 1) * widget_spacing
            start_x = max(10, (parent_rect.width() - total_width) // 2)
            
            current_x = start_x
            for widget in widgets:
                if zone == "top":
                    y = 10
                else:  # bottom
                    y = parent_rect.height() - widget.height() - 10
                    
                widget.move(current_x, y)
                current_x += widget.width() + widget_spacing
                
    def cascade_floating_widgets(self):
        """Arrange floating widgets in a cascade pattern."""
        floating_widgets = [w for w in self.active_widgets.values() 
                          if not w.is_docked and w.isVisible()]
        
        start_x, start_y = 300, 100
        offset = 30
        
        for i, widget in enumerate(floating_widgets):
            x = start_x + (i * offset)
            y = start_y + (i * offset)
            
            # Keep within parent bounds
            parent_rect = self.parent_widget.rect()
            if x + widget.width() > parent_rect.width():
                x = parent_rect.width() - widget.width() - 20
            if y + widget.height() > parent_rect.height():
                y = parent_rect.height() - widget.height() - 20
                
            widget.move(x, y)
            
    def tile_widgets_horizontal(self):
        """Tile all visible widgets horizontally."""
        visible_widgets = [w for w in self.active_widgets.values() if w.isVisible()]
        if not visible_widgets:
            return
            
        parent_rect = self.parent_widget.rect()
        widget_width = parent_rect.width() // len(visible_widgets)
        widget_height = min(400, parent_rect.height() - 100)
        
        for i, widget in enumerate(visible_widgets):
            x = i * widget_width
            y = 50
            widget.setGeometry(x, y, widget_width - 5, widget_height)
            widget.undock()  # Ensure not docked
            
    def tile_widgets_vertical(self):
        """Tile all visible widgets vertically."""
        visible_widgets = [w for w in self.active_widgets.values() if w.isVisible()]
        if not visible_widgets:
            return
            
        parent_rect = self.parent_widget.rect()
        widget_height = parent_rect.height() // len(visible_widgets)
        widget_width = min(350, parent_rect.width() - 100)
        
        for i, widget in enumerate(visible_widgets):
            x = 50
            y = i * widget_height
            widget.setGeometry(x, y, widget_width, widget_height - 5)
            widget.undock()  # Ensure not docked
            
    def minimize_all_widgets(self):
        """Minimize all active widgets."""
        for widget in self.active_widgets.values():
            if not widget.is_minimized:
                widget.minimize()
                
    def restore_all_widgets(self):
        """Restore all minimized widgets."""
        for widget in self.active_widgets.values():
            if widget.is_minimized:
                widget.restore()
                
    def hide_all_widgets(self):
        """Hide all widgets."""
        for widget in self.active_widgets.values():
            widget.hide()
            
    def show_all_widgets(self):
        """Show all widgets."""
        for widget in self.active_widgets.values():
            widget.show_widget()
            
    # === EVENT HANDLERS ===
    
    def on_widget_closed(self, filter_name: str, widget: DraggableWidget):
        """Handle widget closed event."""
        if filter_name in self.active_widgets:
            # Save configuration before closing
            self.save_widget_config(filter_name, widget)
            
            # Remove from dock zones
            for zone_widgets in self.dock_zones.values():
                if widget in zone_widgets:
                    zone_widgets.remove(widget)
                    
            # Remove from active widgets
            del self.active_widgets[filter_name]
            
            self.layout_changed.emit()
            
    def on_widget_docked(self, filter_name: str, widget: DraggableWidget, zone: str):
        """Handle widget docked event."""
        # Remove from previous zone
        for zone_name, zone_widgets in self.dock_zones.items():
            if widget in zone_widgets:
                zone_widgets.remove(widget)
                
        # Add to new zone
        if zone in self.dock_zones:
            self.dock_zones[zone].append(widget)
            self.arrange_docked_widgets(zone)
            
        self.layout_changed.emit()
        
    def on_widget_undocked(self, filter_name: str, widget: DraggableWidget):
        """Handle widget undocked event."""
        # Remove from dock zones
        for zone_widgets in self.dock_zones.values():
            if widget in zone_widgets:
                zone_widgets.remove(widget)
                
        # Add to floating
        self.dock_zones["floating"].append(widget)
        
        self.layout_changed.emit()
        
    def on_parameters_changed(self, filter_name: str, parameters: Dict):
        """Handle parameter changes from widget."""
        self.logger.debug(f"Parameters changed for {filter_name}: {parameters}")
        # Could emit a signal here for the main application to handle
        
    # === PERSISTENCE ===
    
    def save_widget_config(self, filter_name: str, widget: DraggableWidget):
        """Save widget configuration."""
        config = {
            "geometry": {
                "x": widget.x(),
                "y": widget.y(),
                "width": widget.width(),
                "height": widget.height()
            },
            "is_docked": widget.is_docked,
            "dock_zone": widget.dock_zone,
            "is_minimized": widget.is_minimized,
            "is_maximized": widget.is_maximized
        }
        
        self.widget_configs[filter_name] = config
        
    def save_layout_config(self):
        """Save all widget layouts to file."""
        try:
            # Update configs with current widget states
            for filter_name, widget in self.active_widgets.items():
                self.save_widget_config(filter_name, widget)
                
            # Write to file
            with open(self.layout_file, 'w') as f:
                json.dump(self.widget_configs, f, indent=2)
                
            self.logger.info(f"Saved widget layouts to {self.layout_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save widget layouts: {e}")
            
    def load_layout_config(self):
        """Load widget layouts from file."""
        try:
            if os.path.exists(self.layout_file):
                with open(self.layout_file, 'r') as f:
                    self.widget_configs = json.load(f)
                    
                self.logger.info(f"Loaded widget layouts from {self.layout_file}")
            else:
                self.logger.info("No existing widget layout file found")
                
        except Exception as e:
            self.logger.error(f"Failed to load widget layouts: {e}")
            self.widget_configs = {}
            
    def reset_layout(self):
        """Reset all widget layouts to defaults."""
        self.widget_configs.clear()
        
        # Reposition all active widgets
        for filter_name, widget in self.active_widgets.items():
            widget.undock()
            self.position_widget_default(widget)
            
        self.cascade_floating_widgets()
        self.layout_changed.emit()
        
        self.logger.info("Reset all widget layouts to defaults")
        
    def export_layout(self, filename: str):
        """Export current layout to file."""
        try:
            # Update configs
            for filter_name, widget in self.active_widgets.items():
                self.save_widget_config(filter_name, widget)
                
            with open(filename, 'w') as f:
                json.dump(self.widget_configs, f, indent=2)
                
            self.logger.info(f"Exported layout to {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to export layout: {e}")
            
    def import_layout(self, filename: str):
        """Import layout from file."""
        try:
            with open(filename, 'r') as f:
                imported_configs = json.load(f)
                
            self.widget_configs.update(imported_configs)
            
            # Apply to active widgets
            for filter_name, widget in self.active_widgets.items():
                if filter_name in self.widget_configs:
                    self.position_widget(widget, filter_name)
                    
            self.layout_changed.emit()
            self.logger.info(f"Imported layout from {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to import layout: {e}")
            
    def cleanup(self):
        """Cleanup registry (save configs, close widgets)."""
        # Save current layout
        self.save_layout_config()
        
        # Close all widgets
        for widget in list(self.active_widgets.values()):
            widget.close_widget()
            
        self.active_widgets.clear()
        self.dock_zones = {zone: [] for zone in self.dock_zones.keys()}
        
        self.logger.info("Widget registry cleaned up") 