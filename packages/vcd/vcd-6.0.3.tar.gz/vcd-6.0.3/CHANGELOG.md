# Changelog

<!-- towncrier release notes start -->

## Version [6.0.3](https://pypi.org/project/vcd/6.0.3)

### Fixed

- Updated dependencies versions of numpy and python [#13](https://gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/-/issues/13)

### Other

- Add Gitlab SAST testing to CI/CD pipeline [#10](https://gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/-/issues/10)
- Simplify Gitlab CI/CD pipeline [#12](https://gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/-/issues/12)

## Version [6.0.2](https://pypi.org/project/vcd/6.0.2)

### Fixed

- Fixed an issue that prevented to load OpenLABEL files with elements with hexadesimal UUIDs [#8](https://gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/-/issues/8)

### Other

- Update return types of *get_all* function in core module to add None as a possible return value. [#7](https://gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/-/issues/7)


## Version [6.0.1](https://pypi.org/project/vcd/6.0.1)

### Fixed

- Fixed bug in function draw_bevs that prevented to draw topview images. [#4](https://gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/-/issues/4)
- Fixed the way to save boundary tags in ontologies where the content  was not in OpenLABEL format. [#5](https://gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/-/issues/5)


## Version [6.0.0](https://pypi.org/project/vcd/6.0.0)

### Changed

- Python API change when creating VCD object adds  new functions to load data from file and from string
- Python API separated from other languages

### Other

- Added CI/CD builds in new gitlab repository
- Added python type annotations to class and functions definitions
- Improved documentation of _core_ module


## Version [5.0.0](https://pypi.org/project/vcd/5.0.0/)

- VCD schema is now OpenLABEL schema 1.0.0
- Added support for scenario tagging
- Improved performance
- Addition of C++ API (lite version)
- Enhanced support for Quaternions

## Version [4.3.1](https://pypi.org/project/vcd/4.3.1/)

- Bug fixing (npm package)
- Multi-value attributes (vec of strings)
- Additional properties true for all attributes
- Customizable intrinsics

## Version [4.3.0](https://pypi.org/project/vcd/4.3.0/)

- Integrated SCL (Scene Configuration Library) into VCD
- Automatic drawing functions for multi-sensor set-ups (e.g. topview)
- Improved API functions for offline VCD edition
- Added Typescript API for web applications
- Common set of test files for Python and Typescript APIs
- Simplified Relations construction
- Preliminary work on Ontology connection with Neo4j

## Version [4.2.0](https://pypi.org/project/vcd/4.2.0/)

- Improved Frame-message creation
- Enhanced API for adding Relations and RDFs
- Added examples for semantic labeling
- General bug fixing and better frame interval management

## Version [4.1.0](https://pypi.org/project/vcd/4.1.0/)

- Enhanced JSON schema self-documentation
- Explicit definition of timestamps and sync information
- Explicit definition of intrinsics parameters for cameras
- Explicit definition of extrinsics parameters for stream (as 4x4 pose matrices)
- Explicit definition of odometry entries
- Reviewed samples and converters

## Version [4.0.0](https://pypi.org/project/vcd/4.0.0/)

- Python API
- Mixed-mode instead of Element-wise or Frame-wise mode: 'Objects', 'Actions', contain the static data, while 'Frames' contain the dynamic part with pointers to the static data
- Elements can contain multiple frameIntervals, instead of just one. This allows to manage "gaps".
- The API has been simplified, and only VCD objects can be created
- The concept of ObjectDataContainer has disappeared, now all information is within "ObjectData" structures
- Frames are listed in the JSON as a dict(), not as an array. Keys are the frame numbers.
- Elements are listed in the JSON as a dict(), not as an array. Keys are the uid of elements.
- Timestamp information is now optional for the user, who can insert it as frameProperties (along with intrinsics)
- Relations are timeless: are completely defined by the rdf.subjects and rdf.objects
- All fields in JSON are lowercase, e.g. 'vcd', 'objects'.
- Stringify_frame can be executed to create messages asking for dynamic-only or full (static plus dynamic) information
