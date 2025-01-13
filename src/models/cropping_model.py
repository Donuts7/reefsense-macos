

 #VERSION  1
# """Cropping model management."""
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

# class CroppingModel:
#     def __init__(self):
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         CROPPING_MODEL_PATH = os.path.join(current_dir, 'crop.pt')
#         self.model = YOLO(CROPPING_MODEL_PATH)
#         self.latest_output_dir = None
        
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
#         """Process all images in a folder and save to outputs/cropping."""
#         # Define output directory
#         output_dir = os.path.join("outputs", "cropping")
        
#         # Clean up existing cropping folder if it exists
#         if os.path.exists(output_dir):
#             try:
#                 shutil.rmtree(output_dir)
#                 print(f"Removed existing cropping folder: {output_dir}")
#             except Exception as e:
#                 raise Exception(f"Failed to remove existing cropping folder: {str(e)}")
        
#         # Create fresh directory
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
        
#         # Store the output directory
#         self.latest_output_dir = output_dir
                    
#         return success_count, failed_count, output_dir

class CroppingModel:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        CROPPING_MODEL_PATH = os.path.join(current_dir, 'crop.pt')
        self.model = YOLO(CROPPING_MODEL_PATH)
        self.latest_output_dir = None
        
    def process_image(self, image_path, save_path):
        """Process a single image with the cropping model."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to read image: {image_path}")
                return False
                
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
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            return False

    def process_folder(self, input_folder, limit=None, output_dir=None):
        """Process all images in a folder and save to specified output directory."""
        try:
            # If no output directory specified, create one in the current working directory
            if output_dir is None:
                output_dir = os.path.abspath(os.path.join(os.getcwd(), "outputs", "cropping"))
            else:
                output_dir = os.path.abspath(output_dir)
            
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
            
            # Store the output directory using absolute path
            self.latest_output_dir = output_dir
            
            return success_count, failed_count, output_dir
            
        except Exception as e:
            raise Exception(f"Cropping process failed: {str(e)}")