import pytesseract


def ocr_tesseract(img):
    # text = pytesseract.image_to_string(img, lang='fas')
    text = pytesseract.image_to_string(img)
    return (text)
