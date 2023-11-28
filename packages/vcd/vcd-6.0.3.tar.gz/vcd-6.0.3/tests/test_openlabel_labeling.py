"""
VCD (Video Content Description) library.

Project website: http://vcd.vicomtech.org

Copyright (C) 2023, Vicomtech (http://www.vicomtech.es/),
(Spain) all rights reserved.

VCD is a Python library to create and manage OpenLABEL content.
VCD is distributed under MIT License. See LICENSE.
"""

import inspect
import os
import unittest
from pathlib import Path

from vcd import core, types

from .test_config import check_openlabel, openlabel_version_name


class TestBasic(unittest.TestCase):
    def test_create_openlabel(self):
        """
        This test shows how to create a new OpenLABEL object.

        :return:
        """
        openlabel = core.OpenLABEL()
        openlabel.add_object(name="object1", semantic_type="car")
        openlabel.add_object(name="object2", semantic_type="pedestrian")

        # Check equal to reference JSON
        vcd_path = (
            Path(__file__).parent.resolve()
            / "etc"
            / str(
                openlabel_version_name
                + "_"
                + inspect.currentframe().f_code.co_name
                + ".json"
            )
        )
        self.assertTrue(check_openlabel(openlabel, str(vcd_path)))

    def test_read_vcd431_file(self):
        """
        This test is about reading a VCD431 file and passing it to the OpenLABEL constructor.

        :return:
        """
        openlabel = core.OpenLABEL()
        ref_file_name = str(
            Path(__file__).parent.resolve() / "etc" / "vcd431_test_contours.json"
        )
        openlabel.load_from_file(ref_file_name)

        # Check equal to reference JSON
        vcd_path = (
            Path(__file__).parent.resolve()
            / "etc"
            / str(
                openlabel_version_name
                + "_"
                + inspect.currentframe().f_code.co_name
                + ".json"
            )
        )
        self.assertTrue(check_openlabel(openlabel, str(vcd_path)))

    def test_openlabel_bounding_box_points(self):
        openlabel = core.OpenLABEL()
        uid1 = openlabel.add_object(name="object1", semantic_type="van")
        openlabel.add_object_data(
            uid=uid1,
            object_data=types.bbox(name="enclosing_rectangle", val=[182, 150, 678, 466]),
        )
        openlabel.add_object_data(
            uid=uid1,
            object_data=types.poly2d(
                name="extreme_points",
                val=(424, 150, 860, 456, 556, 616, 182, 339),
                mode=types.Poly2DType.MODE_POLY2D_ABSOLUTE,
                closed=True,
            ),
        )
        # Check equal to reference JSON
        vcd_path = (
            Path(__file__).parent.resolve()
            / "etc"
            / str(
                openlabel_version_name
                + "_"
                + inspect.currentframe().f_code.co_name
                + ".json"
            )
        )
        self.assertTrue(check_openlabel(openlabel, str(vcd_path)))

    def test_openlabel_external_data_resource(self):
        openlabel = core.OpenLABEL()
        res_uid = openlabel.add_resource("../resources/xodr/multi_intersections.xodr")
        openlabel.add_object(
            name="road1", semantic_type="road", res_uid=core.ResourceUID(res_uid, 217)
        )
        openlabel.add_object(
            name="lane1", semantic_type="lane", res_uid=core.ResourceUID(res_uid, 3)
        )

        # Check equal to reference JSON
        vcd_path = (
            Path(__file__).parent.resolve()
            / "etc"
            / str(
                openlabel_version_name
                + "_"
                + inspect.currentframe().f_code.co_name
                + ".json"
            )
        )
        self.assertTrue(check_openlabel(openlabel, str(vcd_path)))


if (
    __name__ == "__main__"
):  # This changes the command-line entry point to call unittest.main()
    print("Running " + os.path.basename(__file__))
    unittest.main()
