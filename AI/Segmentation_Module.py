import cv2


def segment(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
    return img_contours
