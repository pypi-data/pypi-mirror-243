import sys
import os
sys.path.append('../')

from segment_lidar import samlidar, view

# Define the view
view = view.PinholeView()

# Define the model
model = samlidar.SamLidar(algorithm='segment-anything',
                          ckpt_path='model/sam_vit_h_4b8939.pth',
                          interactive=True)

# Load the data
points = model.read('data/laundry.las')

# Ground points filter
# cloud, non_ground, ground = model.csf(points, csf_path='results/csf.las', exists=True)

# Segment the point cloud
labels, *_ = model.segment(points=points,
                           view=view,
                           image_path='results/raster.tif',
                           labels_path='results/labeled.tif',
                           image_exists=False,
                           label_exists=False)

# Save the segments
model.write(points=points, segment_ids=labels, save_path="results/segmented.las")