"""
Plugin Registry

Manages registration and access to all loaded effect plugins.
"""

import logging
from typing import Dict, List, Optional, Any
from .plugin_base import EffectPlugin, EffectUI

class PluginRegistry:
    """Registry for managing effect plugins."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Plugin storage
        self.plugins: Dict[str, EffectPlugin] = {}
        self.ui_components: Dict[str, EffectUI] = {}
        self.categories: Dict[str, List[str]] = {}
        
        # Plugin metadata
        self.plugin_metadata: Dict[str, Dict[str, Any]] = {}
        
        # Callbacks
        self.on_plugin_registered: Optional[callable] = None
        self.on_plugin_unregistered: Optional[callable] = None
    
    def register_plugin(self, plugin: EffectPlugin, ui: Optional[EffectUI] = None) -> bool:
        """
        Register a plugin with the registry.
        
        Args:
            plugin: EffectPlugin instance
            ui: Optional EffectUI instance
            
        Returns:
            True if registration was successful
        """
        try:
            plugin_id = self._generate_plugin_id(plugin)
            
            # Check if plugin already exists
            if plugin_id in self.plugins:
                self.logger.warning(f"Plugin {plugin_id} already registered, updating...")
            
            # Register plugin
            self.plugins[plugin_id] = plugin
            
            # Register UI component if provided
            if ui:
                self.ui_components[plugin_id] = ui
            
            # Add to category
            category = plugin.category
            if category not in self.categories:
                self.categories[category] = []
            if plugin_id not in self.categories[category]:
                self.categories[category].append(plugin_id)
            
            # Store metadata
            self.plugin_metadata[plugin_id] = plugin.get_metadata()
            
            self.logger.info(f"Registered plugin: {plugin_id} ({plugin.name})")
            
            # Call callback
            if self.on_plugin_registered:
                self.on_plugin_registered(plugin_id, plugin)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register plugin: {e}")
            return False
    
    def unregister_plugin(self, plugin_id: str) -> bool:
        """
        Unregister a plugin from the registry.
        
        Args:
            plugin_id: ID of the plugin to unregister
            
        Returns:
            True if unregistration was successful
        """
        try:
            if plugin_id not in self.plugins:
                self.logger.warning(f"Plugin {plugin_id} not found in registry")
                return False
            
            # Get plugin for callback
            plugin = self.plugins[plugin_id]
            
            # Clean up plugin
            plugin.cleanup()
            
            # Clean up UI component
            if plugin_id in self.ui_components:
                self.ui_components[plugin_id].cleanup()
                del self.ui_components[plugin_id]
            
            # Remove from plugins
            del self.plugins[plugin_id]
            
            # Remove from categories
            for category in self.categories.values():
                if plugin_id in category:
                    category.remove(plugin_id)
            
            # Remove metadata
            if plugin_id in self.plugin_metadata:
                del self.plugin_metadata[plugin_id]
            
            self.logger.info(f"Unregistered plugin: {plugin_id}")
            
            # Call callback
            if self.on_plugin_unregistered:
                self.on_plugin_unregistered(plugin_id, plugin)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unregister plugin {plugin_id}: {e}")
            return False
    
    def get_plugin(self, plugin_id: str) -> Optional[EffectPlugin]:
        """
        Get a plugin by ID.
        
        Args:
            plugin_id: ID of the plugin
            
        Returns:
            EffectPlugin instance or None if not found
        """
        return self.plugins.get(plugin_id)
    
    def get_ui_component(self, plugin_id: str) -> Optional[EffectUI]:
        """
        Get UI component for a plugin.
        
        Args:
            plugin_id: ID of the plugin
            
        Returns:
            EffectUI instance or None if not found
        """
        return self.ui_components.get(plugin_id)
    
    def get_plugins_by_category(self, category: str) -> List[EffectPlugin]:
        """
        Get all plugins in a specific category.
        
        Args:
            category: Category name
            
        Returns:
            List of EffectPlugin instances
        """
        plugin_ids = self.categories.get(category, [])
        return [self.plugins[pid] for pid in plugin_ids if pid in self.plugins]
    
    def get_all_plugins(self) -> List[EffectPlugin]:
        """
        Get all registered plugins.
        
        Returns:
            List of all EffectPlugin instances
        """
        return list(self.plugins.values())
    
    def get_all_categories(self) -> List[str]:
        """
        Get all plugin categories.
        
        Returns:
            List of category names
        """
        return list(self.categories.keys())
    
    def get_plugin_metadata(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a plugin.
        
        Args:
            plugin_id: ID of the plugin
            
        Returns:
            Plugin metadata dictionary or None if not found
        """
        return self.plugin_metadata.get(plugin_id)
    
    def search_plugins(self, query: str) -> List[EffectPlugin]:
        """
        Search for plugins by name, description, or tags.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching EffectPlugin instances
        """
        query = query.lower()
        results = []
        
        for plugin_id, metadata in self.plugin_metadata.items():
            # Search in name
            if query in metadata.get('name', '').lower():
                results.append(self.plugins[plugin_id])
                continue
            
            # Search in description
            if query in metadata.get('description', '').lower():
                results.append(self.plugins[plugin_id])
                continue
            
            # Search in tags
            tags = metadata.get('tags', [])
            if any(query in tag.lower() for tag in tags):
                results.append(self.plugins[plugin_id])
                continue
        
        return results
    
    def get_enabled_plugins(self) -> List[EffectPlugin]:
        """
        Get all enabled plugins.
        
        Returns:
            List of enabled EffectPlugin instances
        """
        return [plugin for plugin in self.plugins.values() if plugin.is_enabled]
    
    def enable_plugin(self, plugin_id: str) -> bool:
        """
        Enable a plugin.
        
        Args:
            plugin_id: ID of the plugin
            
        Returns:
            True if successful
        """
        plugin = self.get_plugin(plugin_id)
        if plugin:
            plugin.enable()
            return True
        return False
    
    def disable_plugin(self, plugin_id: str) -> bool:
        """
        Disable a plugin.
        
        Args:
            plugin_id: ID of the plugin
            
        Returns:
            True if successful
        """
        plugin = self.get_plugin(plugin_id)
        if plugin:
            plugin.disable()
            return True
        return False
    
    def _generate_plugin_id(self, plugin: EffectPlugin) -> str:
        """
        Generate a unique ID for a plugin.
        
        Args:
            plugin: EffectPlugin instance
            
        Returns:
            Unique plugin ID
        """
        # Use name and version to create unique ID
        base_id = f"{plugin.name}_{plugin.version}".replace(" ", "_").lower()
        
        # Ensure uniqueness
        counter = 1
        plugin_id = base_id
        while plugin_id in self.plugins:
            plugin_id = f"{base_id}_{counter}"
            counter += 1
        
        return plugin_id
    
    def clear(self):
        """Clear all registered plugins."""
        try:
            # Clean up all plugins
            for plugin in self.plugins.values():
                plugin.cleanup()
            
            # Clean up all UI components
            for ui in self.ui_components.values():
                ui.cleanup()
            
            # Clear all collections
            self.plugins.clear()
            self.ui_components.clear()
            self.categories.clear()
            self.plugin_metadata.clear()
            
            self.logger.info("Plugin registry cleared")
            
        except Exception as e:
            self.logger.error(f"Error clearing plugin registry: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the plugin registry.
        
        Returns:
            Dictionary containing registry statistics
        """
        total_plugins = len(self.plugins)
        enabled_plugins = len(self.get_enabled_plugins())
        total_categories = len(self.categories)
        
        category_counts = {}
        for category, plugin_ids in self.categories.items():
            category_counts[category] = len(plugin_ids)
        
        return {
            'total_plugins': total_plugins,
            'enabled_plugins': enabled_plugins,
            'disabled_plugins': total_plugins - enabled_plugins,
            'total_categories': total_categories,
            'category_counts': category_counts
        } 