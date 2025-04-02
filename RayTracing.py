import numpy as np
import matplotlib.pyplot as plt

# Constants for the scene
LIGHT_INTENSITY = np.array([1.0, 1.0, 1.0])  # RGB intensity
LIGHT_LOCATION = np.array([10, 10, -10])     # Light source location
EYE_LOCATION = np.array([0, 0, -10])         # Camera (eye) position
VIEW_PLANE_Z = 0                             # Z-location of the view plane
VIEW_PLANE_SIZE = 10                         # Size of the view plane
RESOLUTION = 500                             # Image resolution (pixels)

K_AMBIENT = 0.1  # Ambient reflection coefficient
K_DIFFUSE = 0.7  # Diffuse reflection coefficient
K_SPECULAR = 0.2 # Specular reflection coefficient
SHININESS = 32   # Shininess coefficient for specular reflection

SCENE_OBJECTS = [
    {'type': 'sphere', 'center': np.array([-3, 0, 5]), 'radius': 1.5, 'color': np.array([1, 0, 0]), 'reflection': 0.3},
    {'type': 'sphere', 'center': np.array([2, -1, 7]), 'radius': 2, 'color': np.array([0, 1, 0]), 'reflection': 0.4},
    {'type': 'sphere', 'center': np.array([1, 2, 10]), 'radius': 1, 'color': np.array([0, 0, 1]), 'reflection': 0.5},
    {'type': 'plane', 'point': np.array([0, -4.5, 0]), 'normal': np.array([0, 1, 0]), 'color': np.array([0.5, 0.5, 0.5])},
    {'type': 'ellipsoid', 'center': np.array([-4, 2, 15]), 'axes': np.array([1.5, 2.0, 1.0]), 'color': np.array([1, 1, 0]), 'reflection': 0.2}
]


# Helper functions
def safe_normalize(vector):
    """Safely normalize a vector, avoiding division by zero."""
    norm = np.linalg.norm(vector)
    return vector / norm if norm > 0 else np.zeros_like(vector)

# Ray-object intersection functions
def intersect_sphere(ray_origin, ray_direction, center, radius):
    oc = ray_origin - center
    a = np.dot(ray_direction, ray_direction)
    b = 2.0 * np.dot(oc, ray_direction)
    c = np.dot(oc, oc) - radius**2
    discriminant = b**2 - 4*a*c
    if discriminant < 0 or np.isnan(discriminant):
        return None
    t1 = (-b - np.sqrt(discriminant)) / (2*a)
    t2 = (-b + np.sqrt(discriminant)) / (2*a)
    t_values = [t for t in [t1, t2] if t > 0]
    return min(t_values) if t_values else None

def intersect_plane(ray_origin, ray_direction, point, normal):
    denom = np.dot(normal, ray_direction)
    if abs(denom) < 1e-6:  # Ray is parallel to the plane
        return None
    t = np.dot(point - ray_origin, normal) / denom
    if t > 0:  # Intersection occurs in front of the ray origin
        intersection_point = ray_origin + t * ray_direction
        # Check if intersection is within the extended plane bounds
        if -20 <= intersection_point[0] <= 20 and -20 <= intersection_point[2] <= 20:
            return t
    return None

def intersect_ellipsoid(ray_origin, ray_direction, center, axes):
    scaled_origin = (ray_origin - center) / axes
    scaled_direction = ray_direction / axes
    return intersect_sphere(scaled_origin, scaled_direction, np.array([0, 0, 0]), 1)

# Lighting and shading model
def compute_lighting(point, normal, view_direction, color, reflection):
    # Ambient component
    ambient = K_AMBIENT * color

    # Diffuse component
    light_direction = safe_normalize(LIGHT_LOCATION - point)
    diffuse = K_DIFFUSE * np.clip(np.dot(normal, light_direction), 0, 1) * color * LIGHT_INTENSITY

    # Specular component
    reflection_direction = 2 * np.dot(normal, light_direction) * normal - light_direction
    specular = K_SPECULAR * np.clip(np.dot(view_direction, reflection_direction), 0, 1)**SHININESS * LIGHT_INTENSITY

    return ambient + diffuse + specular

# Ray tracing algorithm
def trace_ray(ray_origin, ray_direction, depth=3):
    if depth == 0:
        return np.array([0, 0, 0])

    closest_t = float('inf')
    closest_object = None

    # Find the nearest object intersected by the ray
    for obj in SCENE_OBJECTS:
        if obj['type'] == 'sphere':
            t = intersect_sphere(ray_origin, ray_direction, obj['center'], obj['radius'])
        elif obj['type'] == 'plane':
            t = intersect_plane(ray_origin, ray_direction, obj['point'], obj['normal'])
        elif obj['type'] == 'ellipsoid':
            t = intersect_ellipsoid(ray_origin, ray_direction, obj['center'], obj['axes'])
        else:
            continue
        if t and t < closest_t:
            closest_t = t
            closest_object = obj

    if closest_object is None:
        return np.array([0, 0, 0])  # Background color

    # Compute intersection point and normal
    intersection = ray_origin + closest_t * ray_direction
    if closest_object['type'] == 'sphere':
        normal = safe_normalize(intersection - closest_object['center'])
    elif closest_object['type'] == 'plane':
        normal = closest_object['normal']
    elif closest_object['type'] == 'ellipsoid':
        normal = safe_normalize((intersection - closest_object['center']) / closest_object['axes'])

    # Compute lighting and color
    view_direction = safe_normalize(-ray_direction)
    color = compute_lighting(intersection, normal, view_direction, closest_object['color'], closest_object.get('reflection', 0))

    # Add reflection
    if 'reflection' in closest_object:
        reflection_direction = ray_direction - 2 * np.dot(ray_direction, normal) * normal
        reflection_color = trace_ray(intersection + 1e-4 * reflection_direction, reflection_direction, depth - 1)
        color = (1 - closest_object['reflection']) * color + closest_object['reflection'] * reflection_color

    return np.clip(color, 0, 1)

# Render the scene
def render():
    image = np.zeros((RESOLUTION, RESOLUTION, 3))
    aspect_ratio = VIEW_PLANE_SIZE / VIEW_PLANE_SIZE

    for i in range(RESOLUTION):
        for j in range(RESOLUTION):
            # Map pixel to view plane
            x = (i / RESOLUTION - 0.5) * VIEW_PLANE_SIZE * aspect_ratio
            y = (0.5 - j / RESOLUTION) * VIEW_PLANE_SIZE  # Flip the y-axis here
            z = VIEW_PLANE_Z

            # Compute ray direction
            ray_direction = safe_normalize(np.array([x, y, z]) - EYE_LOCATION)

            # Trace the ray
            image[j, i] = trace_ray(EYE_LOCATION, ray_direction)

    return image

# Main
if __name__ == "__main__":
    print("Rendering...")
    image = render()
    plt.imshow(image)
    plt.axis('off')
    plt.show()
