"""Image processing utilities for adding legends and overlays."""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Tuple

# Import utilities from ..utils.useful
from .geometry import read_polygons_from_file, calculate_areas
YOLOV8_COLORS = [
    (4, 42, 255),    # Class 0 - Bright Blue
    (11, 219, 235),  # Class 1 - Cyan
    (243, 243, 243), # Class 2 - Light Grey
    (0, 223, 183),   # Class 3 - Teal
    (17, 31, 104),   # Class 4 - Navy Blue
    (255, 99, 71),   # Class 5 - Tomato Red
    (255, 215, 0),   # Class 6 - Gold
    (34, 139, 34),   # Class 7 - Forest Green
    (75, 0, 130),    # Class 8 - Indigo
    (255, 105, 180), # Class 9 - Hot Pink
    (70, 130, 180),  # Class 10 - Steel Blue
    (128, 0, 0),     # Class 11 - Maroon
    (218, 112, 214), # Class 12 - Orchid
    (244, 164, 96),  # Class 13 - Sandy Brown
    (47, 79, 79)     # Class 14 - Dark Slate Gray
]

def process_predictions_with_legend(predicted_label_dir, predicted_image_dir, class_names, image_coverages, quant_colors= None):
    """
    Add a legend with class coverage percentages to each image in the predicted_label_dir.
    Uses pre-calculated coverage values from calculate_total_coral_cover.
    """
    for label_file in os.listdir(predicted_label_dir):
        if label_file.endswith(".txt"):
            # Corresponding image file
            image_file = os.path.splitext(label_file)[0] + ".JPG"            
            image_path = os.path.join(predicted_image_dir, image_file)

            if not os.path.exists(image_path):
                #print(f"Image {image_file} not found in {predicted_image_dir}. Skipping.")
                continue

            # Get the pre-calculated coverage for this image
            image_name = os.path.splitext(label_file)[0]
            class_coverage_percentages = image_coverages[image_name]

            # Open the predicted image
            image = Image.open(image_path)

            # Add legend
            image_with_legend = add_legend(image, class_coverage_percentages, class_names, quant_colors)
            # print('image path:', image_path)
            # Overwrite the existing image with the updated one
            image_with_legend.save(image_path)


            


def add_legend(image, class_coverage, class_names, quant_colors, font_path="arial.ttf", font_size=50, corner_radius=20):
    """
    Add legend with consistent colors between masks and legend.
    """
    if image.mode != "RGB":
        image = image.convert("RGB")

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # line_height = font_size + 10
    # legend_x = 50
    # legend_y = 50
    # longest_class_name = max(class_coverage.keys(), key=len)
    # # box_width = max(len(longest_class_name) * (font_size), 450)
    # box_width = len(longest_class_name) * font_size + 140  # Added 5px to the calculated width
    # box_height = (len(class_coverage) + 1) * line_height + 20
    line_height = font_size + 10
    legend_x = 50
    legend_y = 50
    
    # Draw title text first on a temporary image to get its dimensions
    temp_img = Image.new('RGB', (420, 100), color='white')
    temp_draw = ImageDraw.Draw(temp_img)
    title_text = "Class Coverage"
    temp_draw.text((0, 0), title_text, fill="black", font=font)
    # Get the bounding box of the text
    bbox = temp_img.getbbox()
    title_width = bbox[2] - bbox[0] + 20  # Add 20px padding
    
    # Calculate width needed for longest class name
    longest_class_name = max(class_coverage.keys(), key=len)
    class_width = len(longest_class_name)* font_size * 0.6
    
    # Use the larger of the two widths
    box_width = max(title_width, class_width)
    box_height = (len(class_coverage) + 1) * line_height + 20
    draw.rounded_rectangle(
        [(legend_x, legend_y), (legend_x + box_width, legend_y + box_height)],
        radius=corner_radius,
        fill=(255, 255, 255, 200),
    )

    draw.text((legend_x + 10, legend_y + 5), "Class Coverage", fill="black", font=font)

    for i, (class_name, coverage) in enumerate(class_coverage.items(), start=1):
        class_idx = list(class_names.keys())[list(class_names.values()).index(class_name)]
        
        if quant_colors is not None:
            # Convert BGR to RGB for PIL
            color = (quant_colors[class_idx % len(quant_colors)][::-1])
        else:
            color = YOLOV8_COLORS[class_idx % len(YOLOV8_COLORS)]
        
        y_offset = legend_y + i * line_height
        draw.rectangle(
            [(legend_x + 15, y_offset), (legend_x + 45, y_offset + font_size)],
            fill=color,
        )
        draw.text(
            (legend_x + 50, y_offset),
            f"{class_name}: {coverage:.2f}%",
            fill="black",
            font=font,
        )

    return image

