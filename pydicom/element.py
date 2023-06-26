import pydicom
from pydicom import ffi, dicom_lib, _to_string, _to_bytes

class Element:
    def __init__(self, pointer, steal=False):
        # record the pointer we were given to manage
        # if steal is set, destroy on GC
        if steal:
            self.pointer = ffi.gc(pointer, dicom_lib.dcm_element_destroy)
        else:
            self.pointer = pointer

        return 

    def __repr__(self):
        return f"{self.tag()} {self.tag().keyword()} | " + \
               f"{self.vr()} | " + \
               f"{self.vm()} | {self.value_to_string()}"

    def tag(self):
        return pydicom.Tag(dicom_lib.dcm_element_get_tag(self.pointer))

    def vr(self):
        return pydicom.VR(dicom_lib.dcm_element_get_vr(self.pointer))

    def vm(self):
        return dicom_lib.dcm_element_get_vm(self.pointer)

    def value_to_string(self):
        pointer = dicom_lib.dcm_element_value_to_string(self.pointer);
        if pointer == ffi.NULL:
            raise Exception(f"Element value cannot be printed")
        pointer = ffi.gc(pointer, dicom_lib.dcm_free)
        return _to_string(pointer)

