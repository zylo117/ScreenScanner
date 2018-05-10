import cv2
import imutils
import numpy as np

class TextImg:
    def __init__(self, gray_img):
        self.img = gray_img

    def whiten_background(self, thresh_val=None):
        if thresh_val is not None:
            self.img[self.img > thresh_val] = 255
        else:
            thresh_val, _ = cv2.threshold(self.img, 0, 255, cv2.THRESH_OTSU)
            self.img[self.img > thresh_val] = 255

    def blacken_text(self, thresh_val=None):
        if thresh_val is not None:
            self.img[self.img < thresh_val] = 0
        else:
            thresh_val, self.img = cv2.threshold(self.img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_TOZERO)

    def _add_random_noise(self, white_noise=0, black_noise=0):
        h, w = self.img.shape[:2]

        white_noise_x = np.random.randint(0, w, size=(1, white_noise))
        white_noise_y = np.random.randint(0, h, size=(1, white_noise ))
        self.img[white_noise_y, white_noise_x] = np.random.randint(192, 256, size=white_noise)

        black_noise_x = np.random.randint(0, w, size=(1, black_noise))
        black_noise_y = np.random.randint(0, h, size=(1, black_noise))
        self.img[black_noise_y, black_noise_x] = np.random.randint(0, 64, size=black_noise)

    def denoise(self, ksize=3):
        self.img = cv2.medianBlur(self.img, ksize)

    def skew_correction(self, angle=None):
        _, thresh = cv2.threshold(self.img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        coords = np.column_stack(np.where(thresh > 0))  # get all non-zero pixel coords
        p1, p3, angle = cv2.minAreaRect(coords)  # bound them with a rotated rect

        # angle of minAreaRect is confusing, recommends to a good answer here https://stackoverflow.com/questions/15956124/minarearect-angles-unsure-about-the-angle-returned
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        text_center = ((p1[0] + p3[0])//2,(p1[1] + p3[1])//2)

        M = cv2.getRotationMatrix2D(text_center, angle, 1)

        h, w = self.img.shape[:2]
        self.img = cv2.warpAffine(self.img, M, (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=255)

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    img = cv2.imread("./test_chs_rotate.tiff", 0)

    text = TextImg(img)

    text._add_random_noise(white_noise=10000, black_noise=10000)
    cv2.imshow("Noise", text.img)

    text.denoise(3)
    cv2.imshow("DeNoise", text.img)

    text.whiten_background()
    cv2.imshow("whiten_background", text.img)

    text.blacken_text()
    cv2.imshow("blacken_text", text.img)

    text.skew_correction()
    cv2.imshow("Skew Correction", text.img)
    cv2.waitKey(0)

    text.img = imutils.resize(text.img, width=1000)

    hist = cv2.calcHist([text.img], [0], None, [256], [0, 256])

    plt.figure()
    plt.plot(np.arange(0, 256), hist)
    plt.xlim(50, 256)
    plt.ylim(0, 4000)
    plt.show()