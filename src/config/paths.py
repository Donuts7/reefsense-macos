"""Path configuration for the application."""
import os
import glob

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Output subdirectories
CROPPING_BASE_DIR = os.path.join(OUTPUTS_DIR, "cropping")

def get_next_cropping_dir():
    """Get the next available cropping directory number."""
    if not os.path.exists(CROPPING_BASE_DIR):
        os.makedirs(CROPPING_BASE_DIR)
        return os.path.join(CROPPING_BASE_DIR, "cropping1")
        
    existing_dirs = glob.glob(os.path.join(CROPPING_BASE_DIR, "cropping*"))
    if not existing_dirs:
        return os.path.join(CROPPING_BASE_DIR, "cropping1")
        
    numbers = [int(dir.split("cropping")[-1]) for dir in existing_dirs]
    next_number = max(numbers) + 1
    return os.path.join(CROPPING_BASE_DIR, f"cropping{next_number}")

# Model paths
HC_MODEL_PATH = os.path.join(MODELS_DIR, "hc.pt")
GROUPS_MODEL_PATH = os.path.join(MODELS_DIR, "groups.pt")
CROPPING_MODEL_PATH = os.path.join(MODELS_DIR, "crop.pt")