"""Custom progress dialog component."""
from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtCore import Qt

class ProcessingDialog(QProgressDialog):
    def __init__(self, message, parent=None):
        super().__init__(message, None, 0, 0, parent)
        self.setLabelText(message)  # Explicitly set the label text
        self.setup_ui()
        
    def setup_ui(self):
        """Configure the progress dialog UI."""
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setMinimumWidth(300)
        self.setAutoClose(True)
        self.setCancelButton(None)  # Remove cancel button

