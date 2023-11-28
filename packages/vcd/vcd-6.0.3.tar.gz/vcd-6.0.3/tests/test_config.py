"""
VCD (Video Content Description) library.

Project website: http://vcd.vicomtech.org

Copyright (C) 2023, Vicomtech (http://www.vicomtech.es/),
(Spain) all rights reserved.

VCD is a Python library to create and manage OpenLABEL content.
VCD is distributed under MIT License. See LICENSE.
"""

import os

from vcd import core, schema

openlabel_version_name = "openlabel" + schema.openlabel_schema_version.replace(".", "")
overwrite = False


def check_openlabel(openlabel, openlabel_file_name, force_write=False):
    if not os.path.isfile(openlabel_file_name) or force_write:
        openlabel.save(openlabel_file_name)

    openlabel_read = core.OpenLABEL()
    openlabel_read.load_from_file(openlabel_file_name, validation=True)
    return openlabel_read.stringify() == openlabel.stringify()
