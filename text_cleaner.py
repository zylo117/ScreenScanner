import cv2
import imutils
import numpy as np
import pytesseract


class TextImg:
    def __init__(self, img):
        self.img = img
        self.gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def whiten_background(self, thresh_val=None):
        if thresh_val is not None:
            self.gray_img[self.gray_img > thresh_val] = 255
        else:
            thresh_val, _ = cv2.threshold(self.gray_img, 0, 255, cv2.THRESH_OTSU)
            self.gray_img[self.gray_img > thresh_val] = 255

        return self.gray_img

    def blacken_text(self, thresh_val=None):
        if thresh_val is not None:
            self.gray_img[self.gray_img < thresh_val] = 0
        else:
            thresh_val, self.gray_img = cv2.threshold(self.gray_img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_TOZERO)

        return self.gray_img

    def sharpen_text(self, kernel=None):
        """

        :return:
        """
        if kernel is None:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # Laplacian sharpen kernel, too thick for text
        invert = cv2.bitwise_not(self.gray_img).astype(np.uint16)
        sharpen_mask = cv2.filter2D(invert, cv2.CV_64F, kernel, borderType=cv2.BORDER_REPLICATE)
        self.gray_img = cv2.convertScaleAbs(cv2.convertScaleAbs(sharpen_mask) + invert)
        self.gray_img = cv2.bitwise_not(self.gray_img)

        return self.gray_img

    def denoise(self, ksize=3):
        self.gray_img = cv2.medianBlur(self.gray_img, ksize)

        return self.gray_img

    def skew_correction(self, angle=None, interpolation_mode=cv2.INTER_NEAREST):
        """
        Correct text skew that usally caused by document scanning
        :param angle: specify an angle, but not recommended.
        :param interpolation_mode: see cv::InterpolationFlags
        :return:
        """
        h, w = self.gray_img.shape[:2]
        if angle is None:
            _, thresh = cv2.threshold(self.gray_img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
            coords = np.column_stack(np.where(thresh > 0))  # get all non-zero pixel coords
            anchor, size, angle = cv2.minAreaRect(coords)  # bound them with a rotated rect

            # angle of minAreaRect is confusing, recommends to a good answer here
            # https://stackoverflow.com/questions/15956124/minarearect-angles-unsure-about-the-angle-returned
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle

            text_center = (anchor[0] + size[0] // 2, anchor[1] + size[1] // 2)
        else:
            text_center = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D(text_center, angle, 1)

        self.gray_img = cv2.warpAffine(self.gray_img, M, (w, h), flags=interpolation_mode, borderMode=cv2.BORDER_REPLICATE)

        return self.gray_img

    # experimental, hardcore
    def skeleton_text(self):
        self.gray_img = cv2.bitwise_not(self.gray_img)
        self.gray_img = imutils.skeletonize(self.gray_img, (3, 3), cv2.MORPH_ELLIPSE)

        self.gray_img = cv2.dilate(self.gray_img, None)
        self.gray_img = cv2.bitwise_not(self.gray_img)

        return self.gray_img

    def stroke_text(self, elem=cv2.MORPH_ELLIPSE):
        kernel = cv2.getStructuringElement(elem, (3, 3))
        text.gray_img = cv2.morphologyEx(text.gray_img, cv2.MORPH_GRADIENT, kernel)
        text.gray_img = cv2.bitwise_not(text.gray_img)

        return self.gray_img

    def _add_random_noise(self, bright_noise=0, dark_noise=0):
        """
        Don't use this method in pre-processing, for this method is to raise the difficulty for algorithm testing
        :param bright_noise: the quantity of bright_noise
        :param dark_noise: the quantity of dark_noise
        :return:
        """
        h, w = self.gray_img.shape[:2]

        bright_noise_x = np.random.randint(0, w, size=(1, bright_noise))
        bright = np.random.randint(0, h, size=(1, bright_noise))
        self.gray_img[bright, bright_noise_x] = np.random.randint(192, 256, size=bright_noise)

        dark_noise_x = np.random.randint(0, w, size=(1, dark_noise))
        dark_noise_y = np.random.randint(0, h, size=(1, dark_noise))
        self.gray_img[dark_noise_y, dark_noise_x] = np.random.randint(0, 64, size=dark_noise)

        return self.gray_img

    def text_boundary(self, kernel=None, iterations=8):
        # transform img into binary img
        _, img = cv2.threshold(self.gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        if kernel is None:
            # set kernel size into (1, 3), because line spacing is much bigger than character spacing
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
        # glue every parts of characters together and separate from one another
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)

        cnts = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        img = cv2.cvtColor(self.gray_img, cv2.COLOR_GRAY2BGR)
        rect_set = np.zeros((len(cnts), 4))  # create a set that filter the false detected rects
        for i in range(len(cnts)):
            x, y, w, h = cv2.boundingRect(cnts[i])
            rect_set[i] = [x, y, w, h]

        rect_mean = np.mean(rect_set, axis=0)

        real_rect_set = []
        for i in range(len(rect_set)):
            x, y, w, h = cv2.boundingRect(cnts[i])
            if w > rect_mean[2] and h > rect_mean[3]:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 1)
                real_rect_set.append([x, y, w, h])

        return img, real_rect_set


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    img = cv2.imread("./test_chs_rotate.tiff")

    text = TextImg(img)

    # text._add_random_noise(bright_noise=10000, dark_noise=10000)
    # cv2.imshow("Noise", text.img)
    #
    # text.denoise(3)
    # cv2.imshow("DeNoise", text.img)

    img = text.skew_correction(interpolation_mode=cv2.INTER_LANCZOS4)
    cv2.imshow("Skew Correction", img)

    img = text.blacken_text(150)
    cv2.imshow("blacken_text", img)

    img = text.whiten_background(200)
    cv2.imshow("whiten_background", img)

    img, real_rect_set = text.text_boundary()
    cv2.imshow("Character recognition", img)
    cv2.waitKey(0)

    # text.sharpen_text()
    # cv2.imshow("Text Sharpening", text.img)
    # cv2.waitKey(0)

    # text.stroke_text(cv2.MORPH_ELLIPSE)
    # cv2.imshow("stroke_text", text.img)
    # cv2.waitKey(0)

    # text.skeleton_text()
    # cv2.imshow("Text Skeleton", text.img)
    # cv2.waitKey(0)

    text.gray_img = imutils.resize(text.gray_img, width=1000)

    # show color distribution histogram
    # hist = cv2.calcHist([text.img], [0], None, [256], [0, 256])
    #
    # plt.figure()
    # plt.plot(np.arange(0, 256), hist)
    # plt.xlim(50, 256)
    # plt.ylim(0, 4000)
    # plt.show()
