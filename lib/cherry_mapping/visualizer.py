import numpy as np
import open3d as o3d


class PointCloudVisualizer:
    def __init__(self):
        """Initialize the visualizer."""
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()

        # Set up initial view
        self.opt = self.vis.get_render_option()
        self.opt.background_color = np.asarray(
            [0.1, 0.1, 0.1])  # Dark background
        self.opt.point_size = 5.0  # Larger point size

        # Initialize with empty point cloud
        self.pcd = o3d.geometry.PointCloud()
        self.boxes = []

        # Add coordinate frame for reference
        coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
            size=1.0)
        self.vis.add_geometry(coordinate_frame)

    def visualize(self, points: np.ndarray):
        """
        Visualize points as boxes.

        Args:
            points (np.ndarray): Point cloud data of shape (N, 3)
        """
        # Remove old boxes
        for box in self.boxes:
            self.vis.remove_geometry(box, False)
        self.boxes.clear()

        # Create new boxes for each point
        box_size = 0.1  # Size of each box
        for point in points:
            box = o3d.geometry.TriangleMesh.create_box(width=box_size,
                                                       height=box_size,
                                                       depth=box_size)
            box.translate(
                point - np.array([box_size/2, box_size/2, box_size/2]))
            box.paint_uniform_color([1, 0.7, 0])  # Yellow color for visibility
            self.boxes.append(box)
            self.vis.add_geometry(box, False)

        self.vis.poll_events()
        self.vis.update_renderer()

    def close(self):
        """Close the visualization window."""
        self.vis.destroy_window()
