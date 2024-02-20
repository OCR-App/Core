# Persian OCR

![image](https://github.com/OCR-App/Core/assets/112611803/a13c3dc2-03ba-447a-af5a-1898e8f44b4b)

This project implements a LeNet convolutional neural network (CNN) for recognizing Persian letters. The model has been trained on a dataset consisting of 570,000 images of Persian letters, and it can accurately classify individual letters from images.

## Dataset

Finding a suitable dataset for classifying Persian alphabets proved challenging, so we took matters into our own hands and created one! The dataset used for training the model can be found on Kaggle: [Persian Alphabets and Numbers](https://www.kaggle.com/datasets/mostafamohammadi1/persian-alphabets-and-numbers).
This meticulously curated dataset contains a diverse collection of images featuring handwritten Persian letters and numbers. With over [number of images] samples, it provides ample data for training robust and accurate models for Persian letter recognition.
We've ensured the dataset's quality and diversity to encompass various writing styles and variations commonly found in real-world scenarios. Whether it's distinct handwriting styles or variations in letter shapes, our dataset offers a comprehensive representation of Persian script.
Feel free to explore and utilize this dataset for your own projects, and don't hesitate to provide feedback or contribute to its enrichment.


## Model Architecture

The LeNet neural network architecture consists of several layers, including convolutional layers, pooling layers, and fully connected layers. The exact architecture used in this project is as follows:

1. Convolutional Layer (input: 30x25x1, output: 28x223x32)
2. ReLU Activation
3. Average Pooling (output: 14x11x32)
4. Convolutional Layer (output: 12x9x64)
5. ReLU Activation
6. Average Pooling (output: 6x4x64)
7. Convolutional Layer (output: 4x3x128)
8. Flatten (output: 1536)
9. Fully Connected Layer (output: 120)
10. ReLU Activation
11. Fully Connected Layer (output: 84)
12. ReLU Activation
13. Output Layer (output: 73, representing 10 classes of Persian letters)

## Usage

To use the trained model for letter recognition, you can install the app and use. We also provide English image to text using EasyOCR.

