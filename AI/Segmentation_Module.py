import cv2

def segment(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    adaptive_threshold = cv2.adaptiveThreshold(
          image_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2
    )
    thresh_bw=255-adaptive_threshold
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 3))
    dilation = cv2.dilate(thresh_bw, rect_kernel, iterations = 3)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_contours = adaptive_threshold.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img_contours, (x, y), (x + w, y + h), (0, 255, 0), 1)
    return img_contours