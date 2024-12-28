"""Image distortion correction utilities."""
import cv2
import numpy as np

def correct_pincushion_distortion(image, k1=0.55, k2=0.15, k3=0):
    """Correct pincushion distortion in an image."""
    h, w = image.shape[:2]
    focal_length = max(w, h)
    center = (w / 2, h / 2)
    camera_matrix = np.array([[focal_length, 0, center[0]],
                            [0, focal_length, center[1]],
                            [0, 0, 1]], dtype=np.float32)
    
    dist_coeffs = np.array([k1, k2, 0, 0, k3], dtype=np.float32)
    new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    return cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)

def warp_image_to_square(image, warp_factor=0.05, padding=50):
    """Warp an image to make it square."""
    h, w = image.shape[:2]
    padded_image = cv2.copyMakeBorder(image, padding, padding, padding, padding, 
                                    cv2.BORDER_CONSTANT, value=[0, 0, 0])
    
    ph, pw = padded_image.shape[:2]
    src_points = np.float32([
        [warp_factor * pw, warp_factor * ph],
        [pw - 1 - warp_factor * pw, warp_factor * ph],
        [pw - 1 - warp_factor * pw, ph - 1 - warp_factor * ph],
        [warp_factor * pw, ph - 1 - warp_factor * ph]
    ])
    
    dst_points = np.float32([
        [0, 0],
        [pw - 1, 0],
        [pw - 1, ph - 1],
        [0, ph - 1]
    ])
    
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_image = cv2.warpPerspective(padded_image, M, (pw, ph))
    return warped_image[padding:padding + h, padding:padding + w]


def crop_image_by_coordinates(image, coordinates, crop_percentage=0.03):
    """Crop an image based on coordinates with additional percentage crop."""
    coordinates = coordinates.reshape(-1, 2)
    corners = [
        coordinates[np.argmin(coordinates[:, 0] + coordinates[:, 1])],  # top_left
        coordinates[np.argmin(coordinates[:, 0] - coordinates[:, 1])],  # bottom_left
        coordinates[np.argmax(coordinates[:, 0] - coordinates[:, 1])],  # top_right
        coordinates[np.argmax(coordinates[:, 0] + coordinates[:, 1])]   # bottom_right
    ]
    
    x_coords = [int(corner[0]) for corner in corners]
    y_coords = [int(corner[1]) for corner in corners]
    
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    
    cropped = image[y_min:y_max, x_min:x_max]
    h, w = cropped.shape[:2]
    crop_x = int(w * crop_percentage)
    crop_y = int(h * crop_percentage)
    
    return cropped[crop_y:h - crop_y, crop_x:w - crop_x]