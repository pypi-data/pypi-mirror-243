
Basic principles of SCL (Scene Configuration Library)
-----------------------------

SCL provides some routines and functions, but it is also a guide to produce scenes coherently.
Read carefully these principles, and see them in practice on the samples.

SCL is based on common conventions. In some cases, SCL allows using different conventions,
but eventually it enforces using specific conventions, such as 'right-hand' coordinate systems,
homogeneous coordinates, right-multiplication of matrices, alias (vs alibi) rotation matrices, etc.

Numpy Arrays
-----------------------------
All geometric data is expressed as numpy n-dimensional arrays.

Homogeneous Data
-----------------------------
All geometric data (points, lines) are expressed in homogeneous coordinates (columns)
All matrices are also expressed in homogeneous coordinates.
E.g. 3D points are column vectors \(4x1\)
        camera calibration matrix (K) is \(3x4\) matrix, where last row is all zeros and 1.0
        all poses are expressed as \(4x4\) matrices
        rotation matrices are \(3x3\)
        If not specified otherwise, all one-dimensional vectors are column vectors
NOTE: Since OpenLABEL 1.0.0, quaternion + translation is also added as an option to express poses.

Internally, SCL converts this form into \(4x4\) matrices

Poses and Coordinates systems
-----------------------------
Each coordinate system may have a pose with respect to a parent coordinate system.
Examples of this are sensors which are installed in vehicles. The Sensor Coordinate System (SCS)
then has a pose with respect to the Local Coordinate System (LCS) of the vehicle.
In SCL this LCS is a point at the ego-vehicle located at the middle of the rear axle, projected
to the ground, being X-to-front, Y-to-left, Z-up as defined in the ISO8855.

There are some other usual acronyms used in the code:

    - LCS : Local Coordinate System (e.g. the vehicle coordinate system at the rear axis,
            as in ISO8855)
    - SCS : Sensor Coordinate System (e.g. the camera coordinate system, or the lidar
            coordinate system)
    - WCS : World Coordinate System (static coordinate system for the entire scene, typically
            equal to the first LCS)
    - GCS : Geographic Coordinate System (UTM Universal Transverse Mercator)
    - ICS : Image coordinate system (this is the 2D image plane)

NOTE: Nevertheless, in VCD and SCL, an entirely customizable graph of dependencies can be
built, declaring coordinate systems and parent-child relations. See vcd.core functions
add_coordinate_system() where static poses can be defined, and add_transform()which is a
function to add frame-specific poses between coordinate systems.

For readability, let's use the following letter conventions:
    - P : Pose \(4x4\)
    - T : Transform \(4x4\)
    - R : Rotation matrix \(3x3\)
    - C : Position of coordinate system wrt to another \(3x1\)
    - K : Camera calibration matrix \(3x4\)
    - d : Distortion coefficients \(1x5\) (or \(1x9\), or \(1x14\))

All Poses are defined right-handed. A Pose encodes the passive rotation and position of a
coordinate system wrt (with respect to) a reference system.

Usually, P_scs_wrt_lcs = [[R_3x3, C_3x1], [0, 0, 0, 1]], where R_3x3 is a 3x3 rotation matrix,
and C_3x1 is the position of the SCS expressed in the LCS.

To actually convert a point from the reference system (e.g. LCS) into another system (e.g. SCS),
the transformation matrix is built as the inverse of the pose
https://en.wikipedia.org/wiki/Active_and_passive_transformation

Cameras coordinate systems are defined with X-to-right, Y-to-bottom, and Z-to-front, following
usual OpenCV camera model convention.
This is the common practice in computer vision, so that image coordinates are defined
x-to-right, y-to-bottom.

Transforming a 3D point expressed in a given coordinate system into another coordinate system
is carried out using right-to-left matrix multiplication:
e.g. X_scs = T_lcs_to_scs @ X_lcs (e.g. X_lcs is 4x1, Transform_lcs_to_scs is 4x4, X_scs is 4x1)
        X_scs = T_lcs_to_scs @ X_lcs
NOTE: @ operator in Python (>3.5) is matrix multiplication, equivalent to Numpy's dot operator

In addition, transformations can be understood as inverse Poses.
e.g. if T_lcs_to_scs converts a point from LCS to SCS, then
        T_lcs_to_scs = np.linalg.inv(P_scs_wrt_lcs)  # or using utils.inv(P_scs_wrt_lcs)

Note that to build a Pose and Transform by knowing the passive rotation R and position C of
a coordinate system wrt to another, it is possible to do:

(pseudo-code)
P_scs_wrt_lcs = (R_scs_wrt_lcs C_scs_wrt_lcs; 0 0 0 1)
or
T_lcs_to_scs = (transpose(R_scs_wrt_lcs) transpose(-R_scs_wrt_lcs)C_scs_wrt_lcs; 0 0 0 1)
Note P = T^-1 and T = P^-1

Since conversion from one system to another is useful, the following equations hold true:
P_scs_wrt_lcs = (T_lcs_to_scs)^-1
P_scs_wrt_lcs = T_scs_to_lcs


Odometry
-----------------------------
The sensors of the setup can move through time (e.g. if onboarded into a moving vehicle or
drone), the motion of the set-up is defined by the odometry information.

As each sensor has its own capturing timestamp, not necessarily coincident with the timestamp of
an odometry entry, odometry information may be provided associated to a specific sensor frame
(this way, it is possible to locate globally sensing information from that sensor).
The library provides tools to interpolate odometry and associate odometry entries to specific
timestamps.

The SCL library is defined in a way it is possible to add odometry values from multiple set-ups
e.g. V2V, a second vehicle sends location information about itself and its sensors, along
     with detections.

Odometry is treated just like a normal frame-specific transform. Therefore, all previous
discussion applies.
See vcd's add_transform() function at core.py


Geo-coordinates
-----------------------------
Just like any other coordinate system, geo-coordinates can be specified in VCD and then are
supported in SCL.
