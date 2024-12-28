"""Analysis options component."""
from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSpinBox, QCheckBox ,QDoubleSpinBox#type: ignore
from PyQt6.QtCore import Qt # type: ignore
from PyQt6.QtCore import Qt, pyqtSignal # type: ignore

class AnalysisOptions(QGroupBox):
    compareToggled = pyqtSignal(bool)
    croppingToggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__("Analysis Options", parent)
        self.setup_ui()
        
    def setup_ui(self):
        
        layout = QHBoxLayout()
        
        # Add left spacer
        layout.addStretch(1)
        
        # Options container for spinboxes
        options_container = QHBoxLayout()
        
        # Image Limit
        limit_container = QHBoxLayout()
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(0, 10000)
        self.limit_spin.setSpecialValueText("No limit")
        limit_container.addWidget(QLabel("Image Limit:"))
        limit_container.addWidget(self.limit_spin)
        options_container.addLayout(limit_container)
        
        # Add some spacing between the spinboxes
        options_container.addSpacing(20)
        
        # Confidence Score
        confidence_container = QHBoxLayout()
        self.confidence_spin = QDoubleSpinBox()
        self.confidence_spin.setRange(0.01, 0.90)
        self.confidence_spin.setSingleStep(0.01)
        self.confidence_spin.setValue(0.50)  # Default value
        confidence_container.addWidget(QLabel("Confidence:"))
        confidence_container.addWidget(self.confidence_spin)
        options_container.addLayout(confidence_container)
        
        layout.addLayout(options_container, 2)
        
        # Center spacer
        layout.addStretch(1)
        
        # Cropping checkbox
        self.cropping_check = QCheckBox("Enable Cropping")
        self.cropping_check.stateChanged.connect(self._on_cropping_changed)
        layout.addWidget(self.cropping_check, 2)
 
        # Compare checkbox
        self.compare_check = QCheckBox("Compare with Ground Truth")
        self.compare_check.setEnabled(False)  # Disabled by default
        self.compare_check.stateChanged.connect(self.compareToggled.emit)
        layout.addWidget(self.compare_check, 2)
                
        # Right spacer
        layout.addStretch(1)
        
        self.setLayout(layout)
        
    def _on_cropping_changed(self, state):
        """Handle cropping checkbox state change."""
        is_checked = bool(state)
        self.croppingToggled.emit(is_checked)
        # Disable comparison if cropping is enabled
        if is_checked:
            self.compare_check.setChecked(False)
            self.compare_check.setEnabled(False)
        else:
            self.compare_check.setEnabled(True)
            
    def _on_compare_changed(self, state):
        """Handle comparison checkbox state change."""
        is_checked = bool(state)
        self.compareToggled.emit(is_checked)
        # Disable cropping if comparison is enabled
        if is_checked:
            self.cropping_check.setChecked(False)
            self.cropping_check.setEnabled(False)
        else:
            self.cropping_check.setEnabled(True)
        
    def get_limit(self):
        """Return the image limit value."""
        return self.limit_spin.value() if self.limit_spin.value() > 0 else None
    def get_confidence(self):
        """Return the confidence value."""
        return self.confidence_spin.value()
        
    def is_cropping_enabled(self):
        """Return whether cropping is enabled."""
        return self.cropping_check.isChecked()
        
    def is_comparison_enabled(self):
        """Return whether comparison is enabled."""
        return self.compare_check.isChecked()
        
    def set_cropping_enabled(self, enabled):
        """Enable or disable the cropping checkbox."""
        self.cropping_check.setEnabled(enabled)
        if not enabled:
            self.cropping_check.setChecked(False)
            self.cropping_check.setStyleSheet("""
                QCheckBox {
                    color: #A0AEC0;  /* Light gray color for disabled state */
                }
                QCheckBox::indicator {
                    border: 2px solid #CBD5E0;  /* Light gray border */
                }
                QCheckBox::indicator:checked {
                    background-color: #CBD5E0;  /* Light gray background */
                    border: 2px solid #CBD5E0;
                }
            """)
        else:
            # Reset to default style
            self.cropping_check.setStyleSheet("")
            
    def set_comparison_enabled(self, enabled):
        """Enable or disable the comparison checkbox."""
        self.compare_check.setEnabled(enabled)
        if not enabled:
            self.compare_check.setChecked(False)
            self.compare_check.setStyleSheet("""
                    QCheckBox {
                        color: #A0AEC0;  /* Light gray color for disabled state */
                    }
                    QCheckBox::indicator {
                        border: 2px solid #CBD5E0;  /* Light gray border */
                    }
                    QCheckBox::indicator:checked {
                        background-color: #CBD5E0;  /* Light gray background */
                        border: 2px solid #CBD5E0;
                    }
                """)
        else:
                # Reset to default style
                self.compare_check.setStyleSheet("")
                
    def set_confidence_enabled(self, enabled):
        """Enable or disable the confidence spinbox."""
        self.confidence_spin.setEnabled(enabled)
        if not enabled:
            self.confidence_spin.setStyleSheet("""
                QDoubleSpinBox {
                    color: #A0AEC0;  /* Light gray color for disabled state */
                    background-color: #F7FAFC;  /* Light background */
                }
            """)
        else:
            self.confidence_spin.setStyleSheet("")