"""
Widget Manager Module for Dreamscape V2 Professional

Handles all widget-related functionality including draggable widget system,
widget registry management, widget creation and lifecycle, and layout persistence.
"""

import logging
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class WidgetManager:
    """Manages all widget-related functionality."""
    
    def __init__(self, main_window):
        """Initialize widget manager with reference to main window."""
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # Widget registry
        self.widget_registry = None
        self.active_widgets = {}
        
        # Signals
        self.widget_created = pyqtSignal(str, object)
        self.widget_closed = pyqtSignal(str)
        self.layout_changed = pyqtSignal()
        
    def init_widget_registry(self):
        """Initialize the widget registry."""
        try:
            self.logger.info("Initializing widget registry")
            
            # Import widget registry
            from src.gui.components.widget_registry import WidgetRegistry
            
            # Create widget registry instance
            self.widget_registry = WidgetRegistry(self.main_window)
            
            # Connect signals
            self.widget_registry.widget_created.connect(self.on_filter_widget_created)
            self.widget_registry.layout_changed.connect(self.on_widget_layout_changed)
            
            self.logger.info("Widget registry initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing widget registry: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            
    def create_filter_widget(self, filter_name):
        """Create a filter widget for the given filter."""
        try:
            if not self.widget_registry:
                self.init_widget_registry()
                
            if self.widget_registry:
                widget = self.widget_registry.create_widget(filter_name)
                if widget:
                    self.active_widgets[filter_name] = widget
                    self.logger.info(f"Filter widget created for: {filter_name}")
                    return widget
                    
            return None
            
        except Exception as e:
            self.logger.error(f"Error creating filter widget: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return None
            
    def on_filter_widget_created(self, filter_name, widget):
        """Handle filter widget creation."""
        try:
            self.logger.info(f"Filter widget created: {filter_name}")
            
            # Store widget reference
            self.active_widgets[filter_name] = widget
            
            # Connect widget signals
            if hasattr(widget, 'parameters_changed'):
                widget.parameters_changed.connect(
                    lambda params: self.on_widget_parameters_changed(filter_name, params)
                )
                
            # Emit signal
            self.widget_created.emit(filter_name, widget)
            
        except Exception as e:
            self.logger.error(f"Error handling filter widget creation: {e}")
            
    def on_widget_layout_changed(self):
        """Handle widget layout changes."""
        try:
            self.logger.info("Widget layout changed")
            
            # Emit signal
            self.layout_changed.emit()
            
        except Exception as e:
            self.logger.error(f"Error handling widget layout change: {e}")
            
    def on_widget_parameters_changed(self, filter_name, parameters):
        """Handle widget parameter changes."""
        try:
            self.logger.info(f"Widget parameters changed for {filter_name}: {parameters}")
            
            # Update main window parameters
            if hasattr(self.main_window, 'pending_params'):
                self.main_window.pending_params = parameters
                
            # Update webcam service if running
            if hasattr(self.main_window, 'webcam_manager'):
                if self.main_window.webcam_manager.is_processing_active():
                    # Get current style
                    if hasattr(self.main_window, 'current_style') and self.main_window.current_style:
                        self.main_window.webcam_manager.update_style(
                            self.main_window.current_style, parameters
                        )
                        
        except Exception as e:
            self.logger.error(f"Error handling widget parameter changes: {e}")
            
    def close_widget(self, filter_name):
        """Close a specific widget."""
        try:
            if filter_name in self.active_widgets:
                widget = self.active_widgets[filter_name]
                if widget:
                    widget.close()
                    del self.active_widgets[filter_name]
                    
                self.logger.info(f"Widget closed: {filter_name}")
                self.widget_closed.emit(filter_name)
                
        except Exception as e:
            self.logger.error(f"Error closing widget: {e}")
            
    def close_all_widgets(self):
        """Close all active widgets."""
        try:
            for filter_name in list(self.active_widgets.keys()):
                self.close_widget(filter_name)
                
            self.logger.info("All widgets closed")
            
        except Exception as e:
            self.logger.error(f"Error closing all widgets: {e}")
            
    def get_active_widgets(self):
        """Get all active widgets."""
        return self.active_widgets.copy()
        
    def get_widget(self, filter_name):
        """Get a specific widget by filter name."""
        return self.active_widgets.get(filter_name)
        
    def is_widget_active(self, filter_name):
        """Check if a widget is active for the given filter."""
        return filter_name in self.active_widgets
        
    def save_widget_layout(self):
        """Save the current widget layout."""
        try:
            if self.widget_registry:
                self.widget_registry.save_layout()
                self.logger.info("Widget layout saved")
                
        except Exception as e:
            self.logger.error(f"Error saving widget layout: {e}")
            
    def load_widget_layout(self):
        """Load the saved widget layout."""
        try:
            if self.widget_registry:
                self.widget_registry.load_layout()
                self.logger.info("Widget layout loaded")
                
        except Exception as e:
            self.logger.error(f"Error loading widget layout: {e}")
            
    def reset_widget_layout(self):
        """Reset the widget layout to default."""
        try:
            if self.widget_registry:
                self.widget_registry.reset_layout()
                self.logger.info("Widget layout reset")
                
        except Exception as e:
            self.logger.error(f"Error resetting widget layout: {e}")
            
    def get_widget_info(self, filter_name):
        """Get information about a widget."""
        try:
            widget = self.get_widget(filter_name)
            if not widget:
                return {}
                
            info = {
                'filter_name': filter_name,
                'is_active': True,
                'position': widget.pos() if hasattr(widget, 'pos') else None,
                'size': widget.size() if hasattr(widget, 'size') else None,
                'is_visible': widget.isVisible() if hasattr(widget, 'isVisible') else False,
                'is_docked': hasattr(widget, 'is_docked') and widget.is_docked,
                'dock_area': getattr(widget, 'dock_area', None)
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting widget info: {e}")
            return {}
            
    def get_all_widget_info(self):
        """Get information about all active widgets."""
        try:
            info = {}
            for filter_name in self.active_widgets:
                info[filter_name] = self.get_widget_info(filter_name)
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting all widget info: {e}")
            return {}
            
    def cleanup(self):
        """Clean up widget resources."""
        try:
            # Close all widgets
            self.close_all_widgets()
            
            # Save layout
            self.save_widget_layout()
            
            # Clear registry
            if self.widget_registry:
                self.widget_registry = None
                
            self.logger.info("Widget manager cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up widget manager: {e}")
            
    def get_widget_statistics(self):
        """Get widget usage statistics."""
        try:
            stats = {
                'total_widgets': len(self.active_widgets),
                'active_widgets': len([w for w in self.active_widgets.values() if w and w.isVisible()]),
                'docked_widgets': len([w for w in self.active_widgets.values() 
                                     if w and hasattr(w, 'is_docked') and w.is_docked]),
                'floating_widgets': len([w for w in self.active_widgets.values() 
                                       if w and hasattr(w, 'is_docked') and not w.is_docked])
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting widget statistics: {e}")
            return {} 