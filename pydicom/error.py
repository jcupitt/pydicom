import pydicom
from pydicom import ffi, dicom_lib, _to_string, _to_bytes

"""
usage:
        error = pydicom.Error()
        pointer = dicom_lib.dcm_filehandle_create_from_file(error.pointer,
                                                            _to_bytes(filename))
        if pointer == ffi.NULL:
            raise Error(error)
"""


class Error:
    def __init__(self, pointer):
        # record the pointer we were given to manage
        # on GC, unref
        self.pointer = ffi.gc(pointer, error_free)
        return 

    @staticmethod
    def error_free(pointer):
        indirect = ffi.new("DcmError*[1]")
        indirect[0] = pointer;
        dicom_lib.dcm_error_clear(indirect)

    @staticmethod
    def error_block():
        """Make an error block that can be passed to functions taking
        DcmError**
        indirect = ffi.new("DcmError*[1]")
        indirect[0] = ffi.NULL;
        return indirect

    @staticmethod
    def str_from_error_code(code):
        return _to_string(dicom_lib.dcm_error_code_str(code))

    @staticmethod
    def name_from_error_code(code):
        return _to_string(dicom_lib.dcm_error_code_name(code))

    @staticmethod
    def name_from_error_code(code):
        return _to_string(dicom_lib.dcm_error_code_name(code))

"""
void dcm_error_clear(DcmError **error);
const char *dcm_error_get_summary(DcmError *error);
const char *dcm_error_get_message(DcmError *error);
DcmErrorCode dcm_error_get_code(DcmError *error);
"""
