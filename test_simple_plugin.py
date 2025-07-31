#!/usr/bin/env python3
"""
Simple Plugin Test

Tests the basic plugin system functionality.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication
from src.plugins.plugin_manager import PluginManager

def test_plugin_system():
    """Test the plugin system."""
    print("=== Simple Plugin Test ===")
    
    # Create QApplication for UI components
    app = QApplication(sys.argv)
    
    try:
        # Test plugin manager import
        print("✓ PluginManager imported")
        
        # Create plugin manager
        plugin_manager = PluginManager()
        print("✓ PluginManager created")
        
        # Initialize with plugin directory
        plugin_dir = os.path.join(project_root, "src", "plugins", "effects")
        print(f"Initializing with plugin directory: {plugin_dir}")
        plugin_manager.initialize([plugin_dir])
        
        # Get loaded effects
        effects = plugin_manager.get_all_effects()
        print(f"Found {len(effects)} effects:")
        
        for effect in effects:
            print(f"  - {effect.name} ({effect.category})")
            print(f"    Description: {effect.description}")
            print(f"    Parameters: {effect.get_parameters()}")
        
        # Test UI creation for each plugin
        print("\nTesting UI creation...")
        for effect in effects:
            try:
                # Get the effect ID by searching for the effect in the registry
                effect_id = None
                for plugin_id, plugin in plugin_manager.registry.plugins.items():
                    if plugin == effect:
                        effect_id = plugin_id
                        break
                
                if effect_id:
                    ui = plugin_manager.get_effect_ui(effect_id)
                    if ui:
                        print(f"✓ UI created for {effect.name}")
                    else:
                        print(f"✗ No UI found for {effect.name}")
                else:
                    print(f"✗ Could not find effect ID for {effect.name}")
            except Exception as e:
                print(f"✗ Error creating UI for {effect.name}: {e}")
        
        print("\n✓ Plugin test passed!")
        
    except Exception as e:
        print(f"✗ Plugin test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_plugin_system() 