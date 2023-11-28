"""
Main module of VCD library.

This module contains the VCD class intended to handle OpenLabel content.
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
import json
import re
import uuid
import warnings
from enum import Enum

from jsonschema import validate as json_validate

from vcd import schema, types, utils

__pdoc__: dict[str, bool | str] = {}


class OntologyBoundaryMode(Enum):
    """Boundary list modes of ontology tags."""

    include: str = "include"
    exclude: str = "exclude"


class TagType(Enum):
    """Tag's first-level categories as defined in the OpenLABEL standard."""

    administrative = 1
    odd = 2
    behaviour = 3
    custom = 4


class ResourceUID:
    """
    Class to add extra UIDs to an element according to its representation in another resource.

    E.g. A Lane or Road object labeled in VCD can correspond to a Lane or Road element in an
    OpenDrive file.

    Then the OpenDrive file path is added with

    ```
    res_opendrive_uidopenlabel.add_resource("../resources/xodr/multi_intersections.xodr")
    ```

    And any object added can add the element UID at the resource using this ResourceUID class

    ```
    openlabel.add_object("road1", "road", res_uid=ResourceUID(res_opendrive_uid, 217))
    ```

    Attributes:
        resource_uid (int, str): The UID of the resource file.

        id_at_resource (int, str): The UID of the element in the resource.
    """

    def __init__(self, resource_uid: int | str | None, id_at_resource: int | str):
        __pdoc__["ResourceUID.__init__"] = False
        """Create ResourceUID object using the resource UID and its UID at the resource."""
        # this is the UID of the resource file
        self.resource_uid = UID(resource_uid)
        # this is the UID of the element in the resource
        self.id_at_resource = UID(id_at_resource)

    def as_dict(self) -> dict:
        """Convert ResourceUID content as dictionary."""
        return {self.resource_uid.as_str(): self.id_at_resource.as_str()}


class ElementType(Enum):
    """Elements of VCD (Object, Action, Event, Context, Relation, Tag)."""

    object = 1
    action = 2
    event = 3
    context = 4
    relation = 5
    tag = 6


class StreamType(Enum):
    """Type of stream (sensor)."""

    camera = 1
    lidar = 2
    radar = 3
    gps_imu = 4
    other = 5


class RDF(Enum):
    """Type of RDF agent (subject or object)."""

    subject = 1
    object = 2


class FrameIntervals:
    """
    FrameIntervals class aims to simplify management of frame intervals.

    A frame interval represents the frames where the element has presence.
    For example, an object can be detected only in certain frames, thus the
    bounding box that represents its location should be limited to those frames.
    If an element has not a frame or frame interval defined, it is considered
    a constant element and thus applied to all the frames registered in the
    data structure. Some examples of static elements: Reference systems,
    weather definitions, camera parameters or video quality parameters.

    To define the frame interval, we can specify a single frame value as an
    integer (frame_value=3) relating the element to a certain frame.
    Additionally, we can define a consecutive frame ranges using tuples
    (frame_interval=(0, 10)).

    The following is an example of the different possible values:

    ```
    import vcd.core as core
    import vcd.types as types

    # 1.- Create VCD
    vcd = core.OpenLABEL()

    # 2.- Create some content
    uid_marcos = vcd.add_object(name='marcos', semantic_type='#Person')
    vcd.add_object_data(uid=uid_marcos, object_data=types.num('age', 37.0), frame_value=None)
    vcd.add_object_data(uid=uid_marcos, object_data=types.boolean('is_blinking', True),
                                                                 frame_value=2)
    vcd.add_object_data(uid=uid_marcos, object_data=types.boolean('is_detected', True),
                                                                 frame_value=(0, 4))

    vcd.save("tmp_vcd_sample.json")

    ```

    Attributes:
            frame_value (int,tuple,dict,list,None): The frame indices related with the
                                                        element. If None, the elements is
                                                        set as constant.
                                                        (Default value = None)
            fuse (bool): If True, the intervals defined in _frame_value_ will be combined
                        before being stored in the data structure. (Default value = False)
    """

    def __init__(
        self,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        fuse: bool = False,
    ):
        """Create a Frame interval object."""
        self.fis_dict = []
        self.fis_num = []

        if frame_value is not None:
            if isinstance(frame_value, int):
                self.fis_dict = [{"frame_start": frame_value, "frame_end": frame_value}]
                self.fis_num = [(frame_value, frame_value)]
            elif isinstance(frame_value, tuple):
                # Then, frame_value is a tuple (one single frame interval)
                self.fis_num = [frame_value]
                self.fis_dict = utils.as_frame_intervals_array_dict(self.fis_num)
            elif isinstance(frame_value, dict):
                # User provided a single dict
                self.fis_dict = [frame_value]
                self.fis_num = utils.as_frame_intervals_array_tuples(self.fis_dict)
            elif isinstance(frame_value, list):
                if len(frame_value) == 0:
                    return
                if all(isinstance(x, tuple) for x in frame_value):
                    # Then, frame_value is an array of tuples
                    self.fis_dict = utils.as_frame_intervals_array_dict(frame_value)
                    if fuse:
                        self.fis_dict = utils.fuse_frame_intervals(self.fis_dict)
                    self.fis_num = utils.as_frame_intervals_array_tuples(self.fis_dict)
                elif all(isinstance(x, list) for x in frame_value):
                    # This is possibly a list of list, e.g. [[0, 10], [12, 15]], instead
                    # of the above case list of tuple
                    self.fis_dict = utils.as_frame_intervals_array_dict(frame_value)
                    if fuse:
                        self.fis_dict = utils.fuse_frame_intervals(self.fis_dict)
                    self.fis_num = utils.as_frame_intervals_array_tuples(self.fis_dict)
                elif all(isinstance(x, dict) for x in frame_value):
                    # User provided a list of dict
                    self.fis_dict = utils.as_frame_intervals_array_dict(frame_value)
                    if fuse:
                        self.fis_dict = utils.fuse_frame_intervals(self.fis_dict)
                    self.fis_num = utils.as_frame_intervals_array_tuples(self.fis_dict)
            else:
                warnings.warn("ERROR: Unsupported FrameIntervals format.", Warning, 2)

    def empty(self) -> bool:
        """Get flag if object is empty."""
        # if len(self.fis_dict) == 0 or len(self.fis_num) == 0:
        return not self.fis_num

    def get_dict(self) -> list[dict]:
        """Get frame interval as dict."""
        return self.fis_dict

    def get(self) -> list:
        """Get frame interval."""
        return self.fis_num

    def get_length(self) -> int:
        """Get frame interval length."""
        length = 0
        for fi in self.fis_num:
            length += fi[1] + 1 - fi[0]
        return length

    def rm_frame(self, frame_num: int):
        """
        Remove frame from frame interval.

        Args:
          frame_num (int): Number of frame to remove.
        """
        self.fis_dict = utils.rm_frame_from_frame_intervals(self.fis_dict, frame_num)
        self.fis_num = utils.as_frame_intervals_array_tuples(self.fis_dict)

    def union(self, frame_intervals: FrameIntervals) -> FrameIntervals:
        """
        Merge two frame intervals.

        Args:
          frame_intervals (FrameIntervals): Input frame intervals.

        Returns:
          FrameIntervals: intervals result of the union.
        """
        # Several quick cases
        if not self.fis_dict:
            return frame_intervals
        if frame_intervals.get() == self.get():
            return frame_intervals

        # Generic case
        fis_union = utils.fuse_frame_intervals(self.fis_dict + frame_intervals.get_dict())
        return FrameIntervals(fis_union)

    def intersection(self, frame_intervals: FrameIntervals) -> FrameIntervals:
        """
        Find the intersection of the two frame intervals.

        Args:
          frame_intervals (FrameIntervals): Input frame intervals.

        Returns:
          FrameIntervals: intervals result of the intersection.
        """
        fis_int = utils.intersection_between_frame_interval_arrays(
            self.fis_num, frame_intervals.get()
        )
        return FrameIntervals(fis_int)

    def equals(self, frame_intervals: FrameIntervals) -> bool:
        """
        Check if frame interval is the same as the interval provided.

        Args:
          frame_intervals (FrameIntervals): Input frame intervals.

        Returns:
            bool: True if the input frame interval is the same as this interval.
        """
        fis_int = self.intersection(frame_intervals)
        fis_union = self.union(frame_intervals)

        if fis_int.get_length() == fis_union.get_length():
            return True

        return False

    def contains(self, frame_intervals: FrameIntervals) -> bool:
        """
        Check if frame interval contains the interval provided.

        Args:
          frame_intervals (FrameIntervals): Input frame intervals.

        Returns:
            bool: True if the input frame interval is contained in this interval.
        """
        fis_int = self.intersection(frame_intervals)
        return bool(fis_int.get_length() == frame_intervals.get_length())

    def is_contained_by(self, frame_intervals: FrameIntervals) -> bool:
        """
        Check if frame interval is contained in the interval provided.

        Args:
          frame_intervals (FrameIntervals): Input frame intervals.

        Returns:
            bool: True if the input frame interval contains this interval.
        """
        fis_int = self.intersection(frame_intervals)
        return bool(fis_int.get_length() == self.get_length())

    def get_outer(self) -> dict | None:
        """
        Get the outmost frame interval.

        Returns:
          dict, None: a dict with the outer frame interval or None if no frame interval
                       is defined.
        """
        return utils.get_outer_frame_interval(self.fis_dict)

    def has_frame(self, frame_num: int) -> bool:
        """
        Get if this frame interval has provided frame.

        Args:
          frame_num (int): the frame number to check.

        Returns:
          bool: True if this frame interval has the frame number.
        """
        return utils.is_inside_frame_intervals(frame_num, self.fis_num)

    def to_str(self) -> str:
        """
        Transform frame interval into text string.

        Returns:
          str: The frame interval un text format.
        """
        text = "["
        for fi in self.fis_num:
            text += "(" + str(fi[0]) + "," + str(fi[1]) + ")"
        text += "]"

        return text


class UID:
    """
    This is a helper class that simplifies management of UIDs.

    Public functions permits the user to introduce either int or string values as UIDs
    Internal functions create the UID objects to ensure the proper format is used where
    needed

    Attributes:
          val (int, str, None): value of the UID to be stored in the UID object.
    """

    def __init__(self, val: int | str | None = None):
        __pdoc__["UID.__init__"] = False
        """Create UID object."""
        exp = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        if val is None:
            # Void uid
            self.__set("", -1, False)
        else:
            if isinstance(val, int):
                self.__set(str(val), val, False)
            elif isinstance(val, str):
                if val == "":
                    self.__set("", -1, False)
                else:
                    if val.strip("-").isnumeric():  # this holds true for "-3" and "3"
                        self.__set(val, int(val), False)
                    elif bool(re.match(exp, val)):
                        self.__set(val, -1, True)
                    else:
                        warnings.warn("ERROR: Unsupported UID string type.", Warning, 2)
                        self.__set("", -1, False)
            else:
                warnings.warn("ERROR: Unsupported UID type.", Warning, 2)
                self.__set("", -1, False)

    def __set(
        self,
        uid_str: str = "",
        uid_int: int = -1,
        is_uuid: bool = False,
    ):
        self.uid_str = uid_str
        self.uid_int = uid_int
        self.uuid = is_uuid

    def is_uuid(self) -> bool:
        """Check if the UID is UUID."""
        return self.uuid

    def as_str(self) -> str:
        """Get UID as string."""
        return self.uid_str

    def as_int(self) -> int | None:
        """Get UID as int."""
        if self.is_uuid():
            warnings.warn(
                "ERROR: This UID is not numeric, can't call getAsInt.", Warning, 2
            )
            return None

        return self.uid_int

    def is_none(self) -> bool:
        """Check if UID is empty."""
        return bool(self.uid_int == -1 and self.uid_str == "")


class SetMode(Enum):
    """The SetMode specifies how added content is inserted."""

    union = 1
    """Is the default value, and determines that any new call to add functions (e.g.
    add_object, or add_action_data), actually adds content, extending the frame_intervals of
    the recipient container to the  limits defined by the newly provided frame_intervals,
    effectively extending it to the union of frame_intervals (existing plus new), substituting
    the content which already existed with coincident frame (and name, uid, etc)."""
    replace = 2
    """Acts replacing old content by new, potentially removing frames if the newly provided
    frame_intervals are shorter than the existing ones."""


class VCD:  # pylint: disable=too-many-public-methods
    """
    VCD class as main container of VCD content.

    Exposes functions to add Elements, to get information and to remove data. Internally
    manages all information as Python dictionaries, and can map data into JSON strings.
    """

    ##################################################
    # Constructor
    ##################################################
    def __init__(self):
        __pdoc__["VCD.__init__"] = False
        """Create an empty VCD object."""
        self.use_uuid = False
        self.data = {}
        self.schema = {}
        self.__lastUID = {}
        # Init the VCD structures
        self.reset()

    def load_from_json(self, json_data: dict, validation: bool = False):
        """
        Load VCD from JSON data.

        Args:
          json_data (str): JSON containing the data in OpenLabel format.

          validation (bool): Set to True if validation against the schema is required.
                             (Default value = False)
        """
        # Check VERSION and call converters if needed
        if "vcd" in json_data:
            # This is 4.x
            if "version" in json_data["vcd"]:
                # This is 4.1.2
                if json_data["vcd"]["version"] == "4.2.0":
                    # This is VCD 4.2.0
                    warnings.warn(
                        "WARNING: Converting VCD 4.2.0 to OpenLABEL 1.0.0."
                        " A full revision is recommended.",
                        Warning,
                        2,
                    )
                    # Convert frame entries to int
                    frames = json_data["vcd"]["frames"]
                    if frames:  # So frames is not empty
                        json_data["vcd"]["frames"] = {
                            int(key): value for key, value in frames.items()
                        }

                    self.reset()  # to init object
                    ConverterVCD420toOpenLabel100(
                        json_data, self
                    )  # self is modified internally

                elif json_data["vcd"]["version"] == "4.1.0":
                    # This is VCD 4.1.0
                    raise RuntimeError(
                        "ERROR: VCD 4.1.0 to OpenLABEL 1.0.0 conversion is not implemented."
                    )
            elif "metadata" in json_data["vcd"]:
                if "schema_version" in json_data["vcd"]["metadata"]:
                    schema_version = json_data["vcd"]["metadata"]["schema_version"]
                    if schema_version in ("4.3.0", "4.3.1"):
                        # This is VCD 4.3.0 or VCD 4.3.1
                        self.data = json_data

                        warnings.warn(
                            "WARNING: Converting VCD 4.3.<0,1> to OpenLABEL 1.0.0. "
                            "A revision is recommended (specially for transforms and "
                            "coordinate systems).",
                            Warning,
                            2,
                        )

                        # 'vcd' content was loaded, need to change root to 'openlabel'
                        # Let's substitute the root from 'vcd' to 'openlabel', and update
                        # the schema version
                        self.data["openlabel"] = self.data.pop("vcd")
                        self.data["openlabel"]["metadata"][
                            "schema_version"
                        ] = schema.openlabel_schema_version

                        if validation:
                            if not hasattr(self, "schema"):
                                self.schema = schema.openlabel_schema
                            # Raises errors if not validated
                            json_validate(instance=self.data, schema=self.schema)

                        # In VCD 4.3.1 uids are strings, because they can be numeric
                        # strings, or UUIDs but frames are still ints, so let's parse
                        # frame numbers as integers
                        if "frames" in self.data["openlabel"]:
                            frames = self.data["openlabel"]["frames"]
                            if frames:  # So frames is not empty
                                self.data["openlabel"]["frames"] = {
                                    int(key): value for key, value in frames.items()
                                }
                    else:
                        raise RuntimeError(
                            "ERROR: This vcd file does not seem to be 4.3.0, 4.3.1"
                        )
                else:
                    raise RuntimeError(
                        "ERROR: This vcd file does not seem to be 4.3.0, 4.3.1 nor 4.2.0"
                    )
        elif "openlabel" in json_data:
            # This is an OpenLABEL file
            schema_version = json_data["openlabel"]["metadata"]["schema_version"]
            if schema_version == "1.0.0":
                # This is OpenLABEL 1.0.0 (are equivalent)
                self.data = json_data
                if validation:
                    if not hasattr(self, "schema"):
                        self.schema = schema.openlabel_schema
                    # Raises errors if not validated
                    json_validate(instance=self.data, schema=self.schema)

                # In OpenLABEL 1.0.0 uids are strings, because they can be numeric strings,
                # or UUIDs but frames are still indexed by ints, so let's parse frame
                # numbers as integers
                if "frames" in self.data["openlabel"]:
                    frames = self.data["openlabel"]["frames"]
                    if frames:  # So frames is not empty
                        self.data["openlabel"]["frames"] = {
                            int(key): value for key, value in frames.items()
                        }
            else:
                raise RuntimeError(
                    "ERROR: This OpenLABEL file has version different than 1.0.0. "
                    "This API is incompatible."
                )
        else:
            raise RuntimeError(
                'ERROR: This JSON file does not have "vcd" nor "openlabel" at root level.'
            )

        # Final set-up
        self.__compute_last_uid()

    def load_from_string(self, string: str, validation: bool = False):
        """
        Load VCD from string data.

        Args:
          string (str): Text string containing the data in OpenLabel format.
          validation (bool): set to True if validation against the schema is required.
                            (Default value = False)
        """
        json_data = json.loads(string)
        self.load_from_json(json_data, validation)

    def load_from_file(self, file_name: str, validation: bool = False):
        """
        Load VCD from file.

        Args:
          file_name (str): Text string containing the path to the input file.
          validation (bool): Set to True if validation against the schema is required.
                             (Default value = False)

        Raises:
          ValueError: if _file_name_ is empty or None
        """
        if file_name is None or file_name == "":
            raise ValueError("File Name is necessary to load VCD data from file.")
        # Load from file
        with open(file_name, encoding="utf-8") as json_file:
            json_data = json.load(
                json_file
            )  # Open without converting strings to integers

        self.load_from_json(json_data, validation)

    def set_use_uuid(self, val: bool):
        """
        Set the use of unique UID.

        Args:
          val (bool): Set to True if use of UUID is required.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(val, bool):
            raise TypeError("Argument 'val' must be of type 'bool'")
        self.use_uuid = val

    def reset(self):
        """Reset VCD internal data."""
        # Main VCD data
        self.data = {"openlabel": {}}
        self.data["openlabel"]["metadata"] = {}
        self.data["openlabel"]["metadata"][
            "schema_version"
        ] = schema.openlabel_schema_version

        # Schema information
        self.schema = schema.openlabel_schema

        # Additional auxiliary structures
        self.__lastUID = {}
        self.__lastUID[ElementType.object] = -1
        self.__lastUID[ElementType.action] = -1
        self.__lastUID[ElementType.event] = -1
        self.__lastUID[ElementType.context] = -1
        self.__lastUID[ElementType.relation] = -1
        self.__lastUID[ElementType.tag] = -1

    ##################################################
    # Private API: inner functions
    ##################################################
    def __get_uid_to_assign(self, element_type: ElementType, uid: UID) -> UID:
        if not isinstance(element_type, ElementType):
            raise TypeError("Argument 'element_type' must be of type 'ElementType'")
        if not isinstance(uid, UID):
            raise TypeError("Argument 'uid' must be of type 'UID'")
        if uid.is_none():
            if self.use_uuid:
                # Let's use UUIDs
                uid_to_assign = UID(str(uuid.uuid4()))
            else:
                # Let's use integers
                self.__lastUID[element_type] += 1
                uid_to_assign = UID(self.__lastUID[element_type])
        else:
            # uid is not None
            if not uid.is_uuid():
                # Ok, user provided a number, let's proceed
                if uid.as_int() > self.__lastUID[element_type]:
                    self.__lastUID[element_type] = uid.as_int()
                    uid_to_assign = UID(self.__lastUID[element_type])
                else:
                    uid_to_assign = uid
            else:
                # This is a UUID
                self.use_uuid = True
                uid_to_assign = uid

        return uid_to_assign

    def __set_vcd_frame_intervals(self, frame_intervals: FrameIntervals):
        if not isinstance(frame_intervals, FrameIntervals):
            raise TypeError("Argument 'frame_intervals' must be of type 'FrameIntervals'")
        if not frame_intervals.empty():
            self.data["openlabel"]["frame_intervals"] = frame_intervals.get_dict()

    def __update_vcd_frame_intervals(self, frame_intervals: FrameIntervals):
        # This function creates the union of existing VCD with the input frameIntervals
        if not isinstance(frame_intervals, FrameIntervals):
            raise TypeError("Argument 'frame_intervals' must be of type 'FrameIntervals'")
        if not frame_intervals.empty():
            if "frame_intervals" not in self.data["openlabel"]:
                self.data["openlabel"]["frame_intervals"] = []
            fis_current = FrameIntervals(self.data["openlabel"]["frame_intervals"])
            fis_union = fis_current.union(frame_intervals)
            self.__set_vcd_frame_intervals(fis_union)

    def __add_frame(self, frame_num: int):
        if "frames" not in self.data["openlabel"]:
            self.data["openlabel"]["frames"] = {}
        if frame_num not in self.data["openlabel"]["frames"]:
            self.data["openlabel"]["frames"][frame_num] = {}

    def __compute_last_uid(self):
        self.__lastUID = {}
        # Read all objects and fill lastUID
        self.__lastUID[ElementType.object] = -1
        if "objects" in self.data["openlabel"]:
            for uid in self.data["openlabel"]["objects"]:
                _uuid = UID(uid)
                if not _uuid.is_uuid():
                    if int(uid) > self.__lastUID[ElementType.object]:
                        self.__lastUID[ElementType.object] = int(uid)

        self.__lastUID[ElementType.action] = -1
        if "actions" in self.data["openlabel"]:
            for uid in self.data["openlabel"]["actions"]:
                _uuid = UID(uid)
                if not _uuid.is_uuid():
                    if int(uid) > self.__lastUID[ElementType.action]:
                        self.__lastUID[ElementType.action] = int(uid)

        self.__lastUID[ElementType.event] = -1
        if "events" in self.data["openlabel"]:
            for uid in self.data["openlabel"]["events"]:
                _uuid = UID(uid)
                if not _uuid.is_uuid():
                    if int(uid) > self.__lastUID[ElementType.event]:
                        self.__lastUID[ElementType.event] = int(uid)

        self.__lastUID[ElementType.context] = -1
        if "contexts" in self.data["openlabel"]:
            for uid in self.data["openlabel"]["contexts"]:
                _uuid = UID(uid)
                if not _uuid.is_uuid():
                    if int(uid) > self.__lastUID[ElementType.context]:
                        self.__lastUID[ElementType.context] = int(uid)

        self.__lastUID[ElementType.relation] = -1
        if "relations" in self.data["openlabel"]:
            for uid in self.data["openlabel"]["relations"]:
                _uuid = UID(uid)
                if not _uuid.is_uuid():
                    if (
                        int(uid) > self.__lastUID[ElementType.relation]
                    ):  # uid is a string!
                        self.__lastUID[ElementType.relation] = int(uid)

    def __add_frames(
        self, frame_intervals: FrameIntervals, element_type: ElementType, uid: UID
    ):
        if not isinstance(frame_intervals, FrameIntervals):
            raise TypeError("Argument 'frame_intervals' must be of type 'FrameIntervals'")
        if not isinstance(element_type, ElementType):
            raise TypeError("Argument 'element_type' must be of type 'ElementType'")
        if not isinstance(uid, UID):
            raise TypeError("Argument 'uid' must be of type 'UID'")
        if frame_intervals.empty():
            return

        # Loop over frames and add
        fis = frame_intervals.get()
        for fi in fis:
            for f in range(fi[0], fi[1] + 1):
                # Add frame
                self.__add_frame(f)
                # Add element entry
                frame = self.get_frame(f)
                frame.setdefault(element_type.name + "s", {})
                frame[element_type.name + "s"].setdefault(uid.as_str(), {})

    def __set_element(
        self,
        element_type: ElementType,
        name: str | None,
        semantic_type: str,
        frame_intervals: FrameIntervals,
        uid: UID,
        ont_uid: UID,
        coordinate_system: str | None,
        set_mode: SetMode,
        res_uid: ResourceUID | None,
        **kwargs: str,
    ) -> UID:
        if not isinstance(uid, UID):
            raise TypeError("Argument 'uid' must be of type 'UID'")
        if not isinstance(ont_uid, UID):
            raise TypeError("Argument 'ont_uid' must be of type 'UID'")
        if not isinstance(frame_intervals, FrameIntervals):
            raise TypeError("Argument 'frame_intervals' must be of type 'FrameIntervals'")
        if not isinstance(set_mode, SetMode):
            raise TypeError("Argument 'set_mode' must be of type 'SetMode'")
        if coordinate_system is not None:
            if not isinstance(coordinate_system, str):
                raise TypeError("Argument 'coordinate_system' must be of type 'str'")
        if res_uid is not None:
            if not isinstance(res_uid, ResourceUID):
                raise TypeError("Argument 'res_uid' must be of type 'ResourceUID'")

        fis = frame_intervals
        if set_mode == SetMode.union:
            # Union means fusion, we are calling this function to "add" content, not to
            # remove any
            fis_existing = self.get_element_frame_intervals(element_type, uid.as_str())
            fis = fis_existing.union(frame_intervals)

        # 0.- Get uid_to_assign
        # note: private functions use UID type for uids
        uid_to_assign = self.__get_uid_to_assign(element_type, uid)

        # 1.- Set the root entries and frames entries
        self.__set_element_at_root_and_frames(
            element_type,
            name,
            semantic_type,
            fis,
            uid_to_assign,
            ont_uid,
            coordinate_system,
            res_uid,
        )

        # 2.- Kwargs
        # Add any additional custom properties
        element = self.data["openlabel"][element_type.name + "s"][uid_to_assign.as_str()]
        for key, value in kwargs.items():
            element[key] = value

        return uid_to_assign

    def __set_element_at_root_and_frames(
        self,
        element_type: ElementType,
        name: str | None,
        semantic_type: str | None,
        frame_intervals: FrameIntervals,
        uid: UID,
        ont_uid: UID,
        coordinate_system: str | None,
        res_uid: ResourceUID | None,
    ):
        # 1.- Copy from existing or create new entry (this copies everything, including
        # element_data)
        # element_data_pointers and frame intervals
        uidstr = uid.as_str()
        # note: public functions use int or str for uids
        element_existed = self.has(element_type, uidstr)
        self.data["openlabel"].setdefault(element_type.name + "s", {})
        self.data["openlabel"][element_type.name + "s"].setdefault(uidstr, {})
        element = self.data["openlabel"][element_type.name + "s"][uidstr]

        fis_old = FrameIntervals()
        if "frame_intervals" in element:
            fis_old = FrameIntervals(element["frame_intervals"])

        # 2.- Copy from arguments
        if name is not None:
            element["name"] = name
        if semantic_type is not None:
            element["type"] = semantic_type
        if not frame_intervals.empty() or (element_existed and not fis_old.empty()):
            # So, either the newFis has something, or the fisOld had something (in which
            # case needs to be substituted)
            # Under the previous control, no 'frame_intervals' field is added to newly
            # created static elements -> should 'frame_intervals' be mandatory
            element["frame_intervals"] = frame_intervals.get_dict()
        if not ont_uid.is_none() and self.get_ontology(ont_uid.as_str()):
            element["ontology_uid"] = ont_uid.as_str()
        if res_uid is not None:
            resource_uid = res_uid.resource_uid
            if not resource_uid.is_none() and self.get_resource(resource_uid.as_str()):
                element["resource_uid"] = res_uid.as_dict()
        if coordinate_system is not None and self.has_coordinate_system(
            coordinate_system
        ):
            element["coordinate_system"] = coordinate_system

        # 2.bis.- For Relations force to have rdf_objects and rdf_subjects entries
        # (to be compliant with schema)
        if element_type is ElementType.relation:
            if "rdf_subjects" not in element:
                element["rdf_subjects"] = []
            if "rdf_objects" not in element:
                element["rdf_objects"] = []

        # 3.- Reshape element_data_pointers according to this new frame intervals
        if element_type.name + "_data_pointers" in element:
            edps = element[element_type.name + "_data_pointers"]
            for edp_name in edps:
                # NOW, we have to UPDATE frame intervals of pointers because we have
                # modified the frame_intervals of the element itself, and
                # If we compute the intersection frame_intervals, we can copy that into
                # element_data_pointers frame intervals
                fis_int = FrameIntervals()
                if not frame_intervals.empty():
                    fis_int = frame_intervals.intersection(
                        FrameIntervals(edps[edp_name]["frame_intervals"])
                    )

                # Update the pointers
                element.setdefault(element_type.name + "_data_pointers", {})
                element[element_type.name + "_data_pointers"][edp_name] = edps[edp_name]
                element[element_type.name + "_data_pointers"][edp_name][
                    "frame_intervals"
                ] = fis_int.get_dict()

        # 4.- Now set at frames
        if not frame_intervals.empty():
            # 2.1.- There is frame_intervals specified
            if not element_existed:
                # 2.1.a) Just create the new element
                self.__add_frames(frame_intervals, element_type, uid)
                self.__update_vcd_frame_intervals(frame_intervals)
            else:
                # 2.1.b) This is a substitution: depending on the new frame_intervals,
                # we may need to delete/add frames
                # Add
                fis_new = frame_intervals
                for fi in fis_new.get():
                    for f in range(fi[0], fi[1] + 1):
                        is_inside = fis_old.has_frame(f)
                        if not is_inside:
                            # New frame is not inside -> let's add this frame
                            fi_ = FrameIntervals(f)
                            self.__add_frames(fi_, element_type, uid)
                            self.__update_vcd_frame_intervals(fi_)
                # Remove
                if element_existed and fis_old.empty():
                    # Ok, the element was originally static (thus with fisOld empty)
                    # so potentially there are pointers of the element in all frames
                    # (in case there are frames)
                    # Now the element is declared with a specific frame intervals. Then
                    # we first need to remove all element entries (pointers) in all
                    # OTHER frames
                    vcd_frame_intervals = self.get_frame_intervals()
                    if not vcd_frame_intervals.empty():
                        for fi in vcd_frame_intervals.get():
                            for f in range(fi[0], fi[1] + 1):
                                if not fis_new.has_frame(
                                    f
                                ):  # Only for those OTHER frames not those just added
                                    elements_in_frame = self.data["openlabel"]["frames"][
                                        f
                                    ][element_type.name + "s"]
                                    if uidstr in elements_in_frame:
                                        del elements_in_frame[uidstr]
                                        if len(elements_in_frame) == 0:
                                            del self.data["openlabel"]["frames"][f][
                                                element_type.name + "s"
                                            ]
                                            if (
                                                len(self.data["openlabel"]["frames"][f])
                                                == 0
                                            ):
                                                self.__rm_frame(f)

                # Next loop for is for the case fis_old wasn't empty, so we just need to
                # remove old content
                for fi in fis_old.get():
                    for f in range(fi[0], fi[1] + 1):
                        is_inside = fis_new.has_frame(f)
                        if not is_inside:
                            # Old frame not inside new ones -> let's remove this frame
                            elements_in_frame = self.data["openlabel"]["frames"][f][
                                element_type.name + "s"
                            ]
                            del elements_in_frame[uidstr]
                            if len(elements_in_frame) == 0:
                                del self.data["openlabel"]["frames"][f][
                                    element_type.name + "s"
                                ]
                                if len(self.data["openlabel"]["frames"][f]) == 0:
                                    self.__rm_frame(f)
        else:
            # 2.2.- The element is declared as static
            if (
                element_type is not ElementType.relation
            ):  # frame-less relation must remain frame-less
                vcd_frame_intervals = self.get_frame_intervals()
                if not vcd_frame_intervals.empty():
                    # ... but VCD has already other elements or info that have established
                    # some frame intervals
                    # The element is then assumed to exist in all frames: let's add a
                    # pointer into all frames
                    self.__add_frames(vcd_frame_intervals, element_type, uid)

            # But, if the element existed previously, and it was dynamic, there is already
            # information inside frames.
            # If there is element_data at frames, they are removed
            if not fis_old.empty():
                self.rm_element_data_from_frames(element_type, uid, fis_old)

                # Additionally, we need to remove element entries at frames, and frames
                # entirely to clean-up
                for fi in fis_old.get():
                    for f in range(fi[0], fi[1] + 1):
                        elements_in_frame = self.data["openlabel"]["frames"][f][
                            element_type.name + "s"
                        ]
                        del elements_in_frame[uidstr]
                        # Clean-up
                        if len(elements_in_frame) == 0:
                            del self.data["openlabel"]["frames"][f][
                                element_type.name + "s"
                            ]
                            if len(self.data["openlabel"]["frames"][f]) == 0:
                                self.__rm_frame(f)

    def __set_element_data(
        self,
        element_type: ElementType,
        uid: UID,
        element_data: types.ObjectData,
        frame_intervals: FrameIntervals,
        set_mode: SetMode,
    ):
        if not isinstance(element_type, ElementType):
            raise TypeError("Argument 'element_type' must be of type 'ElementType'")
        if not isinstance(uid, UID):
            raise TypeError("Argument 'uid' must be of type 'UID'")
        if not isinstance(frame_intervals, FrameIntervals):
            raise TypeError("Argument 'frame_intervals' must be of type 'FrameIntervals'")
        if not isinstance(set_mode, SetMode):
            raise TypeError("Argument 'set_mode' must be of type 'SetMode'")

        # 0.- Checks
        if not self.has(element_type, uid.as_str()):
            warnings.warn(
                "WARNING: Trying to set element_data for a non-existing element.",
                Warning,
                2,
            )
            return
        element = self.get_element(element_type, uid.as_str())
        if element is None:
            return

        # Read existing data about this element, so we can call __set_element
        name: str | None = element.get("name")
        semantic_type: str = element["type"]
        ont_uid = UID(None)
        cs = None
        if "ontology_uid" in element:
            ont_uid = UID(element["ontology_uid"])
        res_uid = None
        if "resource_uid" in element:
            res_uid = ResourceUID(
                element["resource_uid"].keys()[0], element["resource_uid"].values()[0]
            )
        if "coordinate_system" in element:
            cs = element["coordinate_system"]

        if "coordinate_system" in element_data.data:
            if not self.has_coordinate_system(element_data.data["coordinate_system"]):
                warnings.warn(
                    "WARNING: Trying to set element_data with a non-declared coordinate system.",
                    Warning,
                    2,
                )
                return

        if (
            frame_intervals.empty()
            and set_mode == SetMode.union
            and not isinstance(element_data, types.mesh)
        ):
            set_mode = SetMode.replace

        if set_mode == SetMode.replace:
            # Extend also the container Element just in case the frame_interval of this
            # element_data is beyond it removes/creates frames if needed
            # This call is to modify an existing element_data, which may imply removing
            # some frames
            if not frame_intervals.empty():
                fis_existing = FrameIntervals(element["frame_intervals"])
                fis_new = frame_intervals
                fis_union = fis_existing.union(fis_new)
                self.__set_element(
                    element_type,
                    name,
                    semantic_type,
                    fis_union,
                    uid,
                    ont_uid,
                    cs,
                    set_mode,
                    res_uid,
                )
                self.__set_element_data_content_at_frames(
                    element_type, uid, element_data, frame_intervals
                )
            else:
                # This is a static element_data. If it was declared dynamic before, let's
                # remove it self.__set_element(element_type, name, semantic_type,
                # frame_intervals, uid, ont_uid, cs, set_mode)
                if self.has_element_data(element_type, uid.as_str(), element_data):
                    fis_old = self.get_element_data_frame_intervals(
                        element_type, uid.as_str(), element_data.data["name"]
                    )
                    if not fis_old.empty():
                        self.rm_element_data_from_frames_by_name(
                            element_type, uid, element_data.data["name"], fis_old
                        )
                self.__set_element_data_content(element_type, element, element_data)
            # Set the pointers
            self.__set_element_data_pointers(
                element_type, uid, element_data, frame_intervals
            )
        else:  # set_mode = SetMode.union
            # This call is to add element_data to the element, substituting content if
            # overlap, otherwise adding
            # First, extend also the container Element just in case the frame_interval
            # of this element_data is beyond the currently existing frame_intervals of
            # the Element internally computes the union
            self.__set_element(
                element_type,
                name,
                semantic_type,
                frame_intervals,
                uid,
                ont_uid,
                cs,
                set_mode,
                res_uid,
            )

            if not frame_intervals.empty():
                fis_existing = FrameIntervals()
                if element_type.name + "_data_pointers" in element:
                    edp = element[element_type.name + "_data_pointers"]
                    if element_data.data["name"] in edp:
                        fis_existing = FrameIntervals(
                            edp[element_data.data["name"]]["frame_intervals"]
                        )
                fis_new = frame_intervals
                fis_union = fis_existing.union(fis_new)

                # Dynamic
                if element is not None:
                    # It is not a simple call with the union of frame intervals
                    # We need to substitute the content for just this frame_interval,
                    # without modifying the rest that must stay as it was
                    # Loop over the specified frame_intervals to create or substitute
                    # the content
                    self.__set_element_data_content_at_frames(
                        element_type, uid, element_data, fis_new
                    )

                # Set the pointers (but the pointers we have to update using the union)
                self.__set_element_data_pointers(
                    element_type, uid, element_data, fis_union
                )
            elif isinstance(element_data, types.mesh):
                # This is only for mesh case that can have this static part
                # (because it is an object data type which is both static and dynamic)
                self.__set_element_data_content(element_type, element, element_data)

    def __set_element_data_content_at_frames(
        self,
        element_type: ElementType,
        uid: UID,
        element_data: types.ObjectData,
        frame_intervals: FrameIntervals,
    ):
        # Loop over the specified frame_intervals to create or substitute the content
        # Create entries of the element_data at frames
        fis = frame_intervals.get()
        for fi in fis:
            for f in range(fi[0], fi[1] + 1):
                # Add element_data entry
                frame = self.get_frame(f)
                if frame is None:
                    self.__add_frame(f)
                    frame = self.get_frame(f)

                frame.setdefault(element_type.name + "s", {})
                frame[element_type.name + "s"].setdefault(uid.as_str(), {})
                element = frame[element_type.name + "s"][uid.as_str()]
                self.__set_element_data_content(element_type, element, element_data)

    # @staticmethod
    # def __set_tag_data_content(tag, tag_data):
    #     tag.setdefault("val", {})
    #     tag["val"].setdefault(tag_data.type.name, [])
    #     list_aux = tag["val"][tag_data.type.name]
    #     pos_list = [
    #         idx
    #         for idx, val in enumerate(list_aux)
    #         if val["name"] == tag_data.data["name"]
    #     ]
    #     if len(pos_list) == 0:
    #         tag["val"][tag_data.type.name].append(tag_data.data)
    #     else:
    #         pos = pos_list[0]
    #         tag["val"][tag_data.type.name][pos] = tag_data.data

    @staticmethod
    def __set_element_data_content(
        element_type: ElementType, element: dict, element_data: types.ObjectData
    ):
        # Adds the element_data to the corresponding container
        # If an element_data with same name exists, it is substituted
        element.setdefault(element_type.name + "_data", {})
        el_data_dict: dict = element[element_type.name + "_data"]
        el_data_dict.setdefault(element_data.type.name, [])

        # Find if element_data already there
        if "name" in element_data.data:
            list_aux = element[element_type.name + "_data"][element_data.type.name]
            pos_list = [
                idx
                for idx, val in enumerate(list_aux)
                if val["name"] == element_data.data["name"]
            ]
        else:
            pos_list = []

        if len(pos_list) == 0:
            # Not found, then just push this new element data
            element[element_type.name + "_data"][element_data.type.name].append(
                element_data.data
            )
        else:
            # Found: let's substitute
            pos = pos_list[0]
            element[element_type.name + "_data"][element_data.type.name][
                pos
            ] = element_data.data

    def __set_element_data_pointers(
        self,
        element_type: ElementType,
        uid: UID,
        element_data: types.ObjectData,
        frame_intervals: FrameIntervals | None,
    ):
        if not isinstance(element_type, ElementType):
            raise TypeError("Argument 'element_type' must be of type 'ElementType'")

        # For Tags, let's ignore element_data_pointers
        if element_type == ElementType.tag:
            return

        if not isinstance(uid, UID):
            raise TypeError("Argument 'uid' must be of type 'UID'")

        self.data["openlabel"][element_type.name + "s"][uid.as_str()].setdefault(
            element_type.name + "_data_pointers", {}
        )
        edp = self.data["openlabel"][element_type.name + "s"][uid.as_str()][
            element_type.name + "_data_pointers"
        ]
        edp[element_data.data["name"]] = {}
        edp[element_data.data["name"]]["type"] = element_data.type.name
        if frame_intervals is None:
            edp[element_data.data["name"]]["frame_intervals"] = []
        else:
            edp[element_data.data["name"]]["frame_intervals"] = frame_intervals.get_dict()
        if "attributes" in element_data.data:
            edp[element_data.data["name"]]["attributes"] = {}
            for attr_type in element_data.data["attributes"]:
                # attr_type might be 'boolean', 'text', 'num', or 'vec'
                for attr in element_data.data["attributes"][attr_type]:
                    edp[element_data.data["name"]]["attributes"][attr["name"]] = attr_type

    # ### DEPRECATED
    # def __add_element(
    #     self,
    #     element_type: ElementType,
    #     name: str,
    #     semantic_type: str = "",
    #     frame_value: int | list | None = None,
    #     uid: int | str | None = None,
    #     ont_uid: int | str | None = None,
    #     coordinate_system: str = None,
    #     set_mode: SetMode = SetMode.union,
    #     res_uid: int | str | None = None,
    #     **kwargs: str,
    # ) -> str:
    #     """
    #     Add an element to the current data structure considering the defined parameters.

    #     Args:
    #         element_type (ElementType): The type corresponding to the defined element.
    #         name (str): A name defined by the user to refer to the element.
    #         semantic_type (str, optional): The semantic type defined by the user for the
    #                                        element. Defaults to ''.
    #         frame_value (int,tuple,dict,list,None): If the element represents something
    #                                                    that only happens or appears in a
    #                                                    single frame or image, this value
    #                                                    represents the frame index in the
    #                                                    image stream. If this value is _None_,
    #                                                    the element is assumed present during
    #                                                    the entire image sequence. For more
    #                                                    details, check _FrameInterval_
    #                                                    documentation. (Default value = None)
    #         uid (int | str | None, optional): The Unique IDentifier given to this element.
    #                                           (Default value = None)
    #         ont_uid (int | str | None, optional): The Unique IDentifier given to the related
    #                                               ontology. (Default value = None)
    #         coordinate_system (str, optional): The name of the coordinated system used as
    #                                            reference. The named coordinate system should
    #                                            be previously included using
    #                                            _add_coordinate_system_ function.
    #                                            (Default value = None)
    #         set_mode (SetMode, optional): Defines if the current element must be added or
    #                                       should replace previous data. See _SetMode_ for
    #                                       more details. Defaults to SetMode.union.
    #         res_uid (int | str | None, optional): _description_. (Default value = None)

    #     Returns:
    #         UID (str): The Unique IDentification of the generated element.
    #     """
    #     return self.__set_element(
    #         element_type,
    #         name,
    #         semantic_type,
    #         FrameIntervals(frame_value),
    #         UID(uid),
    #         UID(ont_uid),
    #         coordinate_system,
    #         set_mode,
    #         res_uid,
    #         **kwargs,
    #     ).as_str()

    def __rm_frame(self, frame_num: int):
        # This function deletes a frame entry from frames, and updates VCD accordingly
        if "frames" in self.data["openlabel"]:
            if frame_num in self.data["openlabel"]["frames"]:
                del self.data["openlabel"]["frames"][frame_num]
            if len(self.data["openlabel"]["frames"]) == 0:
                del self.data["openlabel"]["frames"]

        # Remove from VCD frame intervals
        if "frame_intervals" in self.data["openlabel"]:
            fis_dict = self.data["openlabel"]["frame_intervals"]
            fis_dict_new = utils.rm_frame_from_frame_intervals(fis_dict, frame_num)

            # Now substitute
            if len(fis_dict_new) == 0:
                del self.data["openlabel"]["frame_intervals"]
            else:
                self.data["openlabel"]["frame_intervals"] = fis_dict_new

    # def __compute_data_pointers(self):
    #     # WARNING! This function might be extremely slow
    #     # It does loop over all frames, and updates data pointers at objects, actions, etc
    #     # It is useful to convert from VCD 4.2.0 into VCD 4.3.1
    #     # (use converter.ConverterVCD420toVCD430)

    #     # Looping over frames and creating the necessary data_pointers
    #     if "frame_intervals" in self.data["openlabel"]:
    #         fis = self.data["openlabel"]["frame_intervals"]
    #         for fi in fis:
    #             for frame_num in range(fi["frame_start"], fi["frame_end"] + 1):
    #                 frame = self.get_frame(frame_num)
    #                 for element_type in ElementType:
    #                     if (
    #                         element_type.name + "s" in frame
    #                     ):  # e.g. "objects", "actions"...
    #                         for uid, element in frame[element_type.name + "s"].items():
    #                             if element_type.name + "_data" in element:
    #                                 # So this element has element_data in this frame and
    #                                 # then we need to update the element_data_pointer at
    #                                 # the root we can safely assume it already exists

    #                                 # First, let's create a element_data_pointer at the
    #                                 # root
    #                                 self.data["openlabel"][element_type.name + "s"][
    #                                     uid
    #                                 ].setdefault(element_type.name + "_data_pointers", {})
    #                                 edp = self.data["openlabel"][element_type.name + "s"][
    #                                     uid
    #                                 ]
    #                                 [element_type.name + "_data_pointers"]

    #                                 # Let's loop over the element_data
    #                                 for ed_type, ed_array in element[
    #                                     element_type.name + "_data"
    #                                 ].items():
    #                                     # e.g. ed_type is 'bbox', ed_array is the array
    #                                     # of such bboxes content
    #                                     for element_data in ed_array:
    #                                         name = element_data["name"]
    #                                         edp.setdefault(
    #                                             name, {}
    #                                         )  # this element_data may already exist
    #                                         edp[name].setdefault(
    #                                             "type", ed_type
    #                                         )  # e.g. 'bbox'
    #                                         edp[name].setdefault(
    #                                             "frame_intervals", []
    #                                         )  # in case it does not exist
    #                                         fis_exist = FrameIntervals(
    #                                             edp[name]["frame_intervals"]
    #                                         )
    #                                         fis_exist.union(
    #                                             FrameIntervals(frame_num)
    #                                         )  # So, let's fuse with this frame
    #                                         edp[name][
    #                                             "frame_intervals"
    #                                         ] = fis_exist.get_dict()  # overwrite
    #                                         # No need to manage attributes

    ##################################################
    # Public API: add, update
    ##################################################
    def add_file_version(self, version: str):
        """
        Add VCD version.

        Usually this refers to the OpenLabel version schema the data is compliant.

        Args:
          version (str): Version text string.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(version, str):
            raise TypeError("Version has to be a string")

        if "metadata" not in self.data["openlabel"]:
            self.data["openlabel"]["metadata"] = {}
        self.data["openlabel"]["metadata"]["file_version"] = version

    def add_metadata_properties(self, properties: dict):
        """
        Add VCD metadata properties.

        Args:
          properties (dict): Input properties to be added to the metadata section of VCD.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(properties, dict):
            raise TypeError("Argument 'properties' must be of type 'dict'")

        prop: dict = self.data["openlabel"]["metadata"]
        prop.update(properties)

    def add_name(self, name: str):
        """
        Add name to VCD metadata.

        Args:
          name (str): Name of the VCD.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(name, str):
            raise TypeError("Argument 'name' must be of type 'str'")

        if "metadata" not in self.data["openlabel"]:
            self.data["openlabel"]["metadata"] = {}
        self.data["openlabel"]["metadata"]["name"] = name

    def add_annotator(self, annotator: str):
        """
        Add annotator to VCD metadata.

        Args:
          annotator (str): Text string of the annotator description to be added to the
                           metadata section.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(annotator, str):
            raise TypeError("Argument 'annotator' must be of type 'str'")

        if "metadata" not in self.data["openlabel"]:
            self.data["openlabel"]["metadata"] = {}
        self.data["openlabel"]["metadata"]["annotator"] = annotator

    def add_comment(self, comment: str):
        """
        Add comment to VCD metadata.

        Args:
          comment (str): Comment to be added to the metadata section of the VCD.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(comment, str):
            raise TypeError("Argument 'comment' must be of type 'str'")

        if "metadata" not in self.data["openlabel"]:
            self.data["openlabel"]["metadata"] = {}
        self.data["openlabel"]["metadata"]["comment"] = comment

    def __add_ontology(
        self,
        ontology_name: str,
        boundary_list: list[str] | None = None,
        boundary_mode: OntologyBoundaryMode | None = None,
        **kwargs: str,
    ) -> str | None:
        """
        Add new ontology to VCD.

        New implementation for consistency with OpenLABEL schema.

        Args:
          ontology_name (str): Text string containing the URI or name of the ontology
          boundary_list (list[str], None): Boundary tags to include or exclude.
                                           This list will added in _boundary_list_
                                           attribute of the ontology. (Default value = None)
          boundary_mode (OntologyBoundaryMode, None): Boundary list mode. Should be a value
                                                      of enum `OntologyBoundaryMode` or None.
                                                      (Default value = None)
          **kwargs (str): Additional properties to add to the ontology.

        Returns:
            str | None: The UID of the new added ontology. None if the ontology already
                        exists.

        Raises:
          TypeError: if input arguments are not of annotated types.
          AttributeError: when either 'boundary_list' or 'boundary_mode' are not given.
        """
        if not isinstance(ontology_name, str):
            raise TypeError("Argument 'ontology_name' must be of type 'str'")

        if (boundary_list is not None and boundary_mode is None) or (
            boundary_list is None and boundary_mode is not None
        ):
            raise AttributeError(
                "Both 'boundary_list' and 'boundary_mode' are required "
                "to define ontology boundaries."
            )

        if (
            boundary_list is not None
            and not isinstance(boundary_list, list)
            and not all(isinstance(elem, str) for elem in boundary_list)
        ):
            raise TypeError("Argument 'boundary_list' must be of type 'list[str]'")

        if boundary_mode is not None and not isinstance(
            boundary_mode, OntologyBoundaryMode
        ):
            raise TypeError(
                "Argument 'boundary_mode' must be of type 'OntologyBoundaryMode'"
            )

        self.data["openlabel"].setdefault("ontologies", {})
        for ont_uid in self.data["openlabel"]["ontologies"]:
            if self.data["openlabel"]["ontologies"][ont_uid] == ontology_name:
                warnings.warn("WARNING: adding an already existing ontology", Warning, 2)
                return None
        length = len(self.data["openlabel"]["ontologies"])

        if boundary_list is None and boundary_mode is None and len(kwargs) == 0:
            self.data["openlabel"]["ontologies"][str(length)] = ontology_name
        else:
            self.data["openlabel"]["ontologies"][str(length)] = {"uri": ontology_name}
            if boundary_list is not None and boundary_mode is not None:
                self.data["openlabel"]["ontologies"][str(length)][
                    "boundary_list"
                ] = boundary_list
                self.data["openlabel"]["ontologies"][str(length)][
                    "boundary_mode"
                ] = boundary_mode.value

        # Add additional arguments
        for key, value in kwargs.items():
            self.data["openlabel"]["ontologies"][str(length)][key] = value

        return str(length)

    def add_ontology(
        self,
        ontology_name: str,
        subset_include: list[str] | None = None,
        subset_exclude: list[str] | None = None,
        **kwargs: str,
    ) -> str | None:
        """
        Add new ontology to VCD (Kept for backward compatibility).

        Args:
          ontology_name (str): Text string containing the URI or name of the ontology
          subset_include (list[str], None): Subset tags to include.
                                            This list will included in _boundary_list_
                                            attribute of the ontology and _boundary_mode_
                                            will be set to 'include'.
                                            Not compatible with parameter `subset_exclude`
                                            (Default value = None)
          subset_exclude (list[str], None): Subset tags to exclude.
                                            This list will included in _boundary_list_
                                            attribute of the ontology and _boundary_mode_
                                            will be set to 'exclude'.
                                            Not compatible with parameter `subset_include`
                                            (Default value = None)
          **kwargs (str): Additional properties to add to the ontology.

        Returns:
            str | None: The UID of the new added ontology. None if the ontology already
                        exists.

        Raises:
          TypeError: if input arguments are not of annotated types.
          AttributeError: if argument 'subset_include' and 'subset_exclude' are given.
        """
        if not isinstance(ontology_name, str):
            raise TypeError("Argument 'ontology_name' must be of type 'str'")

        if subset_include is not None and subset_exclude is not None:
            raise AttributeError(
                "Argument 'subset_include' and 'subset_exclude' "
                "cannot be defined at the same time. "
                "Only pass one of the two Argument. "
            )

        if (
            subset_include is not None
            and not isinstance(subset_include, list)
            and not all(isinstance(elem, str) for elem in subset_include)
        ):
            raise TypeError(
                "Argument 'subset_include' must be of type 'list[str]' or 'None'"
            )

        if (
            subset_exclude is not None
            and not isinstance(subset_exclude, list)
            and not all(isinstance(elem, str) for elem in subset_exclude)
        ):
            raise TypeError(
                "Argument 'subset_exclude' must be of type 'list[str]' or 'None'"
            )

        boundary_list = None
        boundary_mode = None
        if subset_include is not None:
            boundary_list = subset_include
            boundary_mode = OntologyBoundaryMode.include
        elif subset_exclude is not None:
            boundary_list = subset_exclude
            boundary_mode = OntologyBoundaryMode.exclude

        ont_uid = self.__add_ontology(
            ontology_name=ontology_name,
            boundary_list=boundary_list,
            boundary_mode=boundary_mode,
            **kwargs,
        )
        return ont_uid

    def add_resource(self, resource_name: str) -> str | None:
        """
        Add new resource.

        Args:
          resource_name (str): Name of the resource.

        Returns:
          str | None: A string with the UID of the created resource. None if the resource
                      already exist.
        """
        self.data["openlabel"].setdefault("resources", {})
        for res_uid in self.data["openlabel"]["resources"]:
            if self.data["openlabel"]["resources"][res_uid] == resource_name:
                warnings.warn("WARNING: adding an already existing resource", Warning, 2)
                return None
        length = len(self.data["openlabel"]["resources"])
        self.data["openlabel"]["resources"][str(length)] = resource_name
        return str(length)

    def add_coordinate_system(
        self,
        name: str,
        cs_type: types.CoordinateSystemType,
        parent_name: str = "",
        pose_wrt_parent: types.PoseData | None = None,
    ):
        """
        Add new coordinate system.

        Args:
          name (str): name identifier to assign to this coordinate system.
          cs_type (vcd.types.CoordinateSystemType): type of coordinate system.
          parent_name (str): name of parent coordinate system. (Default value = "")
          pose_wrt_parent (vcd.types.PoseData, None): can be used to quickly add a list
                                                  containing the 4x4 matrix. However,
                                                  argument pose can be used to add any
                                                  type (`vcd.types.TransformDataType`)
                                                  of PoseData object (created with
                                                  `vcd.types.PoseData`)
                                                  (Default value = None)
        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(cs_type, types.CoordinateSystemType):
            raise TypeError(
                "Argument 'cs_type' must be of type 'vcd.types.CoordinateSystemType'"
            )
        # Create entry
        self.data["openlabel"].setdefault("coordinate_systems", {})
        self.data["openlabel"]["coordinate_systems"][name] = {
            "type": cs_type.name,
            "parent": parent_name,
            "children": [],
        }

        # Add Pose data
        if pose_wrt_parent is not None:
            if not isinstance(pose_wrt_parent, types.PoseData):
                raise TypeError(
                    "Argument 'pose_wrt_parent' must be of type 'vcd.types.PoseData'"
                )
            self.data["openlabel"]["coordinate_systems"][name].update(
                {"pose_wrt_parent": pose_wrt_parent.data}
            )

        # Update parents
        if parent_name != "":
            found = False
            for n, cs in self.data["openlabel"]["coordinate_systems"].items():
                if n == parent_name:
                    found = True
                    cs["children"].append(name)
            if not found:
                warnings.warn(
                    "WARNING: Creating a coordinate system with a non-defined parent "
                    "coordinate system. "
                    "Coordinate systems must be introduced in order.",
                    Warning,
                    2,
                )

    def add_transform(self, frame_num: int, transform: types.Transform):
        """
        Add new coordinate system.

        Args:
          frame_num (int): frame number to apply transformation.
          transform (vcd.types.Transform): desired transformation.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(frame_num, int):
            raise TypeError("Argument 'frame_num' must be of type 'int'")
        if not isinstance(transform, types.Transform):
            raise TypeError("Argument 'transform' must be of type 'vcd.types.Transform'")

        # this function internally checks if the frame already exists
        self.__add_frame(frame_num)
        self.data["openlabel"]["frames"][frame_num].setdefault("frame_properties", {})
        self.data["openlabel"]["frames"][frame_num]["frame_properties"].setdefault(
            "transforms", {}
        )
        self.data["openlabel"]["frames"][frame_num]["frame_properties"][
            "transforms"
        ].update(transform.data)

    def add_stream(
        self, stream_name: str, uri: str, description: str, stream_type: StreamType
    ):
        """
        Add new data stream.

        Args:
          stream_name (str): name of the stream to add.
          uri (str): URI of the sensor stream data.
          description (str): text description of the stream.
          stream_type (StreamType):type of stream.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(stream_name, str):
            raise TypeError("Argument 'stream_name' must be of type 'str'")
        if not isinstance(uri, str):
            raise TypeError("Argument 'uri' must be of type 'str'")
        if not isinstance(description, str):
            raise TypeError("Argument 'description' must be of type 'str'")

        self.data["openlabel"].setdefault("streams", {})
        self.data["openlabel"]["streams"].setdefault(stream_name, {})
        if isinstance(stream_type, StreamType):
            self.data["openlabel"]["streams"][stream_name] = {
                "description": description,
                "uri": uri,
                "type": stream_type.name,
            }
        elif isinstance(stream_type, str):
            self.data["openlabel"]["streams"][stream_name] = {
                "description": description,
                "uri": uri,
                "type": stream_type,
            }

    def add_frame_properties(
        self,
        frame_num: int,
        timestamp: str | float | None = None,
        properties: dict | None = None,
    ):
        """
        Add properties to the desired frame.

        Args:
          frame_num (int): frame number.
          timestamp (str, float, None):  (Default value = None)
          properties (dict, None): properties to be added to frame. (Default value = None)

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        # this function internally checks if the frame already exists
        self.__add_frame(frame_num)
        self.__update_vcd_frame_intervals(FrameIntervals(frame_num))
        self.data["openlabel"]["frames"][frame_num].setdefault("frame_properties", {})
        if timestamp is not None:
            if not isinstance(timestamp, (str, float)):
                raise TypeError("Argument 'timestamp' must be of type 'str | float'")
            self.data["openlabel"]["frames"][frame_num]["frame_properties"][
                "timestamp"
            ] = timestamp

        if properties is not None:
            if not isinstance(properties, dict):
                raise TypeError("Argument 'properties' must be of type 'dict")
            self.data["openlabel"]["frames"][frame_num]["frame_properties"].update(
                properties
            )

    def add_stream_properties(
        self,
        stream_name: str,
        properties: dict | None = None,
        intrinsics: types.Intrinsics | None = None,
        stream_sync: types.StreamSync | None = None,
    ):
        """
        Add properties to the indicated stream.

        This function can be used to add stream properties. If frame_num is defined,
        the information is embedded inside 'frame_properties' of the specified frame.
        Otherwise, the information is embedded into 'stream_properties' inside 'metadata'.

        Properties of Stream should be defined as a dictionary

        Args:
          stream_name (str): stream name to add properties.
          properties (dict, None): properties dictionary to add. (Default value = None)
          intrinsics (vcd.types.Intrinsics, None): intrinsics of the stream.
                                                   (Default value = None)
          stream_sync: (vcd.types.StreamSync, None): to select the sync frame number to add
                                                     properties.  (Default value = None)

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        has_arguments = False
        if intrinsics is not None:
            if not isinstance(intrinsics, types.Intrinsics):
                raise TypeError(
                    "Argument 'intrinsics' must be of type 'vcd.types.Intrinsics'"
                )
            has_arguments = True
        if properties is not None:
            if not isinstance(properties, dict):
                raise TypeError("Argument 'properties' must be of type 'dict'")
            has_arguments = True
        if stream_sync is not None:
            if not isinstance(stream_sync, types.StreamSync):
                raise TypeError(
                    "Argument 'stream_sync' must be of type 'types.StreamSync'"
                )
            has_arguments = True
            if stream_sync.frame_vcd is not None:
                frame_num = stream_sync.frame_vcd
            else:
                frame_num = None
        else:
            frame_num = None

        if not has_arguments:
            return

        # Find if this stream is declared
        if "metadata" in self.data["openlabel"]:
            if "streams" in self.data["openlabel"]:
                if stream_name in self.data["openlabel"]["streams"]:
                    if frame_num is None:
                        # This information is static
                        self.data["openlabel"]["streams"][stream_name].setdefault(
                            "stream_properties", {}
                        )
                        if properties is not None:
                            self.data["openlabel"]["streams"][stream_name][
                                "stream_properties"
                            ].update(properties)
                        if intrinsics is not None:
                            self.data["openlabel"]["streams"][stream_name][
                                "stream_properties"
                            ].update(intrinsics.data)
                        if stream_sync is not None:
                            if stream_sync.data:
                                self.data["openlabel"]["streams"][stream_name][
                                    "stream_properties"
                                ].update(stream_sync.data)
                    else:
                        # This is information of the stream for a specific frame
                        # to add the frame in case it does not exist
                        self.__add_frame(frame_num)
                        frame = self.data["openlabel"]["frames"][frame_num]
                        frame.setdefault("frame_properties", {})
                        frame["frame_properties"].setdefault("streams", {})
                        frame["frame_properties"]["streams"].setdefault(stream_name, {})
                        frame["frame_properties"]["streams"][stream_name].setdefault(
                            "stream_properties", {}
                        )
                        if properties is not None:
                            frame["frame_properties"]["streams"][stream_name][
                                "stream_properties"
                            ].update(properties)
                        if intrinsics is not None:
                            frame["frame_properties"]["streams"][stream_name][
                                "stream_properties"
                            ].update(intrinsics.data)

                        if stream_sync is not None:
                            if stream_sync.data:
                                frame["frame_properties"]["streams"][stream_name][
                                    "stream_properties"
                                ].update(stream_sync.data)
                else:
                    warnings.warn(
                        "WARNING: Trying to add stream properties for non-existing stream. "
                        "Use add_stream first.",
                        Warning,
                        2,
                    )

    def save_frame(
        self,
        frame_num: int,
        file_name: str,
        dynamic_only: bool = True,
        pretty: bool = False,
    ):
        """
        Save data of the specified frame to a file.

        Args:
          frame_num (int): Number of frame to save in file.
          file_name (str): Path where to save the file.
          dynamic_only (bool): Only save dynamic content. (Default value = True)
          pretty (bool): True to indent the file content (Default value = False)
        """
        string = self.stringify_frame(frame_num, dynamic_only, pretty)
        with open(file_name, "w", encoding="utf8") as file:
            file.write(string)

    def save(self, file_name: str, pretty: bool = False, validate: bool = False):
        """
        Save all data to a file.

        Args:
          file_name (str): Path where to save the file.
          pretty (bool): True to indent the file content (Default value = False)
          validate (bool): True if validation against OpenLabel schema is needed before
                           saving the file. (Default value = False)
        """
        string = self.stringify(pretty, validate)
        with open(file_name, "w", encoding="utf8") as file:
            file.write(string)

    def validate(self, stringified_vcd: str):
        """
        Validate provided VCD data with respect to OpenLabel schema.

        Args:
          stringified_vcd (str): VCD data as text string

        Raises:
          jsonschema.exceptions.ValidationError: if the vcd is invalid

          jsonschema.exceptions.SchemaError: if the schema itself is invalid
        """
        temp = json.loads(stringified_vcd)
        if not hasattr(self, "schema"):
            self.schema = schema.openlabel_schema
        json_validate(instance=temp, schema=self.schema)

    def stringify(self, pretty: bool = True, validate: bool = True) -> str:
        """
        Convert VCD data into a text string.

        Args:
          pretty (bool): True to indent the file content (Default value = True)
          validate (bool): True if validation against OpenLabel schema is needed before
                           saving the file. (Default value = True)

        Returns:
          str: The VCD data as text string.
        """
        if pretty:
            stringified_vcd = json.dumps(
                self.data, indent=4, sort_keys=False, ensure_ascii=False
            )
        else:
            stringified_vcd = json.dumps(
                self.data, separators=(",", ":"), sort_keys=False, ensure_ascii=False
            )
        if validate:
            self.validate(stringified_vcd)
        return stringified_vcd

    def stringify_frame(
        self, frame_num: int, dynamic_only: bool = True, pretty: bool = False
    ) -> str:
        """
        Convert VCD data of desired frame into a text string.

        Args:
          frame_num (int): Number of frame to convert to text string.
          dynamic_only (bool): Only get dynamic content. (Default value = True)
          pretty (bool): True to indent the content (Default value = False)

        Returns:
            str: The VCD data as text string.
        """
        if frame_num not in self.data["openlabel"]["frames"]:
            warnings.warn(
                "WARNING: Trying to stringify a non-existing frame.", Warning, 2
            )
            return ""

        if dynamic_only:
            if pretty:
                return json.dumps(
                    self.data["openlabel"]["frames"][frame_num],
                    indent=4,
                    sort_keys=True,
                )

            return json.dumps(self.data["openlabel"]["frames"][frame_num])

        # Need to compose dynamic and static information into a new structure
        # Copy the dynamic info first
        # Needs to be a copy!
        frame_static_dynamic = copy.deepcopy(self.data["openlabel"]["frames"][frame_num])

        # Now the static info for objects, actions, events, contexts and relations
        # Relations can be frame-less or frame-specific
        for element_type in ElementType:
            # First, elements explicitly defined for this frame
            if element_type.name + "s" in self.data["openlabel"]["frames"][frame_num]:
                for uid, _content in self.data["openlabel"]["frames"][frame_num][
                    element_type.name + "s"
                ].items():
                    frame_static_dynamic[element_type.name + "s"][uid].update(
                        self.data["openlabel"][element_type.name + "s"][uid]
                    )
                    # Remove frameInterval entry
                    if (
                        "frame_intervals"
                        in frame_static_dynamic[element_type.name + "s"][uid]
                    ):
                        del frame_static_dynamic[element_type.name + "s"][uid][
                            "frame_intervals"
                        ]

            # But also other elements without frame intervals specified, which are
            # assumed to exist during the entire sequence, except frame-less Relations
            # which are assumed to not be associated to any frame
            if (
                element_type.name + "s" in self.data["openlabel"]
                and element_type.name != "relation"
            ):
                for uid, element in self.data["openlabel"][
                    element_type.name + "s"
                ].items():
                    frame_intervals_dict = element.get("frame_intervals")
                    if frame_intervals_dict is None or not frame_intervals_dict:
                        # So the list of frame intervals is empty -> this element
                        # lives the entire scene Let's add it to frame_static_dynamic
                        frame_static_dynamic.setdefault(
                            element_type.name + "s", {}
                        )  # in case there are no
                        # such type of elements already in this frame
                        frame_static_dynamic[element_type.name + "s"][uid] = {}
                        frame_static_dynamic[element_type.name + "s"][
                            uid
                        ] = copy.deepcopy(element)

                        # Remove frameInterval entry
                        if (
                            "frame_intervals"
                            in frame_static_dynamic[element_type.name + "s"][uid]
                        ):
                            del frame_static_dynamic[element_type.name + "s"][uid][
                                "frame_intervals"
                            ]

        if pretty:
            return json.dumps(frame_static_dynamic, indent=4, sort_keys=True)
        return json.dumps(frame_static_dynamic)

    def add_object(
        self,
        name: str,
        semantic_type: str = "",
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        uid: int | str | None = None,
        ont_uid: int | str | None = None,
        coordinate_system: str | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add an object to the current data structure considering the defined parameters.

        Args:
          name (str): A name defined by the user to refer to the object.
          semantic_type (str): The semantic type defined by the user for the object.
                              (Default value = "")
          frame_value (int,tuple,dict,list,None): If the object represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    object is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          uid (int , str, None): The Unique IDentifier given to this object.
                                 (Default value = None)
          ont_uid (int, str, None): The Unique IDentifier given to the related ontology.
                                    (Default value = None)
          coordinate_system (str): The name of the coordinated system used as reference.
                                  The named coordinate system should be previously included
                                  using `VCD.add_coordinate_system` function.
                                  (Default value = None)
          set_mode (SetMode): Defines if the current object must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID (Default value = None)
          **kwargs (str): Additional properties to add to the new object. Will be saved as
                         key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated object.
        """
        return self.__set_element(
            ElementType.object,
            name,
            semantic_type,
            FrameIntervals(frame_value),
            UID(uid),
            UID(ont_uid),
            coordinate_system,
            set_mode,
            res_uid,
            **kwargs,
        ).as_str()

    def add_action(
        self,
        name: str,
        semantic_type: str = "",
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        uid: int | str | None = None,
        ont_uid: int | str | None = None,
        coordinate_system: str | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add an action to the current data structure considering the defined parameters.

        Args:
          name (str): A name defined by the user to refer to the action.
          semantic_type (str): The semantic type defined by the user for the action.
                               (Default value = "")
          frame_value (int,tuple,dict,list,None): If the action represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    action is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          uid (int, str, None): The Unique IDentifier given to this action.
                                (Default value = None)
          ont_uid (int): The Unique IDentifier given to the related ontology.
                         (Default value = None)
          coordinate_system(str): The name of the coordinated system used as reference.
                                  The named coordinate system should be previously included
                                  using `VCD.add_coordinate_system` function.
                                  (Default value = None)
          set_mode (SetMode): Defines if the current action must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID (Default value = None)
          **kwargs (str): Additional properties to add to the new object. Will be saved as
                         key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated action.
        """
        return self.__set_element(
            ElementType.action,
            name,
            semantic_type,
            FrameIntervals(frame_value),
            UID(uid),
            UID(ont_uid),
            coordinate_system,
            set_mode,
            res_uid,
            **kwargs,
        ).as_str()

    def add_event(
        self,
        name: str,
        semantic_type: str = "",
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        uid: int | str | None = None,
        ont_uid: int | str | None = None,
        coordinate_system: str | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add an event to the current data structure considering the defined parameters.

        Args:
          name (str): A name defined by the user to refer to the event.
          semantic_type (str): The semantic type defined by the user for the event.
                               (Default value = "")
          frame_value (int,tuple,dict,list,None): If the event represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    event is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          uid (int, str, None): The Unique IDentifier given to this event.
                                (Default value = None)
          ont_uid (int): The Unique IDentifier given to the related ontology.
                         (Default value = None)
          coordinate_system(str): The name of the coordinated system used as reference.
                                  The named coordinate system should be previously included
                                  using `VCD.add_coordinate_system` function.
                                  (Default value = None)
          set_mode (SetMode): Defines if the current event must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID (Default value = None)
          **kwargs (str): Additional properties to add to the new object. Will be saved as
                         key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated event.
        """
        return self.__set_element(
            ElementType.event,
            name,
            semantic_type,
            FrameIntervals(frame_value),
            UID(uid),
            UID(ont_uid),
            coordinate_system,
            set_mode,
            res_uid,
            **kwargs,
        ).as_str()

    def add_context(
        self,
        name: str,
        semantic_type: str = "",
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        uid: int | str | None = None,
        ont_uid: int | str | None = None,
        coordinate_system: str | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add an context to the current data structure considering the defined parameters.

        Args:
          name (str): A name defined by the user to refer to the context.
          semantic_type (str): The semantic type defined by the user for the context.
                               (Default value = "")
          frame_value (int,tuple,dict,list,None): If the context represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    context is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          uid (int, str, None): The Unique IDentifier given to this context.
                                (Default value = None)
          ont_uid (int): The Unique IDentifier given to the related ontology.
                         (Default value = None)
          coordinate_system(str): The name of the coordinated system used as reference.
                                  The named coordinate system should be previously included
                                  using `VCD.add_coordinate_system` function.
                                  (Default value = None)
          set_mode (SetMode): Defines if the current context must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID (Default value = None)
          **kwargs (str): Additional properties to add to the new object. Will be saved as
                         key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated context.
        """
        return self.__set_element(
            ElementType.context,
            name,
            semantic_type,
            FrameIntervals(frame_value),
            UID(uid),
            UID(ont_uid),
            coordinate_system,
            set_mode,
            res_uid,
            **kwargs,
        ).as_str()

    def add_relation(
        self,
        name: str,
        semantic_type: str = "",
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        uid: int | str | None = None,
        ont_uid: int | str | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add an relation to the current data structure considering the defined parameters.

        Args:
          name (str): A name defined by the user to refer to the relation.
          semantic_type (str): The semantic type defined by the user for the relation.
                               (Default value = "")
          frame_value (int,tuple,dict,list,None): If the relation represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    relation is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          uid (int, str, None): The Unique IDentifier given to this relation.
                                (Default value = None)
          ont_uid (int): The Unique IDentifier given to the related ontology.
                         (Default value = None)
          coordinate_system(str): The name of the coordinated system used as reference.
                                  The named coordinate system should be previously included
                                  using `VCD.add_coordinate_system` function.
                                  (Default value = None)
          set_mode (SetMode): Defines if the current relation must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID (Default value = None)
          **kwargs (str): Additional properties to add to the new object. Will be saved as
                         key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated relation.
        """
        if set_mode == SetMode.replace and uid is not None:
            if self.has(ElementType.relation, uid):
                relation = self.data["openlabel"]["relations"][UID(uid).as_str()]
                relation["rdf_subjects"] = []
                relation["rdf_objects"] = []

        relation_uid = self.__set_element(
            ElementType.relation,
            name,
            semantic_type,
            frame_intervals=FrameIntervals(frame_value),
            uid=UID(uid),
            ont_uid=UID(ont_uid),
            set_mode=set_mode,
            coordinate_system=None,
            res_uid=res_uid,
            **kwargs,
        )
        return relation_uid.as_str()

    def add_tag(
        self,
        semantic_type: str = "",
        uid: int | str | None = None,
        ont_uid: int | str | None = None,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add a tag to the current data structure considering the defined parameters.

        Args:
          semantic_type(str): The semantic type defined by the user for the tag.
                              (Default value = "")
          uid (int, str, None): The Unique IDentifier given to this tag.
                                (Default value = None)
          ont_uid (int, str, None): The Unique IDentifier given to the related ontology.
                                    (Default value = None)
          res_uid (ResourceUID, None): External resource UID. (Default value = None)
          **kwargs (str): Additional properties to add to the new tag. Will be saved as
                         key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated tag.
        """
        return self.__set_element(
            ElementType.tag,
            None,
            semantic_type,
            FrameIntervals(None),
            UID(uid),
            UID(ont_uid),
            None,
            SetMode.union,
            res_uid,
            **kwargs,
        ).as_str()

    def add_rdf(
        self,
        relation_uid: int | str,
        rdf_type: RDF,
        element_uid: int | str,
        element_type: ElementType,
    ):
        """
        Add RDF relation to the provided element.

        Args:
          relation_uid (int , str): UID of the relation to be attached to the provided
                                    element.
          rdf_type (RDF): Type of RFD agent for the provided element.
          element_uid (int, str): Element UID to attach the relation.
          element_type (ElementType): Specify the element type. See `ElementType` enum.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(relation_uid, (int, str)):
            raise TypeError("Argument 'relation_uid' must be of type 'int | str'")
        if not isinstance(element_type, ElementType):
            raise TypeError("Argument 'element_type' must be of type 'ElementType'")
        if not isinstance(rdf_type, RDF):
            raise TypeError("Argument 'rdf_type' must be of type 'RDF'")
        if not isinstance(element_uid, (int, str)):
            raise TypeError("Argument 'element_uid' must be of type 'int | str'")

        rel_uid = UID(relation_uid)
        el_uid = UID(element_uid)
        if rel_uid.as_str() not in self.data["openlabel"]["relations"]:
            warnings.warn(
                "WARNING: trying to add RDF to non-existing Relation.", Warning, 2
            )
            return

        relation = self.data["openlabel"]["relations"][rel_uid.as_str()]
        if el_uid.as_str() not in self.data["openlabel"][element_type.name + "s"]:
            warnings.warn(
                "WARNING: trying to add RDF using non-existing Element.", Warning, 2
            )
            return

        if rdf_type == RDF.subject:
            relation.setdefault("rdf_subjects", [])
            relation["rdf_subjects"].append(
                {"uid": el_uid.as_str(), "type": element_type.name}
            )
        else:
            relation.setdefault("rdf_objects", [])
            relation["rdf_objects"].append(
                {"uid": el_uid.as_str(), "type": element_type.name}
            )

    def add_relation_object_action(
        self,
        name: str,
        semantic_type: str,
        object_uid: int | str,
        action_uid: int | str,
        relation_uid: int | str | None = None,
        ont_uid: int | str | None = None,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add Relation between an object and an action.

        The indicated object is the subject in the relation.

        Args:
          name (str): A name defined by the user to refer to the relation.
          semantic_type (str): The semantic type defined by the user for the relation.
          object_uid (int, str): The Unique IDentifier of the object in the relation.
          action_uid (int, str): The Unique IDentifier of the action in the relation.
          relation_uid (int, str, None): The Unique IDentifier given to the relation.
                                         (Default value = None)
          ont_uid (int, str, None): The Unique IDentifier given to the related ontology.
                                    (Default value = None)
          frame_value (int,tuple,dict,list,None): If the relation represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    relation is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          set_mode (SetMode): Defines if the current relation must be added or should replace
                             previous data. See `SetMode` for more details.
                             (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID. (Default value = None)
          **kwargs (str): Additional properties to add to the new relation. Will be saved as
                          key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated relation.
        """
        # Note: no need to wrap uids as UID, since all calls are public functions, and
        # no access to dict is done.
        relation_uid = self.add_relation(
            name,
            semantic_type,
            uid=relation_uid,
            ont_uid=ont_uid,
            frame_value=frame_value,
            set_mode=set_mode,
            res_uid=res_uid,
            **kwargs,
        )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.subject,
            element_uid=object_uid,
            element_type=ElementType.object,
        )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.object,
            element_uid=action_uid,
            element_type=ElementType.action,
        )

        return relation_uid

    def add_relation_action_action(
        self,
        name: str,
        semantic_type: str,
        action_uid_1: int | str,
        action_uid_2: int | str,
        relation_uid: int | str | None = None,
        ont_uid: int | str | None = None,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add Relation between two actions.

        The indicated _action_uid_1_ is the subject in the relation, while _action_uid_2_
        is the object in the relation.

        Args:
          name (str): A name defined by the user to refer to the relation.
          semantic_type (str): The semantic type defined by the user for the relation.
          action_uid_1 (int, str): The Unique IDentifier of one action in the relation.
          action_uid_2 (int, str): The Unique IDentifier of other action in the relation.
          relation_uid (int, str, None): The Unique IDentifier given to the relation.
                                         (Default value = None)
          ont_uid (int, str, None): The Unique IDentifier given to the related ontology.
                                    (Default value = None)
          frame_value (int,tuple,dict,list,None): If the relation represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    relation is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          set_mode (SetMode): Defines if the current relation must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID. (Default value = None)
          **kwargs (str): Additional properties to add to the new relation. Will be saved as
                          key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated relation.
        """
        # Note: no need to wrap uids as UID, since all calls are public functions, and
        # no access to dict is done.
        relation_uid = self.add_relation(
            name,
            semantic_type,
            uid=relation_uid,
            ont_uid=ont_uid,
            frame_value=frame_value,
            set_mode=set_mode,
            res_uid=res_uid,
            **kwargs,
        )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.subject,
            element_uid=action_uid_1,
            element_type=ElementType.action,
        )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.object,
            element_uid=action_uid_2,
            element_type=ElementType.action,
        )

        return relation_uid

    def add_relation_object_object(
        self,
        name: str,
        semantic_type: str,
        object_uid_1: int | str,
        object_uid_2: int | str,
        relation_uid: int | str | None = None,
        ont_uid: int | str | None = None,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add Relation between two objects.

        The indicated _object_uid_1_ is the subject in the relation, while _object_uid_2_
        is the object in the relation.

        Args:
          name (str): A name defined by the user to refer to the relation.
          semantic_type (str): The semantic type defined by the user for the relation.
          object_uid_1 (int, str): The Unique IDentifier of one object in the relation.
          object_uid_2 (int, str): The Unique IDentifier of other object in the relation.
          relation_uid (int, str, None): The Unique IDentifier given to the relation.
                                         (Default value = None)
          ont_uid (int, str, None): The Unique IDentifier given to the related ontology.
                                    (Default value = None)
          frame_value (int,tuple,dict,list,None): If the relation represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    relation is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          set_mode (SetMode): Defines if the current relation must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID. (Default value = None)
          **kwargs (str): Additional properties to add to the new relation. Will be saved as
                          key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated relation.
        """
        # Note: no need to wrap uids as UID, since all calls are public functions, and
        # no access to dict is done.
        relation_uid = self.add_relation(
            name,
            semantic_type,
            uid=relation_uid,
            ont_uid=ont_uid,
            frame_value=frame_value,
            set_mode=set_mode,
            res_uid=res_uid,
            **kwargs,
        )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.subject,
            element_uid=object_uid_1,
            element_type=ElementType.object,
        )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.object,
            element_uid=object_uid_2,
            element_type=ElementType.object,
        )

        return relation_uid

    def add_relation_action_object(
        self,
        name: str,
        semantic_type: str,
        action_uid: int | str,
        object_uid: int | str,
        relation_uid: int | str | None = None,
        ont_uid: int | str | None = None,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add Relation between an action and an object.

        The indicated action is the subject in the relation.

        Args:
          name (str): A name defined by the user to refer to the relation.
          semantic_type (str): The semantic type defined by the user for the relation.
          action_uid (int, str): The Unique IDentifier of the action in the relation.
          object_uid (int, str): The Unique IDentifier of the object in the relation.
          relation_uid (int, str, None): The Unique IDentifier given to the relation.
                                         (Default value = None)
          ont_uid (int, str, None): The Unique IDentifier given to the related ontology.
                                    (Default value = None)
          frame_value (int,tuple,dict,list,None): If the relation represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    relation is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          set_mode (SetMode): Defines if the current relation must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID. (Default value = None)
          **kwargs (str): Additional properties to add to the new relation. Will be saved as
                          key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated relation.
        """
        # Note: no need to wrap uids as UID, since all calls are public functions, and
        # no access to dict is done.
        relation_uid = self.add_relation(
            name,
            semantic_type,
            uid=relation_uid,
            ont_uid=ont_uid,
            frame_value=frame_value,
            set_mode=set_mode,
            res_uid=res_uid,
            **kwargs,
        )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.subject,
            element_uid=action_uid,
            element_type=ElementType.action,
        )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.object,
            element_uid=object_uid,
            element_type=ElementType.object,
        )

        return relation_uid

    def add_relation_subject_object(
        self,
        name: str,
        semantic_type: str,
        subject_type: ElementType,
        subject_uid: int | str,
        object_type: ElementType,
        object_uid: int | str,
        relation_uid: int | str | None = None,
        ont_uid: int | str | None = None,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
        res_uid: ResourceUID | None = None,
        **kwargs: str,
    ) -> str:
        """
        Add Relation between any type of element and an object.

        The indicated element is the subject in the relation.

        Args:
          name (str): A name defined by the user to refer to the relation.
          semantic_type (str): The semantic type defined by the user for the relation.
          subject_type (ElementType): The type of the subject in the relation.
          subject_uid (int, str): The Unique IDentifier of the subject in the relation.
          object_type (ElementType): The type of the object in the relation.
          object_uid (int, str): The Unique IDentifier of the object in the relation.
          relation_uid(int, str, None): The Unique IDentifier given to the relation.
                                        (Default value = None)
          ont_uid (int, str, None): The Unique IDentifier given to the related ontology.
                                    (Default value = None)
          frame_value (int,tuple,dict,list,None): If the relation represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_, the
                                                    relation is assumed present during the entire
                                                    image sequence. For more details, check
                                                    `FrameIntervals`. (Default value = None)
          set_mode (SetMode): Defines if the current relation must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
          res_uid (ResourceUID, None): External resource UID. (Default value = None)
          **kwargs (str): Additional properties to add to the new relation. Will be saved as
                          key-value dictionary.

        Returns:
          str: The Unique IDentification of the generated relation.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        # Note: no need to wrap uids as UID, since all calls are public functions, and
        # no access to dict is done.
        relation_uid = self.add_relation(
            name,
            semantic_type,
            uid=relation_uid,
            ont_uid=ont_uid,
            frame_value=frame_value,
            set_mode=set_mode,
            res_uid=res_uid,
            **kwargs,
        )
        if not isinstance(subject_type, ElementType):
            raise TypeError(
                "Argument 'subject_type' must be of type 'vcd.core.ElementType'"
            )
        if not isinstance(object_type, ElementType):
            raise TypeError(
                "Argument 'object_type' must be of type 'vcd.core.ElementType'"
            )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.subject,
            element_uid=subject_uid,
            element_type=subject_type,
        )
        self.add_rdf(
            relation_uid=relation_uid,
            rdf_type=RDF.object,
            element_uid=object_uid,
            element_type=object_type,
        )

        return relation_uid

    def add_object_data(
        self,
        uid: int | str,
        object_data: types.ObjectData,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
    ):
        """
        Add data to the specified object.

        Args:
          uid (int, str): The Unique IDentifier of the object where the data will be added.
          object_data (vcd.types.ObjectData): The _ObjectData_ element to be added.
          frame_value (int,tuple,dict,list,None): If the object data represents something that only
                                                happens or appears in a single frame or image,
                                                this value represents the frame index in the image
                                                stream. If this value is _None_, the data is
                                                assumed present during the entire image sequence.
                                                For more details, check `FrameIntervals`
                                                documentation. (Default value = None)
          set_mode (SetMode): Defines if the object data must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
        """
        self.__set_element_data(
            ElementType.object,
            UID(uid),
            object_data,
            FrameIntervals(frame_value),
            set_mode,
        )

    def add_action_data(
        self,
        uid: int | str,
        action_data: types.ObjectData,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
    ):
        """
        Add data to the specified action.

        Args:
          uid (int, str): The Unique IDentifier of the action where the data will be added.
          action_data (vcd.types.ObjectData): The _ObjectData_ element to be added.
          frame_value (int,tuple,dict,list,None):  If the action data represents something
                                                    that only happens or appears in a single
                                                    frame or image, this value represents
                                                    the frame index in the image stream.
                                                    If this value is _None_, the data is
                                                    assumed present during the entire image
                                                    sequence. For more details, check
                                                    `FrameIntervals` documentation.
                                                    (Default value = None)
          set_mode (SetMode): Defines if the action data must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
        """
        self.__set_element_data(
            ElementType.action,
            UID(uid),
            action_data,
            FrameIntervals(frame_value),
            set_mode,
        )

    def add_event_data(
        self,
        uid: int | str,
        event_data: types.ObjectData,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
    ):
        """
        Add data to the specified event.

        Args:
          uid (int, str): The Unique IDentifier of the event where the data will be added.
          event_data (vcd.types.ObjectData): The _ObjectData_ element to be added.
          frame_value (int,tuple,dict,list,None): If the event data represents something that only
                                                    happens or appears in a single frame or image,
                                                    this value represents the frame index in the
                                                    image stream. If this value is _None_,
                                                    the data is assumed present during the
                                                    entire image sequence. For more details,
                                                    check `FrameIntervals` documentation.
                                                    (Default value = None)
          set_mode (SetMode): Defines if the event data must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
        """
        self.__set_element_data(
            ElementType.event,
            UID(uid),
            event_data,
            FrameIntervals(frame_value),
            set_mode,
        )

    def add_context_data(
        self,
        uid: int | str,
        context_data: types.ObjectData,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
    ):
        """
        Add data to the specified context.

        Args:
          uid (int, str): The Unique IDentifier of the context where the data will be added.
          context_data (vcd.types.ObjectData): The _ObjectData_ element to be added.
          frame_value (int,tuple,dict,list,None): If the context data represents something
                                                    that only happens or appears in a single
                                                    frame or image, this value represents
                                                    the frame index in the image stream.
                                                    If this value is _None_, the data is
                                                    assumed present during the entire image
                                                    sequence. For more details, check
                                                    `FrameIntervals` documentation.
                                                    (Default value = None)
          set_mode (SetMode): Defines if the context data must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
        """
        self.__set_element_data(
            ElementType.context,
            UID(uid),
            context_data,
            FrameIntervals(frame_value),
            set_mode,
        )

    def add_tag_data(
        self,
        uid: int | str,
        tag_data: types.ObjectData,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
    ):
        """
        Add data to the specified tag.

        Args:
          uid (int, str): The Unique IDentifier of the tag where the data will be added.
          tag_data (vcd.types.ObjectData): The _ObjectData_ element to be added.
          frame_value (int,tuple,dict,list,None): If the tag data represents something that only
                                                    happens or appears in a single frame or
                                                    image, this value represents the frame
                                                    index in the image stream. If this value
                                                    is _None_, the data is assumed present
                                                    during the entire image sequence.
                                                    For more details, check `FrameIntervals`
                                                    documentation.
                                                    (Default value = None)
          set_mode (SetMode): Defines if the tag data must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
        """
        self.__set_element_data(
            ElementType.tag, UID(uid), tag_data, FrameIntervals(frame_value), set_mode
        )

    def add_element_data(
        self,
        element_type: ElementType,
        uid: int | str,
        element_data: types.ObjectData,
        frame_value: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | None = None,
        set_mode: SetMode = SetMode.union,
    ):
        """
        Add data to the specified element.

        It is necessary to pass the _element_type_ with its UID to add the data.

        Args:
          element_type (ElementType): Element type according to enum `ElementType`
          uid (int, str): The Unique IDentifier of the element where the data will be added.
          element_data (vcd.types.ObjectData): The _ObjectData_ element to be added.
          frame_value (int,tuple,dict,list,None): If the element data represents
                                                    something that only happens or appears
                                                    in a single frame or image, this value
                                                    represents the frame index in the image
                                                    stream. If this value is _None_, the
                                                    data is assumed present during the entire
                                                    image sequence.
                                                    For more details, check `FrameIntervals`
                                                    documentation.
                                                    (Default value = None)
          set_mode (SetMode): Defines if the object data must be added or should replace
                              previous data. See `SetMode` for more details.
                              (Default value = `SetMode.union`)
        """
        self.__set_element_data(
            element_type, UID(uid), element_data, FrameIntervals(frame_value), set_mode
        )

    ##################################################
    # Has / check if exist
    ##################################################
    def has_elements(self, element_type: ElementType) -> bool:
        """
        Check if VCD has element of specified `ElementType`.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.

        Returns:
          bool: True if any element of specified type was found.
        """
        element_type_name = element_type.name
        return element_type_name + "s" in self.data["openlabel"]

    def has_objects(self) -> bool:
        """
        Check if VCD has elements of type `ElementType.object`.

        Returns:
          bool: True if any object was found.
        """
        return "objects" in self.data["openlabel"]

    def has_actions(self) -> bool:
        """
        Check if VCD has elements of type `ElementType.action`.

        Returns:
          bool: True if any action was found.
        """
        return "actions" in self.data["openlabel"]

    def has_contexts(self) -> bool:
        """
        Check if VCD has elements of type `ElementType.context`.

        Returns:
          bool: True if any context was found.
        """
        return "contexts" in self.data["openlabel"]

    def has_events(self) -> bool:
        """
        Check if VCD has elements of type `ElementType.event`.

        Returns:
          bool: True if any event was found
        """
        return "events" in self.data["openlabel"]

    def has_relations(self) -> bool:
        """
        Check if VCD has elements of type `ElementType.relation`.

        Returns:
          bool: True if any relation was found
        """
        return "relations" in self.data["openlabel"]

    def has(self, element_type: ElementType, uid: int | str) -> bool:
        """
        Check if VCD has element of specified `ElementType` and _UID_.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the searched element.

        Returns:
          bool: True if any element was found
        """
        if element_type.name + "s" not in self.data["openlabel"]:
            return False

        uid_str = UID(uid).as_str()
        return bool(uid_str in self.data["openlabel"][element_type.name + "s"])

    def has_element_data(
        self, element_type: ElementType, uid: int | str, element_data: types.ObjectData
    ) -> bool:
        """
        Check if VCD has element data in element of specified `ElementType` and _UID_.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the searched element.
          element_data (vcd.types.ObjectData): Instance of any derived class of
                                               main 'vcd.types.ObjectData` class.

        Returns:
          bool: True if any element with the element data was found.
        """
        if not self.has(element_type, uid):
            return False

        uid_str = UID(uid).as_str()
        if (
            element_type.name + "_data_pointers"
            not in self.data["openlabel"][element_type.name + "s"][uid_str]
        ):
            return False

        name = element_data.data["name"]
        return bool(
            name
            in self.data["openlabel"][element_type.name + "s"][uid_str][
                element_type.name + "_data_pointers"
            ]
        )

    def has_frame(self, frame_num: int) -> bool:
        """
        Check if VCD has the specified frame number.

        Args:
          frame_num (int): Number for frame to check existence.

        Returns:
          bool: True if the frame number was found.
        """
        if "frames" not in self.data["openlabel"]:
            return False

        return bool(frame_num in self.data["openlabel"]["frames"])

    def has_coordinate_system(self, cs: str) -> bool:
        """
        Check if VCD has the specified coordinate system.

        Args:
          cs (str): Coordinate system name to check existence.

        Returns:
          bool: True if the coordinate system was found.
        """
        if "coordinate_systems" in self.data["openlabel"]:
            if cs in self.data["openlabel"]["coordinate_systems"]:
                return True
        return False

    def has_stream(self, stream_name: str) -> bool:
        """
        Check if VCD has the specified sensor stream.

        Args:
          stream_name (str): Stream name to check existence.

        Returns:
          bool: True if the stream was found.
        """
        if "streams" in self.data["openlabel"]:
            if stream_name in self.data["openlabel"]["streams"]:
                return True
        return False

    def relation_has_frame_intervals(self, relation_uid: int | str) -> bool:
        """
        Check if the specified relation has frame intervals.

        Relation must exist so this function can check existence pof frame intervals.

        Args:
          relation_uid (int): Relation UID where to check frame intervals existence.

        Returns:
          bool: flag if the relation has frame intervals.
        """
        rel_uid = UID(relation_uid)
        relation = self.get_relation(relation_uid)
        if relation is None:
            warnings.warn(
                "WARNING: Non-existing relation " + rel_uid.as_str(), Warning, 2
            )
            return False
        # Do the check
        if "frame_intervals" not in relation:
            return False

        return bool(len(relation["frame_intervals"]) != 0)

    ##################################################
    # Get / Read
    ##################################################
    def get_data(self) -> dict[str, dict]:
        """
        Get the raw content of the VCD data.

        Returns:
          dict[str, dict]: Dictionary with all the VCD content in OpenLabel format
        """
        return self.data

    def get_root(self) -> dict:
        """
        Get the raw content of the VCD data from the first level in the dictionary.

        In OpenLabel standard the root has the key 'openlabel'

        Returns:
          dict: Dictionary with all the VCD content in OpenLabel format.
        """
        return self.data["openlabel"]

    def get_all(self, element_type: ElementType) -> dict | None:
        """
        Get all elements of the specified `ElementType`.

        e.g. all Object's or Context's

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.

        Returns:
          dict, None: Dictionary with all elements of specified `ElementType`, None otherwise.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(element_type, ElementType):
            raise TypeError("Argument 'element_type' must be of type 'ElementType'")
        return self.data["openlabel"].get(element_type.name + "s")

    def get_element(self, element_type: ElementType, uid: int | str) -> dict | None:
        """
        Get an specific element of the specified `ElementType` and _UID_.

        e.g. element of type _object_ with _UID_: 2

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the searched element.

        Returns:
          dict, None: Dictionary if element was found, None otherwise.

        Raises:
          TypeError: if input arguments are not of annotated types.
        """
        if not isinstance(element_type, ElementType):
            raise TypeError("Argument 'element_type' must be of type 'ElementType'")

        if self.data["openlabel"].get(element_type.name + "s") is None:
            warnings.warn(
                "WARNING: trying to get a "
                + element_type.name
                + " but this VCD has none.",
                Warning,
                2,
            )
            return None

        uid_str = UID(uid).as_str()
        if uid_str in self.data["openlabel"][element_type.name + "s"]:
            return self.data["openlabel"][element_type.name + "s"][uid_str]

        warnings.warn(
            "WARNING: trying to get non-existing "
            + element_type.name
            + " with uid: "
            + uid_str,
            Warning,
            2,
        )
        return None

    def get_objects(self) -> dict:
        """Get all the objects in the VCD."""
        return self.data["openlabel"].get("objects")

    def get_actions(self) -> dict:
        """Get all the actions in the VCD."""
        return self.data["openlabel"].get("actions")

    def get_events(self) -> dict:
        """Get all the events in the VCD."""
        return self.data["openlabel"].get("events")

    def get_contexts(self) -> dict:
        """Get all the contexts in the VCD."""
        return self.data["openlabel"].get("contexts")

    def get_relations(self) -> dict:
        """Get all the relations in the VCD."""
        return self.data["openlabel"].get("relations")

    def get_object(self, uid: int | str) -> dict | None:
        """
        Get the object with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the searched element.

        Returns:
          dict, None: Dictionary if element was found, None elsewhere.
        """
        return self.get_element(ElementType.object, uid)

    def get_action(self, uid: int | str) -> dict | None:
        """
        Get the action with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the searched element.

        Returns:
          dict, None: Dictionary if element was found, None elsewhere.
        """
        return self.get_element(ElementType.action, uid)

    def get_event(self, uid: int | str) -> dict | None:
        """
        Get the event with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the searched element.

        Returns:
          dict, None: Dictionary if element was found, None elsewhere.
        """
        return self.get_element(ElementType.event, uid)

    def get_context(self, uid: int | str) -> dict | None:
        """
        Get the context with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the searched element.

        Returns:
          dict, None: Dictionary if element was found, None elsewhere.
        """
        return self.get_element(ElementType.context, uid)

    def get_relation(self, uid: int | str) -> dict | None:
        """
        Get the relation with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the searched element.

        Returns:
          dict, None: Dictionary if element was found, None elsewhere.
        """
        return self.get_element(ElementType.relation, uid)

    def get_element_uid_by_name(self, element_type: ElementType, name: str) -> str | None:
        """
        Get the _UID_ of element with specified name.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          name (str): Name of the searched element.

        Returns:
          str, None: _UID_ if element was found, None elsewhere.
        """
        if not self.has_elements(element_type):
            return None
        element_type_name = element_type.name
        elements = self.data["openlabel"][element_type_name + "s"]
        for uid, element in elements.items():
            name_element = element["name"]
            if name_element == name:
                return uid
        return None

    def get_object_uid_by_name(self, name: str) -> str | None:
        """
        Get the _UID_ of object with specified name.

        Args:
          name (str): Name of the searched object.

        Returns:
          str, None: _UID_ if object was found, None elsewhere.
        """
        return self.get_element_uid_by_name(ElementType.object, name)

    def get_action_uid_by_name(self, name: str) -> str | None:
        """
        Get the _UID_ of action with specified name.

        Args:
          name (str): Name of the searched action.

        Returns:
          str, None: _UID_ if action was found, None elsewhere.
        """
        return self.get_element_uid_by_name(ElementType.action, name)

    def get_context_uid_by_name(self, name: str) -> str | None:
        """
        Get the _UID_ of context with specified name.

        Args:
          name (str): Name of the searched context.

        Returns:
          str, None: _UID_ if context was found, None elsewhere.
        """
        return self.get_element_uid_by_name(ElementType.context, name)

    def get_event_uid_by_name(self, name: str) -> str | None:
        """
        Get the _UID_ of event with specified name.

        Args:
          name (str): Name of the searched event.

        Returns:
          str, None: _UID_ if event was found, None elsewhere.
        """
        return self.get_element_uid_by_name(ElementType.event, name)

    def get_relation_uid_by_name(self, name: str) -> str | None:
        """
        Get the _UID_ of relation with specified name.

        Args:
          name (str): Name of the searched relation.

        Returns:
          str, None: _UID_ if relation was found, None elsewhere.
        """
        return self.get_element_uid_by_name(ElementType.relation, name)

    def get_frame(self, frame_num: int) -> dict:
        """
        Get the content of specified frame number.

        Args:
          frame_num (int): Number of the searched frame.

        Returns:
          dict: The content of the specified frame number.
        """
        return self.data["openlabel"]["frames"].get(frame_num)

    def get_elements_of_type(self, element_type: ElementType, semantic_type: str) -> list:
        """
        Get all elements of specified ElementType filtered by semantic type.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          semantic_type (str): Semantic type to search in the list of elements.

        Returns:
          list: A list of founded elements _UIDs_. If no element was found the list
                will return empty.
        """
        uids_str: list[str] = []
        if element_type.name + "s" not in self.data["openlabel"]:
            return uids_str
        for uid_str, element in self.data["openlabel"][element_type.name + "s"].items():
            if element["type"] == semantic_type:
                uids_str.append(uid_str)
        return uids_str

    def get_elements_with_element_data_name(
        self, element_type: ElementType, data_name: str
    ) -> list:
        """
        Get all elements of specified type which have data with specific data name.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          data_name (str): Data name to search in the list of elements.

        Returns:
          list: A list of founded elements _UIDs_. If no element was found the list
                will return empty.
        """
        uids_str = []
        for uid_str in self.data["openlabel"][element_type.name + "s"]:
            element = self.data["openlabel"][element_type.name + "s"][uid_str]
            if element_type.name + "_data_pointers" in element:
                for name in element[element_type.name + "_data_pointers"]:
                    if name == data_name:
                        uids_str.append(uid_str)
                        break
        return uids_str

    def get_objects_with_object_data_name(self, data_name: str) -> list:
        """
        Get all objects which have data with specific data name.

        Args:
          data_name (str): Data name to search in the list of objects.

        Returns:
          list: A list of founded objects _UIDs_. If no element was found the list will
                return empty.
        """
        return self.get_elements_with_element_data_name(ElementType.object, data_name)

    def get_actions_with_action_data_name(self, data_name: str) -> list:
        """
        Get all actions which have data with specific data name.

        Args:
          data_name (str): Data name to search in the list of actions.

        Returns:
          list: A list of founded actions _UIDs_. If no element was found the list will
                return empty.
        """
        return self.get_elements_with_element_data_name(ElementType.action, data_name)

    def get_events_with_event_data_name(self, data_name: str) -> list:
        """
        Get all events which have data with specific data name.

        Args:
          data_name (str): Data name to search in the list of events.

        Returns:
          list: A list of founded events _UIDs_. If no element was found the list will
                return empty.
        """
        return self.get_elements_with_element_data_name(ElementType.event, data_name)

    def get_contexts_with_context_data_name(self, data_name: str) -> list:
        """
        Get all contexts which have data with specific data name.

        Args:
          data_name (str): Data name to search in the list of contexts.

        Returns:
          list: A list of founded contexts _UIDs_. If no element was found the list will
                return empty.
        """
        return self.get_elements_with_element_data_name(ElementType.context, data_name)

    def get_frames_with_element_data_name(
        self, element_type: ElementType, uid: int | str, data_name: str
    ) -> FrameIntervals | None:
        """
        Get all frames which have data with specific data name for a element type.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the searched element.
          data_name (str): Data name to search in the specified element.

        Returns:
          FrameIntervals, None: The frame interval of data with name _data_name_ in
                                element of type _element_type_ and _uid_. If no data was
                                found, None is returned.
        """
        uid_str = UID(uid).as_str()
        if uid_str in self.data["openlabel"][element_type.name + "s"]:
            element = self.data["openlabel"][element_type.name + "s"][uid_str]
            if element_type.name + "_data_pointers" in element:
                for name in element[element_type.name + "_data_pointers"]:
                    if name == data_name:
                        return FrameIntervals(
                            element[element_type.name + "_data_pointers"][name][
                                "frame_intervals"
                            ]
                        )
        return None

    def get_frames_with_object_data_name(
        self, uid: int | str, data_name: str
    ) -> FrameIntervals | None:
        """
        Get all frames which have object data with specific data name.

        Args:
          uid (int, str): Unique IDentifier of the searched object.
          data_name (str): Data name to search in the specified object.

        Returns:
          FrameIntervals, None: The frame interval of data with name _data_name_ in
                                object with specified _UID_. If no data was
                                found, None is returned.
        """
        return self.get_frames_with_element_data_name(ElementType.object, uid, data_name)

    def get_frames_with_action_data_name(
        self, uid: int | str, data_name: str
    ) -> FrameIntervals | None:
        """
        Get all frames which have action data with specific data name.

        Args:
          uid (int, str): Unique IDentifier of the searched action.
          data_name (str): Data name to search in the specified action.

        Returns:
          FrameIntervals, None: The frame interval of data with name _data_name_ in
                                action with specified _UID_. If no data was
                                found, None is returned.
        """
        return self.get_frames_with_element_data_name(ElementType.action, uid, data_name)

    def get_frames_with_event_data_name(
        self, uid: int | str, data_name: str
    ) -> FrameIntervals | None:
        """
        Get all frames which have event data with specific data name.

        Args:
          uid (int, str): Unique IDentifier of the searched event.
          data_name (str): Data name to search in the specified event.

        Returns:
          FrameIntervals, None: The frame interval of data with name _data_name_ in
                                event with specified _UID_. If no data was
                                found, None is returned.
        """
        return self.get_frames_with_element_data_name(ElementType.event, uid, data_name)

    def get_frames_with_context_data_name(
        self, uid: int | str, data_name: str
    ) -> FrameIntervals | None:
        """
        Get all frames which have context data with specific data name.

        Args:
          uid (int, str): Unique IDentifier of the searched context.
          data_name (str): Data name to search in the specified context.

        Returns:
          FrameIntervals, None: The frame interval of data with name _data_name_ in
                                context with specified _UID_. If no data was
                                found, None is returned.
        """
        return self.get_frames_with_element_data_name(ElementType.context, uid, data_name)

    def get_element_data_count_per_type(
        self,
        element_type: ElementType,
        uid: int | str,
        data_type: types.ObjectDataType,
        frame_num: int | None = None,
    ) -> int:
        """
        Get the number of object data instances of an specified element.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the searched element.
          data_type (vcd.types.ObjectDataType): A data type according to enum
                                               `vcd.types.ObjectDataType`
          frame_num (int, None): If a frame number is provided, the count is done on dynamic
                                 data (Default value = None).

        Returns:
            int: 0 if no such element exist or if the element does not have the data_type
                 or the count otherwise (e.g. how many "bbox" does this object have)

        Raises:
            TypeError: if input arguments are not of annotated types.
        """
        # Returns 0 if no such element exist or if the element does not have the data_type
        # Returns the count otherwise (e.g. how many "bbox" does this object have)
        if not isinstance(data_type, types.ObjectDataType):
            raise TypeError(
                "Argument 'data_type' must be of type 'vcd.types.ObjectDataType'"
            )
        uid_str = UID(uid).as_str()
        if self.has(element_type, uid):
            if frame_num is not None:
                # Dynamic info
                if not isinstance(frame_num, int):
                    raise TypeError("Argument 'frame_num' must be of type 'int'")
                frame = self.get_frame(frame_num)
                if frame is not None:
                    if element_type.name + "s" in frame:
                        if uid_str in frame[element_type.name + "s"]:
                            element = frame[element_type.name + "s"][uid_str]
                            for prop in element[element_type.name + "_data"]:
                                if prop == data_type.name:
                                    return len(element[element_type.name + "_data"][prop])
                        else:
                            return 0
                    else:
                        return 0
            else:
                # Static info
                element = self.data["openlabel"][element_type.name + "s"][uid_str]
                for prop in element[element_type.name + "_data"]:
                    if prop == data_type.name:
                        return len(element[element_type.name + "_data"][prop])
        else:
            return 0
        return 0

    def get_element_data(
        self,
        element_type: ElementType,
        uid: int | str,
        data_name: str,
        frame_num: int | None = None,
    ) -> dict | None:
        """
        Get attribute data of the specified element.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the searched element.
          data_name (str): Name of the attribute data in the element.
          frame_num (int, None): If a frame number is provided, the search of attribute data
                                 is done in the specified frame. (Default value = None)

        Returns:
          dict: The content of the data section if found, None if the attribute name was not
                found.
        """
        element_exists = self.has(element_type, uid)
        vcd_has_frames = not self.get_frame_intervals().empty()

        # don't ask for frame-specific info in a VCD without frames
        # or the element does not exist
        if (not vcd_has_frames and frame_num is not None) or not element_exists:
            return None

        frame_num_is_number = isinstance(frame_num, int)
        uid_str = UID(uid).as_str()

        element_exists_in_this_frame = False
        if frame_num is not None and frame_num_is_number:
            # The user is asking for frame-specific attributes

            found_in_frame = False
            frame = self.get_frame(frame_num)
            if frame is not None:
                if element_type.name + "s" in frame:
                    if uid_str in frame[element_type.name + "s"]:
                        element_exists_in_this_frame = True
                        element = frame[element_type.name + "s"][uid_str]
                        if element_type.name + "_data" in element:
                            for prop in element[element_type.name + "_data"]:
                                val_array = element[element_type.name + "_data"][prop]
                                for val in val_array:
                                    if val["name"] == data_name:
                                        return val
            if not found_in_frame:
                # The user has asked to get an element_data for a certain frame, but there is no
                # info about this element or element_data at this frame
                if not element_exists_in_this_frame:
                    return None
                # the element exists because of prev. ctrl
                element = self.data["openlabel"][element_type.name + "s"][uid_str]
                for prop in element[element_type.name + "_data"]:
                    val_array = element[element_type.name + "_data"][prop]
                    for val in val_array:
                        if val["name"] == data_name:
                            return val
        else:
            # The user is asking for static attributes at the root of the element
            element = self.data["openlabel"][element_type.name + "s"][
                uid_str
            ]  # the element exists because of prev. ctrl
            for prop in element[element_type.name + "_data"]:
                val_array = element[element_type.name + "_data"][prop]
                for val in val_array:
                    if val["name"] == data_name:
                        return val
        return None

    def get_object_data(
        self,
        uid: int | str,
        data_name: str,
        frame_num: int | None = None,
    ) -> dict | None:
        """
        Get attribute data of the specified object.

        Args:
          uid (int, str): Unique IDentifier of the searched object.
          data_name (str): Name of the attribute data in the object.
          frame_num (int, None): If a frame number is provided, the search of attribute data
                                 is done in the specified frame. (Default value = None)

        Returns:
          dict: The content of the data section if found, None if the attribute name was not
                found.
        """
        return self.get_element_data(ElementType.object, uid, data_name, frame_num)

    def get_action_data(
        self,
        uid: int | str,
        data_name: str,
        frame_num: int | None = None,
    ) -> dict | None:
        """
        Get attribute data of the specified action.

        Args:
          uid (int, str): Unique IDentifier of the searched action.
          data_name (str): Name of the attribute data in the action.
          frame_num (int, None): If a frame number is provided, the search of attribute data
                                 is done in the specified frame. (Default value = None)

        Returns:
          dict: The content of the data section if found, None if the attribute name was not
                found.
        """
        return self.get_element_data(ElementType.action, uid, data_name, frame_num)

    def get_event_data(
        self,
        uid: int | str,
        data_name: str,
        frame_num: int | None = None,
    ) -> dict | None:
        """
        Get attribute data of the specified event.

        Args:
          uid (int, str): Unique IDentifier of the searched event.
          data_name (str): Name of the attribute data in the event.
          frame_num (int, None): If a frame number is provided, the search of attribute data
                                 is done in the specified frame. (Default value = None)

        Returns:
          dict: The content of the data section if found, None if the attribute name was not
                found.
        """
        return self.get_element_data(ElementType.event, uid, data_name, frame_num)

    def get_context_data(
        self,
        uid: int | str,
        data_name: str,
        frame_num: int | None = None,
    ) -> dict | None:
        """
        Get attribute data of the specified context.

        Args:
          uid (int, str): Unique IDentifier of the searched context.
          data_name (str): Name of the attribute data in the context.
          frame_num (int, None): If a frame number is provided, the search of attribute data
                                 is done in the specified frame. (Default value = None)

        Returns:
          dict: The content of the data section if found, None if the attribute name was not
                found.
        """
        return self.get_element_data(ElementType.context, uid, data_name, frame_num)

    def get_element_data_pointer(
        self, element_type: ElementType, uid: int | str, data_name: str
    ) -> dict | None:
        """
        Get the _data_pointer_ section of the specified attribute and element.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the searched element.
          data_name (str): Name of the attribute data in the element.

        Returns:
          dict: The content of the data_pointer section if found, None if the attribute
                name was not found.
        """
        uid_str = UID(uid).as_str()
        if self.has(element_type, uid):
            if element_type.name + "s" in self.data["openlabel"]:
                if uid_str in self.data["openlabel"][element_type.name + "s"]:
                    element = self.data["openlabel"][element_type.name + "s"][uid_str]
                    if element_type.name + "_data_pointers" in element:
                        if data_name in element[element_type.name + "_data_pointers"]:
                            return element[element_type.name + "_data_pointers"][
                                data_name
                            ]
        else:
            warnings.warn(
                "WARNING: Asking element data from a non-existing Element.", Warning, 2
            )
        return None

    def get_element_data_frame_intervals(
        self, element_type: ElementType, uid: int | str, data_name: str
    ) -> FrameIntervals:
        """
        Get the `FrameIntervals` section of the specified attribute  and element.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the searched element.
          data_name (str): Name of the attribute data in the element.

        Returns:
          FrameIntervals, None: The `FrameIntervals` of element data if found, None if the
                                attribute name was not found.
        """
        edp = self.get_element_data_pointer(element_type, uid, data_name)
        if edp is None:
            return FrameIntervals()
        return FrameIntervals(edp["frame_intervals"])

    def get_object_data_frame_intervals(
        self, uid: int | str, data_name: str
    ) -> FrameIntervals | None:
        """
        Get the `FrameIntervals` section of the specified attribute and object.

        Args:
          uid (int, str): Unique IDentifier of the searched object.
          data_name (str): Name of the attribute data in the object.

        Returns:
          FrameIntervals, None: The `FrameIntervals` of object data if found, None if the
                                attribute name was not found.
        """
        return self.get_element_data_frame_intervals(ElementType.object, uid, data_name)

    def get_action_data_frame_intervals(
        self, uid: int | str, data_name: str
    ) -> FrameIntervals | None:
        """
        Get the `FrameIntervals` section of the specified attribute and action.

        Args:
          uid (int, str): Unique IDentifier of the searched action.
          data_name (str): Name of the attribute data in the action.

        Returns:
          FrameIntervals, None: The `FrameIntervals` of action data if found, None if the
                                attribute name was not found.
        """
        return self.get_element_data_frame_intervals(ElementType.action, uid, data_name)

    def get_event_data_frame_intervals(
        self, uid: int | str, data_name: str
    ) -> FrameIntervals | None:
        """
        Get the `FrameIntervals` section of the specified attribute and event.

        Args:
          uid (int, str): Unique IDentifier of the searched event.
          data_name (str): Name of the attribute data in the event.

        Returns:
          FrameIntervals, None: The `FrameIntervals` of event data if found, None if the
                                attribute name was not found.
        """
        return self.get_element_data_frame_intervals(ElementType.event, uid, data_name)

    def get_context_data_frame_intervals(
        self, uid: int | str, data_name: str
    ) -> FrameIntervals | None:
        """
        Get the `FrameIntervals` section of the specified attribute and context.

        Args:
          uid (int, str): Unique IDentifier of the searched context.
          data_name (str): Name of the attribute data in the context.

        Returns:
          FrameIntervals, None: The `FrameIntervals` of context data if found, None if the
                                attribute name was not found.
        """
        return self.get_element_data_frame_intervals(ElementType.context, uid, data_name)

    def get_num_elements(self, element_type: ElementType) -> int:
        """
        Get total number of elements according to the provided type.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.

        Returns:
            int: The total counter of elements, 0 if no element of _element_type_ was found.
        """
        if self.has_elements(element_type):
            return len(self.data["openlabel"][element_type.name + "s"])
        return 0

    def get_num_objects(self) -> int:
        """
        Get total number of objects.

        Returns:
            int: The total counter of objects, 0 if no element of _element_type_ was found.
        """
        return self.get_num_elements(ElementType.object)

    def get_num_actions(self) -> int:
        """
        Get total number of actions.

        Returns:
            int: The total counter of actions, 0 if no element of _element_type_ was found.
        """
        return self.get_num_elements(ElementType.action)

    def get_num_events(self) -> int:
        """
        Get total number of events.

        Returns:
            int: The total counter of events, 0 if no element of _element_type_ was found.
        """
        return self.get_num_elements(ElementType.event)

    def get_num_contexts(self) -> int:
        """
        Get total number of contexts.

        Returns:
            int: The total counter of contexts, 0 if no element of _element_type_ was found.
        """
        return self.get_num_elements(ElementType.context)

    def get_num_relations(self) -> int:
        """
        Get total number of relations.

        Returns:
            int: The total counter of relations, 0 if no element of _element_type_ was found.
        """
        return self.get_num_elements(ElementType.relation)

    def get_elements_uids(self, element_type: ElementType) -> list:
        """
        Get the list of _UIDs_ of elements of specified `ElementType`.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.

        Returns:
            list: The list of UIDs.
        """
        if self.has_elements(element_type):
            return list(self.data["openlabel"][element_type.name + "s"].keys())
        return []

    def get_ontology(self, ont_uid: int | str) -> dict | None:
        """
        Get data of ontology with specified _UID_.

        Args:
          ont_uid (int, str): The ontology _UID_

        Returns:
            dict, None: The data of the ontology if found, _None_ otherwise
        """
        ont_uid_str = UID(ont_uid).as_str()
        if "ontologies" in self.data["openlabel"]:
            if ont_uid_str in self.data["openlabel"]["ontologies"]:
                return copy.deepcopy(self.data["openlabel"]["ontologies"][ont_uid_str])
        return None

    def get_resource(self, res_uid: int | str) -> dict | None:
        """
        Get data of a resource with specified _UID_.

        Args:
          res_uid (int, str): The resource _UID_

        Returns:
            dict, None: The data of the resource if found, _None_ otherwise
        """
        res_uid_str = UID(res_uid).as_str()
        if "resources" in self.data["openlabel"]:
            if res_uid_str in self.data["openlabel"]["resources"]:
                return copy.deepcopy(self.data["openlabel"]["resources"][res_uid_str])
        return None

    def get_metadata(self) -> dict:
        """
        Get the content of metadata.

        Returns:
          dict: The data in the metadata section.
        """
        if "metadata" in self.data["openlabel"]:
            return self.data["openlabel"]["metadata"]
        return {}

    def get_coordinate_systems(self) -> dict:
        """
        Get the content of coordinate systems.

        Returns:
          dict: The data of the _coordinate_systems_ section.
        """
        if "coordinate_systems" in self.data["openlabel"]:
            return copy.deepcopy(self.data["openlabel"]["coordinate_systems"])
        return {}

    def get_coordinate_system(self, coordinate_system: str) -> dict | None:
        """
        Get the data of a coordinate system according to its _UID_.

        Args:
          coordinate_system (str): The name of the searched coordinate system.

        Returns:
            dict, None: The data of the coordinate system if found, _None_ otherwise
        """
        if self.has_coordinate_system(coordinate_system):
            return copy.deepcopy(
                self.data["openlabel"]["coordinate_systems"][coordinate_system]
            )
        return None

    def get_streams(self) -> dict:
        """
        Get the content of streams.

        Returns:
          dict: The data of the _streams_ section.
        """
        if "streams" in self.data["openlabel"]:
            return copy.deepcopy(self.data["openlabel"]["streams"])
        return {}

    def get_stream(self, stream_name: str) -> dict | None:
        """
        Get the data of a stream with specified stream name.

        Args:
          stream_name (str): Name of the searched stream.

        Returns:
          dict: The data of the stream if found, _None_ otherwise.
        """
        if self.has_stream(stream_name):
            return copy.deepcopy(self.data["openlabel"]["streams"][stream_name])
        return None

    def get_frame_intervals(self) -> FrameIntervals:
        """
        Get the content of the _frame_intervals_ section.

        Returns:
          FrameIntervals: Frame intervals as `FrameIntervals`object.
        """
        if "frame_intervals" in self.data["openlabel"]:
            return FrameIntervals(self.data["openlabel"]["frame_intervals"])
        return FrameIntervals()

    def get_element_frame_intervals(
        self, element_type: ElementType, uid: int | str | None
    ) -> FrameIntervals:
        """
        Get the frame intervals of a specific element using its _UID_.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the searched element.

        Returns:
            FrameIntervals: Frame intervals of specified element.
        """
        uid_str = UID(uid).as_str()
        if element_type.name + "s" not in self.data["openlabel"]:
            return FrameIntervals()

        if uid_str not in self.data["openlabel"][element_type.name + "s"]:
            return FrameIntervals()
        return FrameIntervals(
            self.data["openlabel"][element_type.name + "s"][uid_str].get(
                "frame_intervals"
            )
        )

    ##################################################
    # Remove
    ##################################################
    def rm_element_by_type(self, element_type: ElementType, semantic_type: str):
        """
        Remove all elements of specified `ElementType` and with specified semantic type.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          semantic_type (str): Text with the semantic type of the element.
        """
        elements = self.data["openlabel"][element_type.name + "s"]

        # Get Element from summary
        uids_to_remove_str = []
        for uid_str, element in elements.items():
            if element["type"] == semantic_type:
                uids_to_remove_str.append(uid_str)
        for uid_str in uids_to_remove_str:
            self.rm_element(element_type, uid_str)

    def rm_object_by_type(self, semantic_type: str):
        """
        Remove all objects with specified semantic type.

        Args:
          semantic_type (str): Text with the semantic type of the objects.
        """
        self.rm_element_by_type(ElementType.object, semantic_type)

    def rm_action_by_type(self, semantic_type: str):
        """
        Remove all actions with specified semantic type.

        Args:
          semantic_type (str): Text with the semantic type of the actions.
        """
        self.rm_element_by_type(ElementType.action, semantic_type)

    def rm_event_by_type(self, semantic_type: str):
        """
        Remove all events with specified semantic type.

        Args:
          semantic_type (str): Text with the semantic type of the events.
        """
        self.rm_element_by_type(ElementType.event, semantic_type)

    def rm_context_by_type(self, semantic_type: str):
        """
        Remove all contexts with specified semantic type.

        Args:
          semantic_type (str): Text with the semantic type of the contexts.
        """
        self.rm_element_by_type(ElementType.context, semantic_type)

    def rm_relation_by_type(self, semantic_type: str):
        """
        Remove all relations with specified semantic type.

        Args:
          semantic_type (str): Text with the semantic type of the relations.
        """
        self.rm_element_by_type(ElementType.relation, semantic_type)

    def rm_element(self, element_type: ElementType, uid: int | str):
        """
        Remove element with specified `ElementType` and _UID_.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the element to delete.
        """
        uid_str = UID(uid).as_str()
        if not self.has_elements(element_type):
            return

        # Get element from summary
        if not self.has(element_type, uid):
            return

        # Remove from frames: let's read frame_intervals from summary
        elements = self.data["openlabel"][element_type.name + "s"]
        element = elements[uid_str]
        if "frame_intervals" in element:
            for i in range(0, len(element["frame_intervals"])):
                fi = element["frame_intervals"][i]
                for frame_num in range(fi["frame_start"], fi["frame_end"] + 1):
                    elements_in_frame = self.data["openlabel"]["frames"][frame_num][
                        element_type.name + "s"
                    ]
                    if uid in elements_in_frame:
                        del elements_in_frame[uid_str]
                    if (
                        len(elements_in_frame) == 0
                    ):  # objects might have end up empty TODO: test this
                        del self.data["openlabel"]["frames"][frame_num][
                            element_type.name + "s"
                        ]
                        if (
                            len(self.data["openlabel"]["frames"][frame_num]) == 0
                        ):  # this frame may have ended up being empty
                            del self.data["openlabel"]["frames"][frame_num]
                            self.__rm_frame(frame_num)

        # Delete this element from summary
        del elements[uid_str]
        if len(elements) == 0:
            del self.data["openlabel"][element_type.name + "s"]

    def rm_object(self, uid: int | str):
        """
        Remove object with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the object to delete.
        """
        self.rm_element(ElementType.object, uid)

    def rm_action(self, uid: int | str):
        """
        Remove action with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the action to delete.
        """
        self.rm_element(ElementType.action, uid)

    def rm_event(self, uid: int | str):
        """
        Remove event with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the event to delete.
        """
        self.rm_element(ElementType.event, uid)

    def rm_context(self, uid: int | str):
        """
        Remove context with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the context to delete.
        """
        self.rm_element(ElementType.context, uid)

    def rm_relation(self, uid: int | str):
        """
        Remove relation with specified _UID_.

        Args:
          uid (int, str): Unique IDentifier of the relation to delete.
        """
        self.rm_element(ElementType.relation, uid)

    def rm_element_data_from_frames_by_name(
        self,
        element_type: ElementType,
        uid: int | str | UID,
        element_data_name: str,
        frame_intervals: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | FrameIntervals,
    ):
        """
        Remove attribute data from frames by giving the element data name and element _UID_.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the element to search for data.
          element_data_name (str): The name of the attribute to delete
          frame_intervals (int, tuple[int, int], dict[str, int], list[dict[str, int]],
                           list[tuple[int, int]], list[list[int]], FrameIntervals):
                                The frame intervals where to delete the attribute data.
        """
        # Convert to inner UID and FrameIntervals classes
        if not isinstance(uid, UID):
            uid = UID(uid)
        if not isinstance(frame_intervals, FrameIntervals):
            frame_intervals = FrameIntervals(frame_intervals)

        # Quick checks
        if self.has(element_type, uid.as_str()):
            edp = self.get_element_data_pointer(
                element_type, uid.as_str(), element_data_name
            )

            fis_ed = FrameIntervals()
            if edp is not None:
                fis_ed = FrameIntervals(edp["frame_intervals"])

            fis_to_remove = fis_ed.intersection(frame_intervals)
            remove_all = False
            if fis_to_remove.equals(fis_ed):
                remove_all = True

            # Loop over frames that we know the element data is present at
            temp = fis_ed
            for fi in fis_to_remove.get():
                for f in range(fi[0], fi[1] + 1):
                    frame = self.data["openlabel"]["frames"][f]
                    element = frame[element_type.name + "s"][uid.as_str()]
                    # Delete only the element_data with the specified name
                    for prop in list(element[element_type.name + "_data"]):
                        # using list() here to make a copy of the keys, because there is
                        # a delete inside the loop
                        val_array = element[element_type.name + "_data"][prop]
                        idx_to_remove = None
                        for i, val in enumerate(val_array):
                            if val["name"] == element_data_name:
                                # del element[element_type.name + '_data'][prop][i]
                                idx_to_remove = i
                                # break
                                # because we should only delete the one that matches the name
                        del element[element_type.name + "_data"][prop][idx_to_remove]
                        if len(element[element_type.name + "_data"][prop]) == 0:
                            del element[element_type.name + "_data"][
                                prop
                            ]  # e.g. 'bbox': [] is empty, let's remove it
                            if not element[element_type.name + "_data"]:
                                del element[
                                    element_type.name + "_data"
                                ]  # e.g. 'object_data': {}

                    # Clean-up edp frame by frame
                    if not remove_all:
                        temp = FrameIntervals(
                            utils.rm_frame_from_frame_intervals(temp.get_dict(), f)
                        )

            element = self.get_element(element_type, uid.as_str())
            if remove_all:
                # Just delete the entire element_data_pointer
                del element[element_type.name + "_data_pointers"][element_data_name]
            else:
                # Update frame intervals for this edp
                fis_ed_new = temp
                element[element_type.name + "_data_pointers"][element_data_name][
                    "frame_intervals"
                ] = fis_ed_new.get_dict()

    def rm_element_data_from_frames(
        self,
        element_type: ElementType,
        uid: int | str | UID,
        frame_intervals: int
        | tuple[int, int]
        | dict[str, int]
        | list[dict[str, int]]
        | list[tuple[int, int]]
        | list[list[int]]
        | FrameIntervals,
    ):
        """
        Remove all attribute data from frames by giving the element _UID_.

        Args:
          element_type (ElementType): An element type according to enum `ElementType`.
          uid (int, str): Unique IDentifier of the element to search for data.
          frame_intervals (int, tuple[int, int], dict[str, int], list[dict[str, int]],
                           list[tuple[int, int]], list[list[int]], FrameIntervals):
                                The frame intervals where to delete the attribute data.
        """
        if not isinstance(uid, UID):
            uid = UID(uid)
        if not isinstance(frame_intervals, FrameIntervals):
            frame_intervals = FrameIntervals(frame_intervals)
        for fi in frame_intervals.get():
            for f in range(fi[0], fi[1] + 1):
                if self.has_frame(f):
                    frame = self.data["openlabel"]["frames"][f]
                    if element_type.name + "s" in frame:
                        if uid.as_str() in frame[element_type.name + "s"]:
                            element = frame[element_type.name + "s"][uid.as_str()]
                            if element_type.name + "_data" in element:
                                # Delete all its former dynamic element_data entries at old fis
                                del element[element_type.name + "_data"]

        # Clean-up data pointers of object_data that no longer exist!
        # Note, element_data_pointers are correctly updated, but there might be some now
        # declared as static corresponding to element_data that was dynamic but now has
        # been removed when the element changed to static
        if self.has(element_type, uid.as_str()):
            element = self.data["openlabel"][element_type.name + "s"][uid.as_str()]
            if element_type.name + "_data_pointers" in element:
                edps = element[element_type.name + "_data_pointers"]
                edp_names_to_delete = []
                for edp_name in edps:
                    fis_ed = FrameIntervals(edps[edp_name]["frame_intervals"])
                    if fis_ed.empty():
                        # Check if element_data exists
                        ed_type = edps[edp_name]["type"]
                        found = False
                        if element_type.name + "_data" in element:
                            if ed_type in element[element_type.name + "_data"]:
                                for ed in element[element_type.name + "_data"][ed_type]:
                                    if ed["name"] == edp_name:
                                        found = True
                                        break
                        if not found:
                            edp_names_to_delete.append(edp_name)
                for edp_name in edp_names_to_delete:
                    del element[element_type.name + "_data_pointers"][edp_name]


class OpenLABEL(VCD):
    """This is the OpenLABEL class, which inherits from VCD class."""

    def __init__(self):
        __pdoc__["OpenLABEL.__init__"] = False
        """Init the OpenLABEL class."""
        VCD.__init__(self)


class ConverterVCD420toOpenLabel100:
    """
    This class converts from VCD 4.2.0 into OpenLABEL 1.0.0.

    Main changes
    1) Metadata in OpenLABEL 1.0.0 is mostly inside "metadata"
    2) "streams" are at root and not inside "metadata"
    3) element_data_pointers in OpenLABEL 1.0.0 didn't exist in VCD 4.2.0
    4) UIDs are stored as strings in OpenLABEL 1.0.0 (e.g. ontology_uid)
    5) coordinate_systems

    Other changes are implicitly managed by the VCD API

    Attributes:
        vcd_420_data (dict): JSON data of VCD 4.2.0
        openlabel_100 (VCD): output VCD structure.
    """

    def __init__(self, vcd_420_data: dict, openlabel_100: VCD):
        __pdoc__["ConverterVCD420toOpenLabel100.__init__"] = False
        """Init the ConverterVCD420toOpenLabel100 class."""
        if "vcd" not in vcd_420_data:
            raise RuntimeError("This is not a valid VCD 4.2.0 file")

        # While changes 1-2-3 are the only ones implemented, it is easier to just copy
        # everything and then move things
        openlabel_100.data = copy.deepcopy(vcd_420_data)
        openlabel_100.data["openlabel"] = openlabel_100.data.pop("vcd")

        # 1) Metadata (annotator and comment were already inside metadata)
        if "name" in openlabel_100.data["openlabel"]:
            openlabel_100.data["openlabel"].setdefault("metadata", {})
            openlabel_100.data["openlabel"]["metadata"]["name"] = openlabel_100.data[
                "openlabel"
            ]["name"]
            del openlabel_100.data["openlabel"]["name"]
        if "version" in openlabel_100.data["openlabel"]:
            openlabel_100.data["openlabel"].setdefault("metadata", {})
            openlabel_100.data["openlabel"]["metadata"][
                "schema_version"
            ] = schema.openlabel_schema_version
            del openlabel_100.data["openlabel"]["version"]

        # 2) Streams, no longer under "metadata"
        if "metadata" in openlabel_100.data["openlabel"]:
            if "streams" in openlabel_100.data["openlabel"]["metadata"]:
                openlabel_100.data["openlabel"]["streams"] = copy.deepcopy(
                    openlabel_100.data["openlabel"]["metadata"]["streams"]
                )
                del openlabel_100.data["openlabel"]["metadata"]["streams"]

        # 3) Data pointers need to be fully computed
        self.__compute_data_pointers(openlabel_100.data)

        # 4) UIDs, when values, as strings
        for element_type in ElementType:
            if element_type.name + "s" in openlabel_100.data["openlabel"]:
                for _uid, element in openlabel_100.data["openlabel"][
                    element_type.name + "s"
                ].items():
                    if "ontology_uid" in element:
                        element["ontology_uid"] = str(element["ontology_uid"])

    def __compute_data_pointers(self, openlabel_100_data: dict):
        # WARNING! This function might be extremely slow
        # It does loop over all frames, and updates data pointers at objects, actions, etc
        # It is useful to convert from VCD 4.2.0 into OpenLABEL 1.0.0
        # (use converter.ConverterVCD420toOpenLABEL100)

        # Looping over frames and creating the necessary data_pointers
        if "frame_intervals" in openlabel_100_data["openlabel"]:
            fis = openlabel_100_data["openlabel"]["frame_intervals"]
            for fi in fis:
                for frame_num in range(fi["frame_start"], fi["frame_end"] + 1):
                    frame = openlabel_100_data["openlabel"]["frames"][
                        frame_num
                    ]  # warning: at this point, the key is str
                    for element_type in ElementType:
                        if (
                            element_type.name + "s" in frame
                        ):  # e.g. "objects", "actions"...
                            for uid, element in frame[element_type.name + "s"].items():
                                if element_type.name + "_data" in element:
                                    # So this element has element_data in this frame
                                    # and then we need to update the element_data_pointer
                                    # at the root we can safely assume it already exists

                                    # First, let's create a element_data_pointer at the root
                                    openlabel_100_data["openlabel"][
                                        element_type.name + "s"
                                    ][uid].setdefault(
                                        element_type.name + "_data_pointers", {}
                                    )
                                    edp = openlabel_100_data["openlabel"][
                                        element_type.name + "s"
                                    ][uid][element_type.name + "_data_pointers"]

                                    # Let's loop over the element_data
                                    for ed_type, ed_array in element[
                                        element_type.name + "_data"
                                    ].items():
                                        # e.g. ed_type is 'bbox', ed_array is the array
                                        # of such bboxes content
                                        for element_data in ed_array:
                                            name = element_data["name"]
                                            edp.setdefault(
                                                name, {}
                                            )  # this element_data may already exist
                                            edp[name].setdefault(
                                                "type", ed_type
                                            )  # e.g. 'bbox'
                                            edp[name].setdefault(
                                                "frame_intervals", []
                                            )  # in case it does not exist
                                            fis_exist = FrameIntervals(
                                                edp[name]["frame_intervals"]
                                            )
                                            fis_exist = fis_exist.union(
                                                FrameIntervals(frame_num)
                                            )  # So, let's fuse with this frame
                                            edp[name][
                                                "frame_intervals"
                                            ] = fis_exist.get_dict()  # overwrite
                                            # No need to manage attributes
