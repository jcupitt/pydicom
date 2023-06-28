import pydicom
from pydicom import ffi, dicom_lib, _to_string, _to_bytes

class Filehandle:
    def __init__(self, pointer):
        # record the pointer we were given to manage
        # on GC, destroy it
        self.pointer = ffi.gc(pointer, dicom_lib.dcm_filehandle_destroy)
        return 

    @staticmethod
    def create_from_file(filename):
        error = pydicom.Error()
        pointer = dicom_lib.dcm_filehandle_create_from_file(error.pointer,
                                                            _to_bytes(filename))
        if pointer == ffi.NULL:
            raise error.exception()

        return Filehandle(pointer)

    def __repr__(self):
        return "<libdicom Filehandle>"

    def get_file_meta(self):
        error = pydicom.Error()
        pointer = dicom_lib.dcm_filehandle_get_file_meta(error.pointer,
                                                         self.pointer)
        if pointer == ffi.NULL:
            raise error.exception()

        return pydicom.DataSet(pointer)

    def get_metadata(self):
        error = pydicom.Error()
        pointer = dicom_lib.dcm_filehandle_get_metadata(error.pointer,
                                                        self.pointer)
        if pointer == ffi.NULL:
            raise error.exception()

        return pydicom.DataSet(pointer)




