"""Cropping options component."""
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSignal

class CroppingOptions(QGroupBox):
    cropping_enabled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__("Cropping Options", parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Enable cropping checkbox
        self.enable_checkbox = QCheckBox("Enable Image Cropping")
        self.enable_checkbox.stateChanged.connect(self.on_cropping_toggled)
        layout.addWidget(self.enable_checkbox)
        
        # Input folder selection
        input_layout = QHBoxLayout()
        self.input_path_label = QLabel("No input folder selected")
        input_btn = QPushButton("Select Input Folder")
        input_btn.clicked.connect(self.select_input_folder)
        input_layout.addWidget(QLabel("Input:"))
        input_layout.addWidget(self.input_path_label)
        input_layout.addWidget(input_btn)
        layout.addLayout(input_layout)
        
        self.setLayout(layout)
        self.setEnabled(False)
        
    def on_cropping_toggled(self, state):
        self.cropping_enabled.emit(bool(state))
        for child in self.findChildren((QPushButton, QLabel)):
            if isinstance(child, QPushButton) or child.parent() != self:
                child.setEnabled(bool(state))
                
    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_path_label.setText(folder)
            
    def get_input_path(self):
        return self.input_path_label.text()
        
    def is_cropping_enabled(self):
        return self.enable_checkbox.isChecked()