import ctypes
import os
import platform

LIB_NAME_OSX = "libtesseract.4.dylib"  # MAC OSX
LIB_NAME_LINUX = "libtesseract.4.so"  # Linux
LIB_NAME_WIN = "libtesseract-4.dll"  # Windows

def get_os_type():
    current_system_type = platform.uname()
    if current_system_type.system == "Darwin":
        os_type = "mac"
    elif current_system_type.system == "Linux":
        os_type = "linux"
    elif current_system_type.system == "Windows":
        os_type = "windows"
    else:
        os_type = "other"
    return os_type


os_type = get_os_type()
if os_type == "mac":
    LIB_NAME = LIB_NAME_OSX
elif os_type == "linux":
    LIB_NAME = LIB_NAME_LINUX
elif os_type == "windows":
    LIB_NAME = LIB_NAME_WIN
elif os_type == "other":
    raise EnvironmentError("Unable to determine current OS type, please manually specify a path to libtesseract")

env_dist = os.environ  # environ is a dict that defined in os.py, environ = {}

TESSDATA_PREFIX = env_dist.get('TESSDATA_PREFIX')

# print(env_dist.get('TESSDATA_PREFIX'))
# for key in env_dist:
#     print(key + ' : ' + env_dist[key])

if TESSDATA_PREFIX is None:
    raise EnvironmentError(
        "Please check your environment variable to confirm 'TESSDATA_PREFIX' is correctly configured"
        "or succeeded installed/compiled tesseract.")
else:
    TESSDATA_PREFIX = TESSDATA_PREFIX.replace("\\", "/") + "/"

# LIB_PATH = TESSDATA_PREFIX + LIB_NAME
TESSDATA_PREFIX = TESSDATA_PREFIX.encode()
lang = b'chi_sim'

tesseract = ctypes.cdll.LoadLibrary(LIB_NAME)
tesseract.TessBaseAPICreate.restype = ctypes.c_uint64
api = tesseract.TessBaseAPICreate()
rc = tesseract.TessBaseAPIInit3(ctypes.c_uint64(api), TESSDATA_PREFIX, lang)
if rc:
    tesseract.TessBaseAPIDelete(ctypes.c_uint64(api))
    print('Could not initialize tesseract.\n')
    exit(3)

def from_file(path):
    tesseract.TessBaseAPIProcessPages(
        ctypes.c_uint64(api), path, None, 0, None)
    tesseract.TessBaseAPIGetUTF8Text.restype = ctypes.c_uint64
    text_out = tesseract.TessBaseAPIGetUTF8Text(ctypes.c_uint64(api))
    return ctypes.string_at(text_out)





if __name__ == '__main__':
    image_file_path = b'./test_chs.tiff'
    result = from_file(image_file_path)
    print(result)
