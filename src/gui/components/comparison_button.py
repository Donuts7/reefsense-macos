"""Comparison button component."""
from PyQt6.QtWidgets import QPushButton # type: ignore
from PyQt6.QtCore import pyqtSignal # type: ignore

class ComparisonButton(QPushButton):
    compareClicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("Compare with Ground Truth", parent)
        self.setEnabled(False)
        self.clicked.connect(self.compareClicked.emit)
        
    def update_state(self, model_type: str) -> None:
        """Enable button only for HC and Groups models."""
        self.setEnabled(model_type in ["hc", "groups"])