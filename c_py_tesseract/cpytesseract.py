import ctypes
import os

LIB_PATH = "./libtesseract.dylib"

env_dist = os.environ  # environ is a dict that defined in os.py, environ = {}
# https://www.polarxiong.com/archives/python-pytesser-tesseract.html

print(env_dist.get('TESSDATA_PREFIX'))
for key in env_dist:
    print(key + ' : ' + env_dist[key])

TESSDATA_PREFIX = b'./tessdata'
lang = b'chi_sim'

tesseract = ctypes.cdll.LoadLibrary(LIB_PATH)
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