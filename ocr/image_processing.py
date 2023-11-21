import cv2
import pytesseract
import os
from .utils import str_generator


def segment(image):
    image = cv2.imread(image)
    print(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    _, thresh_bw = cv2.threshold(
        gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 3))
    dilation = cv2.dilate(thresh, rect_kernel, iterations=3)
    contours, hierarchy = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_contours = thresh_bw.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img_contours, (x, y), (x + w, y + h), (0, 255, 0), 1)
    photo_name = f"temp_{str_generator(4)}.png"
    cv2.imwrite(photo_name, img_contours)
    return os.path.abspath(photo_name)


def binary_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    adaptive_threshold = cv2.adaptiveThreshold(
        image_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2,
    )
    wb = 255-adaptive_threshold
    return wb


def ocr_tesseract(image):
    text = pytesseract.image_to_string(image, lang='fas')
    return (text)
