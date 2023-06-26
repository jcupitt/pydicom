from cffi import FFI
from .version import __version__

ffi = FFI()

print(f"opening libdicom ...")
dicom_lib = ffi.dlopen("libdicom.so")

ffi.cdef('''
void dcm_init(void);
const char *dcm_get_version(void);

typedef struct _DcmError DcmError;
typedef struct _DcmFilehandle DcmFilehandle;
typedef struct _DcmDataSet DcmDataSet;
typedef struct _DcmElement DcmElement;

const char *dcm_error_code_str(int code);
const char *dcm_error_code_name(int code);
void dcm_error_clear(DcmError **error);
const char *dcm_error_get_summary(DcmError *error);
const char *dcm_error_get_message(DcmError *error);
int dcm_error_get_code(DcmError *error);

void *dcm_calloc(DcmError **error, uint64_t n, uint64_t size);
void dcm_free(void *pointer);

DcmFilehandle *dcm_filehandle_create_from_file(DcmError **error,
                                               const char *filepath);
void dcm_filehandle_destroy(DcmFilehandle *filehandle);

DcmDataSet *dcm_filehandle_get_file_meta(DcmError **error,
                                         DcmFilehandle *filehandle);

const char *dcm_dict_keyword_from_tag(uint32_t tag);
uint32_t dcm_dict_tag_from_keyword(const char *keyword);
int dcm_dict_vr_from_str(const char *vr);
const char *dcm_dict_str_from_vr(int vr);

int dcm_dataset_count(DcmDataSet *dataset);
void dcm_dataset_copy_tags(const DcmDataSet *dataset, uint32_t *tags, uint32_t n);
DcmElement *dcm_dataset_contains(const DcmDataSet *dataset, uint32_t tag);
void dcm_dataset_destroy(DcmDataSet *dataset);

uint32_t dcm_element_get_tag(const DcmElement *element);
int dcm_element_get_vr(const DcmElement *element);
uint32_t dcm_element_get_vm(const DcmElement *element);
char *dcm_element_value_to_string(const DcmElement *element);



''')

print(f"init for libdicom ...")
dicom_lib.dcm_init()


def _to_string(x):
    """Convert to a unicode string.

    If x is a byte string, assume it is utf-8 and decode to a Python unicode
    string. You must call this on text strings you get back from libvips.

    """
    if x == ffi.NULL:
        x = 'NULL'
    else:
        x = ffi.string(x)
        if isinstance(x, bytes):
            x = x.decode('utf-8')

    return x


def _to_bytes(x):
    """Convert to a byte string.

    Convert a Python unicode string or a pathlib.Path to a utf-8-encoded
    byte string. You must call this on strings you pass to libvips.

    """
    if isinstance(x, str):
        # n.b. str also converts pathlib.Path objects
        x = str(x).encode('utf-8')

    return x


def version():
    """Get the libdicom version.

    As a x.y.z semantic version string.

    """
    return _to_string(dicom_lib.dcm_get_version())


print(f"libdicom version: {version()}")

from .error import *
from .enums import *
from .vr import *
from .tag import *
from .element import *
from .dataset import *
from .filehandle import *

__all__ = [
]

