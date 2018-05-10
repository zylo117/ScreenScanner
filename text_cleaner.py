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

    def sharpen_text(self):
        """

        :return:
        """
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # Laplacian sharpen kernel, too thick for text
        invert = cv2.bitwise_not(self.img).astype(np.uint16)
        sharpen_mask = cv2.filter2D(invert, cv2.CV_64F, kernel, borderType=cv2.BORDER_REPLICATE)
        self.img = cv2.convertScaleAbs(cv2.convertScaleAbs(sharpen_mask) + invert)
        self.img = cv2.bitwise_not(self.img)

    # experimental, hardcore
    def skeleton_text(self):
        self.img = cv2.bitwise_not(self.img)
        self.img = imutils.skeletonize(self.img, (3, 3), cv2.MORPH_ELLIPSE)

        self.img = cv2.dilate(self.img, None)
        self.img = cv2.bitwise_not(self.img)

    def stroke_text(self, elem=cv2.MORPH_ELLIPSE):
        kernel = cv2.getStructuringElement(elem, (3, 3))
        text.img = cv2.morphologyEx(text.img, cv2.MORPH_GRADIENT, kernel)
        text.img = cv2.bitwise_not(text.img)

    def _add_random_noise(self, bright_noise=0, dark_noise=0):
        """
        Don't use this method in pre-processing, for this method is to raise the difficulty for algorithm testing
        :param bright_noise: the quantity of bright_noise
        :param dark_noise: the quantity of dark_noise
        :return:
        """
        h, w = self.img.shape[:2]

        bright_noise_x = np.random.randint(0, w, size=(1, bright_noise))
        bright = np.random.randint(0, h, size=(1, bright_noise))
        self.img[bright, bright_noise_x] = np.random.randint(192, 256, size=bright_noise)

        dark_noise_x = np.random.randint(0, w, size=(1, dark_noise))
        dark_noise_y = np.random.randint(0, h, size=(1, dark_noise))
        self.img[dark_noise_y, dark_noise_x] = np.random.randint(0, 64, size=dark_noise)

    def denoise(self, ksize=3):
        self.img = cv2.medianBlur(self.img, ksize)

    def skew_correction(self, angle=None, interpolation_mode=cv2.INTER_NEAREST):
        """
        Correct text skew that usally caused by document scanning
        :param angle: specify an angle, but not recommended.
        :param interpolation_mode: see cv::InterpolationFlags
        :return:
        """
        h, w = self.img.shape[:2]
        if angle is None:
            _, thresh = cv2.threshold(self.img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
            coords = np.column_stack(np.where(thresh > 0))  # get all non-zero pixel coords
            p1, p3, angle = cv2.minAreaRect(coords)  # bound them with a rotated rect

            # angle of minAreaRect is confusing, recommends to a good answer here
            # https://stackoverflow.com/questions/15956124/minarearect-angles-unsure-about-the-angle-returned
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle

            text_center = ((p1[0] + p3[0]) // 2, (p1[1] + p3[1]) // 2)
        else:
            text_center = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D(text_center, angle, 1)

        self.img = cv2.warpAffine(self.img, M, (w, h), flags=interpolation_mode, borderMode=cv2.BORDER_REPLICATE)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    img = cv2.imread("./test_chs_rotate.tiff", 0)

    text = TextImg(img)

    # text._add_random_noise(bright_noise=10000, dark_noise=10000)
    # cv2.imshow("Noise", text.img)
    #
    # text.denoise(3)
    # cv2.imshow("DeNoise", text.img)

    text.skew_correction(interpolation_mode=cv2.INTER_LANCZOS4)
    cv2.imshow("Skew Correction", text.img)
    cv2.waitKey(0)

    # text.blacken_text(150)
    # cv2.imshow("blacken_text", text.img)
    # cv2.waitKey(0)

    text.whiten_background(200)
    cv2.imshow("whiten_background", text.img)
    cv2.waitKey(0)

    text.stroke_text(cv2.MORPH_ELLIPSE)
    cv2.imshow("stroke_text", text.img)
    cv2.waitKey(0)

    text.skeleton_text()
    cv2.imshow("Text Skeleton", text.img)
    cv2.waitKey(0)

    text.sharpen_text()
    cv2.imshow("Text Sharpening", text.img)
    cv2.waitKey(0)



    text.img = imutils.resize(text.img, width=1000)

    # show color distribution histogram
    # hist = cv2.calcHist([text.img], [0], None, [256], [0, 256])
    #
    # plt.figure()
    # plt.plot(np.arange(0, 256), hist)
    # plt.xlim(50, 256)
    # plt.ylim(0, 4000)
    # plt.show()
