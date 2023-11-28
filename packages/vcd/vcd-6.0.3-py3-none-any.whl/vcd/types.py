"""
Module to handle the different data types in VCD library.

This module implements classes to allocate data of different types.
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

from builtins import bool
from enum import Enum
from typing import Any

from vcd import poly2d as poly


class CoordinateSystemType(Enum):
    sensor_cs = 1  # the coordinate system of a certain sensor
    local_cs = 2  # e.g. vehicle-ISO8855 in OpenLABEL, or "base_link" in ROS
    scene_cs = 3  # e.g. "odom" in ROS; starting as the first local-ls
    geo_utm = 4  # In UTM coordinates
    geo_wgs84 = 5  # In WGS84 elliptical Earth coordinates
    custom = 6  # Any other coordinate system


class FisheyeModel(Enum):
    """
    List of the different camera fisheye models.

    Any 3D point in space P=(X,Y,Z,1)^T has a radius with respect to the optical axis Z:

    r = ||X^2 + Y^2||

    The angle of incidence to the optical center is a = atan(r/Z).
    The angle of incidence then spans from 0 to pi/2.

    The model of the lens relates the angle of incidence with the radius of the point in the
    image plane (in pixels):

    - "radial_poly" (4 distortion coefficients) rp = k1*a + k2*a^2 + k3*a^3 + k4*a^4
    - "kannala" (5 distortion coefficients)     rp = k1*a + k2*a^3 + k3*a^5 + k4*a^7 + k5*a^9
    - "opencv_fisheye" (4 distortion coefficients, equivalent to Kannala with k1=1.0, so only the
    last 4 terms are used)                    rp = a + k1*a^3 + k2*a^5 + k3*a^7 + k4*a^9
    """

    radial_poly = 1
    kannala = 2
    opencv_fisheye = 3


class Intrinsics:
    def __init__(self):
        self.data = {}


class IntrinsicsPinhole(Intrinsics):
    def __init__(
        self,
        width_px: int,
        height_px: int,
        camera_matrix_3x4: list,
        distortion_coeffs_1xN: list | None = None,
        **additional_items: Any,
    ):
        Intrinsics.__init__(self)
        if not isinstance(width_px, int):
            raise TypeError("Argument 'width_px' must be of type 'int'")
        if not isinstance(height_px, int):
            raise TypeError("Argument 'height_px' must be of type 'int'")

        self.data["intrinsics_pinhole"] = {}
        self.data["intrinsics_pinhole"]["width_px"] = width_px
        self.data["intrinsics_pinhole"]["height_px"] = height_px
        if not isinstance(camera_matrix_3x4, list):
            raise TypeError("Argument 'camera_matrix_3x4' must be of type 'list'")

        if len(camera_matrix_3x4) != 12:
            raise ValueError("Argument 'camera_matrix_3x4' must have 12 elements")
        self.data["intrinsics_pinhole"]["camera_matrix_3x4"] = camera_matrix_3x4

        if distortion_coeffs_1xN is None:
            distortion_coeffs_1xN = []
        else:
            if not isinstance(distortion_coeffs_1xN, list):
                raise TypeError("Argument 'distortion_coeffs_1xN' must be of type 'list'")
            num_coeffs = len(distortion_coeffs_1xN)
            if not 4 <= num_coeffs <= 14:
                raise ValueError("Invalid value for argument 'num_coeffs'")
        self.data["intrinsics_pinhole"]["distortion_coeffs_1xN"] = distortion_coeffs_1xN

        if additional_items is not None:
            self.data["intrinsics_pinhole"].update(additional_items)


class IntrinsicsFisheye(Intrinsics):
    def __init__(
        self,
        width_px: int,
        height_px: int,
        lens_coeffs_1xN: list,
        center_x: float | None,
        center_y: float | None,
        focal_length_x: float | None,
        focal_length_y: float | None,
        fisheye_model: FisheyeModel | None = None,
        **additional_items: Any,
    ):
        Intrinsics.__init__(self)
        if not isinstance(width_px, int):
            raise TypeError("Argument 'width_px' must be of type 'int'")
        if not isinstance(height_px, int):
            raise TypeError("Argument 'height_px' must be of type 'int'")
        self.data["intrinsics_fisheye"] = {}
        self.data["intrinsics_fisheye"]["width_px"] = width_px
        self.data["intrinsics_fisheye"]["height_px"] = height_px
        if not isinstance(lens_coeffs_1xN, list):
            raise TypeError("Argument 'lens_coeffs_1xN' must be of type 'list'")
        if not isinstance(center_x, (float, type(None))):
            raise TypeError("Argument 'center_x' must be of type 'float' or 'None'")
        if not isinstance(center_y, (float, type(None))):
            raise TypeError("Argument 'center_y' must be of type 'float' or 'None'")
        if not isinstance(focal_length_x, (float, type(None))):
            raise TypeError("Argument 'focal_length_x' must be of type 'float' or 'None'")
        if not isinstance(focal_length_y, (float, type(None))):
            raise TypeError("Argument 'focal_length_y' must be of type 'float' or 'None'")

        self.data["intrinsics_fisheye"]["center_x"] = center_x
        self.data["intrinsics_fisheye"]["center_y"] = center_y
        self.data["intrinsics_fisheye"]["focal_length_x"] = focal_length_x
        self.data["intrinsics_fisheye"]["focal_length_y"] = focal_length_y
        self.data["intrinsics_fisheye"]["lens_coeffs_1xN"] = lens_coeffs_1xN

        if fisheye_model is not None:
            if not isinstance(fisheye_model, FisheyeModel):
                raise TypeError("Argument 'fisheye_model' must be of type 'FisheyeModel'")
            if fisheye_model is FisheyeModel.radial_poly:
                if len(lens_coeffs_1xN) != 4:
                    raise ValueError(
                        "Argument 'lens_coeffs_1xN' for 'FisheyeModel' type "
                        "'radial_poly' must have 4 elements "
                    )
            elif fisheye_model is FisheyeModel.kannala:
                if len(lens_coeffs_1xN) != 5:
                    raise ValueError(
                        "Argument 'lens_coeffs_1xN' for 'FisheyeModel' type "
                        "'kannala' must have 5 elements "
                    )
            elif fisheye_model is FisheyeModel.opencv_fisheye:
                if len(lens_coeffs_1xN) != 4:
                    raise ValueError(
                        "Argument 'lens_coeffs_1xN' for 'FisheyeModel' type "
                        "'opencv_fisheye' must have 4 elements "
                    )
            else:
                raise RuntimeError(
                    "ERROR: Fisheyemodel not supported. See types.FisheyeModel enum."
                )
            self.data["intrinsics_fisheye"]["model"] = fisheye_model.name
        else:
            if len(lens_coeffs_1xN) == 4:
                self.data["intrinsics_fisheye"][
                    "model"
                ] = FisheyeModel.opencv_fisheye.name
            elif len(lens_coeffs_1xN) == 5:
                self.data["intrinsics_fisheye"]["model"] = FisheyeModel.kannala.name

        if additional_items is not None:
            self.data["intrinsics_fisheye"].update(additional_items)


class IntrinsicsCylindrical(Intrinsics):
    def __init__(
        self,
        width_px: int,
        height_px: int,
        fov_horz_rad: float,
        fov_vert_rad: float,
        **additional_items: Any,
    ):
        Intrinsics.__init__(self)
        if not isinstance(width_px, int):
            raise TypeError("Argument 'width_px' must be of type 'int'")
        if not isinstance(height_px, int):
            raise TypeError("Argument 'height_px' must be of type 'int'")
        self.data["intrinsics_cylindrical"] = {}
        self.data["intrinsics_cylindrical"]["width_px"] = width_px
        self.data["intrinsics_cylindrical"]["height_px"] = height_px
        if not isinstance(fov_horz_rad, float):
            raise TypeError("Argument 'fov_horz_rad' must be of type 'float'")
        if not isinstance(fov_vert_rad, float):
            raise TypeError("Argument 'fov_vert_rad' must be of type 'float'")
        self.data["intrinsics_cylindrical"]["fov_horz_rad"] = fov_horz_rad
        self.data["intrinsics_cylindrical"]["fov_vert_rad"] = fov_vert_rad

        if additional_items is not None:
            self.data["intrinsics_cylindrical"].update(additional_items)


class IntrinsicsOrthographic(Intrinsics):
    def __init__(
        self,
        width_px: int,
        height_px: int,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
        **additional_items: Any,
    ):
        Intrinsics.__init__(self)
        if not isinstance(width_px, int):
            raise TypeError("Argument 'width_px' must be of type 'int'")
        if not isinstance(height_px, int):
            raise TypeError("Argument 'height_px' must be of type 'int'")
        self.data["intrinsics_orthographic"] = {}
        self.data["intrinsics_orthographic"]["width_px"] = width_px
        self.data["intrinsics_orthographic"]["height_px"] = height_px
        if not isinstance(xmin, float):
            raise TypeError("Argument 'xmin' must be of type 'float'")
        if not isinstance(xmax, float):
            raise TypeError("Argument 'xmax' must be of type 'float'")
        if not isinstance(ymin, float):
            raise TypeError("Argument 'ymin' must be of type 'float'")
        if not isinstance(ymax, float):
            raise TypeError("Argument 'ymax' must be of type 'float'")
        self.data["intrinsics_orthographic"]["xmin"] = xmin
        self.data["intrinsics_orthographic"]["xmax"] = xmax
        self.data["intrinsics_orthographic"]["ymin"] = ymin
        self.data["intrinsics_orthographic"]["ymax"] = ymax

        if additional_items is not None:
            self.data["intrinsics_orthographic"].update(additional_items)


class IntrinsicsCubemap(Intrinsics):
    def __init__(
        self,
        width_px: int,
        height_px: int,
        camera_matrix_3x4: list,
        distortion_coeffs_1xN: list | None = None,
        **additional_items: Any,
    ):
        Intrinsics.__init__(self)
        if not isinstance(width_px, int):
            raise TypeError("Argument 'width_px' must be of type 'int'")
        if not isinstance(height_px, int):
            raise TypeError("Argument 'height_px' must be of type 'int'")
        self.data["intrinsics_cubemap"] = {}
        self.data["intrinsics_cubemap"]["width_px"] = width_px
        self.data["intrinsics_cubemap"]["height_px"] = height_px
        if not isinstance(camera_matrix_3x4, list):
            raise TypeError("Argument 'camera_matrix_3x4' must be of type 'list'")

        if len(camera_matrix_3x4) != 12:
            raise TypeError("Argument 'camera_matrix_3x4' must have 12 elements")
        self.data["intrinsics_cubemap"]["camera_matrix_3x4"] = camera_matrix_3x4

        if distortion_coeffs_1xN is None:
            distortion_coeffs_1xN = []
        else:
            if not isinstance(distortion_coeffs_1xN, list):
                raise TypeError("Argument 'distortion_coeffs_1xN' must be of type 'list'")
            num_coeffs = len(distortion_coeffs_1xN)
            if not 4 <= num_coeffs <= 14:
                raise ValueError("Invalid value for argument 'num_coeffs'")
        self.data["intrinsics_cubemap"]["distortion_coeffs_1xN"] = distortion_coeffs_1xN

        if additional_items is not None:
            self.data["intrinsics_cubemap"].update(additional_items)


class IntrinsicsCustom(Intrinsics):
    def __init__(self, **additional_items: Any):
        Intrinsics.__init__(self)
        self.data["intrinsics_custom"] = {}
        if additional_items is not None:
            self.data["intrinsics_custom"].update(additional_items)


class TransformDataType(Enum):
    matrix_4x4 = 1
    quat_and_trans_7x1 = 2
    euler_and_trans_6x1 = 3
    custom = 4


class TransformData:
    """
    Define methods to obtain different coordinate system transformation representations.

    This class encodes the transform data in the form of 4x4 matrix, quaternion + translation,
    or Euler angles + translation.
    """

    def __init__(self, val: list, t_type: TransformDataType, **additional_items: Any):
        if not isinstance(val, list):
            raise TypeError("Argument 'val' must be of type 'list'")
        if not isinstance(t_type, TransformDataType):
            raise TypeError("Argument 't_type' must be of type 'TransformDataType'")

        self.data = {}
        if t_type == TransformDataType.matrix_4x4:
            self.data["matrix4x4"] = val
        elif t_type == TransformDataType.quat_and_trans_7x1:
            if len(val) != 7:
                raise ValueError(
                    "Argument 'val' for 'TransformDataType' type 'quat_and_trans_7x1' "
                    "must have 7 elements "
                )
            self.data["quaternion"] = val[0:4]
            self.data["translation"] = val[4:7]
        elif t_type == TransformDataType.euler_and_trans_6x1:
            if len(val) != 6:
                raise ValueError(
                    "Argument 'val' for 'TransformDataType' type 'euler_and_trans_6x1' "
                    "must have 7 elements "
                )
            self.data["euler_angles"] = val[0:3]
            self.data["translation"] = val[3:6]

        if additional_items is not None:
            self.data.update(additional_items)


class PoseData(TransformData):
    """
    Subclass of TransformData.

    Equivalent to TransformData, but intended to be used when passive rotation and translation
    values are provided.
    """

    def __init__(self, val: list, t_type: TransformDataType, **additional_items: Any):
        TransformData.__init__(self, val, t_type, **additional_items)


class Transform:
    def __init__(
        self,
        src_name: str,
        dst_name: str,
        transform_src_to_dst: TransformData,
        **additional_items: Any,
    ):
        if not isinstance(src_name, str):
            raise TypeError("Argument 'src_name' must be of type 'str'")
        if not isinstance(dst_name, str):
            raise TypeError("Argument 'dst_name' must be of type 'str'")
        if not isinstance(transform_src_to_dst, TransformData):
            raise TypeError(
                "Argument 'transform_src_to_dst' must be of type 'TransformData'"
            )
        self.data: dict = {}
        name = src_name + "_to_" + dst_name
        self.data[name] = {}
        transform_name: dict = self.data[name]
        self.data_additional = {}  # this is useful to append only the additional_items
        transform_name["src"] = src_name
        transform_name["dst"] = dst_name
        transform_name["transform_src_to_dst"] = transform_src_to_dst.data
        if additional_items is not None:
            transform_name.update(additional_items)
            self.data_additional.update(additional_items)


class StreamSync:
    def __init__(
        self,
        frame_vcd: int | None = None,
        frame_stream: int | None = None,
        timestamp_ISO8601: str | None = None,
        frame_shift: int | None = None,
        **additional_items: Any,
    ):
        self.data: dict = {}
        self.data["sync"] = {}
        # This is the master frame at vcd (if it is None, frame_shift specifies constant shift
        self.frame_vcd = frame_vcd

        if frame_shift is not None:
            if not isinstance(frame_shift, int):
                raise TypeError("Argument 'frame_shift' must be of type 'int'")
            if not (
                frame_stream is None and timestamp_ISO8601 is None and frame_vcd is None
            ):
                raise ValueError(
                    "At least one of these arguments needs to be different than None: "
                    "'frame_stream', 'timestamp_ISO8601', 'frame_vcd'"
                )
            self.data["sync"]["frame_shift"] = frame_shift
        else:
            if not isinstance(frame_vcd, int):
                raise TypeError("Argument 'frame_vcd' must be of type 'int'")
            if frame_stream is not None:
                if not isinstance(frame_stream, int):
                    raise TypeError("Argument 'frame_stream' must be of type 'int'")
                self.data["sync"]["frame_stream"] = frame_stream
            if timestamp_ISO8601 is not None:
                if not isinstance(timestamp_ISO8601, str):
                    raise TypeError("Argument 'timestamp_ISO8601' must be of type 'str'")
                self.data["sync"]["timestamp"] = timestamp_ISO8601
        if additional_items is not None:
            self.data["sync"].update(additional_items)


class ObjectDataType(Enum):
    generic = 0
    bbox = 1
    rbbox = 2
    num = 3
    text = 4
    boolean = 5
    poly2d = 6
    poly3d = 7
    cuboid = 8
    image = 9
    mat = 10
    binary = 11
    point2d = 12
    point3d = 13
    vec = 14
    line_reference = 15
    area_reference = 16
    mesh = 17


class Poly2DType(Enum):
    MODE_POLY2D_ABSOLUTE = 0
    # MODE_POLY2D_BBOX = 1
    # MODE_POLY2D_BBOX_DIST = 2
    # MODE_POLY2D_F8DCC = 3
    # MODE_POLY2D_RF8DCC = 4
    MODE_POLY2D_SRF6DCC = 5
    MODE_POLY2D_RS6FCC = 6


class ObjectData:
    # pylint: disable=redefined-builtin
    def __init__(
        self,
        name: str,
        coordinate_system: str | None = None,
        properties: dict | None = None,
        type: str | None = None,
    ):
        self.data: dict = {}
        self.type = ObjectDataType.generic
        if name is not None:
            if not isinstance(name, str):
                raise TypeError("Argument 'name' must be of type 'str'")
            self.data["name"] = name
        if coordinate_system is not None:
            if not isinstance(coordinate_system, str):
                raise TypeError("Argument 'coordinate_system' must be of type 'str'")
            self.data["coordinate_system"] = coordinate_system
        if properties is not None:
            if not isinstance(properties, dict):
                raise TypeError("Argument 'properties' must be of type 'dict'")
            self.data.update(properties)
        if type is not None:
            if not isinstance(type, str):
                raise TypeError("Argument 'type' must be of type 'str'")
            self.data["type"] = type

    def add_attribute(self, object_data: ObjectData | ObjectDataGeometry):
        if not isinstance(object_data, (ObjectData, ObjectDataGeometry)):
            raise TypeError(
                "Argument 'object_data' must be of type 'ObjectData' or "
                "'ObjectDataGeometry'"
            )

        # Creates 'attributes' if it does not exist
        self.data.setdefault("attributes", {})

        if object_data.type.name in self.data["attributes"]:
            # Find if element_data already there, if so, replace, otherwise, append
            list_aux = self.data["attributes"][object_data.type.name]
            pos_list = [
                idx
                for idx, val in enumerate(list_aux)
                if val["name"] == object_data.data["name"]
            ]
            if len(pos_list) == 0:
                # No: then, just push this new object data
                self.data["attributes"][object_data.type.name].append(object_data.data)
            else:
                # Ok, exists, so let's substitute
                pos = pos_list[0]
                self.data["attributes"][object_data.type.name][pos] = object_data.data
        else:
            self.data["attributes"][object_data.type.name] = [object_data.data]


class ObjectDataGeometry(ObjectData):
    def __init__(
        self,
        name: str,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        # Calling parent class
        ObjectData.__init__(self, name, coordinate_system, properties)


class bbox(ObjectDataGeometry):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        val: tuple | list,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectDataGeometry.__init__(self, name, coordinate_system, properties)
        if not isinstance(val, (tuple, list)):
            raise TypeError("Argument 'val' must be of type 'tuple' or 'list'")
        if len(val) != 4:
            raise TypeError("Argument 'val' must have 4 elements")
        if isinstance(val, tuple):
            self.data["val"] = val
        elif isinstance(val, list):
            self.data["val"] = tuple(val)
        self.type = ObjectDataType.bbox


class rbbox(ObjectDataGeometry):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        val: tuple | list,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectDataGeometry.__init__(self, name, coordinate_system, properties)
        if not isinstance(val, (tuple, list)):
            raise TypeError("Argument 'val' must be of type 'tuple' or 'list'")
        if len(val) != 5:
            raise TypeError("Argument 'val' must have 5 elements")
        if isinstance(val, tuple):
            self.data["val"] = val
        elif isinstance(val, list):
            self.data["val"] = tuple(val)
        self.type = ObjectDataType.rbbox


class num(ObjectData):  # noqa: N801  # remove capitals in class name warning
    # pylint: disable=redefined-builtin
    def __init__(
        self,
        name: str,
        val: int | float,
        coordinate_system: str | None = None,
        properties: dict | None = None,
        type: str | None = None,
    ):
        ObjectData.__init__(self, name, coordinate_system, properties, type)
        if not isinstance(val, (int, float)):
            raise TypeError("Argument 'val' must be of type 'int' or 'float'")
        self.data["val"] = val
        self.type = ObjectDataType.num


class text(ObjectData):  # noqa: N801  # remove capitals in class name warning
    # pylint: disable=redefined-builtin
    def __init__(
        self,
        name: str,
        val: str,
        coordinate_system: str | None = None,
        properties: dict | None = None,
        type: str | None = None,
    ):
        ObjectData.__init__(self, name, coordinate_system, properties, type)
        if not isinstance(val, str):
            raise TypeError("Argument 'val' must be of type 'str'")
        self.data["val"] = val
        self.type = ObjectDataType.text


class boolean(ObjectData):  # noqa: N801  # remove capitals in class name warning
    # pylint: disable=redefined-builtin
    def __init__(
        self,
        name: str,
        val: bool,
        coordinate_system: str | None = None,
        properties: dict | None = None,
        type: str | None = None,
    ):
        ObjectData.__init__(self, name, coordinate_system, properties, type)
        if not isinstance(val, bool):
            raise TypeError("Argument 'val' must be of type 'bool'")
        self.data["val"] = val
        self.type = ObjectDataType.boolean


class poly2d(ObjectDataGeometry):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        val: tuple | list,
        mode: Poly2DType,
        closed: bool,
        hierarchy: list | None = None,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectDataGeometry.__init__(self, name, coordinate_system, properties)
        if not isinstance(val, (tuple, list)):
            raise TypeError("Argument 'val' must be of type 'tuple' or 'list'")
        if not isinstance(mode, Poly2DType):
            raise TypeError("Argument 'mode' must be of type 'Poly2DType'")
        if not isinstance(closed, bool):
            raise TypeError("Argument 'closed' must be of type 'bool'")
        if isinstance(val, (list, tuple)):
            if mode == Poly2DType.MODE_POLY2D_SRF6DCC:
                srf6, xinit, yinit = poly.compute_srf6dcc(val)
                encoded_poly, rest = poly.chaincode_base64_encoder(srf6, 3)
                self.data["val"] = [str(xinit), str(yinit), str(rest), encoded_poly]
            elif mode == Poly2DType.MODE_POLY2D_RS6FCC:
                rs6, low, high, xinit, yinit = poly.compute_rs6fcc(val)
                encoded_poly, rest = poly.chaincode_base64_encoder(rs6, 3)
                self.data["val"] = [
                    str(xinit),
                    str(yinit),
                    str(low),
                    str(high),
                    str(rest),
                    encoded_poly,
                ]
            else:
                self.data["val"] = list(val)
        self.data["mode"] = mode.name
        self.data["closed"] = closed
        self.type = ObjectDataType.poly2d
        if hierarchy is not None:
            if not isinstance(hierarchy, list):
                raise TypeError("Argument 'hierarchy' must be of type 'list'")
            if not all(isinstance(x, int) for x in hierarchy):
                raise TypeError(
                    "All values of argument 'hierarchy' must be of type 'int'"
                )
            self.data["hierarchy"] = hierarchy


class poly3d(ObjectDataGeometry):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        val: tuple | list,
        closed: bool,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectDataGeometry.__init__(self, name, coordinate_system, properties)
        if not isinstance(val, (tuple, list)):
            raise TypeError("Argument 'val' must be of type 'tuple' or 'list'")
        if not isinstance(closed, bool):
            raise TypeError("Argument 'closed' must be of type 'bool'")
        if isinstance(val, tuple):
            self.data["val"] = val
        elif isinstance(val, list):
            self.data["val"] = tuple(val)
        self.data["closed"] = closed
        self.type = ObjectDataType.poly3d


class cuboid(ObjectDataGeometry):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        val: tuple | list,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectDataGeometry.__init__(self, name, coordinate_system, properties)
        if val is not None:
            if not isinstance(val, (tuple, list)):
                raise TypeError("Argument 'val' must be of type 'tuple' or 'list'")
            if len(val) not in (9, 10):
                raise ValueError("Argument 'val' must have 9 or 10 elements")
            if len(val) == 9:
                self.use_quaternion = False
            else:
                self.use_quaternion = True
        if isinstance(val, tuple):
            self.data["val"] = list(val)
        elif isinstance(val, list):
            self.data["val"] = val
        else:
            self.data["val"] = None
        self.type = ObjectDataType.cuboid


class image(ObjectData):  # noqa: N801  # remove capitals in class name warning
    """
    Host the image data in buffer format.

    It can be used with any codification, although base64 and webp are suggested.

    mimeType: "image/png", "image/jpeg", .. as in
                                https://www.sitepoint.com/mime-types-complete-list/
    encoding: "base64", "ascii", .. as in
                            https://docs.python.org/2.4/lib/standard-encodings.html

    Default is base64

    OpenCV can be used to encode:
    img = cv2.imread(file_name, 1)
    compr_params = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
    result, payload = cv2.imencode('.png', img, compr_params)
    """

    def __init__(
        self,
        name: str,
        val: str,
        mime_type: str,
        encoding: str,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectData.__init__(self, name, coordinate_system, properties, None)
        if not isinstance(val, str):
            raise TypeError("Argument 'val' must be of type 'str'")
        if not isinstance(mime_type, str):
            raise TypeError("Argument 'mime_type' must be of type 'str'")
        if not isinstance(encoding, str):
            raise TypeError("Argument 'encoding' must be of type 'str'")
        self.data["val"] = val
        self.data["mime_type"] = mime_type
        self.data["encoding"] = encoding
        self.type = ObjectDataType.image


class mat(ObjectData):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        val: tuple | list,
        channels: int,
        width: int,
        height: int,
        data_type: str,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectData.__init__(self, name, coordinate_system, properties, None)
        if not isinstance(val, (tuple, list)):
            raise TypeError("Argument 'val' must be of type 'tuple' or 'list'")
        if not isinstance(width, int):
            raise TypeError("Argument 'width' must be of type 'int'")
        if not isinstance(height, int):
            raise TypeError("Argument 'height' must be of type 'int'")
        if not isinstance(channels, int):
            raise TypeError("Argument 'channels' must be of type 'int'")
        if not isinstance(data_type, str):
            raise TypeError("Argument 'dataType' must be of type 'str'")
        if len(val) != width * height * channels:
            raise ValueError("len(val) != width * height * channels")

        if isinstance(val, tuple):
            self.data["val"] = val
        elif isinstance(val, list):
            self.data["val"] = tuple(val)
        self.data["channels"] = channels
        self.data["width"] = width
        self.data["height"] = height
        self.data["data_type"] = data_type
        self.type = ObjectDataType.mat


class binary(ObjectData):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        val: str,
        data_type: str,
        encoding: str,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectData.__init__(self, name, coordinate_system, properties, None)
        if not isinstance(val, str):
            raise TypeError("Argument 'val' must be of type 'str'")
        if not isinstance(data_type, str):
            raise TypeError("Argument 'dataType' must be of type 'str'")
        if not isinstance(encoding, str):
            raise TypeError("Argument 'encoding' must be of type 'str'")
        self.data["val"] = val
        self.data["data_type"] = data_type
        self.data["encoding"] = encoding
        self.type = ObjectDataType.binary


class vec(ObjectData):  # noqa: N801  # remove capitals in class name warning
    # pylint: disable=redefined-builtin
    def __init__(
        self,
        name: str,
        val: tuple | list,
        coordinate_system: str | None = None,
        properties: dict | None = None,
        type: str | None = None,
    ):
        ObjectData.__init__(self, name, coordinate_system, properties, type)
        if not isinstance(val, (tuple, list)):
            raise TypeError("Argument 'val' must be of type 'tuple' or 'list'")
        if isinstance(val, tuple):
            self.data["val"] = val
        elif isinstance(val, list):
            self.data["val"] = tuple(val)
        self.type = ObjectDataType.vec


class point2d(ObjectDataGeometry):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        val: tuple | list,
        point_id: int | None = None,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectDataGeometry.__init__(self, name, coordinate_system, properties)
        if not isinstance(val, (tuple, list)):
            raise TypeError("Argument 'val' must be of type 'tuple' or 'list'")
        if len(val) != 2:
            raise ValueError("Argument 'val' must have 2 elements")
        if isinstance(val, tuple):
            self.data["val"] = val
        elif isinstance(val, list):
            self.data["val"] = tuple(val)
        if point_id is not None:
            if not isinstance(point_id, int):
                raise TypeError("Argument 'point_id' must be of type 'int'")
            self.data["id"] = point_id
        self.type = ObjectDataType.point2d


class point3d(ObjectDataGeometry):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        val: tuple | list,
        point_id: int | None = None,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectDataGeometry.__init__(self, name, coordinate_system, properties)
        if not isinstance(val, (tuple, list)):
            raise TypeError("Argument 'val' must be of type 'tuple' or 'list'")
        if len(val) != 3:
            raise ValueError("Argument 'val' must have 3 elements")

        if isinstance(val, tuple):
            self.data["val"] = val
        elif isinstance(val, list):
            self.data["val"] = tuple(val)
        if point_id is not None:
            if not isinstance(point_id, int):
                raise TypeError("Argument 'id' must be of type 'int'")
            self.data["id"] = point_id
        self.type = ObjectDataType.point3d


class GeometricReference(ObjectDataGeometry):
    def __init__(
        self,
        name: str,
        val: list,
        reference_type: ObjectDataType,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectDataGeometry.__init__(self, name, coordinate_system, properties)
        if not isinstance(reference_type, ObjectDataType):
            raise TypeError("Argument 'reference_type' must be of type ' ObjectDataType'")
        self.data["reference_type"] = reference_type.name
        if val is not None:
            if not isinstance(val, list):
                raise TypeError("Argument 'val' must be of type ' list'")
            self.data["val"] = val


class LineReference(GeometricReference):
    def __init__(
        self,
        name: str,
        val: list,
        reference_type: ObjectDataType,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        GeometricReference.__init__(
            self, name, val, reference_type, coordinate_system, properties
        )


class AreaReference(GeometricReference):
    def __init__(
        self,
        name: str,
        val: list,
        reference_type: ObjectDataType,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        GeometricReference.__init__(
            self, name, val, reference_type, coordinate_system, properties
        )


class VolumeReference(GeometricReference):
    def __init__(
        self,
        name: str,
        val: list,
        reference_type: ObjectDataType,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        GeometricReference.__init__(
            self, name, val, reference_type, coordinate_system, properties
        )


class mesh(ObjectDataGeometry):  # noqa: N801  # remove capitals in class name warning
    def __init__(
        self,
        name: str,
        coordinate_system: str | None = None,
        properties: dict | None = None,
    ):
        ObjectDataGeometry.__init__(self, name, coordinate_system, properties)
        self.pid = "0"
        self.eid = "0"
        self.aid = "0"
        self.vid = "0"
        self.data["point3d"] = {}
        self.data["line_reference"] = {}
        self.data["area_reference"] = {}
        self.type = ObjectDataType.mesh

    # Vertex
    def add_vertex(
        self, p3d: point3d, id: str | None = None  # pylint: disable=redefined-builtin
    ) -> str:
        if not isinstance(p3d, point3d):
            raise TypeError("Argument 'p3d' must be of type ' point3d'")

        # If an id is provided use it
        if id is not None:
            # If it already exists, this is an update call
            if id in self.data["point3d"]:
                # The id already exists: substitute
                idx = id
            else:
                idx = id
                self.pid = str(int(idx) + 1)
        else:
            idx = self.pid
            self.pid = str(int(self.pid) + 1)

        self.data.setdefault("point3d", {})
        self.data["point3d"][idx] = p3d.data
        return idx

    # Edge
    def add_edge(
        self,
        lref: LineReference,
        id: str | None = None,  # pylint: disable=redefined-builtin
    ) -> str:
        if not isinstance(lref, LineReference):
            raise TypeError("Argument 'lref' must be of type ' LineReference'")

        if id is not None:
            if id in self.data["line_reference"]:
                idx = id
            else:
                idx = id
                self.eid = str(int(idx) + 1)
        else:
            idx = self.eid
            self.eid = str(int(self.eid) + 1)

        self.data.setdefault("line_reference", {})
        self.data["line_reference"][idx] = lref.data
        return idx

    # Area
    def add_area(
        self,
        aref: AreaReference,
        id: str | None = None,  # pylint: disable=redefined-builtin
    ) -> str:
        if not isinstance(aref, AreaReference):
            raise TypeError("Argument 'aref' must be of type ' AreaReference'")

        if id is not None:
            if id in self.data["area_reference"]:
                idx = id
            else:
                idx = id
                self.aid = str(int(idx) + 1)
        else:
            idx = self.aid
            self.aid = str(int(self.aid) + 1)

        self.data.setdefault("area_reference", {})
        self.data["area_reference"][idx] = aref.data
        return idx

    def get_mesh_geometry_as_string(self) -> str:
        result = "[["
        for vertex in self.data["point3d"].values():
            val = vertex["val"]
            result += "["
            for _, elem in enumerate(val):
                result += str(elem) + ","
            result += "],"
        result += "],["

        for edge in self.data["line_reference"].values():
            val = edge["val"]
            result += "["
            for _, elem in enumerate(val):
                result += str(elem) + ","
            result += "],"
        result += "],["

        for area in self.data["area_reference"].values():
            val = area["val"]
            result += "["
            for _, elem in enumerate(val):
                result += str(elem) + ","
            result += "],"
        result += "]]"

        # Clean-out commas
        result = result.replace(",]", "]")

        return result
