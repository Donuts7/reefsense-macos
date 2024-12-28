def calculate_polygon_area(vertices):
    """Calculate the area of a polygon using the Shoelace formula."""
    n = len(vertices)
    area = 0.0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - y1 * x2
    return abs(area) / 2.0

def read_polygons_from_file(file_path, class_names):
    """Read polygon data from annotation file."""
    polygons = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            class_id = int(parts[0])
            class_name = class_names.get(class_id, "Unknown Class")
            coords = parts[1:]
            vertices = [(float(coords[i]), float(coords[i + 1])) 
                       for i in range(0, len(coords), 2)]
            polygons.append((class_id, class_name, vertices))
    return polygons

def calculate_areas(polygons, img_size):
    """Calculate areas for each polygon."""
    img_area = img_size[0] * img_size[1]
    class_area_totals = {}
    
    for class_id, class_name, vertices in polygons:
        polygon_area = calculate_polygon_area(vertices) * img_area
        if class_id in class_area_totals:
            class_area_totals[class_id]["total_area"] += polygon_area
        else:
            class_area_totals[class_id] = {
                "class_name": class_name,
                "total_area": polygon_area
            }
            
    for data in class_area_totals.values():
        data["area_percentage"] = (data["total_area"] / img_area) * 100
        
    return class_area_totals