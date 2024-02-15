import numpy as np
import cv2
from .segment import line_horizontal_projection, word_vertical_projection, segment
from tensorflow.keras.models import load_model

persian_letters = ['ر', 'ا', 'ی', 'ن', 'ه', 'ق', 'پ', 'ن', 'د', 'ت', 'پ', 'ز', 'ه', 'ل', 'س', 'و', 'م', 'ح', 'م', 'ط', 'آ', 'چ', 'ف', 'ه', 'ب', 'ی', 'ک', 'ل', 'ژ', 'ج', 'خ', 'ﻻ', 'ص', 'ص', 'ش', 'ت', 'گ', 'ف', 'ک', 'ع', 'ع', 'ه', 'ذ', 'ح', 'س', 'گ', 'خ', 'ش', 'ض', 'ع', 'ب', 'ظ', 'غ', 'ض', 'ق', 'ج', 'چ', 'ئ', 'غ', 'ث', 'ث', 'غ', 'ی', '7', '3', '2', '9', '8', '6', '5', '4', '1', '0']


cnn = load_model('LeNet5.h5')


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
