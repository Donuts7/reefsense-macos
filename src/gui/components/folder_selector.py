"""Folder selection component."""
from pathlib import Path
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog
)

class FolderSelector(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Image Folder", parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Image folder row
        image_row = QHBoxLayout()
        image_label = QLabel("Images:")
        image_label.setFixedWidth(60)
        
        self.image_path_label = QLabel("No folder selected")
        self.image_path_label.setMinimumWidth(200)
        
        image_btn = QPushButton("Select Folder")
        image_btn.setFixedWidth(150)
        image_btn.clicked.connect(self.select_image_folder)
        
        image_row.addWidget(image_label)
        image_row.addWidget(self.image_path_label, 1)
        image_row.addWidget(image_btn)
        
        layout.addLayout(image_row)
        self.setLayout(layout)
        
    def select_image_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            self.image_path_label.setText(str(folder))
            
    def get_image_path(self) -> str:
        """Return the selected image folder path."""
        return self.image_path_label.text()
        
    def get_labels_path(self) -> str:
        """Return the labels subfolder path."""
        image_path = self.get_image_path()
        if image_path and image_path != "No folder selected":
            return str(Path(image_path) / "labels")
        return ""