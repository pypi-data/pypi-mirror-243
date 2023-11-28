"""
VCD (Video Content Description) library.

Project website: http://vcd.vicomtech.org

Copyright (C) 2023, Vicomtech (http://www.vicomtech.es/),
(Spain) all rights reserved.

VCD is a Python library to create and manage OpenLABEL content.
VCD is distributed under MIT License. See LICENSE.
"""

from pathlib import Path

import cv2 as cv
import numpy as np

from vcd import core, draw, scl, utils

from .test_config import openlabel_version_name


def test_draw_topview_bevs():
    vcd = core.VCD()
    cam_params_file = str(
        Path(__file__).parent.resolve()
        / "etc"
        / str(openlabel_version_name + "_cam_params_topview_bevs.json")
    )
    vcd.load_from_file(cam_params_file)

    # Prepare Scene
    scene = scl.Scene(vcd)  # scl.Scene has functions to project images, transforms, etc.

    # Get input camera image
    fv_image_file = str(
        Path(__file__).parent.resolve()
        / "etc"
        / str(openlabel_version_name + "_fv_topview_bevs.jpg")
    )
    img_fv = cv.imread(fv_image_file)

    # Configure the topview range
    img_width_px = 1024
    img_height_px = 1024
    ar = img_width_px / img_height_px
    bev_range_x = (-15.0, 15.0)
    bev_range_y = (
        -((bev_range_x[1] - bev_range_x[0]) / ar) / 2,
        ((bev_range_x[1] - bev_range_x[0]) / ar) / 2,
    )

    # Define the topview parameters
    bev_params = draw.TopView.Params(
        color_map=utils.COLORMAP_1,
        topview_size=(img_width_px, img_height_px),
        background_color=255,
        range_x=bev_range_x,
        range_y=bev_range_y,
        step_x=1.0,
        step_y=1.0,
        draw_grid=False,
    )

    # Create the topview object
    drawer_bev = draw.TopView(
        scene=scene, coordinate_system="vehicle-iso8855", params=bev_params
    )

    # Draw the topview
    drawer_bev.add_images(imgs={"FV": img_fv}, frame_num=0)
    drawer_bev.draw_bevs(0)
    topview_bev = drawer_bev.topView

    # Test the generated topview is the same as expected
    expected_topview_file = str(
        Path(__file__).parent.resolve()
        / "etc"
        / str(openlabel_version_name + "_test_draw_topview_bevs.npy")
    )
    expected_topview_bevs = np.load(expected_topview_file)

    np.testing.assert_equal(topview_bev, expected_topview_bevs)
