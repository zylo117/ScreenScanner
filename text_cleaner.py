import cv2
import numpy as np

class TextImg:
    def __init__(self, img_path):
        self.img = cv2.imread(img_path, 0)

    # def remove_background(self):

    def _add_random_noise(self, white_noise=0, black_noise=0):
        w, h = self.img.shape

        white_noise_corrds = []
        black_noise_corrds = []

        np.random.random_integers(white_noise)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    text = TextImg("./test_chs.tiff")

    text._add_random_noise(white_noise=100, black_noise=100)

    hist = cv2.calcHist([text.img], [0], None, [256], [0,256])

    plt.figure()
    plt.plot(np.arange(0, 256), hist)
    plt.show()