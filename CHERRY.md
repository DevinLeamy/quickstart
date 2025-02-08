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
python3 ./lib/cherry_mapping/main.py --ip <raspberry-pi-ip>
```

> Getting the raspberry pi ip address:
>
> ```bash
> # On the raspberry pi
> hostname -I
> ```

How this works.

On the raspberry pi we run the mapping node. The mapping node will publish a new message type POINT_CLOUD_MSG, to a new topic `/mapping/point_cloud`. The message publisher is configured to accept external connections.

On your Desktop you create a subscriber that subscribes to the new `/mapping/point_cloud` topic.
When a message is received, the received point cloud is visualized using Open3D.
