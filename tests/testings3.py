
import math
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Cube vertices
vertices = [
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1)
]

# Edges connecting the vertices
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def rotate_vertex(vertex, angle_x, angle_y, angle_z):
    x, y, z = vertex
    # Rotation around X axis
    y, z = y * math.cos(angle_x) - z * math.sin(angle_x), y * math.sin(angle_x) + z * math.cos(angle_x)
    # Rotation around Y axis
    x, z = x * math.cos(angle_y) + z * math.sin(angle_y), -x * math.sin(angle_y) + z * math.cos(angle_y)
    # Rotation around Z axis
    x, y = x * math.cos(angle_z) - y * math.sin(angle_z), x * math.sin(angle_z) + y * math.cos(angle_z)
    return x, y, z

def project_vertex(vertex, screen_width, screen_height, scale, viewer_distance):
    x, y, z = vertex
    z += viewer_distance + 0.0001  # Add a small offset to avoid division by zero
    factor = scale / z
    x = int(x * factor + screen_width / 2)
    y = int(y * factor + screen_height / 2)
    return x, y

def draw_cube(vertices, edges, screen_width, screen_height, scale, viewer_distance, angle_x, angle_y, angle_z):
    clear_screen()
    rotated_vertices = [rotate_vertex(v, angle_x, angle_y, angle_z) for v in vertices]
    projected_vertices = [project_vertex(v, screen_width, screen_height, scale, viewer_distance) for v in rotated_vertices]

    screen = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]
    
    for edge in edges:
        start, end = edge
        x1, y1 = projected_vertices[start]
        x2, y2 = projected_vertices[end]
        
        dx, dy = x2 - x1, y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            steps = 1
        x_step, y_step = dx / steps, dy / steps

        x, y = x1, y1
        for _ in range(steps):
            if 0 <= int(y) < screen_height and 0 <= int(x) < screen_width:
                screen[int(y)][int(x)] = '#'
            x += x_step
            y += y_step

    for row in screen:
        print(''.join(row))

# Parameters
screen_width, screen_height = 80, 24
scale = 20
viewer_distance = 5
angle_x, angle_y, angle_z = 0, 0, 0
angle_speed = 0.03

while True:
    draw_cube(vertices, edges, screen_width, screen_height, scale, viewer_distance, angle_x, angle_y, angle_z)
    angle_x += angle_speed
    angle_y += angle_speed
    angle_z += angle_speed
    time.sleep(0.1)
