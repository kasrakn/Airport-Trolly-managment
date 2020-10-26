import numpy as np
import geog
import threading
from MQTTClient import trolley_positions

def generate_points(pivot, radius, n_points = 20):
    angles = np.linspace(0, 360, n_points)
    points = geog.propagate(pivot, angles, radius)
    return list(points)

pivot1 = (59.516600706900025, 36.312902499948134)
pivot2 = (59.516400706900025, 36.313002499948134)
pivot3 = (59.516550706900025, 36.312702499948134)

points1 = generate_points(pivot=pivot1, radius=15, n_points=10)
points2 = generate_points(pivot=pivot2, radius=15, n_points=10)
points3 = generate_points(pivot=pivot3, radius=15, n_points=10)

i = 0
def traverse_points():
    global i

    threading.Timer(5.0, traverse_points).start()

    trolley_positions[1001] = [points1[i % len(points1)][1], points1[i % len(points1)][0]]
    trolley_positions[1002] = [points2[i % len(points2)][1], points2[i % len(points2)][0]]
    trolley_positions[1003] = [points3[i % len(points3)][1], points3[i % len(points3)][0]]

    i = i + 1 if i < 1000 else 0