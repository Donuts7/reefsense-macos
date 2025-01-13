"""Model management for coral analysis."""
import os
import shutil
from pathlib import Path
from ultralytics import YOLO
from ..config import (
    # HC_MODEL_PATH,
    # GROUPS_MODEL_PATH,
    CLASS_NAMES_HC,
    CLASS_NAMES_GROUPS,
    CLASS_NAMES_OTHER
)

# class ModelManager:
#     """Manages the loading and configuration of YOLO models."""
    
#     def __init__(self):
#         self.current_model = None
#         self.current_class_names = None
    
#     def load_model(self, model_type):
#         """Load the appropriate model based on type."""
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         HC_MODEL_PATH = os.path.join(current_dir,'hc.pt')
#         GROUPS_MODEL_PATH = os.path.join(current_dir,'groups.pt')
        
#         if model_type == "hc":
#             self.current_model = YOLO(HC_MODEL_PATH)
#             self.current_class_names = CLASS_NAMES_HC
#         elif model_type == "groups":
#             self.current_model = YOLO(GROUPS_MODEL_PATH)
#             self.current_class_names = CLASS_NAMES_GROUPS
#         else:
#             self.current_class_names = CLASS_NAMES_OTHER
#         return self.current_model, self.current_class_names
class ModelManager:
    """Manages the loading and configuration of YOLO models."""

    def __init__(self):
        self.current_model = None
        self.current_class_names = None

    def load_model(self, model_type, folder_path):
        """Load the appropriate model based on type and optionally update class names from a YAML file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        HC_MODEL_PATH = os.path.join(current_dir, 'hc.pt')
        GROUPS_MODEL_PATH = os.path.join(current_dir, 'groups.pt')

        if model_type == "hc":
            self.current_model = YOLO(HC_MODEL_PATH)
            self.current_class_names = {0: 'hard coral'}
        elif model_type == "groups":
            self.current_model = YOLO(GROUPS_MODEL_PATH)
            self.current_class_names = {
                0: 'bouldering',
                1: 'branching',
                2: 'solitary',
                3: 'plating',
                4: 'encrusting',
            }
        else:
            # Default to numeric class names if no YAML file is present
            self.current_class_names = self.load_class_names_from_yaml(folder_path)

        return self.current_model, self.current_class_names

    def load_class_names_from_yaml(self, folder_path):
        """
        Load class names from a data.yaml file if it exists in the folder.
        If no YAML file is found or it cannot be parsed, default to numeric class names.
        """
        yaml_path = os.path.join(folder_path, 'data.yaml')
        if not os.path.exists(yaml_path):
            # Default to numeric class names
            print("No YAML file found. Defaulting to numeric class names.")
            return {i: str(i) for i in range(100)}  # Adjust the range as needed for maximum expected classes

        try:
            with open(yaml_path, 'r') as f:
                lines = f.readlines()

            class_names = {}
            for line in lines:
                line = line.strip()
                if ':' in line and not line.startswith('#'):
                    parts = line.split(':', 1)
                    try:
                        class_num = int(parts[0].strip())
                        class_name = parts[1].strip().strip("'").strip('"')
                        class_names[class_num] = class_name
                    except ValueError:
                        continue

            if not class_names:
                print("YAML file found but no valid class names extracted. Defaulting to numeric class names.")
                return {i: str(i) for i in range(100)}

            print(f"Class names loaded from YAML: {class_names}")
            return class_names

        except Exception as e:
            print(f"Error reading YAML file: {e}. Defaulting to numeric class names.")
            return {i: str(i) for i in range(100)}
    
    

    def predict_with_limit(self, image_dir, limit, output_folder,conf=0.25):
        """
        Run predictions on images with an optional limit on the number of images.
        Ensures clean prediction folder by removing any existing one before running.
        """
        if not self.current_model:
            raise ValueError("No model loaded. Call load_model first.")
        
        # Use Path for better path handling
        input_path = Path(image_dir)
        
        # Get all image files, excluding subdirectories
        valid_extensions = {'.png', '.jpg', '.jpeg', '.JPG'}
        image_files = [
            f for f in input_path.iterdir()
            if f.is_file() and f.suffix.lower() in valid_extensions
        ]
        
        # Sort files for consistent ordering
        image_files.sort()
        # Apply the limit
        if limit:
            image_files = image_files[:limit]

        # Construct the full paths for the selected images
        image_files_with_path = [os.path.join(image_dir, f) for f in image_files]

        # Define prediction folder path
        prediction_folder = os.path.join(output_folder, 'predict')
        
        # Clean up existing prediction folder if it exists
        if os.path.exists(prediction_folder):
            try:
                shutil.rmtree(prediction_folder)
                print(f"Removed existing prediction folder: {prediction_folder}")
            except Exception as e:
                raise Exception(f"Failed to remove existing prediction folder: {str(e)}")
        
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)
        
        try:
            # Run predictions on the selected images
            results = self.current_model.predict(
                source=image_files_with_path,
                save=True,
                save_txt=True,
                project=output_folder,
                name='predict',  # Use a fixed name
                exist_ok=True,   # Keep this true in case of race conditions
                conf=conf,
                show_boxes=True,
                line_width=3
            )
            
            # Verify the labels directory was created
            labels_dir = os.path.join(prediction_folder, 'labels')
            if not os.path.exists(labels_dir):
                raise ValueError("No prediction folder created. Check YOLO prediction output.")
                
            return labels_dir, prediction_folder
            
        except Exception as e:
            # Clean up prediction folder if something goes wrong during prediction
            if os.path.exists(prediction_folder):
                try:
                    shutil.rmtree(prediction_folder)
                    print(f"Cleaned up prediction folder after error: {prediction_folder}")
                except:
                    pass  # If cleanup fails, just continue with the error
            raise Exception(f"Prediction failed: {str(e)}")