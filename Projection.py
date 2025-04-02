import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.widgets import Slider

# Parameters for perspective projection
f = 1000  # Focal length
d = 10  # Distance offset

# Read 3D points from face-vertices.data
vertices = []
with open('face-vertices.data', 'r') as file:
    for line in file:
        x, y, z = map(float, line.strip().split(','))
        vertices.append((x, y, z))

# Read indices from face-index.txt
triangles = []
with open('face-index.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:  # Check if the line is not empty
            indices = list(map(int, line.split(',')))
            if len(indices) == 3:  # Ensure the line forms a triangle
                triangles.append((indices[0] - 1, indices[1] - 1, indices[2] - 1))  # Convert to 0-based indexing

# Function to apply 3D rotation around the y-axis
def rotate_3d_y(vertices, angle):
    angle_rad = np.radians(angle)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    rotation_matrix = np.array([[cos_a, 0, sin_a],
                                [0, 1, 0],
                                [-sin_a, 0, cos_a]])
    rotated_vertices = []
    for x, y, z in vertices:
        rotated_vertex = np.dot(rotation_matrix, np.array([x, y, z]))
        rotated_vertices.append(rotated_vertex)
    return rotated_vertices

# Function to project 3D points to 2D using perspective projection
def project_3d_to_2d(vertices, f, d, scaling_factor=2.0):
    projected_points = []
    for x, y, z in vertices:
        x_2d = (x * f) / (z + d) * scaling_factor
        y_2d = (y * f) / (z + d) * scaling_factor
        projected_points.append((x_2d, y_2d))
    return projected_points

# Project vertices to 2D
rotated_vertices = rotate_3d_y(vertices, 135)  # No initial rotation
projected_points = project_3d_to_2d(rotated_vertices, f, d)
projected_points = np.array(projected_points)

# Calculate axis limits based on projected points
x_vals, y_vals = projected_points[:, 0], projected_points[:, 1]
padding = 4

# Set up the main plot and the scatter plot for points
fig, (ax, ax_points) = plt.subplots(1, 2, figsize=(20, 10))
plt.subplots_adjust(bottom=0.4)  # Adjust space to fit the sliders below the plot

# Create the PolyCollection object for filled faces in the main plot
polygons = []
for idx1, idx2, idx3 in triangles:
    polygon = [projected_points[idx1], projected_points[idx2], projected_points[idx3]]
    polygons.append(polygon)

poly_collection = PolyCollection(polygons, facecolors='lightblue', edgecolors='darkblue', linewidths=0.5)
ax.add_collection(poly_collection)

# Display points only in the second plot
ax_points.scatter(projected_points[:, 0], projected_points[:, 1], color='darkblue', s=1)
ax_points.set_title("Points")
ax_points.set_aspect('equal')

# Initial axis limits for both plots
ax.set_xlim(x_vals.min() - padding, x_vals.max() + padding)
ax.set_ylim(y_vals.min() - padding, y_vals.max() + padding)
ax.set_title("WireMesh+Polygons")
ax.set_aspect('equal')

ax_points.set_xlim(x_vals.min() - padding, x_vals.max() + padding)
ax_points.set_ylim(y_vals.min() - padding, y_vals.max() + padding)

# SLIDER SECTION
#
#
#

ax_rot = plt.axes([0.2, 0.25, 0.65, 0.03], facecolor='lightgrey')
ax_zoom = plt.axes([0.2, 0.2, 0.65, 0.03], facecolor='lightgrey')
ax_f = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor='lightgrey')
ax_d = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgrey')

# Initial values for sliders
rot_init = 135  # Initial rotation angle
zoom_init = 2.0  # Initial zoom level
f_init = 1000  # Initial focal length
d_init = 10  # Initial distance offset

# Create sliders
slider_rot = Slider(ax_rot, 'Rotation', -180, 180, valinit=rot_init)
slider_zoom = Slider(ax_zoom, 'Zoom', 0.1, 3.0, valinit=zoom_init)
slider_f = Slider(ax_f, 'Focal Length', 100, 1000, valinit=f_init)
slider_d = Slider(ax_d, 'Distance Offset', 1, 20, valinit=d_init)

# Define the update function for sliders
def update(val):
    angle = slider_rot.val
    zoom = slider_zoom.val
    f = slider_f.val
    d = slider_d.val
    
    # Rotate 3D points and project them
    rotated_vertices = rotate_3d_y(vertices, angle)
    projected_points = project_3d_to_2d(rotated_vertices, f, d, scaling_factor=zoom)
    projected_points = np.array(projected_points)
    
    # Update the polygon data for the main plot
    updated_polygons = []
    for idx1, idx2, idx3 in triangles:
        polygon = [projected_points[idx1], projected_points[idx2], projected_points[idx3]]
        updated_polygons.append(polygon)

    poly_collection.set_verts(updated_polygons)

    # Update axis limits dynamically for the main plot
    x_vals, y_vals = projected_points[:, 0], projected_points[:, 1]
    ax.set_xlim(x_vals.min() - padding, x_vals.max() + padding)
    ax.set_ylim(y_vals.min() - padding, y_vals.max() + padding)

    # Update the scatter plot for points only
    ax_points.clear()
    ax_points.scatter(projected_points[:, 0], projected_points[:, 1], color='darkblue', s=1)
    ax_points.set_title("Points")
    ax_points.set_xlim(x_vals.min() - padding, x_vals.max() + padding)
    ax_points.set_ylim(y_vals.min() - padding, y_vals.max() + padding)
    ax_points.set_aspect('equal')

    fig.canvas.draw_idle()

# Connect sliders to the update function
slider_rot.on_changed(update)
slider_zoom.on_changed(update)
slider_f.on_changed(update)
slider_d.on_changed(update)

plt.show()
