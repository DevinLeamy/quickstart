# CHERRY WILL WILL

### Setup

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip3 install .
```

### Visualization

We're using `Open3D` for visualizations. To create a visualization, you provide a 3D numpy array of points, and it
will render them as a point cloud.

```bash
python3 ./lib/cherry_mapping/main.py
```
