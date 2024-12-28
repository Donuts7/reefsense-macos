from ultralytics import YOLO

class ModelManager:
    # HC_MODEL_PATH = r"models\hc.pt"
    # GROUPS_MODEL_PATH = r"models\groups.pt"
    
    CLASS_NAMES_HC = {0: "hard coral"}
    CLASS_NAMES_GROUPS = {
        0: "bouldering",
        1: "branching",
        2: "solitary",
        3: "plating",
        4: "encrusting",
    }
    CLASS_NAMES_OTHER = {0: "substrate"}
    
    def __init__(self):
        self.current_model = None
        self.current_class_names = None
    
    def load_model(self, model_type):
        if model_type == "hc":
            self.current_model = YOLO(self.HC_MODEL_PATH)
            self.current_class_names = self.CLASS_NAMES_HC
        elif model_type == "groups":
            self.current_model = YOLO(self.GROUPS_MODEL_PATH)
            self.current_class_names = self.CLASS_NAMES_GROUPS
        else:
            self.current_class_names = self.CLASS_NAMES_OTHER
        return self.current_model, self.current_class_names