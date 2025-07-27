#!/usr/bin/env python3
"""
DraggableWidget Base Class
Professional draggable, resizable, dockable widget system for filter parameters.
"""

import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QSizeGrip, QApplication, QScrollArea, QGroupBox, QFormLayout,
    QSlider, QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QIcon
import logging


class DraggableWidget(QWidget):
    """
    Base class for draggable, resizable, dockable widgets.
    Provides all the professional window management features.
    """
    
    # Signals for widget management
    widget_closed = pyqtSignal(object)  # Emitted when widget is closed
    widget_docked = pyqtSignal(object, str)  # Emitted when widget is docked
    widget_undocked = pyqtSignal(object)  # Emitted when widget is undocked
    parameters_changed = pyqtSignal(dict)  # Emitted when parameters change
    
    def __init__(self, title="Widget", parent=None):
        super().__init__(parent)
        
        self.logger = logging.getLogger(__name__)
        self.title = title
        self.is_docked = False
        self.is_minimized = False
        self.is_maximized = False
        self.dock_zone = None  # "left", "right", "bottom", "top", "floating"
        
        # Drag and resize state
        self.dragging = False
        self.resizing = False
        self.resize_edge = None
        self.drag_start_pos = QPoint()
        self.original_geometry = QRect()
        self.min_size = QSize(200, 150)
        self.max_size = QSize(800, 600)
        
        # Initialize UI
        self.setup_ui()
        self.setup_styling()
        self.setup_connections()
        
        # Parameter storage
        self.current_parameters = {}
        self.parameter_widgets = {}
        
    def setup_ui(self):
        """Set up the widget UI structure."""
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(self.min_size)
        self.setMaximumSize(self.max_size)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(0)
        
        # Create title bar
        self.create_title_bar()
        
        # Create content area
        self.create_content_area()
        
        # Create resize handles
        self.create_resize_handles()
        
    def create_title_bar(self):
        """Create the draggable title bar with controls."""
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(32)
        self.title_bar.setObjectName("titleBar")
        
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(8, 4, 4, 4)
        
        # Title label
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setFont(QFont("Arial", 10, QFont.Bold))
        title_layout.addWidget(self.title_label)
        
        title_layout.addStretch()
        
        # Control buttons
        self.create_title_buttons(title_layout)
        
        self.main_layout.addWidget(self.title_bar)
        
    def create_title_buttons(self, layout):
        """Create minimize, maximize, dock, close buttons."""
        button_size = 20
        
        # Minimize button
        self.minimize_btn = QPushButton("🗕")
        self.minimize_btn.setFixedSize(button_size, button_size)
        self.minimize_btn.setObjectName("minimizeBtn")
        self.minimize_btn.clicked.connect(self.toggle_minimize)
        layout.addWidget(self.minimize_btn)
        
        # Maximize button
        self.maximize_btn = QPushButton("🗖")
        self.maximize_btn.setFixedSize(button_size, button_size)
        self.maximize_btn.setObjectName("maximizeBtn")
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_btn)
        
        # Dock/Undock button
        self.dock_btn = QPushButton("📌")
        self.dock_btn.setFixedSize(button_size, button_size)
        self.dock_btn.setObjectName("dockBtn")
        self.dock_btn.clicked.connect(self.toggle_dock)
        layout.addWidget(self.dock_btn)
        
        # Close button
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(button_size, button_size)
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.clicked.connect(self.close_widget)
        layout.addWidget(self.close_btn)
        
    def create_content_area(self):
        """Create the scrollable content area for parameters."""
        # Content frame
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        
        # Scrollable area for parameters
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setObjectName("scrollArea")
        
        # Parameter container
        self.parameter_container = QWidget()
        self.parameter_layout = QVBoxLayout(self.parameter_container)
        self.parameter_layout.setContentsMargins(8, 8, 8, 8)
        self.parameter_layout.setSpacing(4)
        
        # Default content
        self.create_default_content()
        
        self.scroll_area.setWidget(self.parameter_container)
        
        # Content layout
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.scroll_area)
        
        self.main_layout.addWidget(self.content_frame)
        
    def create_default_content(self):
        """Create default content when no filter is selected."""
        default_label = QLabel("Select a filter to see parameters")
        default_label.setAlignment(Qt.AlignCenter)
        default_label.setObjectName("defaultLabel")
        self.parameter_layout.addWidget(default_label)
        self.parameter_layout.addStretch()
        
    def create_resize_handles(self):
        """Create resize handles for each edge and corner."""
        # Size grip for bottom-right corner resize
        self.size_grip = QSizeGrip(self)
        self.size_grip.setFixedSize(16, 16)
        
        # Position size grip
        self.position_size_grip()
        
    def position_size_grip(self):
        """Position the size grip at bottom-right corner."""
        self.size_grip.move(
            self.width() - self.size_grip.width(),
            self.height() - self.size_grip.height()
        )
        
    def setup_styling(self):
        """Set up the professional styling for the widget."""
        self.setStyleSheet("""
            DraggableWidget {
                background-color: rgba(42, 42, 42, 0.95);
                border: 2px solid #0096ff;
                border-radius: 8px;
            }
            
            DraggableWidget[docked="true"] {
                border: 1px solid #444;
                border-radius: 4px;
            }
            
            #titleBar {
                background-color: #0096ff;
                border-radius: 6px 6px 0 0;
                border: none;
            }
            
            #titleLabel {
                color: white;
                font-weight: bold;
            }
            
            #minimizeBtn, #maximizeBtn, #dockBtn, #closeBtn {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 3px;
                color: white;
                font-weight: bold;
            }
            
            #minimizeBtn:hover, #maximizeBtn:hover, #dockBtn:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            
            #closeBtn:hover {
                background-color: #ff4444;
            }
            
            #contentFrame {
                background-color: transparent;
                border: none;
            }
            
            #scrollArea {
                background-color: transparent;
                border: none;
            }
            
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 8px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #0096ff;
                border-radius: 4px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #1aa3ff;
            }
            
            #defaultLabel {
                color: #888;
                font-style: italic;
                padding: 20px;
            }
            
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 8px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
            }
            
            QLabel {
                color: white;
            }
            
            QSlider::groove:horizontal {
                background-color: #444;
                height: 6px;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal {
                background-color: #0096ff;
                width: 16px;
                border-radius: 8px;
                margin: -5px 0;
            }
            
            QSlider::handle:horizontal:hover {
                background-color: #1aa3ff;
            }
            
            QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 4px;
                color: white;
            }
            
            QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
                border-color: #0096ff;
            }
            
            QCheckBox {
                color: white;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #555;
                border-radius: 3px;
                background-color: #333;
            }
            
            QCheckBox::indicator:checked {
                background-color: #0096ff;
            }
        """)
        
    def setup_connections(self):
        """Set up signal connections."""
        # Timer for auto-hiding when minimized
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.auto_hide)
        
    # === DRAG AND DROP FUNCTIONALITY ===
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging."""
        if event.button() == Qt.LeftButton:
            if self.title_bar.geometry().contains(event.pos()):
                # Start dragging
                self.dragging = True
                self.drag_start_pos = event.globalPos() - self.pos()
                event.accept()
            else:
                # Check for resize edges
                self.check_resize_edges(event.pos())
        
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging and resizing."""
        if self.dragging and event.buttons() == Qt.LeftButton:
            # Drag the widget
            new_pos = event.globalPos() - self.drag_start_pos
            self.move(new_pos)
            self.check_dock_zones(event.globalPos())
            event.accept()
        elif self.resizing:
            # Resize the widget
            self.handle_resize(event.globalPos())
            event.accept()
        else:
            # Update cursor for resize edges
            self.update_cursor(event.pos())
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if event.button() == Qt.LeftButton:
            if self.dragging:
                self.dragging = False
                self.check_final_dock_position(event.globalPos())
            elif self.resizing:
                self.resizing = False
                self.resize_edge = None
                self.setCursor(Qt.ArrowCursor)
            event.accept()
            
    def check_resize_edges(self, pos):
        """Check if mouse is on resize edges."""
        rect = self.rect()
        edge_size = 8
        
        # Check edges
        if pos.x() <= edge_size:
            if pos.y() <= edge_size:
                self.resize_edge = "top-left"
            elif pos.y() >= rect.height() - edge_size:
                self.resize_edge = "bottom-left"
            else:
                self.resize_edge = "left"
        elif pos.x() >= rect.width() - edge_size:
            if pos.y() <= edge_size:
                self.resize_edge = "top-right"
            elif pos.y() >= rect.height() - edge_size:
                self.resize_edge = "bottom-right"
            else:
                self.resize_edge = "right"
        elif pos.y() <= edge_size:
            self.resize_edge = "top"
        elif pos.y() >= rect.height() - edge_size:
            self.resize_edge = "bottom"
        else:
            self.resize_edge = None
            
        if self.resize_edge:
            self.resizing = True
            self.original_geometry = self.geometry()
            
    def update_cursor(self, pos):
        """Update cursor based on position."""
        rect = self.rect()
        edge_size = 8
        
        if pos.x() <= edge_size or pos.x() >= rect.width() - edge_size:
            if pos.y() <= edge_size or pos.y() >= rect.height() - edge_size:
                # Corners
                if (pos.x() <= edge_size and pos.y() <= edge_size) or \
                   (pos.x() >= rect.width() - edge_size and pos.y() >= rect.height() - edge_size):
                    self.setCursor(Qt.SizeFDiagCursor)
                else:
                    self.setCursor(Qt.SizeBDiagCursor)
            else:
                # Left/right edges
                self.setCursor(Qt.SizeHorCursor)
        elif pos.y() <= edge_size or pos.y() >= rect.height() - edge_size:
            # Top/bottom edges
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
            
    def handle_resize(self, global_pos):
        """Handle widget resizing."""
        if not self.resize_edge:
            return
            
        rect = self.original_geometry
        mouse_pos = self.mapFromGlobal(global_pos)
        
        # Calculate new geometry based on resize edge
        new_rect = QRect(rect)
        
        if "left" in self.resize_edge:
            new_rect.setLeft(rect.left() + mouse_pos.x())
        if "right" in self.resize_edge:
            new_rect.setRight(rect.left() + mouse_pos.x())
        if "top" in self.resize_edge:
            new_rect.setTop(rect.top() + mouse_pos.y())
        if "bottom" in self.resize_edge:
            new_rect.setBottom(rect.top() + mouse_pos.y())
            
        # Enforce minimum and maximum sizes
        if new_rect.width() < self.min_size.width():
            if "left" in self.resize_edge:
                new_rect.setLeft(new_rect.right() - self.min_size.width())
            else:
                new_rect.setRight(new_rect.left() + self.min_size.width())
                
        if new_rect.height() < self.min_size.height():
            if "top" in self.resize_edge:
                new_rect.setTop(new_rect.bottom() - self.min_size.height())
            else:
                new_rect.setBottom(new_rect.top() + self.min_size.height())
                
        if new_rect.width() > self.max_size.width():
            new_rect.setWidth(self.max_size.width())
        if new_rect.height() > self.max_size.height():
            new_rect.setHeight(self.max_size.height())
            
        self.setGeometry(new_rect)
        self.position_size_grip()
        
    def check_dock_zones(self, global_pos):
        """Check for dock zones while dragging."""
        if not self.parent():
            return
            
        parent_rect = self.parent().rect()
        edge_threshold = 50
        
        # Convert to parent coordinates
        parent_pos = self.parent().mapFromGlobal(global_pos)
        
        # Visual feedback for dock zones (could add highlight effects here)
        if parent_pos.x() < edge_threshold:
            self.dock_zone = "left"
        elif parent_pos.x() > parent_rect.width() - edge_threshold:
            self.dock_zone = "right"
        elif parent_pos.y() < edge_threshold:
            self.dock_zone = "top"
        elif parent_pos.y() > parent_rect.height() - edge_threshold:
            self.dock_zone = "bottom"
        else:
            self.dock_zone = "floating"
            
    def check_final_dock_position(self, global_pos):
        """Check if widget should dock after drag ends."""
        if self.dock_zone and self.dock_zone != "floating":
            self.dock_to_zone(self.dock_zone)
            
    # === DOCKING FUNCTIONALITY ===
    
    def dock_to_zone(self, zone):
        """Dock widget to specified zone."""
        if not self.parent():
            return
            
        self.is_docked = True
        self.dock_zone = zone
        
        # Update appearance for docked state
        self.setProperty("docked", "true")
        self.style().unpolish(self)
        self.style().polish(self)
        
        # Emit docked signal
        self.widget_docked.emit(self, zone)
        
        self.logger.info(f"Widget '{self.title}' docked to {zone}")
        
    def undock(self):
        """Undock widget to floating state."""
        self.is_docked = False
        self.dock_zone = "floating"
        
        # Update appearance for floating state
        self.setProperty("docked", "false")
        self.style().unpolish(self)
        self.style().polish(self)
        
        # Emit undocked signal
        self.widget_undocked.emit(self)
        
        self.logger.info(f"Widget '{self.title}' undocked")
        
    def toggle_dock(self):
        """Toggle docked/floating state."""
        if self.is_docked:
            self.undock()
        else:
            # Dock to default position (right side)
            self.dock_to_zone("right")
            
    # === MINIMIZE/MAXIMIZE FUNCTIONALITY ===
    
    def toggle_minimize(self):
        """Toggle minimized state."""
        if self.is_minimized:
            self.restore()
        else:
            self.minimize()
            
    def minimize(self):
        """Minimize widget to title bar only."""
        if not self.is_minimized:
            self.is_minimized = True
            self.content_frame.hide()
            self.setFixedHeight(self.title_bar.height() + 4)
            self.minimize_btn.setText("🗖")
            
            # Auto-hide after delay
            self.hide_timer.start(3000)  # Hide after 3 seconds
            
            self.logger.info(f"Widget '{self.title}' minimized")
            
    def restore(self):
        """Restore widget from minimized state."""
        if self.is_minimized:
            self.is_minimized = False
            self.content_frame.show()
            self.setFixedHeight(16777215)  # Remove fixed height
            self.setMinimumHeight(self.min_size.height())
            self.minimize_btn.setText("🗕")
            
            # Cancel auto-hide
            self.hide_timer.stop()
            
            self.logger.info(f"Widget '{self.title}' restored")
            
    def toggle_maximize(self):
        """Toggle maximized state."""
        if self.is_maximized:
            self.restore_size()
        else:
            self.maximize()
            
    def maximize(self):
        """Maximize widget."""
        if not self.is_maximized and self.parent():
            self.is_maximized = True
            self.original_geometry = self.geometry()
            
            # Set to parent size
            parent_rect = self.parent().rect()
            self.setGeometry(parent_rect)
            self.maximize_btn.setText("🗗")
            
            self.logger.info(f"Widget '{self.title}' maximized")
            
    def restore_size(self):
        """Restore widget from maximized state."""
        if self.is_maximized:
            self.is_maximized = False
            self.setGeometry(self.original_geometry)
            self.maximize_btn.setText("🗖")
            
            self.logger.info(f"Widget '{self.title}' size restored")
            
    def auto_hide(self):
        """Auto-hide widget when minimized."""
        if self.is_minimized:
            self.hide()
            
    # === PARAMETER MANAGEMENT ===
    
    def clear_parameters(self):
        """Clear all parameter widgets."""
        # Clear existing parameters
        for i in reversed(range(self.parameter_layout.count())):
            child = self.parameter_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
                
        self.parameter_widgets.clear()
        self.current_parameters.clear()
        
    def load_filter_parameters(self, filter_name, parameters):
        """Load parameters for a specific filter."""
        self.clear_parameters()
        
        # Update title
        self.title_label.setText(f"{filter_name} Parameters")
        
        # Create parameter groups
        self.create_parameter_groups(parameters)
        
        # Add stretch at the end
        self.parameter_layout.addStretch()
        
        self.logger.info(f"Loaded parameters for filter: {filter_name}")
        
    def create_parameter_groups(self, parameters):
        """Create grouped parameter controls."""
        # Group parameters by category
        groups = {}
        for param in parameters:
            category = param.get('category', 'General')
            if category not in groups:
                groups[category] = []
            groups[category].append(param)
            
        # Create UI for each group
        for category, group_params in groups.items():
            group_box = QGroupBox(category)
            form_layout = QFormLayout(group_box)
            
            for param in group_params:
                widget = self.create_parameter_widget(param)
                if widget:
                    label = QLabel(param.get('label', param['name']))
                    form_layout.addRow(label, widget)
                    self.parameter_widgets[param['name']] = widget
                    
            self.parameter_layout.addWidget(group_box)
            
    def create_parameter_widget(self, param):
        """Create appropriate widget for parameter type."""
        param_type = param.get('type', 'int')
        param_name = param['name']
        default_value = param.get('default', 0)
        
        if param_type == 'int':
            widget = QSpinBox()
            widget.setMinimum(param.get('min', 0))
            widget.setMaximum(param.get('max', 100))
            widget.setValue(default_value)
            widget.valueChanged.connect(lambda v: self.parameter_changed(param_name, v))
            return widget
            
        elif param_type == 'float':
            widget = QDoubleSpinBox()
            widget.setMinimum(param.get('min', 0.0))
            widget.setMaximum(param.get('max', 1.0))
            widget.setDecimals(param.get('decimals', 2))
            widget.setSingleStep(param.get('step', 0.1))
            widget.setValue(default_value)
            widget.valueChanged.connect(lambda v: self.parameter_changed(param_name, v))
            return widget
            
        elif param_type == 'slider':
            widget = QSlider(Qt.Horizontal)
            widget.setMinimum(param.get('min', 0))
            widget.setMaximum(param.get('max', 100))
            widget.setValue(default_value)
            widget.valueChanged.connect(lambda v: self.parameter_changed(param_name, v))
            return widget
            
        elif param_type == 'bool':
            widget = QCheckBox()
            widget.setChecked(default_value)
            widget.toggled.connect(lambda v: self.parameter_changed(param_name, v))
            return widget
            
        elif param_type == 'str' and 'options' in param:
            widget = QComboBox()
            widget.addItems(param['options'])
            if default_value in param['options']:
                widget.setCurrentText(default_value)
            widget.currentTextChanged.connect(lambda v: self.parameter_changed(param_name, v))
            return widget
            
        return None
        
    def parameter_changed(self, name, value):
        """Handle parameter value changes."""
        self.current_parameters[name] = value
        self.parameters_changed.emit(self.current_parameters.copy())
        
    def get_parameters(self):
        """Get current parameter values."""
        return self.current_parameters.copy()
        
    def set_parameter(self, name, value):
        """Set a specific parameter value."""
        if name in self.parameter_widgets:
            widget = self.parameter_widgets[name]
            if isinstance(widget, QSpinBox):
                widget.setValue(value)
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(value)
            elif isinstance(widget, QSlider):
                widget.setValue(value)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(value)
            elif isinstance(widget, QComboBox):
                widget.setCurrentText(str(value))
                
    # === UTILITY METHODS ===
    
    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)
        self.position_size_grip()
        
    def close_widget(self):
        """Close the widget."""
        self.widget_closed.emit(self)
        self.hide()
        self.logger.info(f"Widget '{self.title}' closed")
        
    def show_widget(self):
        """Show the widget."""
        self.show()
        self.raise_()
        self.activateWindow()
        
    def set_title(self, title):
        """Update widget title."""
        self.title = title
        self.title_label.setText(title)


# Example usage and testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create test widget
    widget = DraggableWidget("Test Filter Widget")
    
    # Sample parameters for testing
    test_parameters = [
        {
            'name': 'intensity',
            'type': 'slider',
            'min': 0,
            'max': 100,
            'default': 50,
            'label': 'Effect Intensity',
            'category': 'Basic'
        },
        {
            'name': 'algorithm',
            'type': 'str',
            'options': ['Canny', 'Sobel', 'Laplacian'],
            'default': 'Canny',
            'label': 'Algorithm',
            'category': 'Advanced'
        },
        {
            'name': 'threshold',
            'type': 'int',
            'min': 0,
            'max': 255,
            'default': 100,
            'label': 'Threshold',
            'category': 'Advanced'
        },
        {
            'name': 'preserve_colors',
            'type': 'bool',
            'default': True,
            'label': 'Preserve Colors',
            'category': 'Basic'
        }
    ]
    
    widget.load_filter_parameters("Edge Detection", test_parameters)
    widget.show()
    
    sys.exit(app.exec_()) 