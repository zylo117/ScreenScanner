import cv2
import numpy as np

class TextImg:
    def __init__(self, img_path):
        self.img = cv2.imread(img_path, 0)

    # def remove_background(self):

    def _add_random_noise(self, white_noise=0, black_noise=0):
        h, w = self.img.shape

        white_noise_corrds = []
        black_noise_corrds = []

        white_noise_corrds_x = np.random.random_integers(w, size=(white_noise, 1))
        white_noise_corrds_y = np.random.random_integers(h, size=(white_noise, 1))
        white_noise_corrds = np.hstack([white_noise_corrds_y, white_noise_corrds_x])
        self.img[white_noise_corrds] = 255

        black_noise_corrds_x = np.random.random_integers(w, size=(black_noise, 1))
        black_noise_corrds_y = np.random.random_integers(h, size=(black_noise, 1))
        black_noise_corrds = np.hstack([black_noise_corrds_y, black_noise_corrds_x])
        self.img[black_noise_corrds] = 0

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    text = TextImg("./test_chs.tiff")

    text._add_random_noise(white_noise=100, black_noise=100)
    cv2.imshow(text.img)
    cv2.waitKey(0)

    hist = cv2.calcHist([text.img], [0], None, [256], [0,256])

    plt.figure()
    plt.plot(np.arange(0, 256), hist)
    plt.show()