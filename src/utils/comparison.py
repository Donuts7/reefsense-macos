"""Utilities for comparing prediction and quantification results."""
import os
import cv2
import numpy as np
from PIL import Image

def create_side_by_side_comparison(pred_image_path: str, quant_image_path: str, output_path: str) -> None:
    """Create a side-by-side comparison image."""
    # Read images
    pred_img = cv2.imread(pred_image_path)
    quant_img = cv2.imread(quant_image_path)
    
    # Ensure same height
    height = max(pred_img.shape[0], quant_img.shape[0])
    width = pred_img.shape[1]
    
    # Resize if necessary
    if pred_img.shape[0] != height:
        pred_img = cv2.resize(pred_img, (width, height))
    if quant_img.shape[0] != height:
        quant_img = cv2.resize(quant_img, (width, height))
    
    # # Create side-by-side image
    # comparison = np.hstack((pred_img, quant_img))
    
    # # Add titles
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # title_font = cv2.FONT_HERSHEY_SIMPLEX
    # title_size = 2
    # title_thickness = 3
    # title_color = (255, 255, 255)  # White
    
    # # Title text
    # title_pred = 'Prediction'
    # title_gt = 'Ground Truth'
    
    # # Add title at the top
    # title_width = width  # width for the left title
    # cv2.putText(comparison, title_pred, (10, 50), title_font, title_size, title_color, title_thickness)
    # cv2.putText(comparison, title_gt, (width + 10, 50), title_font, title_size, title_color, title_thickness)
    
    # # Save result
    # cv2.imwrite(output_path, comparison)
        # Create a blank canvas to place the title
    # Create a blank canvas to place the title
    # Create a blank canvas to place the title
    # Create a blank canvas to place the labels and images
  # Create a blank canvas to place the labels and images
    label_height = 100  # Increased space for the labels
    comparison = np.ones((height + label_height, width * 2, 3), dtype=np.uint8) * 255  # White background
    
    # Place the images in the comparison
    comparison[label_height:, :width] = pred_img
    comparison[label_height:, width:] = quant_img
    
    # Add labels for individual images
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 3  # Increased font size
    thickness = 8 # Increased thickness
    color = (0, 0, 0)  # Black font color

    # Center the "Prediction" label on the first image
    pred_label = 'Prediction'
    pred_label_size = cv2.getTextSize(pred_label, font, scale, thickness)[0]
    pred_label_x = (width - pred_label_size[0]) // 2
    pred_label_y = (label_height + pred_label_size[1]) // 2
    cv2.putText(comparison, pred_label, (pred_label_x, pred_label_y), font, scale, color, thickness)
    
    # Center the "Ground Truth" label on the second image
    gt_label = 'Ground Truth'
    gt_label_size = cv2.getTextSize(gt_label, font, scale, thickness)[0]
    gt_label_x = width + (width - gt_label_size[0]) // 2
    gt_label_y = (label_height + gt_label_size[1]) // 2
    cv2.putText(comparison, gt_label, (gt_label_x, gt_label_y), font, scale, color, thickness)
    
    # Save the resulting image
    cv2.imwrite(output_path, comparison)