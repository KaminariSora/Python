import tensorflow as tf
import pandas as pd
import numpy as np
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# ---------------------------
# STEP 1: Load CSV + Set Path
# ---------------------------
df = pd.read_csv('acne_dataset/labels.csv')
image_dir = 'acne_dataset/images'

# ---------------------------
# STEP 2: Custom data loader
# ---------------------------
img_height, img_width = 224, 224  # ขนาดภาพที่ model ต้องการ

def load_image_and_labels(filename, label):
    image_path = tf.strings.join([image_dir, filename], separator=os.sep)
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [img_height, img_width])
    image = image / 255.0  # normalize

    return image, label

# Convert filenames and labels
filenames = df['filename'].values
labels = df[['blackhead', 'inflammatory', 'pustule']].values.astype(np.float32)

# Convert to TensorFlow dataset
dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
dataset = dataset.map(load_image_and_labels)
dataset = dataset.shuffle(buffer_size=100).batch(32).prefetch(tf.data.AUTOTUNE)
