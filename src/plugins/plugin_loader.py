"""
Plugin Loader

Automatically discovers and loads effect plugins from directories.
"""

import os
import sys
import json
import importlib
import importlib.util
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from .plugin_registry import PluginRegistry
from .plugin_base import EffectPlugin, EffectUI

class PluginLoader:
    """Loads plugins from directories and registers them."""
    
    def __init__(self, registry: PluginRegistry):
        self.registry = registry
        self.logger = logging.getLogger(__name__)
        
        # Plugin directories to search
        self.plugin_directories: List[str] = []
        
        # Loaded plugin modules
        self.loaded_modules: Dict[str, Any] = {}
        
        # Plugin validation
        self.required_files = ['__init__.py']
        self.optional_files = ['metadata.json', 'effect.py', 'ui.py']
    
    def add_plugin_directory(self, directory: str):
        """
        Add a directory to search for plugins.
        
        Args:
            directory: Path to plugin directory
        """
        if os.path.exists(directory) and os.path.isdir(directory):
            self.plugin_directories.append(directory)
            self.logger.info(f"Added plugin directory: {directory}")
        else:
            self.logger.warning(f"Plugin directory does not exist: {directory}")
    
    def load_plugins(self) -> Dict[str, bool]:
        """
        Load all plugins from registered directories.
        
        Returns:
            Dictionary mapping plugin IDs to load success status
        """
        results = {}
        
        for directory in self.plugin_directories:
            self.logger.info(f"Scanning plugin directory: {directory}")
            
            try:
                # Scan for plugin directories
                plugin_dirs = self._find_plugin_directories(directory)
                
                for plugin_dir in plugin_dirs:
                    plugin_id = os.path.basename(plugin_dir)
                    
                    try:
                        success = self._load_plugin_from_directory(plugin_dir)
                        results[plugin_id] = success
                        
                        if success:
                            self.logger.info(f"Successfully loaded plugin: {plugin_id}")
                        else:
                            self.logger.warning(f"Failed to load plugin: {plugin_id}")
                            
                    except Exception as e:
                        self.logger.error(f"Error loading plugin {plugin_id}: {e}")
                        results[plugin_id] = False
                        
            except Exception as e:
                self.logger.error(f"Error scanning directory {directory}: {e}")
        
        return results
    
    def load_plugin_from_path(self, plugin_path: str) -> bool:
        """
        Load a specific plugin from a path.
        
        Args:
            plugin_path: Path to plugin directory or file
            
        Returns:
            True if loading was successful
        """
        try:
            if os.path.isdir(plugin_path):
                return self._load_plugin_from_directory(plugin_path)
            elif os.path.isfile(plugin_path):
                return self._load_plugin_from_file(plugin_path)
            else:
                self.logger.error(f"Plugin path does not exist: {plugin_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading plugin from {plugin_path}: {e}")
            return False
    
    def _find_plugin_directories(self, base_directory: str) -> List[str]:
        """
        Find all plugin directories in the base directory.
        
        Args:
            base_directory: Base directory to search
            
        Returns:
            List of plugin directory paths
        """
        plugin_dirs = []
        
        try:
            # Recursively search for plugin directories
            for root, dirs, files in os.walk(base_directory):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    
                    # Check if this looks like a plugin directory
                    if self._is_plugin_directory(dir_path):
                        plugin_dirs.append(dir_path)
                        self.logger.info(f"Found plugin directory: {dir_path}")
                        
        except Exception as e:
            self.logger.error(f"Error finding plugin directories in {base_directory}: {e}")
        
        return plugin_dirs
    
    def _is_plugin_directory(self, directory: str) -> bool:
        """
        Check if a directory contains a valid plugin.
        
        Args:
            directory: Directory path to check
            
        Returns:
            True if directory contains a valid plugin
        """
        try:
            # Check for required files
            for required_file in self.required_files:
                if not os.path.exists(os.path.join(directory, required_file)):
                    return False
            
            # Check for at least one optional file
            has_optional = False
            for optional_file in self.optional_files:
                if os.path.exists(os.path.join(directory, optional_file)):
                    has_optional = True
                    break
            
            return has_optional
            
        except Exception:
            return False
    
    def _load_plugin_from_directory(self, plugin_dir: str) -> bool:
        """
        Load a plugin from a directory.
        
        Args:
            plugin_dir: Plugin directory path
            
        Returns:
            True if loading was successful
        """
        try:
            plugin_name = os.path.basename(plugin_dir)
            
            # Load metadata if available
            metadata = self._load_metadata(plugin_dir)
            
            # Load the plugin module
            module = self._load_module_from_directory(plugin_dir, plugin_name)
            if not module:
                return False
            
            # Look for register_plugin function
            if hasattr(module, 'register_plugin'):
                # Call the register function
                module.register_plugin(self.registry)
                
                # Store additional metadata if available
                if metadata:
                    # Find the plugin that was just registered
                    for plugin_id, plugin in self.registry.plugins.items():
                        if plugin.name == plugin_name or plugin_name in plugin_id:
                            self.registry.plugin_metadata[plugin_id].update(metadata)
                            break
                
                return True
            else:
                # Fallback: Look for plugin classes
                plugin_class = self._find_plugin_class(module)
                ui_class = self._find_ui_class(module)
                
                if not plugin_class:
                    self.logger.error(f"No plugin class or register_plugin function found in {plugin_name}")
                    return False
                
                # Create plugin instance
                plugin = plugin_class()
                
                # Create UI instance if available
                ui = None
                if ui_class:
                    ui = ui_class(plugin)
                
                # Register plugin
                success = self.registry.register_plugin(plugin, ui)
                
                if success and metadata:
                    # Store additional metadata
                    plugin_id = self._get_plugin_id(plugin)
                    if plugin_id:
                        self.registry.plugin_metadata[plugin_id].update(metadata)
                
                return success
            
        except Exception as e:
            self.logger.error(f"Error loading plugin from directory {plugin_dir}: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def _load_plugin_from_file(self, plugin_file: str) -> bool:
        """
        Load a plugin from a single file.
        
        Args:
            plugin_file: Plugin file path
            
        Returns:
            True if loading was successful
        """
        try:
            plugin_name = os.path.splitext(os.path.basename(plugin_file))[0]
            
            # Load the module
            module = self._load_module_from_file(plugin_file, plugin_name)
            if not module:
                return False
            
            # Look for plugin classes
            plugin_class = self._find_plugin_class(module)
            ui_class = self._find_ui_class(module)
            
            if not plugin_class:
                self.logger.error(f"No plugin class found in {plugin_name}")
                return False
            
            # Create plugin instance
            plugin = plugin_class()
            
            # Create UI instance if available
            ui = None
            if ui_class:
                ui = ui_class(plugin)
            
            # Register plugin
            return self.registry.register_plugin(plugin, ui)
            
        except Exception as e:
            self.logger.error(f"Error loading plugin from file {plugin_file}: {e}")
            return False
    
    def _load_metadata(self, plugin_dir: str) -> Optional[Dict[str, Any]]:
        """
        Load metadata from a plugin directory.
        
        Args:
            plugin_dir: Plugin directory path
            
        Returns:
            Metadata dictionary or None if not found
        """
        metadata_file = os.path.join(plugin_dir, 'metadata.json')
        
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Error loading metadata from {metadata_file}: {e}")
        
        return None
    
    def _load_module_from_directory(self, plugin_dir: str, module_name: str) -> Optional[Any]:
        """
        Load a Python module from a directory.
        
        Args:
            plugin_dir: Plugin directory path
            module_name: Name for the module
            
        Returns:
            Loaded module or None if failed
        """
        try:
            # Load the module using importlib.util
            init_file = os.path.join(plugin_dir, '__init__.py')
            if os.path.exists(init_file):
                # Add parent directories to sys.path for relative imports
                parent_dir = os.path.dirname(plugin_dir)
                if parent_dir not in sys.path:
                    sys.path.insert(0, parent_dir)
                
                # Use the directory name as module name
                spec = importlib.util.spec_from_file_location(module_name, init_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                self.loaded_modules[module_name] = module
                return module
            else:
                self.logger.error(f"No __init__.py file found in {plugin_dir}")
                return None
            
        except Exception as e:
            self.logger.error(f"Error loading module {module_name} from {plugin_dir}: {e}")
            return None
    
    def _load_module_from_file(self, plugin_file: str, module_name: str) -> Optional[Any]:
        """
        Load a Python module from a file.
        
        Args:
            plugin_file: Plugin file path
            module_name: Name for the module
            
        Returns:
            Loaded module or None if failed
        """
        try:
            # Load the module from file
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            self.loaded_modules[module_name] = module
            return module
            
        except Exception as e:
            self.logger.error(f"Error loading module {module_name} from {plugin_file}: {e}")
            return None
    
    def _find_plugin_class(self, module: Any) -> Optional[type]:
        """
        Find the plugin class in a module.
        
        Args:
            module: Python module
            
        Returns:
            Plugin class or None if not found
        """
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            
            # Check if it's a class that inherits from EffectPlugin
            if (isinstance(attr, type) and 
                issubclass(attr, EffectPlugin) and 
                attr != EffectPlugin):
                return attr
        
        return None
    
    def _find_ui_class(self, module: Any) -> Optional[type]:
        """
        Find the UI class in a module.
        
        Args:
            module: Python module
            
        Returns:
            UI class or None if not found
        """
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            
            # Check if it's a class that inherits from EffectUI
            if (isinstance(attr, type) and 
                issubclass(attr, EffectUI) and 
                attr != EffectUI):
                return attr
        
        return None
    
    def _get_plugin_id(self, plugin: EffectPlugin) -> Optional[str]:
        """
        Get the plugin ID for a plugin.
        
        Args:
            plugin: EffectPlugin instance
            
        Returns:
            Plugin ID or None if not found
        """
        for plugin_id, registered_plugin in self.registry.plugins.items():
            if registered_plugin == plugin:
                return plugin_id
        return None
    
    def reload_plugin(self, plugin_id: str) -> bool:
        """
        Reload a specific plugin.
        
        Args:
            plugin_id: ID of the plugin to reload
            
        Returns:
            True if reload was successful
        """
        try:
            # Unregister the plugin
            if not self.registry.unregister_plugin(plugin_id):
                return False
            
            # Find the plugin module
            if plugin_id in self.loaded_modules:
                module = self.loaded_modules[plugin_id]
                
                # Reload the module
                importlib.reload(module)
                
                # Find and register the plugin again
                plugin_class = self._find_plugin_class(module)
                ui_class = self._find_ui_class(module)
                
                if plugin_class:
                    plugin = plugin_class()
                    ui = None
                    if ui_class:
                        ui = ui_class(plugin)
                    
                    return self.registry.register_plugin(plugin, ui)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error reloading plugin {plugin_id}: {e}")
            return False
    
    def get_loaded_modules(self) -> Dict[str, Any]:
        """
        Get all loaded plugin modules.
        
        Returns:
            Dictionary of loaded modules
        """
        return self.loaded_modules.copy()
    
    def cleanup(self):
        """Clean up the plugin loader."""
        try:
            # Clean up loaded modules
            self.loaded_modules.clear()
            
            # Remove plugin directories from Python path
            for directory in self.plugin_directories:
                if directory in sys.path:
                    sys.path.remove(directory)
            
            self.logger.info("Plugin loader cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up plugin loader: {e}") 