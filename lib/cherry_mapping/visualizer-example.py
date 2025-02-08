import open3d as o3d
import numpy as np
import time

import visualizer

vis = visualizer.PointCloudVisualizer()

num_points = 1000
points = np.random.rand(num_points, 3)

for _ in range(500):
    points += (np.random.rand(num_points, 3) - 0.5) * \
        0.01

    vis.visualize(points)
    time.sleep(0.02)

vis.close()
