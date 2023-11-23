import pytesseract

def ocr_tesseract(img, type: str):
    if type == "persian":
        text = pytesseract.image_to_string(img, lang='fas')
    elif type == "english":
        text = pytesseract.image_to_string(img)
    return (text)
