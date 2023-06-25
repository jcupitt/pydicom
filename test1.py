#!/usr/bin/env python

import pydicom

print(f"testing enums ...")
print(f"pydicom.VR.SQ = {pydicom.VR.SQ}")

print(f"testing create_from_file ...")
file = pydicom.Filehandle.create_from_file("synthetic.dcm")
print(f"file = {file}")

print(f"testing read_file_meta ...")
file_meta = file.read_file_meta()
print(f"file_meta = {file_meta}")


