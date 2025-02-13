from __future__ import absolute_import, unicode_literals
from celery import shared_task
import tensorflow as tf
import numpy as np
from PIL import Image
from tqdm import tqdm
from .models import DigitImage
from io import BytesIO
import os
import pandas as pd


def load_and_process_csv(csv_path):
    df = pd.read_csv(csv_path, header=None)
    images = df.iloc[:, 1:].values
    labels = df.iloc[:, 0].values
    return images, labels


def image_array_to_picture(image_array):
    try:
        image_array = np.array(image_array, dtype=np.uint8).reshape(28, 28)
        image = Image.fromarray(image_array, mode='L')
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Error converting image: {e}")
        return None


def insert_images_to_mongo(images, labels):
    with tqdm(total=len(images), desc="Inserting images into MongoDB", dynamic_ncols=True) as pbar:
        for image_array, label in zip(images, labels):
            image = image_array_to_picture(image_array)
            if image:
                try:
                    digit_image = DigitImage(
                        image=image,
                        label=label,
                        verified=True
                    )
                    digit_image.save()
                except Exception as e:
                    print(f"Error inserting image: {e}")
            pbar.update(1)
            pbar.refresh()


def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


@shared_task
def train_and_save_model():
    images = []
    labels = []

    digit_images = DigitImage.objects.filter(verified=True)
    for digit_image in digit_images:
        image = Image.open(BytesIO(digit_image.image.read())).convert('L')
        image_array = np.array(image).reshape((28, 28)) * 255
        images.append(image_array)
        labels.append(digit_image.label)

    if images and labels:
        X = np.array(images)
        y = np.array(labels)

        model = create_model()
        model.fit(X, y, epochs=2, validation_split=0.2)

        model.save('ocr_model_old.h5')


@shared_task
def initialize_and_save_model():
    if os.path.exists('ocr_model_old.h5'):
        print("Le modèle existe déjà. Ignorer l'entraînement initial.")
        return

    images = []
    labels = []

    base_path = os.path.dirname(os.path.abspath(__file__))
    train_csv_path = os.path.join(base_path, '../mnist_train.csv')
    test_csv_path = os.path.join(base_path, '../mnist_test.csv')

    train_images, train_labels = load_and_process_csv(train_csv_path)
    test_images, test_labels = load_and_process_csv(test_csv_path)

    insert_images_to_mongo(train_images, train_labels)
    insert_images_to_mongo(test_images, test_labels)

    digit_images = DigitImage.objects.filter(verified=True)
    for digit_image in digit_images:
        image = Image.open(BytesIO(digit_image.image.read())).convert('L')
        image_array = np.array(image).reshape((28, 28)) * 255
        images.append(image_array)
        labels.append(digit_image.label)

    if images and labels:
        X = np.array(images)
        y = np.array(labels)

        model = create_model()
        model.fit(X, y, epochs=5, validation_split=0.2)

        model.save('ocr_model_old.h5')
    else:
        print("No data available for initial training.")
