import pytesseract as ocr
import cv2

sys_tessdata_config = '--tessdata-dir "/usr/local/share"'
user_tessdata_config = '--tessdata-dir "./training/tessdata/"'

if __name__ == "__main__":
    image = cv2.imread("./user.normal.exp1.png")
    # text = ocr.image_to_string(image, lang="user", config=user_tessdata_config)
    text = ocr.image_to_boxes(image, lang="chi_sim", config=sys_tessdata_config, output_type="bytes")

    box = open("./training/%s.%s.exp%s.box" %("user", "mes", "1"), mode="wb")
    cv2.imwrite("./training/%s.%s.exp%s.tiff" %("user", "mes", "1"), image)
    box.write(text)
    box.close()

    print(text)