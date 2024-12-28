"""Image viewer component with results overlay."""
from PyQt6.QtWidgets import (
    QScrollArea, QWidget, QVBoxLayout, QLabel,
    QGridLayout, QFrame
)
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QPointF, QRectF
import os

class ImageResultFrame(QFrame):
    """Frame containing an image and its results overlay."""
    def __init__(self, image_path, coverage_data):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setup_ui(image_path, coverage_data)
        
    def setup_ui(self, image_path, coverage_data):
        layout = QVBoxLayout(self)
        
        # Image display
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        
        # Scale image if too large
        if pixmap.width() > 800:
            pixmap = pixmap.scaledToWidth(800, Qt.TransformationMode.SmoothTransformation)
            
        # Create overlay with coverage data
        painter = QPainter(pixmap)
        self.draw_legend(painter, coverage_data, pixmap.width())
        painter.end()
        
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)
        
        # Add image name
        name_label = QLabel(os.path.basename(image_path))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)
        
    def draw_legend(self, painter, coverage_data, width):
        """Draw coverage information overlay."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Setup font
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        
        # Setup background
        bg_color = QColor(0, 0, 0, 180)  # Semi-transparent black
        text_color = QColor(255, 255, 255)  # White
        
        # Position and size
        padding = 10
        line_height = 20
        y_position = float(padding)  # Convert to float
        
        # Draw background and text for each class
        for class_name, percentage in coverage_data.items():
            text = f"{class_name}: {percentage:.1f}%"
            text_width = painter.fontMetrics().horizontalAdvance(text)
            
            # Draw background rectangle
            painter.fillRect(
                width - text_width - padding * 2,
                y_position,
                text_width + padding * 2,
                line_height,
                bg_color
            )
            
            # Draw text using QPointF for floating-point coordinates
            text_point = QPointF(float(width - text_width - padding), y_position + line_height - padding/2)
            painter.setPen(text_color)
            painter.drawText(text_point, text)
            
            y_position += line_height + 2

class ImageViewer(QScrollArea):
    """Scrollable area containing processed images with results."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.setWidget(self.container)
        
    def display_results(self, image_dir, image_coverages):
        """Display images with their coverage results."""
        # Clear previous results
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Add new results
        row = 0
        col = 0
        max_cols = 2  # Display 2 images per row
        
        for image_name, coverage in image_coverages.items():
            image_path = os.path.join(image_dir, f"{image_name}.jpg")
            if os.path.exists(image_path):
                frame = ImageResultFrame(image_path, coverage)
                self.grid_layout.addWidget(frame, row, col)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1