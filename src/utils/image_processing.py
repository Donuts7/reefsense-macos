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
# def process_predictions_with_legend(predicted_label_dir, predicted_image_dir ,class_names):
#     """
#     Add a legend with class coverage percentages to each image in the predicted_label_dir.
#     """
#     for label_file in os.listdir(predicted_label_dir):
#         if label_file.endswith(".txt"):
#             # Corresponding image file
#             image_file = os.path.splitext(label_file)[0] + ".JPG"            
#             image_path = os.path.join(predicted_image_dir, image_file)

#             if not os.path.exists(image_path):
#                 print(f"Image {image_file} not found in {predicted_image_dir}. Skipping.")
#                 continue

#             # Read polygons and calculate class coverage
#             annotation_path = os.path.join(predicted_label_dir, label_file)
#             polygons = read_polygons_from_file(annotation_path, class_names)
#             img_size = Image.open(image_path).size
#             class_coverage = calculate_areas(polygons, img_size)

#             # Prepare a dictionary for class coverage percentages
#             class_coverage_percentages = {
#                 data["class_name"]: data["area_percentage"]
#                 for _, data in class_coverage.items()
#             }

#             # Open the predicted image
#             image = Image.open(image_path)

#             # Add legend
#             image_with_legend = add_legend(image, class_coverage_percentages, class_names)
#             print('image path:',image_path)
#             # Overwrite the existing image with the updated one
#             image_with_legend.save(image_path)
#             # print(f"Updated image with legend: {image_path}")
def process_predictions_with_legend(predicted_label_dir, predicted_image_dir, class_names, image_coverages):
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
            image_with_legend = add_legend(image, class_coverage_percentages, class_names)
            # print('image path:', image_path)
            # Overwrite the existing image with the updated one
            image_with_legend.save(image_path)


            
def add_legend(image, class_coverage, class_names, font_path="arial.ttf", font_size=50, corner_radius=20):
    """
    Add a dynamic legend to the image displaying class coverage percentages,
    using the same colors as the YOLOv8 model for each class, with rounded corners.
    """
    # print('classs', class_names )
    # Convert image to RGB if not already
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Create a new image to overlay the legend
    draw = ImageDraw.Draw(image)

    # Load font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate the height of the legend box based on the number of classes
    line_height = font_size + 10
    legend_x = 50
    legend_y = 50
    num_classes = len(class_coverage)

    # Dynamically adjust the box width based on the longest class name and font size
    longest_class_name = max(class_coverage.keys(), key=len)
    box_width = max(len(longest_class_name) * (font_size), 350)  # Ensure it is wide enough

    # Adjust size based on the number of classes
    box_height = (num_classes + 1) * line_height + 20

    # Draw the rounded rectangle (legend box)
    draw.rounded_rectangle(
        [(legend_x, legend_y), (legend_x + box_width, legend_y + box_height)],
        radius=corner_radius,
        fill=(255, 255, 255, 200),  # Semi-transparent white
    )

    # Add the title
    draw.text((legend_x + 10, legend_y + 5), "Class Coverage", fill="black", font=font)

    # Add class names and their coverage percentages
    for i, (class_name, coverage) in enumerate(class_coverage.items(), start=1):
        # Get the index of the class and map it to the corresponding color
        class_idx = list(class_names.keys())[list(class_names.values()).index(class_name)]
        color = YOLOV8_COLORS[class_idx % len(YOLOV8_COLORS)]  # Cycle through available colors
        
        y_offset = legend_y + i * line_height
        draw.rectangle(
            [(legend_x + 10, y_offset), (legend_x + 40, y_offset + font_size)],
            fill=color,
        )
        draw.text(
            (legend_x + 50, y_offset),
            f"{class_name}: {coverage:.2f}%",
            fill="black",
            font=font,
        )

    return image