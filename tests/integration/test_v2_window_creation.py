import pytest
from PyQt5.QtWidgets import QApplication
import sys
import os
from pytestqt.qt_api import QtTest

# Add project root to sys.path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.gui.v2_main_window import ProfessionalV2MainWindow

@pytest.fixture(scope="module")
def qapp():
    """Create a QApplication instance."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    app.quit()

def test_main_window_creation(qapp, qtbot):
    """Test that the ProfessionalV2MainWindow can be created without crashing."""
    window = ProfessionalV2MainWindow()
    qtbot.addWidget(window)
    
    # Use QtTest to wait for the window to be shown
    QtTest.QTest.qWaitForWindowExposed(window)
    
    window.close() 