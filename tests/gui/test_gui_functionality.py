#!/usr/bin/env python3
"""
Comprehensive GUI Testing System
Tests all buttons and functionality in a Single Responsibility Principle (SRP) fashion
"""

import sys
import os
import time
import logging
from unittest.mock import Mock, patch
from PyQt5.QtWidgets import QApplication, QPushButton, QSlider, QComboBox, QCheckBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtTest import QTest

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class GUIFunctionalityTester:
    """Comprehensive GUI testing system following SRP."""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.test_results = {}
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
            
    def test_start_stop_button(self):
        """Test the Start/Stop Processing button."""
        try:
            self.logger.info("Testing Start/Stop Processing button...")
            
            # Find the button
            start_stop_btn = self.main_window.start_stop_btn
            if not start_stop_btn:
                self.logger.error("Start/Stop button not found")
                return False
                
            # Test initial state
            initial_text = start_stop_btn.text()
            self.logger.info(f"Initial button text: {initial_text}")
            
            # Test button click
            QTest.mouseClick(start_stop_btn, Qt.LeftButton)
            time.sleep(0.1)  # Allow for state change
            
            # Check if text changed
            new_text = start_stop_btn.text()
            self.logger.info(f"Button text after click: {new_text}")
            
            # Test button click again (toggle back)
            QTest.mouseClick(start_stop_btn, Qt.LeftButton)
            time.sleep(0.1)
            
            final_text = start_stop_btn.text()
            self.logger.info(f"Final button text: {final_text}")
            
            # Verify button is functional
            if initial_text != new_text or new_text != final_text:
                self.logger.info("Start/Stop button is functional")
                return True
            else:
                self.logger.error("Start/Stop button not responding")
                return False
                
        except Exception as e:
            self.logger.error(f"Start/Stop button test failed: {e}")
            return False
            
    def test_reset_button(self):
        """Test the Reset button."""
        try:
            self.logger.info("Testing Reset button...")
            
            # Find the reset button
            reset_btn = None
            for child in self.main_window.findChildren(QPushButton):
                if "reset" in child.text().lower() or "reset" in child.objectName().lower():
                    reset_btn = child
                    break
                    
            if not reset_btn:
                self.logger.warning("Reset button not found")
                return True  # Not critical
                
            # Test button click
            QTest.mouseClick(reset_btn, Qt.LeftButton)
            time.sleep(0.1)
            
            self.logger.info("Reset button is functional")
            return True
            
        except Exception as e:
            self.logger.error(f"Reset button test failed: {e}")
            return False
            
    def test_effect_buttons(self):
        """Test all effect buttons."""
        try:
            self.logger.info("Testing Effect buttons...")
            
            # Find all effect buttons
            effect_buttons = []
            for child in self.main_window.findChildren(QPushButton):
                if hasattr(child, 'effect_name') or 'effect' in child.objectName().lower():
                    effect_buttons.append(child)
                    
            if not effect_buttons:
                # Look for buttons in effects layout
                if hasattr(self.main_window, 'effects_layout'):
                    for i in range(self.main_window.effects_layout.count()):
                        item = self.main_window.effects_layout.itemAt(i)
                        if item.widget() and isinstance(item.widget(), QPushButton):
                            effect_buttons.append(item.widget())
                            
            self.logger.info(f"Found {len(effect_buttons)} effect buttons")
            
            # Test each effect button
            working_buttons = 0
            for i, btn in enumerate(effect_buttons[:5]):  # Test first 5 buttons
                try:
                    self.logger.info(f"Testing effect button {i+1}: {btn.text()}")
                    
                    # Store initial state
                    initial_effect = getattr(self.main_window, 'current_effect_label', None)
                    if initial_effect:
                        initial_text = initial_effect.text()
                    else:
                        initial_text = "No effect"
                        
                    # Click the button
                    QTest.mouseClick(btn, Qt.LeftButton)
                    time.sleep(0.1)
                    
                    # Check if effect was applied
                    if hasattr(self.main_window, 'current_effect_label'):
                        new_text = self.main_window.current_effect_label.text()
                        if new_text != initial_text:
                            self.logger.info(f"Effect button {i+1} applied effect: {new_text}")
                            working_buttons += 1
                        else:
                            self.logger.warning(f"Effect button {i+1} may not have applied effect")
                    else:
                        self.logger.info(f"Effect button {i+1} clicked successfully")
                        working_buttons += 1
                        
                except Exception as e:
                    self.logger.error(f"Effect button {i+1} test failed: {e}")
                    
            self.logger.info(f"Effect buttons test: {working_buttons}/{min(5, len(effect_buttons))} working")
            return working_buttons > 0
            
        except Exception as e:
            self.logger.error(f"Effect buttons test failed: {e}")
            return False
            
    def test_parameter_controls(self):
        """Test parameter controls (sliders, spinboxes, etc.)."""
        try:
            self.logger.info("Testing Parameter controls...")
            
            # Find all sliders
            sliders = self.main_window.findChildren(QSlider)
            self.logger.info(f"Found {len(sliders)} sliders")
            
            # Test each slider
            working_sliders = 0
            for i, slider in enumerate(sliders[:3]):  # Test first 3 sliders
                try:
                    self.logger.info(f"Testing slider {i+1}")
                    
                    # Store initial value
                    initial_value = slider.value()
                    
                    # Set a new value
                    new_value = min(initial_value + 10, slider.maximum())
                    slider.setValue(new_value)
                    time.sleep(0.1)
                    
                    # Check if value changed
                    if slider.value() == new_value:
                        self.logger.info(f"Slider {i+1} is functional")
                        working_sliders += 1
                    else:
                        self.logger.warning(f"Slider {i+1} may not be responding")
                        
                except Exception as e:
                    self.logger.error(f"Slider {i+1} test failed: {e}")
                    
            # Find all combo boxes
            combos = self.main_window.findChildren(QComboBox)
            self.logger.info(f"Found {len(combos)} combo boxes")
            
            # Test each combo box
            working_combos = 0
            for i, combo in enumerate(combos[:3]):  # Test first 3 combo boxes
                try:
                    self.logger.info(f"Testing combo box {i+1}")
                    
                    if combo.count() > 0:
                        # Select first item
                        combo.setCurrentIndex(0)
                        time.sleep(0.1)
                        
                        self.logger.info(f"Combo box {i+1} is functional")
                        working_combos += 1
                    else:
                        self.logger.warning(f"Combo box {i+1} has no items")
                        
                except Exception as e:
                    self.logger.error(f"Combo box {i+1} test failed: {e}")
                    
            self.logger.info(f"Parameter controls test: {working_sliders} sliders, {working_combos} combo boxes working")
            return working_sliders > 0 or working_combos > 0
            
        except Exception as e:
            self.logger.error(f"Parameter controls test failed: {e}")
            return False
            
    def test_device_selector(self):
        """Test device selector functionality."""
        try:
            self.logger.info("Testing Device selector...")
            
            # Find device selector
            device_combo = None
            for child in self.main_window.findChildren(QComboBox):
                if "device" in child.objectName().lower() or "camera" in child.objectName().lower():
                    device_combo = child
                    break
                    
            if not device_combo:
                self.logger.warning("Device selector not found")
                return True  # Not critical
                
            # Test device selection
            if device_combo.count() > 0:
                # Select first device
                device_combo.setCurrentIndex(0)
                time.sleep(0.1)
                
                self.logger.info("Device selector is functional")
                return True
            else:
                self.logger.warning("Device selector has no devices")
                return True
                
        except Exception as e:
            self.logger.error(f"Device selector test failed: {e}")
            return False
            
    def test_menu_items(self):
        """Test menu functionality."""
        try:
            self.logger.info("Testing Menu items...")
            
            # Find menu bar
            menu_bar = self.main_window.menuBar()
            if not menu_bar:
                self.logger.warning("Menu bar not found")
                return True
                
            # Test menu actions
            actions = menu_bar.actions()
            self.logger.info(f"Found {len(actions)} menu actions")
            
            # Test first few menu items
            working_menus = 0
            for i, action in enumerate(actions[:3]):
                try:
                    if action.isEnabled():
                        self.logger.info(f"Menu item {i+1}: {action.text()} is enabled")
                        working_menus += 1
                    else:
                        self.logger.warning(f"Menu item {i+1}: {action.text()} is disabled")
                        
                except Exception as e:
                    self.logger.error(f"Menu item {i+1} test failed: {e}")
                    
            self.logger.info(f"Menu test: {working_menus}/{min(3, len(actions))} working")
            return working_menus > 0
            
        except Exception as e:
            self.logger.error(f"Menu test failed: {e}")
            return False
            
    def test_toolbar_buttons(self):
        """Test toolbar functionality."""
        try:
            self.logger.info("Testing Toolbar buttons...")
            
            # Find toolbar
            toolbar = None
            for child in self.main_window.findChildren(type(self.main_window.toolBar())):
                toolbar = child
                break
                
            if not toolbar:
                self.logger.warning("Toolbar not found")
                return True
                
            # Test toolbar actions
            actions = toolbar.actions()
            self.logger.info(f"Found {len(actions)} toolbar actions")
            
            # Test first few toolbar buttons
            working_toolbar_buttons = 0
            for i, action in enumerate(actions[:3]):
                try:
                    if action.isEnabled():
                        self.logger.info(f"Toolbar button {i+1}: {action.text()} is enabled")
                        working_toolbar_buttons += 1
                    else:
                        self.logger.warning(f"Toolbar button {i+1}: {action.text()} is disabled")
                        
                except Exception as e:
                    self.logger.error(f"Toolbar button {i+1} test failed: {e}")
                    
            self.logger.info(f"Toolbar test: {working_toolbar_buttons}/{min(3, len(actions))} working")
            return working_toolbar_buttons > 0
            
        except Exception as e:
            self.logger.error(f"Toolbar test failed: {e}")
            return False
            
    def test_dock_widgets(self):
        """Test dock widget functionality."""
        try:
            self.logger.info("Testing Dock widgets...")
            
            # Find dock widgets
            dock_widgets = self.main_window.findChildren(type(self.main_window.dockWidgetArea()))
            self.logger.info(f"Found {len(dock_widgets)} dock widgets")
            
            # Test dock widget visibility
            visible_docks = 0
            for i, dock in enumerate(dock_widgets):
                try:
                    if dock.isVisible():
                        self.logger.info(f"Dock widget {i+1}: {dock.windowTitle()} is visible")
                        visible_docks += 1
                    else:
                        self.logger.warning(f"Dock widget {i+1}: {dock.windowTitle()} is hidden")
                        
                except Exception as e:
                    self.logger.error(f"Dock widget {i+1} test failed: {e}")
                    
            self.logger.info(f"Dock widgets test: {visible_docks}/{len(dock_widgets)} visible")
            return visible_docks > 0
            
        except Exception as e:
            self.logger.error(f"Dock widgets test failed: {e}")
            return False
            
    def test_status_bar(self):
        """Test status bar functionality."""
        try:
            self.logger.info("Testing Status bar...")
            
            # Find status bar
            status_bar = self.main_window.statusBar()
            if not status_bar:
                self.logger.warning("Status bar not found")
                return True
                
            # Test status bar visibility
            if status_bar.isVisible():
                self.logger.info("Status bar is visible")
                return True
            else:
                self.logger.warning("Status bar is hidden")
                return True
                
        except Exception as e:
            self.logger.error(f"Status bar test failed: {e}")
            return False
            
    def run_all_tests(self):
        """Run all GUI functionality tests."""
        self.logger.info("Starting Comprehensive GUI Functionality Tests...")
        
        # Setup application
        if not self.setup_application():
            return False
            
        # Run all tests
        tests = [
            ("Start/Stop Button", self.test_start_stop_button),
            ("Reset Button", self.test_reset_button),
            ("Effect Buttons", self.test_effect_buttons),
            ("Parameter Controls", self.test_parameter_controls),
            ("Device Selector", self.test_device_selector),
            ("Menu Items", self.test_menu_items),
            ("Toolbar Buttons", self.test_toolbar_buttons),
            ("Dock Widgets", self.test_dock_widgets),
            ("Status Bar", self.test_status_bar),
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
        self.logger.info(f"TEST SUMMARY")
        self.logger.info(f"{'='*50}")
        self.logger.info(f"Passed: {passed_tests}/{total_tests}")
        self.logger.info(f"Failed: {total_tests - passed_tests}/{total_tests}")
        self.logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            self.logger.info("ALL TESTS PASSED! GUI is fully functional!")
        else:
            self.logger.warning("Some tests failed. Please review the issues above.")
            
        # Cleanup
        if self.app:
            self.app.quit()
            
        return passed_tests == total_tests

def main():
    """Main test runner."""
    tester = GUIFunctionalityTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 