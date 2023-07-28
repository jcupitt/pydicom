import pylibdicom
from pylibdicom import ffi, dicom_lib, _to_string, _to_bytes

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
               f"{self.length()} | " + \
               f"{self.vm()} | " + \
               f"{self.value_to_string()}"

    def tag(self):
        return pylibdicom.Tag(dicom_lib.dcm_element_get_tag(self.pointer))

    def vr(self):
        return pylibdicom.VR(dicom_lib.dcm_element_get_vr(self.pointer))

    def vr_class(self):
        return dicom_lib.dcm_dict_vr_class(self.vr().value)

    def vm(self):
        return dicom_lib.dcm_element_get_vm(self.pointer)

    def length(self):
        return dicom_lib.dcm_element_get_length(self.pointer)

    def get_value_integer(self, index):
        error = pylibdicom.Error()
        intp = ffi.new("int64_t[1]")
        success = dicom_lib.dcm_element_get_value_integer(error.pointer,
                                                          self.pointer,
                                                          index,
                                                          intp)
        if not success:
            raise error.exception()
    
        return intp[0]

    def get_value_decimal(self, index):
        error = pylibdicom.Error()
        doublep = ffi.new("double[1]")
        success = dicom_lib.dcm_element_get_value_decimal(error.pointer,
                                                          self.pointer,
                                                          index,
                                                          doublep)
        if not success:
            raise error.exception()
    
        return doublep[0]

    def get_value_string(self, index):
        error = pylibdicom.Error()
        strp = ffi.new("char*[1]")
        success = dicom_lib.dcm_element_get_value_string(error.pointer,
                                                         self.pointer,
                                                         index,
                                                         strp)
        if not success:
            raise error.exception()
    
        return _to_string(strp[0]);

    def get_value_binary(self):
        length = self.length()
        error = pylibdicom.Error()
        binp = ffi.new("char*[1]")
        success = dicom_lib.dcm_element_get_value_binary(error.pointer,
                                                         self.pointer,
                                                         binp)
        if not success:
            raise error.exception()

        # allocate a chunk of memory and copy to that ... we can't use the
        # pointer from libdicom, since that will be freed when element is
        # freed
        mem = ffi.new(f"unsigned char[{length}]")
        ffi.memmove(mem, binp[0], length)

        return mem

    def get_value_sequence(self):
        length = self.length()
        error = pylibdicom.Error()
        seqp = ffi.new("DcmSequence*[1]")
        success = dicom_lib.dcm_element_get_value_sequence(error.pointer,
                                                           self.pointer,
                                                           seqp)
        if not success:
            raise error.exception()

        return pylibdicom.Sequence(seqp[0])

    def get_value(self):
        klass = self.vr_class()
        if klass == pylibdicom.VRClass.NUMERIC_INTEGER:
            return [self.get_value_integer(i) for i in range(0, self.vm())]
        elif klass == pylibdicom.VRClass.NUMERIC_DECIMAL:
            return [self.get_value_decimal(i) for i in range(0, self.vm())]
        elif klass == pylibdicom.VRClass.STRING_SINGLE or \
            klass == pylibdicom.VRClass.STRING_MULTI:
            return [self.get_value_string(i) for i in range(0, self.vm())]
        elif klass == pylibdicom.VRClass.BINARY:
            return self.get_value_binary()
        elif klass == pylibdicom.VRClass.SEQUENCE:
            return self.get_value_sequence()
        else:
            raise Exception("unimplemented VR class")

    def value_to_string(self):
        pointer = dicom_lib.dcm_element_value_to_string(self.pointer);
        if pointer == ffi.NULL:
            raise Exception(f"Element value cannot be printed")
        pointer = ffi.gc(pointer, dicom_lib.dcm_free)
        return _to_string(pointer)

