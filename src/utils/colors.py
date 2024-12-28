"""Color utilities for visualization."""

def generate_colors(num_classes):
    """
    Generate visually distinct colors proportional to the number of classes.
    Uses HSV color space for better distribution.
    """
    colors = []
    for i in range(num_classes):
        # Distribute hue evenly across the spectrum
        hue = i * (360 / num_classes)
        
        # Convert HSV to RGB (using fixed saturation and value for visibility)
        h = hue / 360  # Normalize to 0-1
        s = 0.8  # High saturation for vivid colors
        v = 0.9  # High value for visibility
        
        # HSV to RGB conversion
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        if i % 6 == 0:
            r, g, b = v, t, p
        elif i % 6 == 1:
            r, g, b = q, v, p
        elif i % 6 == 2:
            r, g, b = p, v, t
        elif i % 6 == 3:
            r, g, b = p, q, v
        elif i % 6 == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
            
        # Convert to 0-255 range and return as BGR for OpenCV
        colors.append((
            int(b * 255),
            int(g * 255),
            int(r * 255)
        ))
        
    return colors