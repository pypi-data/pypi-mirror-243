"""
VCD (Video Content Description) library v5.0.1.

Project website: http://vcd.vicomtech.org

Copyright (C) 2023, Vicomtech (http://www.vicomtech.es/),
(Spain) all rights reserved.

VCD is a Python library to create and manage OpenLABEL content.
VCD is distributed under MIT License. See LICENSE.
"""


import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation

import vcd.core as core
import vcd.draw as draw
import vcd.scl as scl
import vcd.types as types
import vcd.utils as utils
from vcd.draw import SetupViewer

add_1 = True
add_2 = True

# Create basic cuboids
vcd = core.VCD()
vcd.add_coordinate_system(name="world", cs_type=types.CoordinateSystemType.custom)

# Sample rotation
euler = [0.0, 0.0, 0.52]  # XYZ
quat = [0.0, 0.0, 0.25708, 0.96638]
translation1 = [3.0, 0.0, 0.7]
translation2 = [3.0, 0.0, 0.7]
size1 = [4.0, 1.6, 1.4]
size2 = size1

# Check:
R = utils.euler2R(euler, seq=utils.EulerSeq.ZYX)
R_ = Rotation.from_euler("zyx", euler, degrees=False)
quat = R_.as_quat().flatten().tolist()
print(quat)

# Add car1 as Euler + traslation
if add_1:
    vcd.add_coordinate_system(
        name="cuboid1",
        parent_name="world",
        cs_type=types.CoordinateSystemType.local_cs,
        pose_wrt_parent=types.PoseData(
            val=euler + translation1, t_type=types.TransformDataType.euler_and_trans_6x1
        ),
    )
    uid1 = vcd.add_object(name="car1", semantic_type="car")
    cuboid1 = types.cuboid(
        name="shape", val=translation1 + euler + size1, coordinate_system="world"
    )
    vcd.add_object_data(uid=uid1, object_data=cuboid1)

# Add car2 as Quaternion + traslation
if add_2:
    vcd.add_coordinate_system(
        name="cuboid2",
        parent_name="world",
        cs_type=types.CoordinateSystemType.local_cs,
        pose_wrt_parent=types.PoseData(
            val=quat + translation2, t_type=types.TransformDataType.quat_and_trans_7x1
        ),
    )
    uid2 = vcd.add_object(name="car2", semantic_type="car")
    cuboid2 = types.cuboid(
        name="shape", val=translation2 + quat + size2, coordinate_system="world"
    )
    vcd.add_object_data(uid=uid2, object_data=cuboid2)

# Use SCL to draw
scene = scl.Scene(vcd)
setup_viewer = draw.SetupViewer(scene, "world")

setup_viewer.plot_setup([[-1, 6], [-3, 3], [0, 5]])
plt.show()
