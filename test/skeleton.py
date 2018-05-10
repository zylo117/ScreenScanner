import cv2
import numpy as np


def skeletonize(image, size, structuring=cv2.MORPH_RECT):
    # determine the area (i.e. total number of pixels in the image),
    # initialize the output skeletonized image, and construct the
    # morphological structuring element
    area = image.shape[0] * image.shape[1]
    skeleton = np.zeros(image.shape, dtype="uint8")
    elem = cv2.getStructuringElement(structuring, size)

    # keep looping until the erosions remove all pixels from the
    # image
    while True:
        # erode and dilate the image using the structuring element
        eroded = cv2.erode(image, elem)
        cv2.imshow("test", eroded)
        cv2.waitKey(0)

        temp = cv2.dilate(eroded, elem)
        cv2.imshow("test", temp)
        cv2.waitKey(0)

        # subtract the temporary image from the original, eroded
        # image, then take the bitwise 'or' between the skeleton
        # and the temporary image
        temp = cv2.subtract(image, temp)
        cv2.imshow("test", temp)
        cv2.waitKey(0)

        skeleton = cv2.bitwise_or(skeleton, temp)
        cv2.imshow("test", skeleton)
        cv2.waitKey(0)
        image = eroded.copy()

        # if there are no more 'white' pixels in the image, then
        # break from the loop
        if area == area - cv2.countNonZero(image):
            break

    # return the skeletonized image
    return skeleton

if __name__ == "__main__":
    img = cv2.imread("skeleton.jpg", 0)
    cv2.imshow("Img", img)
    cv2.waitKey(0)

    skeletonize(img, (3, 3))