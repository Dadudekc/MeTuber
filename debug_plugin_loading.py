#!/usr/bin/env python3
"""
Debug Plugin Loading

Test the plugin loading process step by step.
"""

import sys
import os
import importlib.util
from PyQt5.QtWidgets import QApplication

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_module_loading():
    """Test loading a plugin module directly."""
    print("=== Testing Module Loading ===")
    
    # Test loading cartoon effect
    plugin_dir = "src/plugins/effects/artistic/cartoon_effect"
    init_file = os.path.join(plugin_dir, "__init__.py")
    
    print(f"Plugin directory: {plugin_dir}")
    print(f"Init file exists: {os.path.exists(init_file)}")
    
    if os.path.exists(init_file):
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location("cartoon_effect", init_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            print("✓ Module loaded successfully")
            print(f"Module attributes: {dir(module)}")
            
            # Check for register_plugin function
            if hasattr(module, 'register_plugin'):
                print("✓ register_plugin function found")
                
                # Test calling register_plugin
                from src.plugins.plugin_registry import PluginRegistry
                registry = PluginRegistry()
                
                try:
                    module.register_plugin(registry)
                    print("✓ register_plugin called successfully")
                    print(f"Registered plugins: {list(registry.plugins.keys())}")
                except Exception as e:
                    print(f"✗ Error calling register_plugin: {e}")
            else:
                print("✗ register_plugin function not found")
                
        except Exception as e:
            print(f"✗ Error loading module: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("✗ Init file not found")

def test_plugin_manager():
    """Test the plugin manager."""
    print("\n=== Testing Plugin Manager ===")
    
    try:
        from src.plugins.plugin_manager import PluginManager
        
        manager = PluginManager()
        print("✓ PluginManager created")
        
        # Initialize with plugin directory
        plugin_dir = os.path.join(project_root, "src/plugins/effects")
        manager.initialize([plugin_dir])
        print(f"✓ Initialized with plugin directory: {plugin_dir}")
        
        # Get all effects
        effects = manager.get_all_effects()
        print(f"✓ Found {len(effects)} effects")
        
        for effect in effects:
            print(f"  - {effect.name} ({effect.category})")
        
        # Test UI creation
        print("\nTesting UI creation...")
        for effect in effects:
            try:
                # Generate plugin ID (same as registry does)
                plugin_id = f"{effect.name}_{effect.version}".replace(" ", "_").lower()
                ui = manager.get_effect_ui(plugin_id)
                if ui:
                    print(f"✓ UI created for {effect.name}")
                else:
                    print(f"✗ No UI for {effect.name}")
            except Exception as e:
                print(f"✗ Error creating UI for {effect.name}: {e}")
        
    except Exception as e:
        print(f"✗ Error testing plugin manager: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Create QApplication first
    app = QApplication(sys.argv)
    
    test_module_loading()
    test_plugin_manager() 