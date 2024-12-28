import os
from PIL import Image
from .utils import read_polygons_from_file, calculate_areas

def calculate_coverage(image_dir, annotation_dir, class_names, limit=None):
    """Calculate coral coverage for a set of images."""
    total_image_area = 0.0
    class_area_totals = {class_id: 0.0 for class_id in class_names}
    image_coverages = {}
    
    annotation_files = [f for f in os.listdir(annotation_dir) if f.endswith(".txt")]
    if limit:
        annotation_files = annotation_files[:limit]
        
    for annotation_filename in annotation_files:
        annotation_path = os.path.join(annotation_dir, annotation_filename)
        image_path = os.path.join(image_dir, os.path.splitext(annotation_filename)[0] + ".jpg")
        
        if not os.path.exists(image_path):
            continue
            
        img_size = Image.open(image_path).size
        img_area = img_size[0] * img_size[1]
        total_image_area += img_area
        
        polygons = read_polygons_from_file(annotation_path, class_names)
        image_class_areas = calculate_areas(polygons, img_size)
        
        image_coverage = {}
        for class_id, area in image_class_areas.items():
            coverage_percentage = (area["total_area"] / img_area) * 100
            class_name = class_names[class_id]
            image_coverage[class_name] = coverage_percentage
            class_area_totals[class_id] += area["total_area"]
            
        image_coverages[os.path.splitext(annotation_filename)[0]] = image_coverage
    
    class_coverage = {
        class_names[class_id]: (area / total_image_area) * 100
        for class_id, area in class_area_totals.items()
    }
    
    total_coverage = sum(class_coverage.values())
    
    return class_coverage, total_coverage, image_coverages