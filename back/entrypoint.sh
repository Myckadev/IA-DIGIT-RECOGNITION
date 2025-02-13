#!/bin/sh

MNIST_TRAIN_PATH="/app/mnist_train.csv"
MNIST_TEST_PATH="/app/mnist_test.csv"

echo "📌 Checking for MNIST datasets in /app..."

if [ ! -f "$MNIST_TRAIN_PATH" ]; then
    echo "📥 Downloading mnist_train.csv..."
    wget -O "$MNIST_TRAIN_PATH" https://pjreddie.com/media/files/mnist_train.csv
else
    echo "✅ mnist_train.csv already exists, skipping download."
fi

if [ ! -f "$MNIST_TEST_PATH" ]; then
    echo "📥 Downloading mnist_test.csv..."
    wget -O "$MNIST_TEST_PATH" https://pjreddie.com/media/files/mnist_test.csv
else
    echo "✅ mnist_test.csv already exists, skipping download."
fi

echo "🚀 Starting Celery worker..."
exec celery -A back worker --loglevel=info
