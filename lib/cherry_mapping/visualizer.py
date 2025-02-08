import numpy as np
import open3d as o3d


class PointCloudVisualizer:
    def __init__(self):
        """Initialize the visualizer."""
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()

        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(np.random.rand(1000, 3))
        self.vis.add_geometry(self.pcd)

    def visualize(self, points: np.ndarray):
        """
        Visualize a point cloud.

        Args:
            points (np.ndarray): Point cloud data of shape (N, 3)
        """
        self.pcd.points = o3d.utility.Vector3dVector(points)


        self.vis.update_geometry(self.pcd)
        self.vis.poll_events()
        self.vis.update_renderer()

    def close(self):
        """Close the visualization window."""
        self.vis.destroy_window()
