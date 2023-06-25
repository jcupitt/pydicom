import pydicom
from pydicom import ffi, dicom_lib, _to_string, _to_bytes

class DataSet:
    def __init__(self, pointer, steal=False):
        # record the pointer we were given to manage
        # if steal is set, destroy on GC
        if steal:
            self.pointer = ffi.gc(pointer, dicom_lib.dcm_dataset_destroy)
        else:
            self.pointer = pointer

        return 

    def __repr__(self):
        return "<libdicom DataSet>"

    def count(self):
        return dicom_lib.dcm_dataset_count(self.pointer)


