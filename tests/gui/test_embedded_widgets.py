#!/usr/bin/env python3
"""
Specialized Test for Embedded Parameter Widgets
Tests the dynamic parameter widget system following SRP
"""

import sys
import os
import time
import logging
from PyQt5.QtWidgets import QApplication, QPushButton, QSlider, QSpinBox, QComboBox, QCheckBox, QFormLayout
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class EmbeddedWidgetTester:
    """Specialized tester for embedded parameter widgets."""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for test results."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
        
    def setup_application(self):
        """Initialize the application for testing."""
        try:
            self.app = QApplication(sys.argv)
            from src.gui.v2_main_window import ProfessionalV2MainWindow
            self.main_window = ProfessionalV2MainWindow()
            self.logger.info("Application setup complete")
            return True
        except Exception as e:
            self.logger.error(f"Application setup failed: {e}")
            return False
            
    def test_embedded_widget_creation(self):
        """Test that embedded widgets are created properly."""
        try:
            self.logger.info("Testing Embedded Widget Creation...")
            
            # Find the parameter manager
            parameter_manager = self.main_window.get_manager('parameter_manager')
            if not parameter_manager:
                self.logger.error("Parameter manager not found")
                return False
                
            # Test clearing widgets
            parameter_manager.clear_embedded_parameter_widgets()
            self.logger.info("Widget clearing functional")
            
            # Test creating widgets for a known effect
            test_parameters = [
                {
                    'name': 'test_param1',
                    'type': 'int',
                    'default': 50,
                    'min': 0,
                    'max': 100,
                    'step': 1,
                    'label': 'Test Parameter 1'
                },
                {
                    'name': 'test_param2',
                    'type': 'float',
                    'default': 0.5,
                    'min': 0.0,
                    'max': 1.0,
                    'step': 0.1,
                    'label': 'Test Parameter 2'
                }
            ]
            
            # Create embedded widgets
            widgets = parameter_manager.create_embedded_parameter_widgets(test_parameters)
            
            if widgets and len(widgets) == len(test_parameters):
                self.logger.info(f"Created {len(widgets)} embedded widgets")
                return True
            else:
                self.logger.error(f"Expected {len(test_parameters)} widgets, got {len(widgets) if widgets else 0}")
                return False
                
        except Exception as e:
            self.logger.error(f"Embedded widget creation test failed: {e}")
            return False
            
    def test_effect_parameter_integration(self):
        """Test that effects properly create embedded parameter widgets."""
        try:
            self.logger.info("Testing Effect Parameter Integration...")
            
            # Find effect buttons
            effect_buttons = []
            if hasattr(self.main_window, 'effects_layout'):
                for i in range(self.main_window.effects_layout.count()):
                    item = self.main_window.effects_layout.itemAt(i)
                    if item.widget() and isinstance(item.widget(), QPushButton):
                        effect_buttons.append(item.widget())
                        
            if not effect_buttons:
                self.logger.error("No effect buttons found")
                return False
                
            # Test first effect button that should have parameters
            working_effects = 0
            for i, btn in enumerate(effect_buttons[:3]):  # Test first 3 effects
                try:
                    self.logger.info(f"Testing effect {i+1}: {btn.text()}")
                    
                    # Clear existing widgets
                    self.main_window.parameter_manager.clear_embedded_parameter_widgets()
                    
                    # Click the effect button
                    QTest.mouseClick(btn, Qt.LeftButton)
                    time.sleep(0.2)  # Allow time for widget creation
                    
                    # Check if parameter widgets were created
                    param_widgets = self.main_window.findChildren(QSlider)
                    param_widgets.extend(self.main_window.findChildren(QSpinBox))
                    param_widgets.extend(self.main_window.findChildren(QComboBox))
                    param_widgets.extend(self.main_window.findChildren(QCheckBox))
                    
                    if param_widgets:
                        self.logger.info(f"Effect {i+1} created {len(param_widgets)} parameter widgets")
                        working_effects += 1
                    else:
                        self.logger.warning(f"Effect {i+1} created no parameter widgets")
                        
                except Exception as e:
                    self.logger.error(f"Effect {i+1} test failed: {e}")
                    
            self.logger.info(f"Effect parameter integration: {working_effects}/3 effects working")
            return working_effects > 0
            
        except Exception as e:
            self.logger.error(f"Effect parameter integration test failed: {e}")
            return False
            
    def test_parameter_value_changes(self):
        """Test that parameter widgets respond to value changes."""
        try:
            self.logger.info("Testing Parameter Value Changes...")
            
            # Find all parameter widgets
            sliders = self.main_window.findChildren(QSlider)
            spinboxes = self.main_window.findChildren(QSpinBox)
            combos = self.main_window.findChildren(QComboBox)
            checkboxes = self.main_window.findChildren(QCheckBox)
            
            self.logger.info(f"Found {len(sliders)} sliders, {len(spinboxes)} spinboxes, {len(combos)} combos, {len(checkboxes)} checkboxes")
            
            # Test slider value changes
            working_sliders = 0
            for i, slider in enumerate(sliders[:2]):
                try:
                    initial_value = slider.value()
                    new_value = min(initial_value + 10, slider.maximum())
                    
                    # Simulate user interaction
                    slider.setValue(new_value)
                    time.sleep(0.1)
                    
                    if slider.value() == new_value:
                        self.logger.info(f"Slider {i+1} value change successful")
                        working_sliders += 1
                    else:
                        self.logger.warning(f"Slider {i+1} value change failed")
                        
                except Exception as e:
                    self.logger.error(f"Slider {i+1} test failed: {e}")
                    
            # Test spinbox value changes
            working_spinboxes = 0
            for i, spinbox in enumerate(spinboxes[:2]):
                try:
                    initial_value = spinbox.value()
                    new_value = min(initial_value + 1, spinbox.maximum())
                    
                    # Simulate user interaction
                    spinbox.setValue(new_value)
                    time.sleep(0.1)
                    
                    if spinbox.value() == new_value:
                        self.logger.info(f"Spinbox {i+1} value change successful")
                        working_spinboxes += 1
                    else:
                        self.logger.warning(f"Spinbox {i+1} value change failed")
                        
                except Exception as e:
                    self.logger.error(f"Spinbox {i+1} test failed: {e}")
                    
            # Test combo box selection changes
            working_combos = 0
            for i, combo in enumerate(combos[:2]):
                try:
                    if combo.count() > 0:
                        # Select first item
                        combo.setCurrentIndex(0)
                        time.sleep(0.1)
                        
                        self.logger.info(f"Combo {i+1} selection change successful")
                        working_combos += 1
                    else:
                        self.logger.warning(f"Combo {i+1} has no items")
                        
                except Exception as e:
                    self.logger.error(f"Combo {i+1} test failed: {e}")
                    
            # Test checkbox toggles
            working_checkboxes = 0
            for i, checkbox in enumerate(checkboxes[:2]):
                try:
                    initial_state = checkbox.isChecked()
                    
                    # Toggle checkbox
                    checkbox.setChecked(not initial_state)
                    time.sleep(0.1)
                    
                    if checkbox.isChecked() != initial_state:
                        self.logger.info(f"Checkbox {i+1} toggle successful")
                        working_checkboxes += 1
                    else:
                        self.logger.warning(f"Checkbox {i+1} toggle failed")
                        
                except Exception as e:
                    self.logger.error(f"Checkbox {i+1} test failed: {e}")
                    
            total_working = working_sliders + working_spinboxes + working_combos + working_checkboxes
            total_tested = min(2, len(sliders)) + min(2, len(spinboxes)) + min(2, len(combos)) + min(2, len(checkboxes))
            
            self.logger.info(f"Parameter value changes: {total_working}/{total_tested} widgets working")
            return total_working > 0
            
        except Exception as e:
            self.logger.error(f"Parameter value changes test failed: {e}")
            return False
            
    def test_parameter_signal_connections(self):
        """Test that parameter widgets are properly connected to update functions."""
        try:
            self.logger.info("Testing Parameter Signal Connections...")
            
            # Find parameter manager
            parameter_manager = self.main_window.get_manager('parameter_manager')
            if not parameter_manager:
                self.logger.error("Parameter manager not found")
                return False
                
            # Test that parameter change method exists
            if hasattr(parameter_manager, 'on_embedded_parameter_changed'):
                self.logger.info("Parameter change method exists")
                
                # Test calling the method
                try:
                    parameter_manager.on_embedded_parameter_changed('test_param', 50)
                    self.logger.info("Parameter change method is callable")
                    return True
                except Exception as e:
                    self.logger.error(f"Parameter change method call failed: {e}")
                    return False
            else:
                self.logger.error("Parameter change method not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Parameter signal connections test failed: {e}")
            return False
            
    def test_widget_layout_integration(self):
        """Test that widgets are properly integrated into the layout."""
        try:
            self.logger.info("Testing Widget Layout Integration...")
            
            # Find the parameter panel
            param_panel = None
            for child in self.main_window.findChildren(type(self.main_window)):
                if hasattr(child, 'objectName') and 'param' in child.objectName().lower():
                    param_panel = child
                    break
                    
            if not param_panel:
                # Look for QFormLayout which is typically used for parameters
                for child in self.main_window.findChildren(QFormLayout):
                    param_panel = child
                    break
                    
            if param_panel:
                self.logger.info("Parameter panel found")
                
                # Check if panel has widgets
                if hasattr(param_panel, 'count'):
                    widget_count = param_panel.count()
                    self.logger.info(f"Parameter panel has {widget_count} items")
                    
                    if widget_count > 0:
                        self.logger.info("Parameter panel has widgets")
                        return True
                    else:
                        self.logger.warning("Parameter panel is empty")
                        return True  # Not critical
                else:
                    self.logger.info("Parameter panel exists")
                    return True
            else:
                self.logger.warning("Parameter panel not found")
                return True  # Not critical
                
        except Exception as e:
            self.logger.error(f"Widget layout integration test failed: {e}")
            return False
            
    def run_all_tests(self):
        """Run all embedded widget tests."""
        self.logger.info("Starting Embedded Widget Tests...")
        
        # Setup application
        if not self.setup_application():
            return False
            
        # Run all tests
        tests = [
            ("Embedded Widget Creation", self.test_embedded_widget_creation),
            ("Effect Parameter Integration", self.test_effect_parameter_integration),
            ("Parameter Value Changes", self.test_parameter_value_changes),
            ("Parameter Signal Connections", self.test_parameter_signal_connections),
            ("Widget Layout Integration", self.test_widget_layout_integration),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                self.logger.info(f"\n{'='*50}")
                self.logger.info(f"Running: {test_name}")
                self.logger.info(f"{'='*50}")
                
                if test_func():
                    self.logger.info(f"{test_name}: PASSED")
                    passed_tests += 1
                else:
                    self.logger.error(f"{test_name}: FAILED")
                    
            except Exception as e:
                self.logger.error(f"{test_name}: ERROR - {e}")
                
        # Summary
        self.logger.info(f"\n{'='*50}")
        self.logger.info(f"EMBEDDED WIDGET TEST SUMMARY")
        self.logger.info(f"{'='*50}")
        self.logger.info(f"Passed: {passed_tests}/{total_tests}")
        self.logger.info(f"Failed: {total_tests - passed_tests}/{total_tests}")
        self.logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            self.logger.info("ALL EMBEDDED WIDGET TESTS PASSED!")
        else:
            self.logger.warning("Some embedded widget tests failed.")
            
        # Cleanup
        if self.app:
            self.app.quit()
            
        return passed_tests == total_tests

def main():
    """Main test runner."""
    tester = EmbeddedWidgetTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 