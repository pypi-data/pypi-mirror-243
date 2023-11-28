"""
Module to handle drawing functions using VCD data.

This module helps to draw TopView images, VCD info and other functionalities.
"""
# VCD (Video Content Description) library.
#
# Project website: http://vcd.vicomtech.org
#
# Copyright (C) 2023, Vicomtech (http://www.vicomtech.es/),
# (Spain) all rights reserved.
#
# VCD is a Python library to create and manage OpenLABEL content.
# VCD is distributed under MIT License. See LICENSE.


from __future__ import annotations

import copy
import warnings
from secrets import randbelow
from typing import Any

import cv2 as cv
import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

from vcd import core, scl, utils


class SetupViewer:
    """This class offers Matplotlib routines to display the coordinate systems of the Scene."""

    def __init__(self, scene: scl.Scene, coordinate_system: str):
        if not isinstance(scene, scl.Scene):
            raise TypeError("Argument 'scene' must be of type 'vcd.scl.Scene'")
        self.scene = scene
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(projection="3d")
        self.coordinate_system = coordinate_system
        if not self.scene.vcd.has_coordinate_system(coordinate_system):
            raise ValueError(
                "The provided scene does not have the specified coordinate system"
            )

    def __plot_cs(self, pose_wrt_ref: npt.NDArray, name: str, la: float = 1):
        # Explore the coordinate systems defined for this scene
        axis = np.array(
            [
                [0, la, 0, 0, 0, 0],
                [0, 0, 0, la, 0, 0],
                [0, 0, 0, 0, 0, la],
                [1, 1, 1, 1, 1, 1],
            ]
        )  # matrix with several 4x1 points
        pose_wrt_ref = np.array(pose_wrt_ref).reshape(4, 4)
        axis_ref = pose_wrt_ref.dot(axis)
        origin = axis_ref[:, 0]
        x_axis_end = axis_ref[:, 1]
        y_axis_end = axis_ref[:, 3]
        z_axis_end = axis_ref[:, 5]
        self.ax.plot(
            [origin[0], x_axis_end[0]],
            [origin[1], x_axis_end[1]],
            [origin[2], x_axis_end[2]],
            "r-",
        )
        self.ax.plot(
            [origin[0], y_axis_end[0]],
            [origin[1], y_axis_end[1]],
            [origin[2], y_axis_end[2]],
            "g-",
        )
        self.ax.plot(
            [origin[0], z_axis_end[0]],
            [origin[1], z_axis_end[1]],
            [origin[2], z_axis_end[2]],
            "b-",
        )

        self.ax.text(origin[0], origin[1], origin[2], rf"{name}")
        self.ax.text(x_axis_end[0], x_axis_end[1], x_axis_end[2], "X")
        self.ax.text(y_axis_end[0], y_axis_end[1], y_axis_end[2], "Y")
        self.ax.text(z_axis_end[0], z_axis_end[1], z_axis_end[2], "Z")

    def plot_cuboid(self, cuboid_cs: str, cuboid_vals: tuple | list, color: Any):
        t, static = self.scene.get_transform(cuboid_cs, self.coordinate_system)
        cuboid_vals_transformed = utils.transform_cuboid(cuboid_vals, t)

        p = utils.generate_cuboid_points_ref_4x8(cuboid_vals_transformed)

        pairs = (
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
        )
        for pair in pairs:
            self.ax.plot(
                [p[0, pair[0]], p[0, pair[1]]],
                [p[1, pair[0]], p[1, pair[1]]],
                [p[2, pair[0]], p[2, pair[1]]],
                c=color,
            )

    def plot_setup(self, axes: list[list] | None = None) -> fig.Figure:
        for cs_name, cs in self.scene.vcd.get_root()["coordinate_systems"].items():
            transform, _static = self.scene.get_transform(cs_name, self.coordinate_system)
            la = 2.0
            if cs["type"] == "sensor_cs":
                la = 0.5
            self.__plot_cs(transform, cs_name, la)

        if "objects" in self.scene.vcd.get_root():
            for _object_id, obj in self.scene.vcd.get_root()["objects"].items():
                if obj["name"] == "Ego-car":
                    cuboid = obj["object_data"]["cuboid"][0]
                    cuboid_cs = cuboid["coordinate_system"]
                    cuboid_vals = cuboid["val"]
                    self.plot_cuboid(cuboid_cs, cuboid_vals, "k")

                else:
                    if "object_data" in obj:
                        if "cuboid" in obj["object_data"]:
                            for cuboid in obj["object_data"]["cuboid"]:
                                self.plot_cuboid(
                                    cuboid["coordinate_system"], cuboid["val"], "k"
                                )

        if axes is None:
            self.ax.set_xlim(-1.25, 4.25)
            self.ax.set_ylim(-2.75, 2.75)
            self.ax.set_zlim(0, 5.5)
        else:
            self.ax.set_xlim(axes[0][0], axes[0][1])
            self.ax.set_ylim(axes[1][0], axes[1][1])
            self.ax.set_zlim(axes[2][0], axes[2][1])

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        return self.fig


class TopView:
    """
    Define functions to draw topview representations.

    This class draws a top view of the scene, assuming Z=0 is the ground plane (i.e. the
    topview sees the XY plane) Range and scale can be used to select a certain part of the XY
    plane.
    """

    class Params:  # pylint: disable=too-many-instance-attributes
        """
        Define the parameters needed to draw topview representations.

        Assuming cuboids are drawn top view, so Z coordinate is ignored RZ is the rotation in
        Z-axis, it assumes/enforces SY>SX, thus keeping RZ between pi/2 and -pi/2.

        Z, RX, RY, and SZ are ignored

        For Vehicle cases, we adopt ISO8855: origin at rear axle at ground, x-to-front, y-to-
        left
        """

        def __init__(
            self,
            step_x: float | None = None,
            step_y: float | None = None,
            background_color: int | None = None,
            topview_size: tuple[int, int] | None = None,
            range_x: tuple[float, float] | None = None,
            range_y: tuple[float, float] | None = None,
            color_map: dict | None = None,
            ignore_classes: dict | None = None,
            draw_grid: bool = True,
            draw_only_current_image: bool = True,
        ):
            self.topview_size = (1920, 1080)  # width, height
            if topview_size is not None:
                if not isinstance(topview_size, tuple):
                    raise TypeError("Argument 'topview_size' must be of type 'tuple'")
                self.topview_size = topview_size

            self.ar = self.topview_size[0] / self.topview_size[1]

            self.range_x = (-80.0, 80.0)
            if range_x is not None:
                if not isinstance(range_x, tuple):
                    raise TypeError("Argument 'range_x' must be of type 'tuple'")
                self.range_x = range_x

            self.range_y = (self.range_x[0] / self.ar, self.range_x[1] / self.ar)
            if range_y is not None:
                if not isinstance(range_y, tuple):
                    raise TypeError("Argument 'range_y' must be of type 'tuple'")
                self.range_y = range_y

            self.scale_x = self.topview_size[0] / (self.range_x[1] - self.range_x[0])
            self.scale_y = -self.topview_size[1] / (
                self.range_y[1] - self.range_y[0]
            )  # Negative?

            self.offset_x = round(-self.range_x[0] * self.scale_x)
            self.offset_y = round(
                -self.range_y[1] * self.scale_y
            )  # TODO: shouldn't it be -self.rangeY[0]?

            self.S = np.array(
                [
                    [self.scale_x, 0, self.offset_x],
                    [0, self.scale_y, self.offset_y],
                    [0, 0, 1],
                ]
            )

            self.step_x = 1.0
            if step_x is not None:
                self.step_x = step_x
            self.step_y = 1.0
            if step_y is not None:
                self.step_y = step_y

            self.grid_lines_thickness = 1
            self.background_color = 255
            if background_color is not None:
                self.background_color = background_color

            self.grid_text_color = (0, 0, 0)

            if color_map is None:
                self.color_map = {}
            else:
                if not isinstance(color_map, dict):
                    raise TypeError("Argument 'color_map' must be of type 'dict'")
                self.color_map = color_map

            if ignore_classes is None:
                self.ignore_classes = {}
            else:
                self.ignore_classes = ignore_classes

            self.draw_grid = True
            if draw_grid is not None:
                self.draw_grid = draw_grid

            self.draw_only_current_image = draw_only_current_image

    def __init__(
        self,
        scene: scl.Scene,
        coordinate_system: str,
        params: TopView.Params | None = None,
    ):
        # scene contains the VCD and helper functions for transforms and projections
        if not isinstance(scene, scl.Scene):
            raise TypeError("Argument 'scene' must be of type 'vcd.scl.Scene'")
        self.scene = scene
        # This value specifies which coordinate system is fixed in the
        # center of the TopView, e.g. "odom" or "vehicle-iso8855"
        if not scene.vcd.has_coordinate_system(coordinate_system):
            raise ValueError(
                f"The provided scene does not have coordinate system {coordinate_system}"
            )
        self.coordinate_system = coordinate_system
        if params is not None:
            self.params = params
        else:
            self.params = TopView.Params()

        # Start topView base with a background color
        self.topView = np.zeros(
            (self.params.topview_size[1], self.params.topview_size[0], 3), np.uint8
        )  # Needs to be here
        self.topView.fill(self.params.background_color)
        self.images: dict = {}

    def add_images(self, imgs: dict, frame_num: int):
        """
        Add images to the TopView representation.

        By specifying the frame num and the camera name, several images can be loaded in one
        single call. Images should be provided as dictionary:

        {"CAM_FRONT": img_front, "CAM_REAR": img_rear}

        The function pre-computes all the necessary variables to create the TopView, such as
        the homography from image plane to world plane, or the camera region of interest, which
        is stored in scene.cameras dictionary.

        :param imgs: dictionary of images
        :param frame_num: frame number
        :return: nothing
        """
        # Base images
        # should be {"CAM_FRONT": img_front, "CAM_REAR": img_rear}
        if not isinstance(imgs, dict):
            raise TypeError("Argument 'imgs' must be of type 'dict'")

        # This option creates 1 remap for the entire topview, and not 1 per camera
        # The key idea is to weight the contribution of each camera depending on the
        # distance between point and cam
        # Instead of storing the result in self.images[cam_name] and then paint them
        # in drawBEV, we can store in self.images[frameNum] directly
        h = self.params.topview_size[1]
        w = self.params.topview_size[0]
        num_cams = len(imgs)
        cams: dict[str, scl.Camera | None] = {}
        need_to_recompute_weights_acc = False
        need_to_recompute_maps = {}
        need_to_recompute_weights = {}
        for cam_name, img in imgs.items():
            if not self.scene.vcd.has_coordinate_system(cam_name):
                raise ValueError(
                    f"The provided scene does not have coordinate system {cam_name}"
                )
            # this call creates an entry inside scene
            cam = self.scene.get_camera(cam_name, frame_num, compute_remaps=False)
            cams[cam_name] = cam
            self.images.setdefault(cam_name, {})
            self.images[cam_name]["img"] = img
            t_ref_to_cam_4x4, static = self.scene.get_transform(
                self.coordinate_system, cam_name, frame_num
            )

            # Compute distances to this camera and add to weight map
            need_to_recompute_maps[cam_name] = False
            need_to_recompute_weights[cam_name] = False

            if (num_cams > 1 and not static) or (
                num_cams > 1 and static and "weights" not in self.images[cam_name]
            ):
                need_to_recompute_weights[cam_name] = True
                need_to_recompute_weights_acc = True

            if (not static) or (static and "mapX" not in self.images[cam_name]):
                need_to_recompute_maps[cam_name] = True

            if need_to_recompute_maps[cam_name]:
                print(cam_name + " top view remap computation...")
                self.images[cam_name]["mapX"] = np.zeros((h, w), dtype=np.float32)
                self.images[cam_name]["mapY"] = np.zeros((h, w), dtype=np.float32)

            if need_to_recompute_weights[cam_name]:
                print(cam_name + " top view weights computation...")
                self.images[cam_name].setdefault(
                    "weights", np.zeros((h, w, 3), dtype=np.float32)
                )

        # Loop over top view domain
        for i in range(0, h):
            # Read all pixels pos of this row
            points2d_z0_3xN = np.array(
                [np.linspace(0, w - 1, num=w), i * np.ones(w), np.ones(w)]
            )
            # from pixels to points 3d
            temp = utils.inv(self.params.S).dot(points2d_z0_3xN)
            # hom. coords.
            points3d_z0_4xN = np.vstack((temp[0, :], temp[1, :], np.zeros(w), temp[2, :]))

            # Loop over cameras
            for _idx, (cam_name, cam) in enumerate(cams.items()):
                # Convert into camera coordinate system for all M cameras
                t_ref_to_cam_4x4, static = self.scene.get_transform(
                    self.coordinate_system, cam_name, frame_num
                )
                points3d_cam_4xN = t_ref_to_cam_4x4.dot(points3d_z0_4xN)

                if need_to_recompute_weights[cam_name]:
                    self.images[cam_name]["weights"][i, :, 0] = 1.0 / np.linalg.norm(
                        points3d_cam_4xN, axis=0
                    )
                    self.images[cam_name]["weights"][i, :, 1] = self.images[cam_name][
                        "weights"
                    ][i, :, 0]
                    self.images[cam_name]["weights"][i, :, 2] = self.images[cam_name][
                        "weights"
                    ][i, :, 0]

                if need_to_recompute_maps[cam_name]:
                    if cam is not None:
                        # Project into image
                        points2d_dist_3xN, idx_valid = cam.project_points3d(
                            points3d_cam_4xN, remove_outside=True
                        )

                        # Assign into map
                        self.images[cam_name]["mapX"][i, :] = points2d_dist_3xN[0, :]
                        self.images[cam_name]["mapY"][i, :] = points2d_dist_3xN[1, :]

        # Compute accumulated weights if more than 1 camera
        if need_to_recompute_weights_acc:
            self.images["weights_acc"] = np.zeros((h, w, 3), dtype=np.float32)
            for _idx, (cam_name, _cam) in enumerate(cams.items()):
                self.images["weights_acc"] = cv.add(
                    self.images[cam_name]["weights"], self.images["weights_acc"]
                )

    def draw(
        self,
        frame_num: int | None = None,
        uid: int | str | None = None,
        _draw_trajectory: bool = True,
    ) -> cv.Mat:
        """
        Define the main drawing function for the TopView drawer.

        It explores the provided params to select different options.

        :param frameNum: frame number
        :param uid: unique identifier of object to be drawn (if None, all are drawn)
        :param _drawTrajectory: boolean to draw the trajectory of objects
        :param _params: additional parameters
        :return: the TopView image
        """
        # Base top view is used from previous iteration
        if self.params.draw_only_current_image:
            # Needs to be here
            self.topView = np.zeros(
                (self.params.topview_size[1], self.params.topview_size[0], 3), np.uint8
            )
            self.topView.fill(self.params.background_color)

            # Draw BEW
        self.draw_bevs(frame_num)

        # Base grids
        self.draw_topview_base()

        # Draw objects
        topview_with_objects = copy.deepcopy(self.topView)
        self.draw_objects_at_frame(topview_with_objects, uid, frame_num, _draw_trajectory)

        # Draw frame info
        self.draw_info(topview_with_objects, frame_num)

        return topview_with_objects

    def draw_info(self, topview: cv.Mat, frame_num: int | None = None):
        h = topview.shape[0]
        w = topview.shape[1]
        w_margin = 250
        h_margin = 140
        h_step = 20
        font_size = 0.8
        cv.putText(
            topview,
            "Img. Size(px): " + str(w) + " x " + str(h),
            (w - w_margin, h - h_margin),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )
        if frame_num is None:
            frame_num = -1
        cv.putText(
            topview,
            "Frame: " + str(frame_num),
            (w - w_margin, h - h_margin + h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )
        cv.putText(
            topview,
            "CS: " + str(self.coordinate_system),
            (w - w_margin, h - h_margin + 2 * h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )

        cv.putText(
            topview,
            "RangeX (m): ("
            + str(self.params.range_x[0])
            + ", "
            + str(self.params.range_x[1])
            + ")",
            (w - w_margin, h - h_margin + 3 * h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )
        cv.putText(
            topview,
            "RangeY (m): ("
            + str(self.params.range_y[0])
            + ", "
            + str(self.params.range_y[1])
            + ")",
            (w - w_margin, h - h_margin + 4 * h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )

        cv.putText(
            topview,
            "OffsetX (px): ("
            + str(self.params.offset_x)
            + ", "
            + str(self.params.offset_x)
            + ")",
            (w - w_margin, h - h_margin + 5 * h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )
        cv.putText(
            topview,
            "OffsetY (px): ("
            + str(self.params.offset_y)
            + ", "
            + str(self.params.offset_y)
            + ")",
            (w - w_margin, h - h_margin + 6 * h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )

    def draw_topview_base(self):
        # self.topView.fill(self.params.backgroundColor)

        if self.params.draw_grid:
            # Grid x (1/2)
            for x in np.arange(
                self.params.range_x[0],
                self.params.range_x[1] + self.params.step_x,
                self.params.step_x,
            ):
                x_round = round(x)
                pt_img1 = self.point2pixel((x_round, self.params.range_y[0]))
                pt_img2 = self.point2pixel((x_round, self.params.range_y[1]))
                cv.line(
                    self.topView,
                    pt_img1,
                    pt_img2,
                    (127, 127, 127),
                    self.params.grid_lines_thickness,
                )

            # Grid y (1/2)
            for y in np.arange(
                self.params.range_y[0],
                self.params.range_y[1] + self.params.step_y,
                self.params.step_y,
            ):
                y_round = round(y)
                pt_img1 = self.point2pixel((self.params.range_x[0], y_round))
                pt_img2 = self.point2pixel((self.params.range_x[1], y_round))
                cv.line(
                    self.topView,
                    pt_img1,
                    pt_img2,
                    (127, 127, 127),
                    self.params.grid_lines_thickness,
                )

            # Grid x (2/2)
            for x in np.arange(
                self.params.range_x[0],
                self.params.range_x[1] + self.params.step_x,
                self.params.step_x,
            ):
                x_round = round(x)
                pt_img1 = self.point2pixel((x_round, self.params.range_y[0]))
                cv.putText(
                    self.topView,
                    str(round(x)) + " m",
                    (pt_img1[0] + 5, 15),
                    cv.FONT_HERSHEY_PLAIN,
                    0.6,
                    self.params.grid_text_color,
                    1,
                    cv.LINE_AA,
                )
            # Grid y (2/2)
            for y in np.arange(
                self.params.range_y[0],
                self.params.range_y[1] + self.params.step_y,
                self.params.step_y,
            ):
                y_round = round(y)
                pt_img1 = self.point2pixel((self.params.range_x[0], y_round))
                cv.putText(
                    self.topView,
                    str(round(y)) + " m",
                    (5, pt_img1[1] - 5),
                    cv.FONT_HERSHEY_PLAIN,
                    0.6,
                    self.params.grid_text_color,
                    1,
                    cv.LINE_AA,
                )

        # World origin
        cv.circle(self.topView, self.point2pixel((0.0, 0.0)), 4, (255, 255, 255), -1)
        cv.line(
            self.topView,
            self.point2pixel((0.0, 0.0)),
            self.point2pixel((5.0, 0.0)),
            (0, 0, 255),
            2,
        )
        cv.line(
            self.topView,
            self.point2pixel((0.0, 0.0)),
            self.point2pixel((0.0, 5.0)),
            (0, 255, 0),
            2,
        )

        cv.putText(
            self.topView,
            "X",
            self.point2pixel((5.0, -0.5)),
            cv.FONT_HERSHEY_PLAIN,
            1.0,
            (0, 0, 255),
            1,
            cv.LINE_AA,
        )
        cv.putText(
            self.topView,
            "Y",
            self.point2pixel((-1.0, 5.0)),
            cv.FONT_HERSHEY_PLAIN,
            1.0,
            (0, 255, 0),
            1,
            cv.LINE_AA,
        )

    def draw_points3d(self, _img: cv.Mat, points3d_4xN: npt.NDArray, _color: tuple):
        rows, cols = points3d_4xN.shape
        for i in range(0, cols):
            # thus ignoring z component
            pt = self.point2pixel((points3d_4xN[0, i], points3d_4xN[1, i]))
            cv.circle(_img, pt, 2, _color, -1)

    def draw_cuboid_topview(
        self,
        _img: cv.Mat,
        _cuboid: list,
        _class: str,
        _color: tuple[int, int, int],
        _thick: int,
        _id: int | str = "",
    ):
        if not isinstance(_cuboid, list):
            raise TypeError("Argument '_cuboid' must be of type 'list'")

        # (X, Y, Z, RX, RY, RZ, SX, SY, SZ)
        if len(_cuboid) != 9 or len(_cuboid) != 10:
            raise ValueError("Invalid argument '_cuboid' size")

        points_4x8 = utils.generate_cuboid_points_ref_4x8(_cuboid)
        # Project into topview
        points_4x8[2, :] = 0

        pairs = (
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
        )
        for pair in pairs:
            p_a = (points_4x8[0, pair[0]], points_4x8[1, pair[0]])
            p_b = (points_4x8[0, pair[1]], points_4x8[1, pair[1]])
            cv.line(_img, self.point2pixel(p_a), self.point2pixel(p_b), _color, _thick)

    def draw_mesh_topview(self, img: cv.Mat, mesh: dict, points3d_4xN: npt.NDArray):
        mesh_point_dict = mesh["point3d"]
        mesh_line_refs = mesh["line_reference"]
        mesh_area_refs = mesh["area_reference"]

        # Convert points into pixels
        points2d = []
        rows, cols = points3d_4xN.shape
        for i in range(0, cols):
            pt = self.point2pixel(
                (points3d_4xN[0, i], points3d_4xN[1, i])
            )  # thus ignoring z component
            points2d.append(pt)

        # Draw areas first
        for _area_id, area in mesh_area_refs.items():
            line_refs = area["val"]
            points_area = []
            # Loop over lines and create a list of points
            for line_ref in line_refs:
                line = mesh_line_refs[str(line_ref)]

                point_refs = line["val"]
                point_a_ref = point_refs[0]
                point_b_ref = point_refs[1]
                point_a = points2d[list(mesh_point_dict).index(str(point_a_ref))]
                point_b = points2d[list(mesh_point_dict).index(str(point_b_ref))]

                points_area.append(point_a)
                points_area.append(point_b)

            cv.fillConvexPoly(img, np.array(points_area), (0, 255, 0))

        # Draw lines
        for _line_id, line in mesh_line_refs.items():
            point_refs = line["val"]
            point_a_ref = point_refs[0]
            point_b_ref = point_refs[1]

            point_a = points2d[list(mesh_point_dict).index(str(point_a_ref))]
            point_b = points2d[list(mesh_point_dict).index(str(point_b_ref))]

            cv.line(img, point_a, point_b, (255, 0, 0), 2)

        # Draw points
        for pt in points2d:
            cv.circle(img, pt, 5, (0, 0, 0), -1)
            cv.circle(img, pt, 3, (0, 0, 255), -1)

    def draw_object_data(
        self,
        object_: dict,
        object_class: str,
        _img: cv.Mat,
        uid: int | str,
        _frame_num: int | None,
        _draw_trajectory: bool,
    ):  # pylint: disable=too-many-locals
        # Reads cuboids
        if "object_data" not in object_:
            return

        for object_data_key in object_["object_data"].keys():
            for object_data_item in object_["object_data"][object_data_key]:
                ########################################
                # CUBOIDS
                ########################################
                if object_data_key == "cuboid":
                    cuboid_vals = object_data_item["val"]
                    cuboid_name = object_data_item["name"]
                    if "coordinate_system" in object_data_item:
                        cs_data = object_data_item["coordinate_system"]
                    else:
                        warnings.warn(
                            "WARNING: The cuboids of this VCD don't have a "
                            "coordinate_system.",
                            Warning,
                            2,
                        )
                        # For simplicity, let's assume they are already expressed in
                        # the target cs
                        cs_data = self.coordinate_system

                    # Convert from data coordinate system (e.g. "CAM_LEFT")
                    #  into reference coordinate system (e.g. "VEHICLE-ISO8855")
                    cuboid_vals_transformed = cuboid_vals
                    if cs_data != self.coordinate_system:
                        cuboid_vals_transformed = self.scene.transform_cuboid(
                            cuboid_vals, cs_data, self.coordinate_system, _frame_num
                        )
                    # Draw
                    self.draw_cuboid_topview(
                        _img,
                        cuboid_vals_transformed,
                        object_class,
                        self.params.color_map[object_class],
                        2,
                        uid,
                    )

                    if _draw_trajectory and _frame_num is not None:
                        fis = self.__get_object_data_fis(uid, cuboid_name)

                        for fi in fis:
                            prev_center: dict = {}
                            for f in range(fi["frame_start"], _frame_num + 1):
                                object_data_item = self.scene.vcd.get_object_data(
                                    uid, cuboid_name, f
                                )

                                cuboid_vals = object_data_item["val"]
                                cuboid_vals_transformed = cuboid_vals
                                if cs_data != self.coordinate_system:
                                    src_cs = cs_data
                                    dst_cs = self.coordinate_system
                                    (
                                        transform_src_dst,
                                        _,
                                    ) = self.scene.get_transform(src_cs, dst_cs, f)
                                    cuboid_vals_transformed = utils.transform_cuboid(
                                        cuboid_vals, transform_src_dst
                                    )

                                name = object_data_item["name"]

                                center = (
                                    cuboid_vals_transformed[0],
                                    cuboid_vals_transformed[1],
                                )
                                center_pix = self.point2pixel(center)

                                # this is a dict to allow multiple trajectories
                                # (e.g. several cuboids per object)
                                if prev_center.get(name) is not None:
                                    cv.line(
                                        _img,
                                        prev_center[name],
                                        center_pix,
                                        (0, 0, 0),
                                        1,
                                        cv.LINE_AA,
                                    )

                                cv.circle(
                                    _img,
                                    center_pix,
                                    2,
                                    self.params.color_map[object_class],
                                    -1,
                                )

                                prev_center[name] = center_pix
                ########################################
                # mat - points3d_4xN
                ########################################
                elif object_data_key == "mat":
                    width = object_data_item["width"]
                    height = object_data_item["height"]

                    if height == 4:
                        # These are points 4xN
                        color = self.params.color_map[object_class]
                        points3d_4xN = np.array(object_data_item["val"]).reshape(
                            height, width
                        )
                        points_cs = object_data_item["coordinate_system"]

                        # First convert from the src coordinate system into the camera
                        # coordinate system
                        points3d_4xN_transformed = self.scene.transform_points3d_4xN(
                            points3d_4xN, points_cs, self.coordinate_system
                        )

                        if "attributes" in object_data_item:
                            for attr_type, attr_list in object_data_item[
                                "attributes"
                            ].items():
                                if attr_type == "vec":
                                    for attr in attr_list:
                                        if attr["name"] == "color":
                                            color = attr["val"]
                        if points3d_4xN_transformed is not None:
                            self.draw_points3d(_img, points3d_4xN_transformed, color)
                ########################################
                # point3d - Single point in 3D
                ########################################
                elif object_data_key == "point3d":
                    color = self.params.color_map[object_class]
                    point_name = object_data_item["name"]

                    if "coordinate_system" in object_data_item:
                        cs_data = object_data_item["coordinate_system"]
                    else:
                        warnings.warn(
                            "WARNING: The point3d of this VCD don't have a "
                            "coordinate_system.",
                            Warning,
                            2,
                        )
                        # For simplicity, let's assume they are already expressed in
                        # the target cs
                        cs_data = self.coordinate_system

                    x = object_data_item["val"][0]
                    y = object_data_item["val"][1]
                    z = object_data_item["val"][2]
                    points3d_4xN = np.array([x, y, z, 1]).reshape(4, 1)
                    points_cs = object_data_item["coordinate_system"]

                    # First convert from the src coordinate system into the camera
                    # coordinate system
                    points3d_4xN_transformed = self.scene.transform_points3d_4xN(
                        points3d_4xN, points_cs, self.coordinate_system
                    )

                    if "attributes" in object_data_item:
                        for attr_type, attr_list in object_data_item[
                            "attributes"
                        ].items():
                            if attr_type == "vec":
                                for attr in attr_list:
                                    if attr["name"] == "color":
                                        color = attr["val"]

                    if points3d_4xN_transformed is not None:
                        self.draw_points3d(_img, points3d_4xN_transformed, color)

                    if _draw_trajectory and _frame_num is not None:
                        fis = self.__get_object_data_fis(uid, point_name)

                        for fi in fis:
                            prev_center = {}
                            for f in range(fi["frame_start"], _frame_num + 1):
                                object_data_item = self.scene.vcd.get_object_data(
                                    uid, point_name, f
                                )

                                x = object_data_item["val"][0]
                                y = object_data_item["val"][1]
                                z = object_data_item["val"][2]
                                points3d_4xN = np.array([x, y, z, 1]).reshape(4, 1)
                                points3d_4xN_transformed = points3d_4xN

                                if cs_data != self.coordinate_system:
                                    src_cs = cs_data
                                    dst_cs = self.coordinate_system
                                    (
                                        transform_src_dst,
                                        _,
                                    ) = self.scene.get_transform(src_cs, dst_cs, f)
                                    points3d_4xN_transformed = (
                                        self.scene.transform_points3d_4xN(
                                            points3d_4xN,
                                            points_cs,
                                            self.coordinate_system,
                                        )
                                    )

                                name = object_data_item["name"]

                                if points3d_4xN_transformed is not None:
                                    center = (
                                        points3d_4xN_transformed[0, 0],
                                        points3d_4xN_transformed[1, 0],
                                    )
                                    center_pix = self.point2pixel(center)

                                    # this is a dict to allow multiple trajectories
                                    # (e.g. several cuboids per object)
                                    if prev_center.get(name) is not None:
                                        cv.line(
                                            _img,
                                            prev_center[name],
                                            center_pix,
                                            (0, 0, 0),
                                            1,
                                            cv.LINE_AA,
                                        )

                                    cv.circle(
                                        _img,
                                        center_pix,
                                        2,
                                        self.params.color_map[object_class],
                                        -1,
                                    )

                                    prev_center[name] = center_pix
                ########################################
                # mesh - Point-line-area structure
                ########################################
                elif object_data_key == "mesh":
                    if "coordinate_system" in object_data_item:
                        cs_data = object_data_item["coordinate_system"]
                    else:
                        warnings.warn(
                            "WARNING: The mesh of this VCD don't have a coordinate_system.",
                            Warning,
                            2,
                        )
                        # For simplicity, let's assume they are already expressed in
                        # the target cs
                        cs_data = self.coordinate_system

                    # Let's convert mesh points into 4xN array
                    points = object_data_item["point3d"]
                    points3d_4xN = np.ones((4, len(points)))
                    for point_count, (_point_id, point) in enumerate(points.items()):
                        points3d_4xN[0, point_count] = point["val"][0]
                        points3d_4xN[1, point_count] = point["val"][1]
                        points3d_4xN[2, point_count] = point["val"][2]

                    points3d_4xN_transformed = self.scene.transform_points3d_4xN(
                        points3d_4xN, cs_data, self.coordinate_system
                    )

                    if points3d_4xN_transformed is not None:
                        # Let's send the data and the possible transform info to the
                        # drawing function
                        self.draw_mesh_topview(
                            img=_img,
                            mesh=object_data_item,
                            points3d_4xN=points3d_4xN_transformed,
                        )

    def draw_objects_at_frame(
        self,
        top_view: cv.Mat,
        uid: int | str | None,
        _frame_num: int | None,
        _draw_trajectory: bool,
    ):
        img = top_view

        # Select static or dynamic objects depending on the provided input _frameNum
        objects = {}
        if _frame_num is not None:
            vcd_frame = self.scene.vcd.get_frame(_frame_num)
            if "objects" in vcd_frame:
                objects = vcd_frame["objects"]
        else:
            if self.scene.vcd.has_objects():
                objects = self.scene.vcd.get_objects()

        # Explore objects at this VCD frame
        for object_id, object_ in objects.items():
            if uid is not None:
                if core.UID(object_id).as_str() != core.UID(uid).as_str():
                    continue

            object_element = self.scene.vcd.get_object(object_id)
            if object_element is not None:
                # Get object static info
                object_class = object_element["type"]

            # Ignore classes
            if object_class in self.params.ignore_classes:
                continue

            # Colors
            if self.params.color_map.get(object_class) is None:
                # Let's create a new entry for this class
                self.params.color_map[object_class] = (
                    randbelow(255),
                    randbelow(255),
                    randbelow(255),
                )

            # Check if the object has specific info at this frame, or if we need to consult the
            # static object info
            if len(object_) == 0:
                # So this is a pointer to a static object
                static_object = self.scene.vcd.get_root()["objects"][object_id]
                self.draw_object_data(
                    static_object,
                    object_class,
                    img,
                    object_id,
                    _frame_num,
                    _draw_trajectory,
                )
            else:
                # Let's use the dynamic info of this object
                self.draw_object_data(
                    object_, object_class, img, object_id, _frame_num, _draw_trajectory
                )

    def draw_bev(self, cam_name: str) -> npt.NDArray[np.float32]:
        img = self.images[cam_name]["img"]

        map_x = self.images[cam_name]["mapX"]
        map_y = self.images[cam_name]["mapY"]
        bev = cv.remap(
            img,
            map_x,
            map_y,
            interpolation=cv.INTER_LINEAR,
            borderMode=cv.BORDER_CONSTANT,
        )

        bev32 = np.array(bev, np.float32)
        if "weights" in self.images[cam_name]:
            cv.multiply(self.images[cam_name]["weights"], bev32, bev32)

        # cv.imshow('bev' + cam_name, bev)
        # cv.waitKey(1)

        # bev832 = np.uint8(bev32)
        # cv.imshow('bev8' + cam_name, bev832)
        # cv.waitKey(1)

        return bev32

    def draw_bevs(self, _frame_num: int | None = None):
        """
        Draw BEVs into the topview.

        :param _frameNum:
        :return:
        """
        num_cams = len(self.images)
        if num_cams == 0:
            return

        h = self.params.topview_size[1]
        w = self.params.topview_size[0]
        # Prepare image with drawing for this call
        # black background
        acc32: npt.NDArray[np.float32] = np.zeros((h, w, 3), dtype=np.float32)

        for cam_name in self.images:
            if self.scene.get_camera(cam_name, _frame_num) is not None:
                temp32 = self.draw_bev(cam_name=cam_name)
                # mask = np.zeros((h, w), dtype=np.uint8)
                # mask[temp32 > 0] = 255
                # mask = (temp32 > 0)
                if num_cams > 1:
                    acc32 = cv.add(temp32, acc32)
        if num_cams > 1:
            acc32 /= self.images["weights_acc"]
        else:
            acc32 = temp32
        acc8 = acc32.astype(dtype=np.uint8)
        # cv.imshow('acc', acc8)
        # cv.waitKey(1)

        # Copy into topView only new pixels
        nonzero = acc8 > 0
        self.topView[nonzero] = acc8[nonzero]

    def size2pixel(self, _size: tuple[int, int]) -> tuple[int, int]:
        return (
            int(round(_size[0] * abs(self.params.scale_x))),
            int(round(_size[1] * abs(self.params.scale_y))),
        )

    def point2pixel(self, _point: tuple[int, int]) -> tuple[int, int]:
        pixel = (
            int(round(_point[0] * self.params.scale_x + self.params.offset_x)),
            int(round(_point[1] * self.params.scale_y + self.params.offset_y)),
        )
        return pixel

    def __get_object_data_fis(self, uid: int | str, name: str) -> list[dict]:
        fis_object = self.scene.vcd.get_object_data_frame_intervals(uid, name)
        if fis_object is None:
            fis: list[dict] = [{}]
        elif fis_object.empty():
            # So this object is static, let's project its cuboid into
            # the current transform
            fis = self.scene.vcd.get_frame_intervals().get_dict()
        else:
            fis = fis_object.get_dict()
        return fis


class Image:
    """
    Draw 2D elements in the Image.

    Devised to draw bboxes, it can also project 3D entities (e.g. cuboids) using the
    calibration parameters
    """

    class Params:
        def __init__(
            self,
            _draw_trajectory: bool = False,
            _color_map: dict | None = None,
            _ignore_classes: dict | None = None,
            _draw_types: set[str] | None = None,
            _barrel: bool | None = None,
            _thickness: int | None = None,
        ):
            if _color_map is None:
                self.color_map = {}
            else:
                if not isinstance(_color_map, dict):
                    raise TypeError("Argument '_color_map' must be of type 'dict'")
                self.color_map = _color_map
            self.draw_trajectory = _draw_trajectory
            if _ignore_classes is None:
                self.ignore_classes = {}
            else:
                self.ignore_classes = _ignore_classes

            if _draw_types is not None:
                self.draw_types = _draw_types
            else:
                self.draw_types = {"bbox"}

            if _barrel is not None:
                self.draw_barrel = _barrel
            else:
                self.draw_barrel = False

            if _thickness is not None:
                self.thickness = _thickness
            else:
                self.thickness = 1

    def __init__(self, scene: scl.Scene, camera_coordinate_system: str | None = None):
        if not isinstance(scene, scl.Scene):
            raise TypeError("Argument 'scene' must be of type 'vcd.scl.Scene'")
        self.scene = scene
        if camera_coordinate_system is not None:
            if not scene.vcd.has_coordinate_system(camera_coordinate_system):
                raise ValueError(
                    "The provided scene does not have the specified coordinate system"
                )
            self.camera_coordinate_system = camera_coordinate_system
            self.camera = self.scene.get_camera(
                self.camera_coordinate_system, compute_remaps=False
            )

        self.params = Image.Params()

    def reset_image(self) -> cv.Mat:
        img = np.array([], np.int8)
        if self.camera is not None:
            img = np.zeros((self.camera.height, self.camera.width, 3), np.uint8)
            img.fill(255)
        return img

    def draw_points3d(
        self, _img: cv.Mat, points3d_4xN: npt.NDArray, _color: tuple[int, int, int]
    ):
        if self.camera is None:
            return
        # this function may return LESS than N points IF 3D points are BEHIND the camera
        points2d_3xN, idx_valid = self.camera.project_points3d(
            points3d_4xN, remove_outside=True
        )
        if points2d_3xN is None:
            return
        rows, cols = points2d_3xN.shape
        img_rows, img_cols, img_channels = _img.shape
        for i in range(0, cols):
            if idx_valid[i]:
                if np.isnan(points2d_3xN[0, i]) or np.isnan(points2d_3xN[1, i]):
                    continue
                center = (
                    utils.round(points2d_3xN[0, i]),
                    utils.round(points2d_3xN[1, i]),
                )
                if not utils.is_inside_image(img_cols, img_rows, center[0], center[1]):
                    continue
                cv.circle(_img, (int(center[0]), int(center[1])), 2, _color, -1)

    def draw_cuboid(
        self,
        _img: cv.Mat,
        _cuboid_vals: list[float],
        _class: str,
        _color: tuple[int, int, int],
        _thickness: int = 1,
    ):
        if not isinstance(_cuboid_vals, list):
            raise TypeError("Argument '_cuboid' must be of type 'list'")

        # (X, Y, Z, RX, RY, RZ, SX, SY, SZ)
        if len(_cuboid_vals) != 9:
            raise ValueError("Invalid argument '_cuboid' size")
        # TODO cuboids with quaternions

        # Generate object coordinates
        points3d_4x8 = utils.generate_cuboid_points_ref_4x8(_cuboid_vals)

        # this function may return LESS than 8 points IF 3D points are BEHIND the camera
        if self.camera is None:
            return
        points2d_4x8, idx_valid = self.camera.project_points3d(points3d_4x8, True)

        if points2d_4x8 is None:
            return
        img_rows, img_cols, img_channels = _img.shape

        pairs = (
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
        )
        for _count, pair in enumerate(pairs):
            if idx_valid[pair[0]] and idx_valid[pair[1]]:
                # if pair[0] >= num_points_projected or pair[1] >= num_points_projected:
                #    continue
                p_a = (
                    utils.round(points2d_4x8[0, pair[0]]),
                    utils.round(points2d_4x8[1, pair[0]]),
                )
                p_b = (
                    utils.round(points2d_4x8[0, pair[1]]),
                    utils.round(points2d_4x8[1, pair[1]]),
                )

                if not utils.is_inside_image(
                    img_cols, img_rows, p_a[0], p_b[1]
                ) or not utils.is_inside_image(img_cols, img_rows, p_b[0], p_b[1]):
                    continue

                cv.line(_img, p_a, p_b, _color, _thickness)

    def draw_bbox(
        self,
        _img: cv.Mat,
        _bbox: tuple[int, int, int, int],
        _object_class: str,
        _color: tuple[int, int, int],
        add_border: bool = False,
    ):
        pt1 = (int(round(_bbox[0] - _bbox[2] / 2)), int(round(_bbox[1] - _bbox[3] / 2)))
        pt2 = (int(round(_bbox[0] + _bbox[2] / 2)), int(round(_bbox[1] + _bbox[3] / 2)))

        pta = (pt1[0], pt1[1] - 15)
        ptb = (pt2[0], pt1[1])
        img_rows, img_cols, img_channels = _img.shape

        if add_border:
            cv.rectangle(_img, pta, ptb, _color, 2)
            cv.rectangle(_img, pta, ptb, _color, -1)

        cv.putText(
            _img,
            _object_class,
            (pta[0], pta[1] + 10),
            cv.FONT_HERSHEY_PLAIN,
            0.6,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )

        if utils.is_inside_image(
            img_cols, img_rows, pt1[0], pt1[1]
        ) and utils.is_inside_image(img_cols, img_rows, pt2[0], pt2[1]):
            cv.rectangle(_img, pt1, pt2, _color, 2)

    def draw_line(
        self,
        _img: cv.Mat,
        _pt1: tuple[int, int],
        _pt2: tuple[int, int],
        _color: tuple[int, int, int],
        _thickness: int = 1,
    ):
        cv.line(_img, _pt1, _pt2, _color, _thickness)

    def draw_trajectory(
        self, _img: cv.Mat, _object_id: str, _frame_num: int, _params: Image.Params | None
    ):
        # object_class = self.scene.vcd.get_object(_object_id)["type"]
        fis = (
            self.scene.vcd.get_element_frame_intervals(
                core.ElementType.object, _object_id
            )
        ).get_dict()

        for fi in fis:
            prev_center: dict = {}
            for f in range(fi["frame_start"], _frame_num + 1):
                vcd_other_frame = self.scene.vcd.get_frame(f)
                if "objects" in vcd_other_frame:
                    for object_id_this, obj in vcd_other_frame["objects"].items():
                        if object_id_this is not _object_id:
                            continue

                        # Get value at this frame
                        if "object_data" in obj:
                            for object_data_key in obj["object_data"].keys():
                                for object_data_item in obj["object_data"][
                                    object_data_key
                                ]:
                                    if object_data_key == "bbox":
                                        bbox = object_data_item["val"]
                                        name = object_data_item["name"]

                                        center = (
                                            int(round(bbox[0])),
                                            int(round(bbox[1])),
                                        )

                                        # this is a dict to allow multiple trajectories
                                        # (e.g. several bbox per object)
                                        if prev_center.get(name) is not None:
                                            cv.line(
                                                _img,
                                                prev_center[name],
                                                center,
                                                (0, 0, 0),
                                                1,
                                                cv.LINE_AA,
                                            )

                                        # if _param is not None
                                        # cv.circle(_img, center, 2,
                                        #          _params.color_map[object_class], -1)

                                        prev_center[name] = center

    def draw_barrel_distortion_grid(
        self,
        img: cv.Mat,
        color: tuple[int, int, int],
        only_outer: bool = True,
        extended: bool = False,
    ):
        if self.camera is None:
            return
        if not isinstance(self.camera, (scl.CameraPinhole, scl.CameraFisheye)):
            return

        # Define grid in undistorted space and then apply distortPoint
        height, width = img.shape[:2]

        # Debug, see where the points fall if undistorted
        num_steps = 50
        x_start = 0
        x_end = width
        y_start = 0
        y_end = height

        if extended:
            factor = 1
            x_start = int(-factor * width)
            x_end = int(width + factor * width)
            y_start = int(-factor * height)
            y_end = int(height + factor * height)

        step_x = (x_end - x_start) / num_steps
        step_y = (y_end - y_start) / num_steps

        # Lines in X
        for y in np.linspace(y_start, y_end, num_steps + 1):
            for x in np.linspace(x_start, x_end, num_steps + 1):
                if only_outer:
                    if 0 < y < height:
                        continue

                p_a = (x, y, 1)  # (i * stepX, j * stepY)
                p_b = (x + step_x, y, 1)  # ((i+1) * stepX, j * stepY)
                if not extended:
                    if x + step_x > width:
                        continue
                p_da = self.camera.distort_points2d(np.array(p_a).reshape(3, 1))
                p_db = self.camera.distort_points2d(np.array(p_b).reshape(3, 1))

                # cv2.circle(imgDist, pointDistA, 3, bgr, -1)
                if (
                    0 <= p_da[0, 0] < width
                    and 0 <= p_da[1, 0] < height
                    and 0 <= p_db[0, 0] < width
                    and 0 <= p_db[1, 0] < height
                ):
                    color_to_use = color
                    if y in (0, height):
                        color_to_use = (255, 0, 0)
                    cv.line(
                        img,
                        (utils.round(p_da[0, 0]), utils.round(p_da[1, 0])),
                        (utils.round(p_db[0, 0]), utils.round(p_db[1, 0])),
                        color_to_use,
                        2,
                    )

        # Lines in Y
        for y in np.linspace(y_start, y_end, num_steps + 1):
            for x in np.linspace(x_start, x_end, num_steps + 1):
                if only_outer:
                    if 0 < x < width:
                        continue
                p_a = (x, y, 1)  # (i * stepX, j * stepY)
                p_b = (x, y + step_y, 1)  # (i * stepX, (j + 1) * stepY)
                if not extended:
                    if y + step_y > height:
                        continue
                p_da = self.camera.distort_points2d(np.array(p_a).reshape(3, 1))
                p_db = self.camera.distort_points2d(np.array(p_b).reshape(3, 1))

                # cv2.circle(imgDist, pointDistA, 3, bgr, -1)
                if (
                    0 <= p_da[0, 0] < width
                    and 0 <= p_da[1, 0] < height
                    and 0 <= p_db[0, 0] < width
                    and 0 <= p_db[1, 0] < height
                ):
                    color_to_use = color
                    if x in (0, width):
                        color_to_use = (255, 0, 0)
                    cv.line(
                        img,
                        (utils.round(p_da[0, 0]), utils.round(p_da[1, 0])),
                        (utils.round(p_db[0, 0]), utils.round(p_db[1, 0])),
                        color_to_use,
                        2,
                    )

        # r_limit
        if isinstance(self.camera, scl.CameraPinhole) and self.camera.r_limit is not None:
            # r_limit is a radius limit in calibrated coordinates
            # It might be possible to draw it by sampling points of a circle r in the
            # undistorted domain and apply distortPoints to them
            num_points = 100
            points2d_und_3xN = np.ones((3, num_points), dtype=np.float64)
            count = 0
            for angle in np.linspace(0, 2 * np.pi, num_points, endpoint=False):
                x = np.sin(angle) * self.camera.r_limit
                y = np.cos(angle) * self.camera.r_limit
                points2d_und_3xN[0, count] = x
                points2d_und_3xN[1, count] = y
                count += 1
            points2d_und_3xN = self.camera.K_3x3.dot(points2d_und_3xN)
            points2d_dist_3xN = self.camera.distort_points2d(points2d_und_3xN)
            point2d_prev = None
            for point2d in points2d_dist_3xN.transpose():
                x = utils.round(point2d[0])
                y = utils.round(point2d[1])
                if point2d_prev is not None:
                    cv.line(img, point2d_prev, (x, y), (0, 255, 255), 3)
                point2d_prev = (x, y)

    def draw_cs(
        self, _img: cv.Mat, cs_name: str, length: float = 1.0, thickness: int = 1
    ):
        """
        Draw a coordinate system.

        This function draws a coordinate system, as 3 lines of 1 meter length (Red, Green,
        Blue) corresponding to the X-axis, Y-axis, and Z-axis of the coordinate system.
        """
        if not self.scene.vcd.has_coordinate_system(cs_name):
            warnings.warn(
                "WARNING: Trying to draw coordinate system"
                + cs_name
                + " not existing in VCD.",
                Warning,
                2,
            )

        x_axis_as_points3d_4x2 = np.array(
            [[0.0, length], [0.0, 0.0], [0.0, 0.0], [1.0, 1.0]]
        )
        y_axis_as_points3d_4x2 = np.array(
            [[0.0, 0.0], [0.0, length], [0.0, 0.0], [1.0, 1.0]]
        )
        z_axis_as_points3d_4x2 = np.array(
            [[0.0, 0.0], [0.0, 0.0], [0.0, length], [1.0, 1.0]]
        )

        x_axis, _ = self.scene.project_points3d_4xN(
            x_axis_as_points3d_4x2, cs_name, cs_cam=self.camera_coordinate_system
        )
        y_axis, _ = self.scene.project_points3d_4xN(
            y_axis_as_points3d_4x2, cs_name, cs_cam=self.camera_coordinate_system
        )
        z_axis, _ = self.scene.project_points3d_4xN(
            z_axis_as_points3d_4x2, cs_name, cs_cam=self.camera_coordinate_system
        )

        self.draw_line(
            _img,
            (int(x_axis[0, 0]), int(x_axis[1, 0])),
            (int(x_axis[0, 1]), int(x_axis[1, 1])),
            (0, 0, 255),
            thickness,
        )
        self.draw_line(
            _img,
            (int(y_axis[0, 0]), int(y_axis[1, 0])),
            (int(y_axis[0, 1]), int(y_axis[1, 1])),
            (0, 255, 0),
            thickness,
        )
        self.draw_line(
            _img,
            (int(z_axis[0, 0]), int(z_axis[1, 0])),
            (int(z_axis[0, 1]), int(z_axis[1, 1])),
            (255, 0, 0),
            thickness,
        )

        cv.putText(
            _img,
            "X",
            (int(x_axis[0, 1]), int(x_axis[1, 1])),
            cv.FONT_HERSHEY_DUPLEX,
            0.8,
            (0, 0, 255),
            thickness,
            cv.LINE_AA,
        )
        cv.putText(
            _img,
            "Y",
            (int(y_axis[0, 1]), int(y_axis[1, 1])),
            cv.FONT_HERSHEY_DUPLEX,
            0.8,
            (0, 255, 0),
            thickness,
            cv.LINE_AA,
        )
        cv.putText(
            _img,
            "Z",
            (int(z_axis[0, 1]), int(z_axis[1, 1])),
            cv.FONT_HERSHEY_DUPLEX,
            0.8,
            (255, 0, 0),
            thickness,
            cv.LINE_AA,
        )

    def draw(
        self,
        _img: cv.Mat = None,
        _frame_num: int | None = None,
        _params: Image.Params | None = None,
        **kwargs: list[str] | dict,
    ) -> cv.Mat:
        _ = kwargs
        if _params is not None:
            if not isinstance(_params, Image.Params):
                raise TypeError(
                    "Argument '_params' must be of type 'vcd.draw.Image.Params'"
                )

            self.params = _params

        if _img is not None:
            img = _img
        else:
            img = self.reset_image()

        # Explore objects at VCD
        objects = None
        if _frame_num is not None:
            vcd_frame = self.scene.vcd.get_frame(_frame_num)
            if "objects" in vcd_frame:
                objects = vcd_frame["objects"]
        else:
            if self.scene.vcd.has_objects():
                objects = self.scene.vcd.get_objects()

        if not objects:
            return img

        for object_id, obj in objects.items():
            # Get object static info
            # name = self.scene.vcd.get_object(object_id)["name"]
            object_ = self.scene.vcd.get_object(object_id)
            if object_ is not None:
                object_class = object_["type"]
                if object_class in self.params.ignore_classes:
                    continue

                # Colors
                if self.params.color_map.get(object_class) is None:
                    # Let's create a new entry for this class
                    self.params.color_map[object_class] = (
                        randbelow(255),
                        randbelow(255),
                        randbelow(255),
                    )

            # Get current value at this frame
            if "object_data" in obj:
                object_data = obj["object_data"]
            else:
                # Check if the object has an object_data in root
                object_ = self.scene.vcd.get_object(object_id)
                if object_ is not None and "object_data" in object_:
                    object_data = object_["object_data"]

            # Loop over object data
            for object_data_key in object_data.keys():
                for object_data_item in object_data[object_data_key]:
                    ############################################
                    # bbox
                    ############################################
                    if object_data_key == "bbox":
                        bbox = object_data_item["val"]
                        bbox_name = object_data_item["name"]
                        if (
                            "coordinate_system" in object_data_item
                        ):  # Check if this bbox corresponds to this camera
                            if (
                                object_data_item["coordinate_system"]
                                != self.camera_coordinate_system
                            ):
                                continue

                        if len(object_data[object_data_key]) == 1:
                            # Only one bbox, let's write the class name
                            text = object_id + " " + object_class
                        else:
                            # If several bounding boxes, let's write the bounding box name
                            # text = "(" + object_id + "," + name +")-(" + object_class +
                            # ")-(" + bbox_name +")"
                            text = object_id + " " + bbox_name
                        self.draw_bbox(
                            img, bbox, text, self.params.color_map[object_class], True
                        )
                        if _frame_num is not None and self.params.draw_trajectory:
                            self.draw_trajectory(img, object_id, _frame_num, _params)
                    ############################################
                    # cuboid
                    ############################################
                    elif object_data_key == "cuboid":
                        # Read coordinate system of this cuboid, and transform into
                        # camera coordinate system
                        cuboid_cs = object_data_item["coordinate_system"]
                        cuboid_vals = object_data_item["val"]
                        cuboid_vals_transformed = self.scene.transform_cuboid(
                            cuboid_vals, cuboid_cs, self.camera_coordinate_system
                        )
                        self.draw_cuboid(
                            img,
                            cuboid_vals_transformed,
                            "",
                            self.params.color_map[object_class],
                            self.params.thickness,
                        )
                    ############################################
                    # mat as points3d_4xN
                    ############################################
                    elif object_data_key == "mat":
                        width = object_data_item["width"]
                        height = object_data_item["height"]

                        if height == 4:
                            # These are points 4xN
                            color = self.params.color_map[object_class]
                            points3d_4xN = np.array(object_data_item["val"]).reshape(
                                height, width
                            )
                            points_cs = object_data_item["coordinate_system"]

                            # First convert from the src coordinate system into the
                            # camera coordinate system
                            points3d_4xN_transformed = self.scene.transform_points3d_4xN(
                                points3d_4xN,
                                points_cs,
                                self.camera_coordinate_system,
                            )

                            if "attributes" in object_data_item:
                                for attr_type, attr_list in object_data_item[
                                    "attributes"
                                ].items():
                                    if attr_type == "vec":
                                        for attr in attr_list:
                                            if attr["name"] == "color":
                                                color = attr["val"]

                            if points3d_4xN_transformed is not None:
                                self.draw_points3d(img, points3d_4xN_transformed, color)

        # Draw info
        if self.camera_coordinate_system is not None:
            text = self.camera_coordinate_system
            margin = 20
            cv.putText(
                img,
                text,
                (margin, margin),
                cv.FONT_HERSHEY_DUPLEX,
                0.8,
                (0, 0, 0),
                2,
                cv.LINE_AA,
            )
            cv.putText(
                img,
                text,
                (margin, margin),
                cv.FONT_HERSHEY_DUPLEX,
                0.8,
                (255, 255, 255),
                1,
                cv.LINE_AA,
            )

        # Draw barrel
        # if self.params.draw_barrel:
        #    self.draw_barrel_distortion_grid(_img, (0, 255, 0), False, False)

        return img


class TopViewOrtho(Image):
    def __init__(
        self,
        scene: scl.Scene,
        camera_coordinate_system: str | None = None,
        step_x: float = 1.0,
        step_y: float = 1.0,
    ):
        super().__init__(scene, camera_coordinate_system=camera_coordinate_system)

        # Initialize image
        self.images: dict = {}

        # Grid config
        self.stepX = step_x  # meters
        self.stepY = step_y
        self.gridTextColor = (0, 0, 0)

    ##################################
    # Public functions
    ##################################
    def draw(
        self,
        _img: cv.Mat = None,
        _frame_num: int | None = None,
        _params: Image.Params | None = None,
        **kwargs: list[str] | dict,
    ) -> cv.Mat:
        # Create image
        if _img is not None:
            img = _img
        else:
            img = super().reset_image()

        # Compute and draw warped images
        for key, value in kwargs.items():
            if key == "add_images" and isinstance(value, dict):
                self.__add_images(value, _frame_num)

        # Draw BEW
        self.__draw_bevs(img, _frame_num)

        # Draw base grid
        self.__draw_topview_base(img)

        # Draw coordinate systems
        for key, value in kwargs.items():
            if key == "cs_names_to_draw":
                for cs_name in value:
                    self.draw_cs(img, cs_name, 2, 2)

        # Draw objects
        super().draw(img, _frame_num, _params)

        # Draw frame info
        self.__draw_info(img, _frame_num)

        return img

    ##################################
    # Internal functions
    ##################################
    def __add_images(self, imgs: dict, frame_num: int | None):
        if self.camera is not None and imgs is not None:
            h = self.camera.height  # this is the orthographic camera
            w = self.camera.width
            if not isinstance(imgs, dict):
                raise TypeError("Argument 'imgs' must be of type 'dict'")
            num_cams = len(imgs)
            cams = {}

            need_to_recompute_weights_acc = False
            need_to_recompute_maps = {}
            need_to_recompute_weights = {}

            for cam_name, img in imgs.items():
                if not self.scene.vcd.has_coordinate_system(cam_name):
                    raise ValueError(
                        "The provided scene does not have the specified coordinate system"
                    )
                # this call creates an entry inside scene
                cam = self.scene.get_camera(cam_name, frame_num, compute_remaps=False)
                if cam is not None:
                    cams[cam_name] = cam
                self.images.setdefault(cam_name, {})
                self.images[cam_name]["img"] = img
                _, static = self.scene.get_transform(
                    self.camera_coordinate_system, cam_name, frame_num
                )

                # Compute distances to this camera and add to weight map
                need_to_recompute_maps[cam_name] = False
                need_to_recompute_weights[cam_name] = False

                if (num_cams > 1 and not static) or (
                    num_cams > 1 and static and "weights" not in self.images[cam_name]
                ):
                    need_to_recompute_weights[cam_name] = True
                    need_to_recompute_weights_acc = True

                if (not static) or (static and "mapX" not in self.images[cam_name]):
                    need_to_recompute_maps[cam_name] = True

                # For each camera, compute the remaps and weights
                if need_to_recompute_maps:
                    map_x, map_y = self.scene.create_img_projection_maps(
                        cam_src_name=cam_name,
                        cam_dst_name=self.camera.name,
                        frame_num=frame_num,
                    )
                    self.images[cam_name]["mapX"] = map_x
                    self.images[cam_name]["mapY"] = map_y

                if need_to_recompute_weights[cam_name]:
                    print(cam_name + " top view weights computation...")
                    # self.images[cam_name].setdefault('weights', np.zeros((h, w, 3),
                    #  dtype=np.float32))
                    # self.images[cam_name].setdefault('weights',
                    #  (1.0/num_cams)*np.ones((h, w, 3),
                    #  dtype=np.float32))

                    # Weight according to distance to center point in image
                    # Might be good for fisheye
                    r_max_2 = (w / 2) * (w / 2) + (h / 2) * (h / 2)
                    x = map_x[:, :, 0]
                    y = map_x[:, :, 1]
                    r_2 = (x - w / 2) ** 2 + (y - h / 2) ** 2  # this is a matrix
                    weights = 1 - r_2 / r_max_2
                    temp = np.zeros((h, w, 3), dtype=np.float32)
                    temp[:, :, 0] = weights
                    temp[:, :, 1] = weights
                    temp[:, :, 2] = weights
                    self.images[cam_name].setdefault("weights", temp)

            # Compute accumulated weights if more than 1 camera
            if need_to_recompute_weights_acc:
                self.images["weights_acc"] = np.ones((h, w, 3), dtype=np.float32)
                # for idx, (cam_name, cam) in enumerate(cams.items()):
                #    self.images['weights_acc'] = cv.add(self.images[cam_name]['weights'],
                #  self.images['weights_acc'])

    def __draw_topview_base(self, _img: cv.Mat):
        if self.camera is None:
            warnings.warn(
                "__draw_topview_base: Camera is not  set",
                Warning,
                2,
            )
            return
        if not isinstance(self.camera, scl.CameraOrthographic):
            warnings.warn(
                "__draw_topview_base: Camera is not orthographic",
                Warning,
                2,
            )
            return

        # Grid x (1/2)
        for x in np.arange(self.camera.xmin, self.camera.xmax + self.stepX, self.stepX):
            x_0 = round(x)
            y_0 = self.camera.ymin
            y_1 = self.camera.ymax
            # points3d_4x2 = np.array([[x_0, y_0, 0.0, 1.0], [x_0, y_1, 0.0, 1.0]])
            points3d_4x2 = np.array([[x_0, x_0], [y_0, y_1], [0.0, 0.0], [1.0, 1.0]])
            points2d_3x2, _ = self.camera.project_points3d(points3d_4xN=points3d_4x2)
            self.draw_line(
                _img,
                (int(points2d_3x2[0, 0]), int(points2d_3x2[1, 0])),
                (int(points2d_3x2[0, 1]), int(points2d_3x2[1, 1])),
                (127, 127, 127),
            )
        # Grid y (1/2)
        for y in np.arange(self.camera.ymin, self.camera.ymax + self.stepY, self.stepY):
            y_0 = round(y)
            x_0 = self.camera.xmin
            x_1 = self.camera.xmax
            # points3d_4x2 = np.array([[x_0, y_0, 0.0, 1.0], [x_1, y_0, 0.0, 1.0]])
            points3d_4x2 = np.array([[x_0, x_1], [y_0, y_0], [0.0, 0.0], [1.0, 1.0]])
            points2d_3x2, _ = self.camera.project_points3d(points3d_4xN=points3d_4x2)
            self.draw_line(
                _img,
                (int(points2d_3x2[0, 0]), int(points2d_3x2[1, 0])),
                (int(points2d_3x2[0, 1]), int(points2d_3x2[1, 1])),
                (127, 127, 127),
            )
        # Grid x (2/2)
        for x in np.arange(self.camera.xmin, self.camera.xmax + self.stepX, self.stepX):
            x_0 = round(x)
            y_0 = self.camera.ymin
            points3d_4x1 = np.array([[x_0], [y_0], [0.0], [1.0]])
            points2d_3x1, _ = self.camera.project_points3d(points3d_4xN=points3d_4x1)
            cv.putText(
                _img,
                str(round(x_0)) + " m",
                (int(points2d_3x1[0, 0]) + 5, 15),
                cv.FONT_HERSHEY_PLAIN,
                0.6,
                self.gridTextColor,
                1,
                cv.LINE_AA,
            )
        # Grid y (2/2)
        for y in np.arange(self.camera.ymin, self.camera.ymax + self.stepY, self.stepY):
            y_0 = round(y)
            x_0 = self.camera.xmin
            points3d_4x1 = np.array([[x_0], [y_0], [0.0], [1.0]])
            points2d_3x1, _ = self.camera.project_points3d(points3d_4xN=points3d_4x1)
            cv.putText(
                _img,
                str(round(y_0)) + " m",
                (5, int(points2d_3x1[1, 0]) - 5),
                cv.FONT_HERSHEY_PLAIN,
                0.6,
                self.gridTextColor,
                1,
                cv.LINE_AA,
            )

        # World origin
        # cv.circle(self.topView, self.point2Pixel((0.0, 0.0)), 4, (255, 255, 255), -1)
        # cv.line(self.topView, self.point2Pixel((0.0, 0.0)), self.point2Pixel((5.0, 0.0)),
        #  (0, 0, 255), 2)
        # cv.line(self.topView, self.point2Pixel((0.0, 0.0)), self.point2Pixel((0.0, 5.0)),
        #  (0, 255, 0), 2)
        # cv.putText(self.topView, "X", self.point2Pixel((5.0, -0.5)), cv.FONT_HERSHEY_PLAIN,
        #  1.0, (0, 0, 255), 1, cv.LINE_AA)
        # cv.putText(self.topView, "Y", self.point2Pixel((-1.0, 5.0)), cv.FONT_HERSHEY_PLAIN,
        #  1.0, (0, 255, 0), 1, cv.LINE_AA)

    def __draw_bev(self, cam_name: str) -> npt.NDArray[np.float32]:
        img = self.images[cam_name]["img"]

        map_x = self.images[cam_name]["mapX"]
        map_y = self.images[cam_name]["mapY"]
        bev = cv.remap(
            img,
            map_x,
            map_y,
            interpolation=cv.INTER_LINEAR,
            borderMode=cv.BORDER_CONSTANT,
        )

        bev32 = np.array(bev, np.float32)
        if "weights" in self.images[cam_name]:
            cv.multiply(self.images[cam_name]["weights"], bev32, bev32)

        # cv.imshow('bev' + cam_name, bev)
        # cv.waitKey(1)

        # bev832 = np.uint8(bev32)
        # cv.imshow('bev8' + cam_name, bev832)
        # cv.waitKey(1)

        return bev32

    def __draw_bevs(self, _img: cv.Mat, _frame_num: int | None = None):
        """
        Draw BEVs into the topview.

        :param _frameNum:
        :return:
        """
        if self.camera is None:
            return

        num_cams = len(self.images)
        if num_cams == 0:
            return

        h = self.camera.height
        w = self.camera.width
        # Prepare image with drawing for this call
        # black background
        acc32: npt.NDArray[np.float32] = np.zeros((h, w, 3), dtype=np.float32)

        for cam_name in self.images:
            if self.scene.get_camera(cam_name, _frame_num) is not None:
                temp32 = self.__draw_bev(cam_name=cam_name)
                # mask = np.zeros((h, w), dtype=np.uint8)
                # mask[temp32 > 0] = 255
                # mask = (temp32 > 0)
                if num_cams > 1:
                    acc32 = cv.add(temp32, acc32)
        if num_cams > 1:
            acc32 /= self.images["weights_acc"]
        else:
            acc32 = temp32
        acc8 = np.uint8(acc32)
        # cv.imshow('acc', acc8)
        # cv.waitKey(1)

        # Copy into topView only new pixels
        nonzero = acc8 > 0
        _img[nonzero] = acc8

    def __draw_info(self, topview: npt.NDArray, frame_num: int | None = None):
        if not isinstance(self.camera, scl.CameraOrthographic):
            warnings.warn("__draw_info: Camera is not orthographic", Warning, 2)
            return

        h = topview.shape[0]
        w = topview.shape[1]
        w_margin = 250
        h_margin = 140
        h_step = 20
        font_size = 0.8
        cv.putText(
            topview,
            "Img. Size(px): " + str(w) + " x " + str(h),
            (w - w_margin, h - h_margin),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )
        if frame_num is None:
            frame_num = -1
        cv.putText(
            topview,
            "Frame: " + str(frame_num),
            (w - w_margin, h - h_margin + h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )
        cv.putText(
            topview,
            "CS: " + str(self.camera_coordinate_system),
            (w - w_margin, h - h_margin + 2 * h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )

        cv.putText(
            topview,
            "RangeX (m): (" + str(self.camera.xmin) + ", " + str(self.camera.xmax) + ")",
            (w - w_margin, h - h_margin + 3 * h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )
        cv.putText(
            topview,
            "RangeY (m): (" + str(self.camera.ymin) + ", " + str(self.camera.ymax) + ")",
            (w - w_margin, h - h_margin + 4 * h_step),
            cv.FONT_HERSHEY_PLAIN,
            font_size,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )

        # cv.putText(topView, "OffsetX (px): (" + str(self.params.offsetX) + ", " +
        #           str(self.params.offsetX) + ")",
        #           (w - w_margin, h - h_margin + 5*h_step),
        #           cv.FONT_HERSHEY_PLAIN, font_size, (0, 0, 0), 1, cv.LINE_AA)
        # cv.putText(topView, "OffsetY (px): (" + str(self.params.offsetY) + ", " +
        #           str(self.params.offsetY) + ")",
        #           (w - w_margin, h - h_margin + 6*h_step),
        #           cv.FONT_HERSHEY_PLAIN, font_size, (0, 0, 0), 1, cv.LINE_AA)


class FrameInfoDrawer:
    # This class draws Element information in a window
    class Params:
        def __init__(self, _color_map: dict | None = None):
            if _color_map is None:
                self.color_map = {}
            else:
                if not isinstance(_color_map, dict):
                    raise TypeError("Argument '_color_map' must be of type 'dict'")
                self.color_map = _color_map

    def __init__(self, vcd: core.VCD):
        if not isinstance(vcd, core.VCD):
            raise TypeError("Argument 'vcd' must be of type 'vcd.core.VCD'")
        self.vcd = vcd
        self.params = FrameInfoDrawer.Params()

    def draw_base(self, _img: cv.Mat, _frame_num: int):
        if _frame_num is not None:
            last_frame = self.vcd.get_frame_intervals().get()[-1][1]
            text = "Frame: " + str(_frame_num) + " / " + str(last_frame)
        else:
            text = "Static image"

        margin = 20
        cv.putText(
            _img,
            text,
            (margin, margin),
            cv.FONT_HERSHEY_DUPLEX,
            0.8,
            (0, 0, 0),
            1,
            cv.LINE_AA,
        )
        rows, cols, channels = _img.shape
        cv.line(_img, (0, margin + 10), (cols, margin + 10), (0, 0, 0), 1)

    def draw(
        self,
        _frame_num: int,
        cols: int = 600,
        rows: int = 1200,
        _params: FrameInfoDrawer.Params | None = None,
    ) -> cv.Mat:
        img = 255 * np.ones((rows, cols, 3), np.uint8)
        if _params is not None:
            if not isinstance(_params, FrameInfoDrawer.Params):
                raise TypeError(
                    "Argument '_params' must be of type 'vcd.draw.FrameInfoDrawer.Params'"
                )
            self.params = _params

        self.draw_base(img, _frame_num)
        rows, cols, channels = img.shape

        # Explore objects at VCD
        count = 0
        margin = 50
        jump = 30

        # Explore objects at VCD
        if _frame_num is not None:
            vcd_frame = self.vcd.get_frame(_frame_num)
            if "objects" in vcd_frame:
                objects = vcd_frame["objects"]
        else:
            if self.vcd.has_objects():
                objects = self.vcd.get_objects()

        if len(objects) > 0:
            num_objects = len(objects.keys())
            text = "Objects: " + str(num_objects)
            cv.putText(
                img,
                text,
                (margin, margin),
                cv.FONT_HERSHEY_DUPLEX,
                0.8,
                (0, 0, 0),
                1,
                cv.LINE_AA,
            )
            cv.line(img, (0, margin + 10), (cols, margin + 10), (0, 0, 0), 1)
            count += 1
            for object_id, _object in objects.items():
                # Get object static info
                # name = self.vcd.get_object(object_id)["name"]
                fis = self.vcd.get_element_frame_intervals(
                    core.ElementType.object, object_id
                )

                # Colors
                _object = self.vcd.get_object(object_id)
                if _object is None:
                    continue
                object_class = _object["type"]
                if self.params.color_map.get(object_class) is None:
                    # Let's create a new entry for this class
                    self.params.color_map[object_class] = (
                        randbelow(255),
                        randbelow(255),
                        randbelow(255),
                    )

                # text = object_id + " " + object_class + " \"" + name + "\" " + fis.to_str()
                text = object_id + " " + object_class + " " + fis.to_str()
                cv.putText(
                    img,
                    text,
                    (margin, margin + count * jump),
                    cv.FONT_HERSHEY_DUPLEX,
                    0.6,
                    self.params.color_map[object_class],
                    1,
                    cv.LINE_AA,
                )
                count += 1

        return img


class TextDrawer:
    def __init__(self):
        pass

    def draw(self, _str: str, cols: int = 600, rows: int = 1200) -> cv.Mat:
        img = np.zeros((rows, cols, 3), np.uint8)
        count = 0

        # Split into pieces
        chars_per_line = cols // 8  # fits well with 0.4 fontsize
        text_rows = [
            _str[i : i + chars_per_line] for i in range(0, len(_str), chars_per_line)
        ]

        margin = 20
        jump = 20
        for text_row in text_rows:
            cv.putText(
                img,
                text_row,
                (margin, margin + count * jump),
                cv.FONT_HERSHEY_DUPLEX,
                0.4,
                (255, 255, 255),
                1,
                cv.LINE_AA,
            )
            count += 1

        return img
