"""
Plugin Manager

High-level interface for managing the plugin system.
Coordinates the registry and loader to provide a unified API.
"""

import os
import logging
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

from .plugin_registry import PluginRegistry
from .plugin_loader import PluginLoader
from .plugin_base import EffectPlugin, EffectUI

class PluginManager:
    """Main plugin manager that coordinates the plugin system."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.registry = PluginRegistry()
        self.loader = PluginLoader(self.registry)
        
        # Application state
        self.current_effect: Optional[EffectPlugin] = None
        self.current_effect_id: Optional[str] = None
        self.effect_parameters: Dict[str, Any] = {}
        
        # Callbacks
        self.on_effect_changed: Optional[Callable] = None
        self.on_parameter_changed: Optional[Callable] = None
        self.on_plugin_loaded: Optional[Callable] = None
        
        # Setup callbacks
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Setup internal callbacks."""
        self.registry.on_plugin_registered = self._on_plugin_registered
        self.registry.on_plugin_unregistered = self._on_plugin_unregistered
    
    def initialize(self, plugin_directories: Optional[List[str]] = None):
        """
        Initialize the plugin manager.
        
        Args:
            plugin_directories: List of directories to search for plugins
        """
        try:
            self.logger.info("Initializing plugin manager...")
            
            # Add default plugin directories if none provided
            if plugin_directories is None:
                plugin_directories = self._get_default_plugin_directories()
            
            # Add plugin directories
            for directory in plugin_directories:
                self.loader.add_plugin_directory(directory)
            
            # Load plugins
            results = self.loader.load_plugins()
            
            # Log results
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            self.logger.info(f"Plugin loading complete: {successful}/{total} plugins loaded successfully")
            
            # Print statistics
            stats = self.registry.get_statistics()
            self.logger.info(f"Plugin statistics: {stats}")
            
        except Exception as e:
            self.logger.error(f"Error initializing plugin manager: {e}")
    
    def _get_default_plugin_directories(self) -> List[str]:
        """
        Get default plugin directories.
        
        Returns:
            List of default plugin directory paths
        """
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent
        
        # Default plugin directories
        directories = [
            str(project_root / "plugins" / "effects"),
            str(project_root / "src" / "plugins" / "effects"),
            str(project_root / "styles"),  # Legacy styles directory
        ]
        
        # Filter out non-existent directories
        return [d for d in directories if os.path.exists(d)]
    
    def get_effect(self, effect_id: str) -> Optional[EffectPlugin]:
        """
        Get an effect plugin by ID.
        
        Args:
            effect_id: Effect plugin ID
            
        Returns:
            EffectPlugin instance or None if not found
        """
        return self.registry.get_plugin(effect_id)
    
    def get_effect_ui(self, effect_id: str) -> Optional[EffectUI]:
        """
        Get UI component for an effect.
        
        Args:
            effect_id: Effect plugin ID
            
        Returns:
            EffectUI instance or None if not found
        """
        return self.registry.get_ui_component(effect_id)
    
    def get_all_effects(self) -> List[EffectPlugin]:
        """
        Get all available effects.
        
        Returns:
            List of all EffectPlugin instances
        """
        return self.registry.get_all_plugins()
    
    def get_effects_by_category(self, category: str) -> List[EffectPlugin]:
        """
        Get effects by category.
        
        Args:
            category: Category name
            
        Returns:
            List of EffectPlugin instances in the category
        """
        return self.registry.get_plugins_by_category(category)
    
    def get_categories(self) -> List[str]:
        """
        Get all available effect categories.
        
        Returns:
            List of category names
        """
        return self.registry.get_all_categories()
    
    def search_effects(self, query: str) -> List[EffectPlugin]:
        """
        Search for effects by name, description, or tags.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching EffectPlugin instances
        """
        return self.registry.search_plugins(query)
    
    def set_current_effect(self, effect_id: str) -> bool:
        """
        Set the currently active effect.
        
        Args:
            effect_id: Effect plugin ID
            
        Returns:
            True if effect was set successfully
        """
        try:
            effect = self.registry.get_plugin(effect_id)
            if not effect:
                self.logger.warning(f"Effect {effect_id} not found")
                return False
            
            # Update current effect
            self.current_effect = effect
            self.current_effect_id = effect_id
            
            # Reset parameters to defaults
            self.effect_parameters = {}
            for param in effect.get_parameters():
                self.effect_parameters[param.name] = param.default
            
            self.logger.info(f"Current effect set to: {effect.name}")
            
            # Call callback
            if self.on_effect_changed:
                self.on_effect_changed(effect_id, effect)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting current effect: {e}")
            return False
    
    def get_current_effect(self) -> Optional[EffectPlugin]:
        """
        Get the currently active effect.
        
        Returns:
            Current EffectPlugin instance or None
        """
        return self.current_effect
    
    def get_current_effect_id(self) -> Optional[str]:
        """
        Get the ID of the currently active effect.
        
        Returns:
            Current effect ID or None
        """
        return self.current_effect_id
    
    def set_parameter(self, parameter_name: str, value: Any) -> bool:
        """
        Set a parameter for the current effect.
        
        Args:
            parameter_name: Parameter name
            value: Parameter value
            
        Returns:
            True if parameter was set successfully
        """
        try:
            if not self.current_effect:
                self.logger.warning("No current effect set")
                return False
            
            # Update parameter
            self.effect_parameters[parameter_name] = value
            
            # Update effect's internal parameter
            self.current_effect.set_parameter(parameter_name, value)
            
            # Call callback
            if self.on_parameter_changed:
                self.on_parameter_changed(parameter_name, value)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting parameter {parameter_name}: {e}")
            return False
    
    def get_parameter(self, parameter_name: str, default: Any = None) -> Any:
        """
        Get a parameter value for the current effect.
        
        Args:
            parameter_name: Parameter name
            default: Default value if parameter not found
            
        Returns:
            Parameter value or default
        """
        return self.effect_parameters.get(parameter_name, default)
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """
        Get all parameters for the current effect.
        
        Returns:
            Dictionary of parameter names and values
        """
        return self.effect_parameters.copy()
    
    def reset_parameters(self):
        """Reset all parameters to their default values."""
        try:
            if not self.current_effect:
                return
            
            self.effect_parameters = {}
            for param in self.current_effect.get_parameters():
                self.effect_parameters[param.name] = param.default
                self.current_effect.set_parameter(param.name, param.default)
            
            self.logger.info("Parameters reset to defaults")
            
        except Exception as e:
            self.logger.error(f"Error resetting parameters: {e}")
    
    def apply_effect(self, frame) -> Optional[Any]:
        """
        Apply the current effect to a frame.
        
        Args:
            frame: Input frame
            
        Returns:
            Processed frame or None if no effect is active
        """
        try:
            if not self.current_effect:
                return frame
            
            if not self.current_effect.is_enabled:
                return frame
            
            # Validate parameters
            validated_params = self.current_effect.validate_parameters(self.effect_parameters)
            
            # Apply effect
            result = self.current_effect.apply_effect(frame, validated_params)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error applying effect: {e}")
            return frame
    
    def enable_effect(self, effect_id: str) -> bool:
        """
        Enable an effect.
        
        Args:
            effect_id: Effect plugin ID
            
        Returns:
            True if effect was enabled successfully
        """
        return self.registry.enable_plugin(effect_id)
    
    def disable_effect(self, effect_id: str) -> bool:
        """
        Disable an effect.
        
        Args:
            effect_id: Effect plugin ID
            
        Returns:
            True if effect was disabled successfully
        """
        return self.registry.disable_plugin(effect_id)
    
    def reload_effect(self, effect_id: str) -> bool:
        """
        Reload an effect plugin.
        
        Args:
            effect_id: Effect plugin ID
            
        Returns:
            True if effect was reloaded successfully
        """
        return self.loader.reload_plugin(effect_id)
    
    def load_plugin_from_path(self, plugin_path: str) -> bool:
        """
        Load a plugin from a specific path.
        
        Args:
            plugin_path: Path to plugin directory or file
            
        Returns:
            True if plugin was loaded successfully
        """
        return self.loader.load_plugin_from_path(plugin_path)
    
    def get_effect_metadata(self, effect_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for an effect.
        
        Args:
            effect_id: Effect plugin ID
            
        Returns:
            Effect metadata dictionary or None if not found
        """
        return self.registry.get_plugin_metadata(effect_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get plugin system statistics.
        
        Returns:
            Dictionary containing statistics
        """
        return self.registry.get_statistics()
    
    def _on_plugin_registered(self, plugin_id: str, plugin: EffectPlugin):
        """Callback when a plugin is registered."""
        self.logger.info(f"Plugin registered: {plugin_id} ({plugin.name})")
        
        if self.on_plugin_loaded:
            self.on_plugin_loaded(plugin_id, plugin)
    
    def _on_plugin_unregistered(self, plugin_id: str, plugin: EffectPlugin):
        """Callback when a plugin is unregistered."""
        self.logger.info(f"Plugin unregistered: {plugin_id} ({plugin.name})")
    
    def cleanup(self):
        """Clean up the plugin manager."""
        try:
            self.logger.info("Cleaning up plugin manager...")
            
            # Clean up current effect
            if self.current_effect:
                self.current_effect.cleanup()
                self.current_effect = None
                self.current_effect_id = None
            
            # Clear parameters
            self.effect_parameters.clear()
            
            # Clean up components
            self.loader.cleanup()
            self.registry.clear()
            
            self.logger.info("Plugin manager cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up plugin manager: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup() 