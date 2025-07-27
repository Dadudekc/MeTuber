import os
from PyQt5.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QProgressBar, QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont

class SplashScreen(QSplashScreen):
    """Professional splash screen for Dream.OS Stream Software."""
    
    finished = pyqtSignal()
    
    def __init__(self):
        # Load the logo
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Scale to a reasonable size for splash screen
            pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            # Fallback if logo not found
            pixmap = QPixmap(400, 300)
            pixmap.fill(Qt.black)
        
        super().__init__(pixmap, Qt.WindowStaysOnTopHint)
        
        self.setWindowTitle("Dream.OS Stream Software")
        
        # Add loading text and progress bar
        self.progress = 0
        self.setup_ui()
        
        # Timer for progress animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        
    def setup_ui(self):
        """Setup the splash screen UI elements."""
        # Create a transparent overlay for text
        self.setStyleSheet("""
            QSplashScreen {
                background-color: rgba(0, 0, 0, 200);
                color: white;
            }
        """)
        
        # Show initial message
        self.showMessage("Starting Dream.OS Stream Software...", 
                        Qt.AlignBottom | Qt.AlignCenter, Qt.white)
    
    def start_loading(self, tasks):
        """Start the loading animation with a list of tasks."""
        self.tasks = tasks
        self.current_task = 0
        self.progress = 0
        self.timer.start(50)  # Update every 50ms for smooth animation
        
    def update_progress(self):
        """Update the loading progress."""
        self.progress += 2
        
        if self.current_task < len(self.tasks):
            task_name = self.tasks[self.current_task]
            message = f"Loading {task_name}... {self.progress}%"
            self.showMessage(message, Qt.AlignBottom | Qt.AlignCenter, Qt.white)
            
            # Move to next task every 25%
            if self.progress >= 25 * (self.current_task + 1):
                self.current_task += 1
                
        if self.progress >= 100:
            self.showMessage("Ready! Opening application...", 
                           Qt.AlignBottom | Qt.AlignCenter, Qt.white)
            self.timer.stop()
            QTimer.singleShot(500, self.close_splash)
            
    def close_splash(self):
        """Close the splash screen and emit finished signal."""
        self.close()
        self.finished.emit()
        
    def update_message(self, message):
        """Update the splash screen message manually."""
        self.showMessage(message, Qt.AlignBottom | Qt.AlignCenter, Qt.white)
        
    def show_error(self, error_message):
        """Show an error message on the splash screen."""
        self.showMessage(f"Error: {error_message}", 
                        Qt.AlignBottom | Qt.AlignCenter, Qt.red) 