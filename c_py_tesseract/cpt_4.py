import ctypes
import ctypes.util
import os
import sys

if sys.platform == "win32":
    LIBNAME = "libtesseract302"
else:
    LIBNAME = "tesseract"

env_dist = os.environ
TESSDATA_PREFIX = env_dist.get("TESSDATA_PREFIX")
PATH_TO_LIBTESS = ctypes.util.find_library(LIBNAME)

import cffi  # requires "pip install cffi"

ffi = cffi.FFI()
ffi.cdef("""
struct Pix;
typedef struct Pix PIX;
PIX * pixRead ( const char *filename );
char * getLeptonicaVersion (  );

typedef struct TessBaseAPI TessBaseAPI;
typedef int BOOL;

const char* TessVersion();

TessBaseAPI* TessBaseAPICreate();
int TessBaseAPIInit3(TessBaseAPI* handle, const char* datapath, const char* language);

void TessBaseAPISetImage2(TessBaseAPI* handle, struct Pix* pix);

BOOL   TessBaseAPIDetectOrientationScript(TessBaseAPI* handle, char** best_script_name, 
                                                            int* best_orientation_deg, float* script_confidence, 
                                                            float* orientation_confidence);
""")

libtess = ffi.dlopen(PATH_TO_LIBTESS)
from ctypes.util import find_library
liblept = ffi.dlopen(find_library('lept'))

a = ffi.string(libtess.TessVersion())

b = ffi.string(liblept.getLeptonicaVersion())

api = libtess.TessBaseAPICreate()

libtess.TessBaseAPIInit3(api, ffi.NULL, ffi.NULL)

pix = liblept.pixRead('test_eng.jpg'.encode())

libtess.TessBaseAPISetImage2(api, pix)

script_name = ffi.new('char **')
orient_deg = ffi.new('int *')
script_conf = ffi.new('float *')
orient_conf = ffi.new('float *')
libtess.TessBaseAPIDetectOrientationScript(api, script_name, orient_deg, script_conf, orient_conf)

ffi.string(script_name[0])

print(orient_deg[0])
print(script_conf[0])
print(orient_conf[0])