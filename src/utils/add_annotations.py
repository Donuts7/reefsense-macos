import os
import cv2
import numpy as np
from random import randint
from .colors import generate_colors # type: ignore
from .image_processing import process_predictions_with_legend

# def add_segmentation_annotations(image_dir, labels_dir, class_names,quantify_folder,image_coverages, limit=None):
#     """
#     Overlay segmentation masks on images based on annotation files.

#     Args:
#         image_dir (str): Path to the directory containing the images.
#         labels_dir (str): Path to the directory containing the label files.
#         class_names (list): List of class names.
#         limit (int, optional): Maximum number of images to process. If None, processes all images.

#     Returns:
#         list: A list of combined images with overlays.
#     """


#     overlayed_images = []
#     annotation_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    
#     if limit:
#         annotation_files = annotation_files[:limit]

#     # Define colors for each class (using YOLO colors)
#     colors = generate_colors(len(class_names))

#     for label_file in annotation_files:
#         base_name = os.path.splitext(label_file)[0]
        
#         # Find and load the corresponding image
#         image_path = None
#         for ext in ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']:
#             potential_path = os.path.join(image_dir, base_name + ext)
#             if os.path.exists(potential_path):
#                 image_path = potential_path
#                 break

#         if not image_path:
#             continue

#         # Load image and create mask
#         image = cv2.imread(image_path)
#         height, width = image.shape[:2]
        
#         # Create a transparent overlay
#         overlay = np.zeros((height, width, 4), dtype=np.uint8)
        
#         # Read and process the label file
#         label_path = os.path.join(labels_dir, label_file)
#         with open(label_path, 'r') as f:
#             for line in f:
#                 parts = line.strip().split()
#                 if len(parts) < 3:  # Skip invalid lines
#                     continue
                    
#                 class_id = int(parts[0])
#                 coords = parts[1:]
                
#                 # Convert normalized coordinates to pixel coordinates
#                 polygon_points = []
#                 for i in range(0, len(coords), 2):
#                     x = float(coords[i]) * width
#                     y = float(coords[i + 1]) * height
#                     polygon_points.append([int(x), int(y)])
                    
#                 # Create mask for this polygon
#                 color = colors[class_id % len(colors)]

#                 pts = np.array(polygon_points, np.int32)
#                 pts = pts.reshape((-1, 1, 2))
                
#                 # Draw filled polygon with transparency
#                 # Adjust the mask color manually
 
#                 cv2.fillPoly(overlay, [pts], (*color, 128))  # Apply with reduced red/green


#         # Combine original image with overlay
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
#         result = cv2.addWeighted(image, 1, overlay, 0.5, 0)       
#         overlayed_images.append(result)
#         output_path = os.path.join(quantify_folder, os.path.basename(image_path))
#         cv2.imwrite(output_path, cv2.cvtColor(result, cv2.COLOR_BGRA2BGR))
#         # Add legends to the processed images
       
#         process_predictions_with_legend(
#             predicted_label_dir=labels_dir,
#             predicted_image_dir=quantify_folder,
#             class_names=class_names,
#             image_coverages=image_coverages,
#             quant_colors= colors
#         )

    # return image_path, overlayed_images
def add_segmentation_annotations(image_dir, labels_dir, class_names, quantify_folder, image_coverages, limit=None):
    overlayed_images = []
    annotation_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    
    if limit:
        annotation_files = annotation_files[:limit]

    colors = generate_colors(len(class_names))

    for label_file in annotation_files:
        base_name = os.path.splitext(label_file)[0]
        
        # Find and load the corresponding image
        image_path = None
        for ext in ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']:
            potential_path = os.path.join(image_dir, base_name + ext)
            if os.path.exists(potential_path):
                image_path = potential_path
                break

        if not image_path:
            continue

        # Load image and create mask
        image = cv2.imread(image_path)
        height, width = image.shape[:2]
        
        # Create a transparent overlay
        overlay = np.zeros((height, width, 3), dtype=np.uint8)  # Changed to 3 channels
        alpha_channel = np.zeros((height, width), dtype=np.uint8)  # Separate alpha channel
        
        # Read and process the label file
        label_path = os.path.join(labels_dir, label_file)
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
                    
                class_id = int(parts[0])
                coords = parts[1:]
                
                polygon_points = []
                for i in range(0, len(coords), 2):
                    x = float(coords[i]) * width
                    y = float(coords[i + 1]) * height
                    polygon_points.append([int(x), int(y)])
                    
                color = colors[class_id % len(colors)]
                pts = np.array(polygon_points, np.int32)
                pts = pts.reshape((-1, 1, 2))
                
                # Draw the filled polygon on both the color and alpha channels
                cv2.fillPoly(overlay, [pts], color)
                cv2.fillPoly(alpha_channel, [pts], 100)  # Reduced opacity value (0-255)

        # Blend the overlay with the original image using the alpha channel
        alpha_3channel = np.stack([alpha_channel, alpha_channel, alpha_channel], axis=-1) / 255.0
        result = np.uint8(image * (1 - alpha_3channel) + overlay * alpha_3channel)
        
        overlayed_images.append(result)
        output_path = os.path.join(quantify_folder, os.path.basename(image_path))
        cv2.imwrite(output_path, result)
        
        process_predictions_with_legend(
            predicted_label_dir=labels_dir,
            predicted_image_dir=quantify_folder,
            class_names=class_names,
            image_coverages=image_coverages,
            quant_colors=colors
        )