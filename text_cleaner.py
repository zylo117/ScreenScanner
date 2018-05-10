import cv2
import imutils
import numpy as np

class TextImg:
    def __init__(self, gray_img):
        self.img = gray_img

    def whiten_background(self, thresh_val):
        self.img[self.img > thresh_val] = 255

    def _add_random_noise(self, white_noise=0, black_noise=0):
        h, w = self.img.shape

        white_noise_x = np.random.randint(0, w, size=(1, white_noise))
        white_noise_y = np.random.randint(0, h, size=(1, white_noise ))
        self.img[white_noise_y, white_noise_x] = np.random.randint(192, 256, size=white_noise)

        black_noise_x = np.random.randint(0, w, size=(1, black_noise))
        black_noise_y = np.random.randint(0, h, size=(1, black_noise))
        self.img[black_noise_y, black_noise_x] = np.random.randint(0, 64, size=black_noise)

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    img = cv2.imread("./test_chs.tiff", 0)

    text = TextImg(img)

    text._add_random_noise(white_noise=10000, black_noise=10000)
    cv2.imshow("Noise", text.img)
    cv2.waitKey(0)

    text.img = cv2.medianBlur(text.img, 3)
    cv2.imshow("DeNoise", text.img)
    cv2.waitKey(0)

    text.whiten_background(220)
    cv2.imshow("Remove Noise", text.img)
    cv2.waitKey(0)

    text.img = imutils.resize(text.img, width=1000)

    hist = cv2.calcHist([text.img], [0], None, [256], [0, 256])

    plt.figure()
    plt.plot(np.arange(0, 256), hist)
    plt.xlim(50, 256)
    plt.ylim(0, 4000)
    plt.show()