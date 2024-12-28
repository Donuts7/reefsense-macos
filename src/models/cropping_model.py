# """Cropping model management."""
# import os
# import cv2
# import numpy as np
# from ultralytics import YOLO
# from ..config.paths import get_next_cropping_dir
# from ..utils.image_distortion import (
#     correct_pincushion_distortion,
#     warp_image_to_square,
#     crop_image_by_coordinates
# )

# class CroppingModel:
#     def __init__(self):
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         CROPPING_MODEL_PATH = os.path.join(current_dir, 'crop.pt')
#         self.model = YOLO(CROPPING_MODEL_PATH)
        
#     def process_image(self, image_path, save_path):
#         """Process a single image with the cropping model."""
#         image = cv2.imread(image_path)
#         corrected = correct_pincushion_distortion(image, k1=0.42)
#         warped = warp_image_to_square(corrected, warp_factor=0.025, padding=500)
        
#         result = self.model.predict(warped, conf=0.8, verbose=False)
#         if result[0].masks is None:
#             cv2.imwrite(save_path, warped)
#             return False
            
#         confidences = np.array(result[0].boxes.conf)
#         max_conf_index = np.argmax(confidences)
#         coord = np.array(result[0].masks.xy[max_conf_index])
        
#         final_image = crop_image_by_coordinates(warped, coord)
#         cv2.imwrite(save_path, final_image)
#         return True

#     def process_folder(self, input_folder, limit=None):
#         """Process all images in a folder and save to cropping_outputs."""
#         # Get the next available cropping directory
#         output_dir = get_next_cropping_dir()
#         os.makedirs(output_dir, exist_ok=True)
        
#         success_count = 0
#         failed_count = 0
        
#         # Get list of image files and apply limit if specified
#         image_files = [f for f in sorted(os.listdir(input_folder)) 
#                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.JPG'))]
#         if limit is not None:
#             image_files = image_files[:limit]
        
#         for filename in image_files:
#             input_path = os.path.join(input_folder, filename)
#             output_path = os.path.join(output_dir, filename)
            
#             if self.process_image(input_path, output_path):
#                 success_count += 1
#             else:
#                 failed_count += 1
                    
#         return success_count, failed_count, output_dir
"""Cropping model management."""
import os
import cv2
import numpy as np
import shutil
from ultralytics import YOLO
from ..config.paths import get_next_cropping_dir
from ..utils.image_distortion import (
    correct_pincushion_distortion,
    warp_image_to_square,
    crop_image_by_coordinates
)

class CroppingModel:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        CROPPING_MODEL_PATH = os.path.join(current_dir, 'crop.pt')
        self.model = YOLO(CROPPING_MODEL_PATH)
        self.latest_output_dir = None
        
    def process_image(self, image_path, save_path):
        """Process a single image with the cropping model."""
        image = cv2.imread(image_path)
        corrected = correct_pincushion_distortion(image, k1=0.42)
        warped = warp_image_to_square(corrected, warp_factor=0.025, padding=500)
        
        result = self.model.predict(warped, conf=0.8, verbose=False)
        if result[0].masks is None:
            cv2.imwrite(save_path, warped)
            return False
            
        confidences = np.array(result[0].boxes.conf)
        max_conf_index = np.argmax(confidences)
        coord = np.array(result[0].masks.xy[max_conf_index])
        
        final_image = crop_image_by_coordinates(warped, coord)
        cv2.imwrite(save_path, final_image)
        return True

    def process_folder(self, input_folder, limit=None):
        """Process all images in a folder and save to outputs/cropping."""
        # Define output directory
        output_dir = os.path.join("outputs", "cropping")
        
        # Clean up existing cropping folder if it exists
        if os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
                print(f"Removed existing cropping folder: {output_dir}")
            except Exception as e:
                raise Exception(f"Failed to remove existing cropping folder: {str(e)}")
        
        # Create fresh directory
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        failed_count = 0
        
        # Get list of image files and apply limit if specified
        image_files = [f for f in sorted(os.listdir(input_folder)) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.JPG'))]
        if limit is not None:
            image_files = image_files[:limit]
        
        for filename in image_files:
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_dir, filename)
            
            if self.process_image(input_path, output_path):
                success_count += 1
            else:
                failed_count += 1
        
        # Store the output directory
        self.latest_output_dir = output_dir
                    
        return success_count, failed_count, output_dir