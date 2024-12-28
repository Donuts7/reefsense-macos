"""Configuration settings for the Coral Analysis Tool."""

import os

# Class definitions for different model types
CLASS_NAMES_OTHER = {0: "substrate"}
CLASS_NAMES_HC = {0: "hard coral"}
CLASS_NAMES_GROUPS = {
    0: "bouldering",
    1: "branching",
    2: "solitary",
    3: "plating",
    4: "encrusting",
}

# Model paths
MODELS_DIR = "models"
HC_MODEL_PATH = os.path.join(MODELS_DIR, "hc.pt")
GROUPS_MODEL_PATH = os.path.join(MODELS_DIR, "groups.pt")

# YOLOv8 color palette for classes
YOLOV8_COLORS = [
    (4, 42, 255),    # Class 0
    (11, 219, 235),  # Class 1
    (243, 243, 243), # Class 2
    (0, 223, 183),   # Class 3
    (17, 31, 104),   # Class 4
]