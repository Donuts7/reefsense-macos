"""Results view component."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import ( # type: ignore
    QWidget, QVBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QTabWidget,QSizePolicy
)
from PyQt6.QtCore import Qt # type: ignore

from PyQt6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt

# class ResultsView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setup_ui()
        
#     def setup_ui(self):
#         layout = QVBoxLayout(self)
        
#         # Summary section
#         self.summary_label = QLabel()
#         layout.addWidget(self.summary_label)
        
#         # Class coverage table
#         self.class_table = QTableWidget()
#         self.class_table.setColumnCount(2)
#         self.class_table.setHorizontalHeaderLabels(["Class", "Coverage (%)"])
#         layout.addWidget(self.class_table)
        
    # def display_results(self, class_coverage, total_coverage):
    #     # Update summary
    #     self.summary_label.setText(f"Total Coverage: {total_coverage:.2f}%")
        
    #     # Update class coverage table
    #     self.class_table.setRowCount(len(class_coverage))
    #     for i, (class_name, coverage) in enumerate(class_coverage.items()):
    #         self.class_table.setItem(i, 0, QTableWidgetItem(class_name))
    #         self.class_table.setItem(i, 1, QTableWidgetItem(f"{coverage:.2f}%"))
            
    #     # Adjust column widths
    #     self.class_table.resizeColumnsToContents()

# """Results view component."""

# class ResultsTable(QTableWidget):
#     def __init__(self):
#         super().__init__()
#         self.setColumnCount(2)
#         self.setHorizontalHeaderLabels(["Class", "Coverage"])
#         self.verticalHeader().setVisible(False)
        

#     def display_results(self, class_coverage, total_coverage):
#         self.setRowCount(len(class_coverage))
#         for i, (class_name, coverage) in enumerate(class_coverage.items()):
#             self.setItem(i, 0, QTableWidgetItem(class_name))
#             self.setItem(i, 1, QTableWidgetItem(f"{coverage:.2f}%"))
#         self.resizeColumnsToContents()

        
# class ResultsView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setup_ui()
        
#     def setup_ui(self):
#         layout = QVBoxLayout(self)
        
#         # Create tab widget
#         self.tab_widget = QTabWidget()
        
#         # Prediction results tab
#         self.pred_tab = QWidget()
#         pred_layout = QVBoxLayout(self.pred_tab)
#         self.pred_summary = QLabel()
#         self.pred_table = ResultsTable()
#         self.pred_table.setFixedWidth(200)
#         pred_layout.addWidget(self.pred_summary)
#         pred_layout.addWidget(self.pred_table)
        
#         # Ground truth results tab
#         self.gt_tab = QWidget()
#         gt_layout = QVBoxLayout(self.gt_tab)
#         self.gt_summary = QLabel()
#         self.gt_table = ResultsTable()
#         self.gt_table.setFixedWidth(200)
#         gt_layout.addWidget(self.gt_summary)
#         gt_layout.addWidget(self.gt_table)
        
#         # Add tabs
#         self.tab_widget.addTab(self.pred_tab, "Prediction Results")
#         self.tab_widget.addTab(self.gt_tab, "Ground Truth")
        
#         layout.addWidget(self.tab_widget)
#     def display_results(self, class_coverage, total_coverage):
#         # Update summary
#         self.pred_summary.setText(f"Total Coverage: {total_coverage:.2f}%")
        
#         # Update class coverage table
#         self.pred_table.setRowCount(len(class_coverage))
        
#         for i, (class_name, coverage) in enumerate(class_coverage.items()):
#             self.pred_table.setItem(i, 0, QTableWidgetItem(class_name))
#             self.pred_table.setItem(i, 1, QTableWidgetItem(f"{coverage:.2f}%"))
                
#         # Adjust column widths
#         self.pred_table.setFixedWidth(145)
#         #self.pred_table.resizeColumnsToContents()
        
#     def display_results_compared(self, pred_results=None, gt_results=None):
#         """Display prediction and/or ground truth results."""
#         if pred_results:
#             class_coverage, total_coverage = pred_results
#             self.pred_summary.setText(f"Total Coverage: {total_coverage:.2f}%")
            
#             self.pred_table.display_results(class_coverage, total_coverage)            
#             self.tab_widget.setTabEnabled(0, True)
#             self.pred_table.setFixedWidth(145)
#             self.pred_table.updateGeometry()  # Force the layout to update
#             self.tab_widget.updateGeometry()
#         else:
#             self.tab_widget.setTabEnabled(0, False)
            
#         if gt_results:
#             class_coverage, total_coverage = gt_results
#             self.gt_summary.setText(f"Total Coverage: {total_coverage:.2f}%")
            
#             self.gt_table.display_results(class_coverage, total_coverage)
#             self.tab_widget.setTabEnabled(1, True)
#             self.gt_table.setFixedWidth(145)
#             self.gt_table.updateGeometry()  # Force the layout to update
#             self.tab_widget.updateGeometry()
#         else:
#             self.tab_widget.setTabEnabled(1, False)
            
#     def reset_display(self):
#         """Reset all display elements to their initial state."""
#         # Reset summary labels
#         self.pred_summary.setText("")
#         self.gt_summary.setText("")
        
#         # Clear tables
#         self.pred_table.setRowCount(0)
#         self.gt_table.setRowCount(0)
        
#         # Enable prediction tab by default
#         self.tab_widget.setTabEnabled(0, True)
#         # Ground truth tab will be enabled when needed
#         self.tab_widget.setTabEnabled(1, False)
"""Results view component."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QTabWidget, QSizePolicy
)
from PyQt6.QtCore import Qt

class ResultsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Class", "Coverage"])
        self.verticalHeader().setVisible(False)
        
        # Make table expand horizontally
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Make columns stretch to fill available space
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def display_results(self, class_coverage, total_coverage):
        self.setRowCount(len(class_coverage))
        for i, (class_name, coverage) in enumerate(class_coverage.items()):
            self.setItem(i, 0, QTableWidgetItem(class_name))
            self.setItem(i, 1, QTableWidgetItem(f"{coverage:.2f}%"))

class ResultsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Make the widget expand to fill available space
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Prediction results tab
        self.pred_tab = QWidget()
        pred_layout = QVBoxLayout(self.pred_tab)
        self.pred_summary = QLabel()
        self.pred_table = ResultsTable()
        pred_layout.addWidget(self.pred_summary)
        pred_layout.addWidget(self.pred_table)
        
        # Ground truth results tab
        self.gt_tab = QWidget()
        gt_layout = QVBoxLayout(self.gt_tab)
        self.gt_summary = QLabel()
        self.gt_table = ResultsTable()
        gt_layout.addWidget(self.gt_summary)
        gt_layout.addWidget(self.gt_table)
        
        # Add tabs
        self.tab_widget.addTab(self.pred_tab, "Prediction Results")
        self.tab_widget.addTab(self.gt_tab, "Ground Truth")
        
        layout.addWidget(self.tab_widget)

    def display_results(self, class_coverage, total_coverage):
        """Legacy method that updates only prediction results."""
        self.display_results_compared(pred_results=(class_coverage, total_coverage))

    def display_results_compared(self, pred_results=None, gt_results=None):
        """Display prediction and/or ground truth results."""
        if pred_results:
            class_coverage, total_coverage = pred_results
            self.pred_summary.setText(f"Total Coverage: {total_coverage:.2f}%")
            self.pred_table.display_results(class_coverage, total_coverage)            
            self.tab_widget.setTabEnabled(0, True)
        else:
            self.tab_widget.setTabEnabled(0, False)
            
        if gt_results:
            class_coverage, total_coverage = gt_results
            self.gt_summary.setText(f"Total Coverage: {total_coverage:.2f}%")
            self.gt_table.display_results(class_coverage, total_coverage)
            self.tab_widget.setTabEnabled(1, True)
        else:
            self.tab_widget.setTabEnabled(1, False)
            
    def reset_display(self):
        """Reset all display elements to their initial state."""
        self.pred_summary.setText("")
        self.gt_summary.setText("")
        self.pred_table.setRowCount(0)
        self.gt_table.setRowCount(0)
        self.tab_widget.setTabEnabled(0, True)
        self.tab_widget.setTabEnabled(1, False)