from text_processor import TextImg
import cv2

img = cv2.imread("./test_chs_rotate.tiff")

text = TextImg(img)

img = text.skew_correction(interpolation_mode=cv2.INTER_LANCZOS4)
cv2.imshow("Skew Correction", img)

img = text.blacken_text(150)
cv2.imshow("blacken_text", img)

img = text.whiten_background(200)
cv2.imshow("whiten_background", img)

demo_img, character_roi_set, character_loc_set = text.text_boundary(thresh=200)
cv2.imshow("Character recognition", demo_img)
cv2.waitKey(0)