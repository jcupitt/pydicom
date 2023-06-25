import pydicom
from pydicom import ffi, dicom_lib, _to_string, _to_bytes

class Filehandle:
    def __init__(self, pointer):
        # record the pointer we were given to manage
        # on GC, unref
        self.pointer = ffi.gc(pointer, dicom_lib.dcm_filehandle_destroy)
        return 

    @staticmethod
    def create_from_file(filename):
        error = pydicom.Error()
        pointer = dicom_lib.dcm_filehandle_create_from_file(error.pointer,
                                                            _to_bytes(filename))
        if pointer == ffi.NULL:
            raise Error(error)

        return Filehandle(pointer)

    def __repr__(self):
        return "<libdicom Filehandle>"

    def read_file_meta(self):
        pointer = dicom_lib.dcm_filehandle_read_file_meta(ffi.NULL,
                                                          self.pointer)
        return pydicom.DataSet(pointer)


