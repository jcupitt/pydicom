import pydicom
from pydicom import ffi, dicom_lib, _to_string, _to_bytes

class Tag:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def create_from_keyword(keyword):
        value = dicom_lib.dcm_dict_tag_from_keyword(_to_bytes(keyword))
        if value == 0xffffffff:
            raise Exception("Unknown keyword '{keyword}'")
        return Tag(value)

    def keyword(self):
        return _to_string(dicom_lib.dcm_error_code_str(self.value))

    def group(self):
        return self.value >> 16

    def number(self):
        return self.value & 0xffff

    def __repr__(self):
        return f"({self.group():04x}, {self.number():04x})"

