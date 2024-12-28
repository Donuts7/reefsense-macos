"""File handling utilities."""

import os
import glob

def get_latest_predicted_folder(base_path="outputs"):
    """Get the path to the latest prediction folder."""
    folders = glob.glob(os.path.join(base_path, 'predict*'))
    if not folders:
        raise ValueError("No prediction folders found in 'outputs'")
    
    latest_folder = max(folders, key=os.path.getmtime)
    label_folder = os.path.join(latest_folder, 'labels')
    
    if not os.path.exists(label_folder) or not os.listdir(label_folder):
        raise ValueError(f"No labels found in the predicted folder: {latest_folder}")
    
    return os.path.join(latest_folder, "labels").replace("\\", "/")