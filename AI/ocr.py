import numpy as np
import cv2
from .segment import line_horizontal_projection, word_vertical_projection, segment
from tensorflow.keras.models import load_model

persian_letters=['ﻪ', 'ر', '3', 'ژ', 'ﻬ', 'ه', 'ظ', '7', 'ن', '9', 'ق', '6', '5', '1', 'ث', 'ب', 'ل', 'ا', 'ع', 'ض', 'ح', '4', 'س', 'ز', 'ک', 'آ', 'خ', 'ص', 'ش', 'گ', 'پ', 'چ', 'غ', 'ت', '8', '2', 'م', 'و', 'د', '0', 'ف', 'ﻻ', 'ﺋ', 'ط', 'ی', 'ج', 'ﻫ', 'ذ']

cnn = load_model('ocr_tuesday_3.h5')


def OCR(img):
    text = []
    c = 0
    # segment main image to image of lines
    lines = line_horizontal_projection(img)
    for line in lines:
        # segment image to image of a lines to images of words
        words = word_vertical_projection(line)
        for word in words:
            if c != 0:
                text.append(' ')
            c += 1
            # segment image to image of a word to images of characters
            alphas = segment(line, word)
            for alpha in alphas:
                height, original_width = alpha.shape
                if 25 - original_width > 0:
                    add_width = (25 - original_width) / 2
                    left_columns = int(add_width)
                    right_columns = int(add_width)
                    new_width = 25
                    new_img = np.zeros((height, new_width), dtype=np.uint8)
                    new_img[:, left_columns:left_columns +
                            original_width] = alpha
                    new_img = cv2.resize(new_img, (new_width, 30))
                else:
                    new_img = cv2.resize(alpha, (25, 30))

                _, targ = cv2.threshold(new_img, 128, 255, cv2.THRESH_BINARY)
                targ = np.expand_dims(targ, axis=-1)
                targ = np.array(targ)
                targ = targ / 255.0
                targ = targ.reshape((1, 30, 25, 1))
                text.append(persian_letters[np.argmax(cnn.predict(targ))])

    return text
