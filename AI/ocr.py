import numpy as np
import cv2
from .segment import line_horizontal_projection, word_vertical_projection, segment
from tensorflow.keras.models import load_model
import os

persian_letters = ['ﺛ', 'ﻣ', 'ﺑ', 'ل', 'ﮐ', 'ﺷ', 'ح', 'ژ', 'د', '2', 'و', 'ت', 'ک', '9', 'ن', 'م', 'ف', 'ط', '6', 'ﻻ',
                   'ﭘ', 'ﻧ', 'ﻏ', '،', 'ض', 'ﻳ', 'ج', 'ﻫ', 'پ', 'ﻟ', 'ﻋ', 'ز', 'ب', 'ﺻ', 'ق', '1', '3', 'ث', '0', 'ﻓ',
                   'آ', 'ﺗ', 'ﭼ', 'ه', 'ﺧ', 'ی', '5', 'ﻪ', 'ﻌ', 'ذ', 'ﺿ', 'ﺣ', 'چ', 'ا', '8', '4', 'ﺋ', 'ﺳ', 'ظ', 'غ',
                   'ﮔ', 'ﻬ', 'ص', '.', 'ﯾ', 'خ', 'ﺟ', 'گ', 'ش', 'س', ':', 'ﻐ', 'ر', 'ع', 'ﻗ']


cnn = load_model(f'{os.getcwd()}/ocr.h5')


def OCR(img):
    text = []
    c = 0
    lines = line_horizontal_projection(img)
    for line in lines:
        words = word_vertical_projection(line)
        for word in words:
            if c != 0:
                text.append(' ')
            c += 1
            alphas = segment(line, word)
            for alpha in alphas:
                target = cv2.resize(alpha, (10, 20))
                target = target.astype('float32')/255
                target = np.expand_dims(target, axis=-1)
                target = np.reshape(target, (1, 20, 10, 1))
                text.append(persian_letters[np.argmax(cnn.predict(target))])
    return text
