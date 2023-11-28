"""
VCD (Video Content Description) library.

Project website: http://vcd.vicomtech.org

Copyright (C) 2023, Vicomtech (http://www.vicomtech.es/),
(Spain) all rights reserved.

VCD is a Python library to create and manage OpenLABEL content.
VCD is distributed under MIT License. See LICENSE.
"""

import os
import unittest
from pathlib import Path

import numpy as np

from vcd import core, draw, scl, utils

from .test_config import openlabel_version_name

# Fisheye polynomial inversion (woodscape and OpenCV)
# with open('../jupyter/data/Woodscape/00000_FV.json') as f:
#    config_fv = json.load(f)

#    intrinsic_fv = config_fv['intrinsic']
#    coefficients_fv = [intrinsic_fv['k1'], intrinsic_fv['k2'], intrinsic_fv['k3'], intrinsic_fv['k4']]

#    kp_woodscape_inverted, error_a_deg = invert_polynomial(np.array(coefficients_fv), model='radial_poly')
#    print('Invert radial_poly, error (deg): ' + str(error_a_deg))


class TestBasic(unittest.TestCase):
    def test_scl_camera_pinhole(self):
        # Read camera from VCD and create Scene object
        vcd = core.OpenLABEL()
        ref_file_name = str(
            Path(__file__).parent.resolve()
            / "etc"
            / str(openlabel_version_name + "_test_scl_camera_pinhole.json")
        )
        vcd.load_from_file(ref_file_name)
        scene = scl.Scene(vcd)
        camera = scene.get_camera("camera_pinhole")

        # Create grid of 3D points
        xm, ym, zm = utils.generate_grid(
            x_params=(-0.5, 0.5, 2), y_params=(-0.5, 0.5, 2), z_params=(3, 3, 1)
        )
        points3d_4xN = utils.grid_as_4xN_points3d(xm, ym, zm)
        # print(points3d_4xN)

        # Project into image
        points2d_3xN, idx_valid = camera.project_points3d(
            points3d_4xN, remove_outside=True
        )
        # print(points2d_3xN)

        # Reproject as rays
        rays3d_3xN = camera.reproject_points2d(points2d_3xN[:, idx_valid])
        # print(rays3d_3xN)

        # Project rays again as points
        points2d_rep_3xN, idx_rep_valid = camera.project_points3d(
            rays3d_3xN, remove_outside=True
        )
        # print(points2d_rep_3xN)

        self.assertTrue(all(idx_rep_valid))  # all points should be valid
        error = np.linalg.norm(points2d_3xN[:, idx_valid] - points2d_rep_3xN)
        self.assertTrue(error < 1e-4)

    def test_scl_camera_fisheye_xz1z2_radial_poly(self):
        # Read camera from VCD and create Scene object
        vcd = core.OpenLABEL()
        ref_file_name = str(
            Path(__file__).parent.resolve()
            / "etc"
            / str(
                openlabel_version_name + "_test_scl_camera_fisheye_xz1z2_radial_poly.json"
            )
        )
        vcd.load_from_file(ref_file_name)
        scene = scl.Scene(vcd)

        # Read points that are defined to be in the ground plane
        ground_x_pos = vcd.get_object_data(uid=2, data_name="wall", frame_num=0)
        val = np.array(ground_x_pos["val"])
        width = ground_x_pos["width"]
        height = ground_x_pos["height"]
        points3d_4xN = val.reshape(height, width)

        # Project into one camera
        points2d_3xN, idx_valid = scene.project_points3d_4xN(
            points3d_4xN=points3d_4xN,
            cs_src="vehicle-iso8855",
            cs_cam="CAM_FRONT",
            remove_outside=True,
        )

        # Reproject into plane
        points2d_3xN = points2d_3xN[:, idx_valid]
        points3d_4xN_rep, idx_valid_rep = scene.reproject_points2d_3xN_into_plane(
            points2d_3xN=points2d_3xN,
            plane=[0, 0, 1, 0],
            cs_cam="CAM_FRONT",
            cs_dst="vehicle-iso8855",
        )

        # Measure error
        error = np.linalg.norm(
            points3d_4xN[:, idx_valid][:, idx_valid_rep]
            - points3d_4xN_rep[:, idx_valid_rep]
        )
        self.assertTrue(error < 1e-2)  # less than 1 cm error

    def test_scl_camera_cylindrical(self):
        vcd_file = str(
            Path(__file__).parent.resolve()
            / "etc"
            / str(openlabel_version_name + "_test_scl_camera_fisheye_kannala.json")
        )

        # Load a basic 4 camera set-up with fisheye and cylindrical
        vcd = core.OpenLABEL()
        vcd.load_from_file(vcd_file)
        scene = scl.Scene(vcd)

        # setupViewer = draw.SetupViewer(scene, "vehicle-iso8855")
        # fig1 = setupViewer.plot_setup()
        # plt.show()

        # Create grid of 3D points
        xm, ym, zm = utils.generate_grid(
            x_params=(-20, 20, 10), y_params=(-20, 20, 10), z_params=(0, 0, 1)
        )
        points3d_4xN = utils.grid_as_4xN_points3d(xm, ym, zm)

        # Project and reproject
        points2d_3xN_0, idx_valid_0 = scene.project_points3d_4xN(
            points3d_4xN=points3d_4xN,
            cs_src="vehicle-iso8855",
            cs_cam="Front_cylindrical",
            remove_outside=True,
        )
        points2d_3xN_1, idx_valid_1 = scene.project_points3d_4xN(
            points3d_4xN=points3d_4xN,
            cs_src="vehicle-iso8855",
            cs_cam="Left_cylindrical",
            remove_outside=True,
        )
        points2d_3xN_2, idx_valid_2 = scene.project_points3d_4xN(
            points3d_4xN=points3d_4xN,
            cs_src="vehicle-iso8855",
            cs_cam="Right_cylindrical",
            remove_outside=True,
        )
        points2d_3xN_3, idx_valid_3 = scene.project_points3d_4xN(
            points3d_4xN=points3d_4xN,
            cs_src="vehicle-iso8855",
            cs_cam="Rear_cylindrical",
            remove_outside=True,
        )

        points2d_3xN_0 = points2d_3xN_0[:, idx_valid_0]
        points2d_3xN_1 = points2d_3xN_1[:, idx_valid_1]
        points2d_3xN_2 = points2d_3xN_2[:, idx_valid_2]
        points2d_3xN_3 = points2d_3xN_3[:, idx_valid_3]

        points3d_4xN_rep_0, idx_valid_rep_0 = scene.reproject_points2d_3xN_into_plane(
            points2d_3xN=points2d_3xN_0,
            plane=[0, 0, 1, 0],
            cs_cam="Front_cylindrical",
            cs_dst="vehicle-iso8855",
        )
        points3d_4xN_rep_1, idx_valid_rep_1 = scene.reproject_points2d_3xN_into_plane(
            points2d_3xN=points2d_3xN_1,
            plane=[0, 0, 1, 0],
            cs_cam="Left_cylindrical",
            cs_dst="vehicle-iso8855",
        )
        points3d_4xN_rep_2, idx_valid_rep_2 = scene.reproject_points2d_3xN_into_plane(
            points2d_3xN=points2d_3xN_2,
            plane=[0, 0, 1, 0],
            cs_cam="Right_cylindrical",
            cs_dst="vehicle-iso8855",
        )
        points3d_4xN_rep_3, idx_valid_rep_3 = scene.reproject_points2d_3xN_into_plane(
            points2d_3xN=points2d_3xN_3,
            plane=[0, 0, 1, 0],
            cs_cam="Rear_cylindrical",
            cs_dst="vehicle-iso8855",
        )

        # Measure error
        error_0 = np.linalg.norm(
            points3d_4xN[:, idx_valid_0][:, idx_valid_rep_0]
            - points3d_4xN_rep_0[:, idx_valid_rep_0]
        )
        error_1 = np.linalg.norm(
            points3d_4xN[:, idx_valid_1][:, idx_valid_rep_1]
            - points3d_4xN_rep_1[:, idx_valid_rep_1]
        )
        error_2 = np.linalg.norm(
            points3d_4xN[:, idx_valid_2][:, idx_valid_rep_2]
            - points3d_4xN_rep_2[:, idx_valid_rep_2]
        )
        error_3 = np.linalg.norm(
            points3d_4xN[:, idx_valid_3][:, idx_valid_rep_3]
            - points3d_4xN_rep_3[:, idx_valid_rep_3]
        )

        # print(error_0)
        # print(error_1)
        # print(error_2)
        # print(error_3)

        # For this test, the inverse of the fisheye distortion throws about 4.5º error, so at 20 meters distance, the error is large
        self.assertTrue(error_0 < 1e-2)  # less than 1 cm error
        self.assertTrue(error_1 < 1e-2)
        self.assertTrue(error_2 < 1e-2)
        self.assertTrue(error_3 < 1e-2)

    def test_scl_camera_fisheye_kannala(self):
        """Reprojection using fisheye with Kannala distortion model."""
        vcd_file = str(
            Path(__file__).parent.resolve()
            / "etc"
            / str(openlabel_version_name + "_test_scl_camera_fisheye_kannala.json")
        )

        # Load a basic 4 camera set-up with fisheye and cylindrical
        vcd = core.OpenLABEL()
        vcd.load_from_file(vcd_file)
        scene = scl.Scene(vcd)

        # setupViewer = draw.SetupViewer(scene, "vehicle-iso8855")
        # fig1 = setupViewer.plot_setup()
        # plt.show()

        # Create grid of 3D points
        xm, ym, zm = utils.generate_grid(
            x_params=(-20, 20, 10), y_params=(-20, 20, 10), z_params=(0, 0, 1)
        )
        points3d_4xN = utils.grid_as_4xN_points3d(xm, ym, zm)

        # Project and reproject
        points2d_3xN_0, idx_valid_0 = scene.project_points3d_4xN(
            points3d_4xN=points3d_4xN,
            cs_src="vehicle-iso8855",
            cs_cam="Front",
            remove_outside=True,
        )
        points2d_3xN_1, idx_valid_1 = scene.project_points3d_4xN(
            points3d_4xN=points3d_4xN,
            cs_src="vehicle-iso8855",
            cs_cam="Left",
            remove_outside=True,
        )
        points2d_3xN_2, idx_valid_2 = scene.project_points3d_4xN(
            points3d_4xN=points3d_4xN,
            cs_src="vehicle-iso8855",
            cs_cam="Right",
            remove_outside=True,
        )
        points2d_3xN_3, idx_valid_3 = scene.project_points3d_4xN(
            points3d_4xN=points3d_4xN,
            cs_src="vehicle-iso8855",
            cs_cam="Rear",
            remove_outside=True,
        )

        points2d_3xN_0 = points2d_3xN_0[:, idx_valid_0]
        points2d_3xN_1 = points2d_3xN_1[:, idx_valid_1]
        points2d_3xN_2 = points2d_3xN_2[:, idx_valid_2]
        points2d_3xN_3 = points2d_3xN_3[:, idx_valid_3]

        points3d_4xN_rep_0, idx_valid_rep_0 = scene.reproject_points2d_3xN_into_plane(
            points2d_3xN=points2d_3xN_0,
            plane=[0, 0, 1, 0],
            cs_cam="Front",
            cs_dst="vehicle-iso8855",
        )
        points3d_4xN_rep_1, idx_valid_rep_1 = scene.reproject_points2d_3xN_into_plane(
            points2d_3xN=points2d_3xN_1,
            plane=[0, 0, 1, 0],
            cs_cam="Left",
            cs_dst="vehicle-iso8855",
        )
        points3d_4xN_rep_2, idx_valid_rep_2 = scene.reproject_points2d_3xN_into_plane(
            points2d_3xN=points2d_3xN_2,
            plane=[0, 0, 1, 0],
            cs_cam="Right",
            cs_dst="vehicle-iso8855",
        )
        points3d_4xN_rep_3, idx_valid_rep_3 = scene.reproject_points2d_3xN_into_plane(
            points2d_3xN=points2d_3xN_3,
            plane=[0, 0, 1, 0],
            cs_cam="Rear",
            cs_dst="vehicle-iso8855",
        )

        # Measure error
        error_0 = np.linalg.norm(
            points3d_4xN[:, idx_valid_0][:, idx_valid_rep_0]
            - points3d_4xN_rep_0[:, idx_valid_rep_0]
        )
        error_1 = np.linalg.norm(
            points3d_4xN[:, idx_valid_1][:, idx_valid_rep_1]
            - points3d_4xN_rep_1[:, idx_valid_rep_1]
        )
        error_2 = np.linalg.norm(
            points3d_4xN[:, idx_valid_2][:, idx_valid_rep_2]
            - points3d_4xN_rep_2[:, idx_valid_rep_2]
        )
        error_3 = np.linalg.norm(
            points3d_4xN[:, idx_valid_3][:, idx_valid_rep_3]
            - points3d_4xN_rep_3[:, idx_valid_rep_3]
        )

        # print(error_0)
        # print(error_1)
        # print(error_2)
        # print(error_3)

        # For this test, the inverse of the fisheye distortion throws about 4.5º error, so at 20 meters distance, the error is large
        self.assertTrue(error_0 < 1e-2)  # less than 1 cm error
        self.assertTrue(error_1 < 1e-2)
        self.assertTrue(error_2 < 1e-2)
        self.assertTrue(error_3 < 1e-2)

    def test_scl_camera_cubemap(self):
        """Cubemap to fisheye camera projection maps."""
        # Read camera from VCD and create Scene object
        vcd = core.OpenLABEL()
        ref_file_name = str(
            Path(__file__).parent.resolve()
            / "etc"
            / str(openlabel_version_name + "_test_scl_camera_cubemap.json")
        )
        vcd.load_from_file(ref_file_name)
        scene = scl.Scene(vcd)

        # Read projection maps from cubemap pixels into fisheye image

        map_x = np.load(
            str(
                Path(__file__).parent.resolve()
                / "etc"
                / str(openlabel_version_name + "_test_scl_camera_cubemap_map_x.npy")
            )
        )
        map_y = np.load(
            str(
                Path(__file__).parent.resolve()
                / "etc"
                / str(openlabel_version_name + "_test_scl_camera_cubemap_map_y.npy")
            )
        )

        # Create projection maps from VCD cameras
        remap_x, remap_y = scene.create_img_projection_maps(
            "CAM_CUBEMAP_FRONT", "CAM_FISHEYE_FRONT", 0
        )

        # Compare projection maps
        self.assertTrue((map_x == remap_x).all)
        self.assertTrue((map_y == remap_y).all)

    def test_scl_camera_cubemap_filter_z_neg(self):
        """Cubemap to fisheye camera projection maps, when z negative points (behind the
        camera) are filtered out."""
        # Read camera from VCD and create Scene object
        vcd = core.OpenLABEL()
        ref_file_name = str(
            Path(__file__).parent.resolve()
            / "etc"
            / str(openlabel_version_name + "_test_scl_camera_cubemap.json")
        )
        vcd.load_from_file(ref_file_name)
        scene = scl.Scene(vcd)

        # Read projection maps from cubemap pixels into fisheye image
        map_x = np.load(
            str(
                Path(__file__).parent.resolve()
                / "etc"
                / str(
                    openlabel_version_name
                    + "_test_scl_camera_cubemap_map_x_filter_z_neg.npy"
                )
            )
        )
        map_y = np.load(
            str(
                Path(__file__).parent.resolve()
                / "etc"
                / str(
                    openlabel_version_name
                    + "_test_scl_camera_cubemap_map_y_filter_z_neg.npy"
                )
            )
        )

        # Create projection maps from VCD cameras
        remap_x, remap_y = scene.create_img_projection_maps(
            "CAM_CUBEMAP_FRONT", "CAM_FISHEYE_FRONT", 0, filter_z_neg=True
        )

        # Compare projection maps
        self.assertTrue((map_x == remap_x).all)
        self.assertTrue((map_y == remap_y).all)

    # def test_undistortion(self, img, img_und):
    #     # TODO: To check this test
    #     # Let's test if we project a 3D point into the distorted image
    #     # and into the undistorted image
    #     # And convert from one into another
    #     # Conclusions would be: we can work in any domain (distorted or undistorted), and
    #     # keep the ability to project and reproject 3D points

    #     # 1.- Create some points
    #     n = 100
    #     points3d_4xN = np.ones((3, n))
    #     points3d_4xN[0:3, :] = points3d_4xN[0:3, :] * np.random.random((3, n)) * 10

    #     # 2.- Project points into distorted image
    #     points2d_3xN_dist, idx_valid = self.project_points3d(points3d_4xN)
    #     points2d_3xN_dist = points2d_3xN_dist[:, idx_valid]

    #     # 3.- Draw into image
    #     for i in range(0, points2d_3xN_dist.shape[1]):
    #         cv.circle(
    #             img,
    #             (
    #                 utils.round(points2d_3xN_dist[0, i]),
    #                 utils.round(points2d_3xN_dist[1, i]),
    #             ),
    #             2,
    #             (255, 0, 0),
    #             -1,
    #         )

    #     # 4.- Undistort these points
    #     self.undistort_points2d(points2d_3xN_dist)


if (
    __name__ == "__main__"
):  # This changes the command-line entry point to call unittest.main()
    print("Running " + os.path.basename(__file__))
    unittest.main()
