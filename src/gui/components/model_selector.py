"""Model selection component."""
from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QRadioButton, QButtonGroup # type: ignore
from PyQt6.QtCore import Qt, pyqtSignal # type: ignore

class ModelSelector(QGroupBox):
    modeChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__("Select Mode", parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        self.button_group = QButtonGroup()
        
        # Create radio buttons
        self.hc_radio = QRadioButton("Hard Coral")
        self.groups_radio = QRadioButton("Growth Forms")
        self.quantify_radio = QRadioButton("Quantify Substrate")
        self.crop_only_radio = QRadioButton("Crop Only")  # New radio button

        # self.hc_radio.setChecked(True)
        
        # Add to button group
        self.button_group.addButton(self.hc_radio)
        self.button_group.addButton(self.groups_radio)
        self.button_group.addButton(self.quantify_radio)
        self.button_group.addButton(self.crop_only_radio)  # Add to button group        
        # Connect signal
        self.button_group.buttonClicked.connect(self._on_mode_changed)
        
        # Add spacers for equal distribution
        layout.addWidget(self.hc_radio, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.groups_radio, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.quantify_radio, 1, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.crop_only_radio, 1, Qt.AlignmentFlag.AlignRight)
      
        self.setLayout(layout)
        
    def _on_mode_changed(self, button):
        mode = self.get_selected_model()
        self.modeChanged.emit(mode)
        
    def get_selected_model(self):
        """Return the selected model type."""
        if self.hc_radio.isChecked():
            return "hc"
        elif self.groups_radio.isChecked():
            return "groups"
        elif self.quantify_radio.isChecked():
            return "quantify"
        else:
            return "crop_only"