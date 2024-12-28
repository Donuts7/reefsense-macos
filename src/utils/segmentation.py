"""Segmentation evaluation utilities."""
import numpy as np
from shapely.geometry import Polygon
from typing import List, Tuple, Dict
import os
from pathlib import Path
from tqdm import tqdm

def read_polygons_from_file(file_path: str) -> List[Tuple[int, List[Tuple[float, float]]]]:
    """
    Read YOLO format polygons from a file.
    Each line format: class_id x1 y1 x2 y2 x3 y3 ...
    Coordinates are normalized (0-1)
    """
    polygons = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:  # Skip empty or invalid lines
                    continue
                class_id = int(parts[0])
                # Convert pairs of coordinates into vertices
                coords = [float(x) for x in parts[1:]]
                vertices = list(zip(coords[::2], coords[1::2]))
                polygons.append((class_id, vertices))
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return []
    return polygons

def calculate_iou(poly1: List[Tuple[float, float]], 
                 poly2: List[Tuple[float, float]]) -> float:
    """
    Calculate Intersection over Union between two polygons.
    Coordinates are assumed to be normalized (0-1).
    """
    try:
        # Convert to Shapely polygons
        polygon1 = Polygon(poly1)
        polygon2 = Polygon(poly2)
        
        # Handle invalid polygons
        if not polygon1.is_valid or not polygon2.is_valid:
            return 0.0
        
        # Calculate intersection and union areas
        intersection_area = polygon1.intersection(polygon2).area
        union_area = polygon1.union(polygon2).area
        
        # Handle edge case where both polygons are empty
        if union_area == 0:
            return 0.0
        
        return intersection_area / union_area
    except Exception:
        return 0.0

def calculate_metrics_for_file_pair(gt_file: str, 
                                  pred_file: str,
                                  iou_threshold: float = 0.5) -> Dict[str, float]:
    """
    Calculate metrics for a single pair of ground truth and prediction files.
    """
    # Read ground truth and predicted polygons
    gt_polygons = read_polygons_from_file(gt_file)
    pred_polygons = read_polygons_from_file(pred_file)
    
    # Initialize metrics
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    total_iou = 0
    
    # If either file is empty, count appropriately
    if not gt_polygons:
        return {
            'true_positives': 0,
            'false_positives': len(pred_polygons),
            'false_negatives': 0,
            'total_iou': 0
        }
    if not pred_polygons:
        return {
            'true_positives': 0,
            'false_positives': 0,
            'false_negatives': len(gt_polygons),
            'total_iou': 0
        }
    
    # Calculate IoU matrix between all GT and pred polygons
    n_gt = len(gt_polygons)
    n_pred = len(pred_polygons)
    iou_matrix = np.zeros((n_gt, n_pred))
    
    for i, (gt_class, gt_poly) in enumerate(gt_polygons):
        for j, (pred_class, pred_poly) in enumerate(pred_polygons):
            # Only calculate IoU if classes match
            if gt_class == pred_class:
                iou_matrix[i, j] = calculate_iou(gt_poly, pred_poly)
    
    # Match predictions to ground truth using greedy assignment
    matched_gt = set()
    matched_pred = set()
    
    while True:
        # Find highest remaining IoU
        unmatched_mask = np.ones_like(iou_matrix, dtype=bool)
        unmatched_mask[list(matched_gt), :] = False
        unmatched_mask[:, list(matched_pred)] = False
        
        if not np.any(unmatched_mask):
            break
            
        curr_ious = np.where(unmatched_mask, iou_matrix, 0)
        if np.max(curr_ious) < iou_threshold:
            break
            
        i, j = np.unravel_index(np.argmax(curr_ious), iou_matrix.shape)
        matched_gt.add(i)
        matched_pred.add(j)
        total_iou += iou_matrix[i, j]
        true_positives += 1
    
    # Count unmatched as false positives/negatives
    false_negatives = n_gt - len(matched_gt)
    false_positives = n_pred - len(matched_pred)
    
    return {
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'total_iou': total_iou
    }

def evaluate_segmentation_directory(annotation_dir: str,
                                  predicted_label_dir: str,
                                  iou_threshold: float = 0.5) -> Dict[str, float]:
    """
    Evaluate segmentation metrics across all matching files in two directories.
    """
    # Convert paths to Path objects
    ann_dir = Path(annotation_dir).resolve()
    pred_dir = Path(predicted_label_dir).resolve()
    
    # Get all txt files in annotation directory
    ann_files = list(ann_dir.glob('*.txt'))
    
    # Initialize overall metrics
    total_true_positives = 0
    total_false_positives = 0
    total_false_negatives = 0
    total_iou = 0
    processed_files = 0
    
    print(f"\nProcessing {len(ann_files)} files...")
    
    # Process each file
    for ann_file in tqdm(ann_files):
        pred_file = pred_dir / ann_file.name
        if not pred_file.exists():
            print(f"\nSkipping {ann_file.name} - no matching prediction file")
            continue
            
        # Calculate metrics for this file pair
        metrics = calculate_metrics_for_file_pair(
            str(ann_file),
            str(pred_file),
            iou_threshold
        )
        
        # Accumulate metrics
        total_true_positives += metrics['true_positives']
        total_false_positives += metrics['false_positives']
        total_false_negatives += metrics['false_negatives']
        total_iou += metrics['total_iou']
        processed_files += 1
    
    # Calculate final metrics
    precision = total_true_positives / (total_true_positives + total_false_positives) if (total_true_positives + total_false_positives) > 0 else 0.0
    recall = total_true_positives / (total_true_positives + total_false_negatives) if (total_true_positives + total_false_negatives) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    mean_iou = total_iou / total_true_positives if total_true_positives > 0 else 0.0
    
    return {
        'mean_iou': mean_iou,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'processed_files': processed_files,
        'total_true_positives': total_true_positives,
        'total_false_positives': total_false_positives,
        'total_false_negatives': total_false_negatives
    }