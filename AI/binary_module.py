import cv2

def black_and_white(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    adaptive_threshold = cv2.adaptiveThreshold(
        image_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2
    )
    wb = 255-adaptive_threshold

    return wb
