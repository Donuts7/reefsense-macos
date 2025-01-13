"""Main application window."""
import os
import sys
import numpy as np # type: ignore
import shutil
from pathlib import Path
from PyQt6.QtWidgets import ( # type: ignore
    QMainWindow, QWidget, QVBoxLayout, QPushButton, 
    QMessageBox, QProgressDialog, QHBoxLayout, QLabel,
    QApplication, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation # type: ignore
from PyQt6.QtGui import QPalette, QColor, QFont, QIcon,QPixmap # type: ignore

from .components.model_selector import ModelSelector
from .components.folder_selector import FolderSelector
from .components.analysis_options import AnalysisOptions
from .components.results_view import ResultsView,ResultsTable
from .components.progress_dialog import ProcessingDialog
from ..config import *
from .styles.stylesheet import MAIN_STYLESHEET, TITLE_LABEL_STYLE, STATUS_LABEL_STYLE, COLORS, DIMENSIONS, TYPOGRAPHY
from ..models.model_manager import ModelManager
from ..models.cropping_model import CroppingModel
from ..analysis.coral_coverage import calculate_total_coral_cover
from ..utils.image_processing import process_predictions_with_legend
from ..utils.comparison import create_side_by_side_comparison  # type: ignore
from ..utils.add_annotations import add_segmentation_annotations  # type: ignore

from PyQt6.QtCore import Qt, QPropertyAnimation, QRectF # type: ignore
#from PyQt5.QtCore import Qt  # Make sure Qt is imported from QtCore

from PyQt6.QtGui import QPainter, QColor # type: ignore
from PyQt6.QtWidgets import QPushButton # type: ignore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("reefsense")
        self.setMinimumSize(750,680)
        self.setStyleSheet(MAIN_STYLESHEET)
        self.setWindowIcon(QIcon("_internal/src/gui/components/logo.png"))
        
        self.model_manager = ModelManager()
        self.cropping_model = CroppingModel()
        self.latest_output_dir = None
        self.class_names = None  # Will store class names from YAML
        self.setup_ui()
        self._connect_signals()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)
        
        # Header
        header = QHBoxLayout()  # Create the header layout
        if getattr(sys, 'frozen', False):
    # If running from a bundled app, the resources will be inside `sys._MEIPASS`
            base_path = sys._MEIPASS
        else:
            # If running from source, use the current directory
            base_path = os.path.dirname(__file__)

        # Construct the path to the logo image
        logo_path = os.path.join(base_path, 'src', 'gui', 'components', 'logo.png')
        
        # Add logo next to the title
        logo_label = QLabel()
        pixmap = QPixmap(logo_path)  # Provide the correct path to your logo
        logo_label.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_label.setFixedSize(40, 40)  # Ensure enough space for the logo
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(logo_label)
        
        # Add title
        title_label = QLabel("reefsense")
        title_label.setStyleSheet(TITLE_LABEL_STYLE)
        header.addWidget(title_label)
    
        # Add slogan
        slogan_label = QLabel("         AI powered substrate assesment")  # Customize the slogan text
        slogan_label.setStyleSheet("font-size: 18px; color: gray; padding-top: 7px;")  # Add padding to lower the slogan
        slogan_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # Vertically align
        header.addWidget(slogan_label)
        
        header.addStretch()  # Add stretch to align items to the left
        
        layout.addLayout(header)  # Add header layout to the main layout
        # Components
        self.model_selector = ModelSelector()
        layout.addWidget(self.model_selector)
        
        self.folder_selector = FolderSelector()
        layout.addWidget(self.folder_selector)
        
        self.analysis_options = AnalysisOptions()
        layout.addWidget(self.analysis_options)
        
        # Buttons
        button_container = QHBoxLayout()
        button_container.setSpacing(10)
        
        analyze_btn = QPushButton("Analyze")
        analyze_btn.clicked.connect(self.run_analysis)
        button_container.addWidget(analyze_btn)
        
        self.view_results_btn = QPushButton("View Results")
        self.view_results_btn.clicked.connect(self.open_results_folder)
        self.view_results_btn.setEnabled(False)

        button_container.addWidget(self.view_results_btn)        
        layout.addLayout(button_container)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.status_label.hide()
        layout.addWidget(self.status_label)
        
        # Results view
        self.results_view = ResultsView()
        layout.addWidget(self.results_view)

        # Apply hover effect with animation
        self.apply_hover_effect(analyze_btn)
        
        if self.view_results_btn.isEnabled():
            self.apply_hover_effect(self.view_results_btn)

    def apply_hover_effect(self, button: QPushButton):
        """Applies hover effect to the button by changing its background color"""
        
        # Define the hover behavior
        def on_hover_enter(event):
            button.setStyleSheet("background-color: {}".format(COLORS['primary_dark']))  # Change hover color

        def on_hover_leave(event):
            button.setStyleSheet("background-color: {}".format(COLORS['primary']))  # Restore original color

        # Assign the hover enter and leave events
        button.enterEvent = on_hover_enter
        button.leaveEvent = on_hover_leave

    def _connect_signals(self):
        """Connect all signal handlers."""
        # Connect model selector to analysis options
        self.model_selector.modeChanged.connect(self._on_mode_changed)
        
    def _on_mode_changed(self, mode):
        """Handle mode change events."""
        # Disable cropping if quantify mode is selected
        is_crop_only = mode == "crop_only"
        is_quantify = mode == "quantify"
        
        self.analysis_options.set_comparison_enabled(mode in ["hc", "groups"])
        self.analysis_options.set_cropping_enabled(not is_crop_only)  # Disable cropping options in crop_only mode
        self.analysis_options.set_cropping_enabled(mode != "quantify" and mode != 'crop_only')
        self.analysis_options.set_confidence_enabled(not is_crop_only and not is_quantify)

    def validate_folders(self, image_dir):
        """Validate input folders and their structure."""
        if image_dir == "No folder selected":
            raise ValueError("Please select an image folder")
            
        if not os.path.exists(image_dir):
            raise ValueError(f"Selected folder does not exist: {image_dir}")
            
        # For quantification, check if labels folder exists
        if self.model_selector.get_selected_model() == "quantify":
            labels_dir = os.path.join(image_dir, "labels")
            if not os.path.exists(labels_dir):
                raise ValueError("Labels folder not found. For quantification, there must be a 'labels' subfolder in the selected image directory.")
            
        return True
    


    def run_analysis(self):
        try:
            self.setEnabled(False)
            self.results_view.reset_display()
            self.status_label.setText("Processing images...")
            self.status_label.show()
            self.centralWidget().findChild(QPushButton, "").setEnabled(False)
            self.repaint()
            
            image_dir = self.folder_selector.get_image_path()
            self.validate_folders(image_dir)
            
            # Get the limit from analysis options
            limit = self.analysis_options.get_limit()
            
            # Create base output directory
            base_output_dir = os.path.join(os.getcwd(), "outputs")
            os.makedirs(base_output_dir, exist_ok=True)
            
            if self.model_selector.get_selected_model() == "crop_only":
                success_count, failed_count, output_dir = self.cropping_model.process_folder(
                    image_dir,
                    limit=limit
                )
                
                QMessageBox.information(
                    self,
                    "Cropping Complete",
                    f"Successfully cropped {success_count} images\nFailed to crop {failed_count} images"
                )
                self.latest_output_dir = output_dir
                self.view_results_btn.setEnabled(True)
                return
                
            # Handle cropping if enabled
            working_dir = image_dir
            if self.analysis_options.is_cropping_enabled():
                cropping_output_dir = os.path.join(base_output_dir, "cropping")
                os.makedirs(cropping_output_dir, exist_ok=True)
                
                success_count, failed_count, output_dir = self.cropping_model.process_folder(
                    image_dir,
                    limit=limit,
                    output_dir=cropping_output_dir  # Specify the output directory explicitly
                )
                
                QMessageBox.information(
                    self,
                    "Cropping Complete",
                    f"Successfully cropped {success_count} images\nFailed to crop {failed_count} images"
                )
                # Use cropped images for next step
                working_dir = output_dir
                    
                    

            # Run prediction or quantification
            try:
                self._run_analysis_step(working_dir)
                self.view_results_btn.setEnabled(True)
            except Exception as e:
                raise e
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
        finally:
            self.setEnabled(True)
            self.status_label.hide()
            self.centralWidget().findChild(QPushButton, "").setEnabled(True)

    def _run_analysis_step(self, image_dir):
        """Run either prediction or quantification based on options."""
        limit = self.analysis_options.get_limit()
        model_type = self.model_selector.get_selected_model()
        compare = self.analysis_options.is_comparison_enabled()
        confidence = self.analysis_options.get_confidence()
        
        # Create clean output directories
        base_output_dir = os.path.join(os.getcwd(), "outputs")
        os.makedirs(base_output_dir, exist_ok=True)
        
        # Load appropriate model
        model, class_names = self.model_manager.load_model(model_type,image_dir)
        
        if compare:
            self._run_comparison_analysis(image_dir, model_type, limit, class_names, confidence)
        elif model_type == "quantify":
            labels_dir = os.path.join(image_dir, "labels")
            self._run_quantification(image_dir, labels_dir, class_names, limit)
        else:
            self._run_prediction(model, image_dir, class_names, limit, confidence)



    def _run_comparison_analysis(self, image_dir, model_type, limit, class_names, confidence):
        """Run analysis with comparison to ground truth."""
        try:
            # Check for labels subfolder
            labels_dir = os.path.join(image_dir, "labels")
            if not os.path.exists(labels_dir):
                raise ValueError("Labels subfolder must exist for comparison")
                
            # Run prediction first
            pred_labels_dir, pred_images_dir = self.model_manager.predict_with_limit(
                image_dir=image_dir,
                limit=limit,
                output_folder="outputs",
                conf=confidence
            )
            
            # Run quantification on ground truth
            quantify_folder = os.path.join("outputs", "quantify")
            if os.path.exists(quantify_folder):
                shutil.rmtree(quantify_folder)
            os.makedirs(quantify_folder)
            
            # Calculate coverages for prediction
            pred_class_coverage, pred_total_coverage, pred_image_coverages = calculate_total_coral_cover(
                image_dir=image_dir,
                annotation_dir=pred_labels_dir,
                class_names=class_names,
                limit=limit
            )
            
            # Calculate coverages for ground truth using CLASS_NAMES_OTHER
            gt_class_coverage, gt_total_coverage, gt_image_coverages = calculate_total_coral_cover(
                image_dir=image_dir,
                annotation_dir=labels_dir,
                class_names=CLASS_NAMES_OTHER,  # Use substrate class for ground truth
                limit=limit
            )
            

            
            # Process ground truth with legends
            add_segmentation_annotations(
                image_dir=image_dir,
                labels_dir=labels_dir,
                class_names=CLASS_NAMES_OTHER,  # Use substrate class for ground truth
                quantify_folder=quantify_folder,
                image_coverages=gt_image_coverages,
                limit=limit
            )
            
            # Process predictions with legends
            process_predictions_with_legend(
                pred_labels_dir,
                pred_images_dir,
                class_names,
                pred_image_coverages,
                
            )
            
            # Create comparison directory
            comparison_dir = os.path.join("outputs", "comparison")
            if os.path.exists(comparison_dir):
                shutil.rmtree(comparison_dir)
            os.makedirs(comparison_dir)
            
            # Create side-by-side comparisons using quantified images
            for img_name in os.listdir(pred_images_dir):
                if img_name.endswith(('.jpg', '.JPG', '.png', '.PNG')):
                    pred_img = os.path.join(pred_images_dir, img_name)
                    gt_img = os.path.join(quantify_folder, img_name)  # Use quantified image instead of raw
                    output_path = os.path.join(comparison_dir, f"comparison_{img_name}")
                    create_side_by_side_comparison(pred_img, gt_img, output_path)
            
            # Display results
            self.results_view.display_results_compared(
                pred_results=(pred_class_coverage, pred_total_coverage),
                gt_results=(gt_class_coverage, gt_total_coverage)
            )
            
            self.latest_output_dir = comparison_dir
            self.view_results_btn.setEnabled(True)
            
        except Exception as e:
            if os.path.exists(comparison_dir):
                try:
                    shutil.rmtree(comparison_dir)
                except:
                    pass
            raise Exception(f"Comparison analysis failed: {str(e)}")
            
    def _run_prediction(self, model, image_dir, class_names, limit,confidence):
        """Run prediction on images."""
        try:
            # Get the labels directory from prediction
            predicted_labels_dir, predicted_images_dir = self.model_manager.predict_with_limit(
                image_dir=image_dir,
                limit=limit,
                output_folder="outputs",
                conf=confidence
            )
            
            # Store the output directory
            self.latest_output_dir = os.path.dirname(predicted_labels_dir)
            
            # Calculate coverage using predicted labels
            class_coverage, total_coverage, image_coverages = calculate_total_coral_cover(
                image_dir=image_dir,
                annotation_dir=predicted_labels_dir,
                class_names=class_names,
                limit=limit
            )
            
            
            # Process predictions using the already calculated coverages
            process_predictions_with_legend(
                predicted_labels_dir, 
                predicted_images_dir, 
                class_names, 
                image_coverages
            )
            
            self.results_view.display_results(class_coverage, total_coverage)
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")




    def _run_quantification(self, image_dir, labels_dir,class_names, limit):
       
        """Run quantification on existing labels and save overlay images."""
        try:
            # Create output directories
            output_base = "outputs"
            os.makedirs(output_base, exist_ok=True)
            quantify_folder = os.path.join(output_base, "quantify")
            
            # Clean up existing quantify folder
            if os.path.exists(quantify_folder):
                try:
                    shutil.rmtree(quantify_folder)
                    print(f"Removed existing quantify folder: {quantify_folder}")
                except Exception as e:
                    raise Exception(f"Failed to remove existing quantify folder: {str(e)}")
            
            # Create fresh directory for processed images
            os.makedirs(quantify_folder)
            
            # Calculate coverage
            class_coverage, total_coverage, image_coverages = calculate_total_coral_cover(
                image_dir=image_dir,
                annotation_dir=labels_dir,
                class_names=class_names,
                limit=limit
            )

            
            add_segmentation_annotations(
            image_dir=image_dir,
            labels_dir=labels_dir,
            class_names=class_names,
            quantify_folder=quantify_folder,
            image_coverages=image_coverages,
            limit=limit
        )

            
            # Process predictions with legends
            # process_predictions_with_legend(
            #     image_dir,
            #     labels_dir,
            #     class_names,
            #     image_coverages,
            #     quant_colors = quant_colors
            # )
            # Store the output directory and update UI
            self.latest_output_dir = quantify_folder
            self.results_view.display_results(class_coverage, total_coverage)
            self.view_results_btn.setEnabled(True)
            
        except Exception as e:
            if os.path.exists(quantify_folder):
                try:
                    shutil.rmtree(quantify_folder)
                    print(f"Cleaned up quantify folder after error: {quantify_folder}")
                except:
                    pass
            raise Exception(f"Quantification failed: {str(e)}")
        
 
            
    # def open_results_folder(self):
    #     """Open the folder containing the predicted images."""
    #     if self.latest_output_dir and os.path.exists(self.latest_output_dir):
    #         try:
    #             if os.name == 'nt':  # Windows
    #                 os.startfile(self.latest_output_dir)
    #             else:  # Linux/Mac
    #                 subprocess.run(['xdg-open', self.latest_output_dir])
    #         except Exception as e:
    #             QMessageBox.warning(self, "Error", f"Could not open folder: {str(e)}")
    #     else:
    #         QMessageBox.warning(self, "Error", "No output folder available")
    def open_results_folder(self):
        """Open the folder containing the results."""
        folders_to_open = []
        
        # Add main results folder if it exists
        if self.latest_output_dir and os.path.exists(self.latest_output_dir):
            folders_to_open.append(self.latest_output_dir)
        
        # Add cropping folder if cropping was enabled
        if self.analysis_options.is_cropping_enabled() and self.cropping_model.latest_output_dir:
            if os.path.exists(self.cropping_model.latest_output_dir):
                folders_to_open.append(self.cropping_model.latest_output_dir)
        
        if not folders_to_open:
            QMessageBox.warning(self, "Error", "No output folders available")
            return
            
        try:
            for folder in folders_to_open:
                if os.name == 'nt':  # Windows
                    os.startfile(folder)
                else:  # Linux/Mac
                    subprocess.run(['xdg-open', folder])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open folder(s): {str(e)}")
                
            
 
