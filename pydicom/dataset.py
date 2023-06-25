import pydicom
from pydicom import ffi, dicom_lib, _to_string, _to_bytes

class DataSet:
    def __init__(self, pointer):
        # record the pointer we were given to manage
        # on GC, unref
        self.pointer = ffi.gc(pointer, dicom_lib.dcm_dataset_destroy)
        return 

    def __repr__(self):
        return "<libdicom DataSet>"



