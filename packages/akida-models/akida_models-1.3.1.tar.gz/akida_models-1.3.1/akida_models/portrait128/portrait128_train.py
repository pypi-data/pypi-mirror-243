#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
Portrait128 training script.
"""

import os
import argparse

import tensorflow as tf
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.metrics import BinaryIoU

from cnn2snn import convert

from ..param_scheduler import get_cosine_lr_scheduler
from ..training import (get_training_parser, compile_model, evaluate_model, print_history_stats,
                        RestoreBest, save_model)
from ..extract import extract_samples
from ..model_io import load_model


def get_data(path, batch_size):
    """ Loads Portrait128 data.

    Args:
        path (str): path to npy data
        batch_size (int): the batch size

    Returns:
        tuple: train generator, validation generator, steps per epoch and validation step
    """
    # Load the dataset
    x_train = np.load(os.path.join(path, "img_uint8.npy"))
    y_train = np.load(os.path.join(path, "msk_uint8.npy")) / 255

    # Data generator for training and validation
    data_gen_args = dict(width_shift_range=0.1,
                         height_shift_range=0.1,
                         zoom_range=0.2,
                         horizontal_flip=True,
                         validation_split=0.2)

    image_datagen = ImageDataGenerator(**data_gen_args)
    mask_datagen = ImageDataGenerator(**data_gen_args)

    seed = 1
    train_image_generator = image_datagen.flow(x_train,
                                               batch_size=batch_size,
                                               shuffle=True,
                                               subset='training',
                                               seed=seed)

    train_mask_generator = mask_datagen.flow(y_train,
                                             batch_size=batch_size,
                                             shuffle=True,
                                             subset='training',
                                             seed=seed)

    val_image_generator = image_datagen.flow(x_train,
                                             batch_size=batch_size,
                                             shuffle=True,
                                             subset='validation',
                                             seed=seed)

    val_mask_generator = mask_datagen.flow(y_train,
                                           batch_size=batch_size,
                                           shuffle=True,
                                           subset='validation',
                                           seed=seed)

    # Combine generators into one which yields image and masks
    train_generator = zip(train_image_generator, train_mask_generator)
    val_generator = zip(val_image_generator, val_mask_generator)

    return (train_generator, val_generator, train_image_generator.n // batch_size,
            val_image_generator.n // batch_size)


def train_model(model, train_gen, steps_per_epoch, val_gen, val_steps, epochs, learning_rate):
    """ Trains the model.

    Args:
        model (keras.Model): the model to train
        train_gen (keras.ImageDataGenerator): train data generator
        steps_per_epoch (int): training steps
        val_gen (keras.ImageDataGenerator): validation data generator
        val_steps (int): validation steps
        epochs (int): the number of epochs
        learning_rate (float): the learning rate
    """
    # Define learning rate scheduler
    callbacks = [get_cosine_lr_scheduler(learning_rate, epochs * steps_per_epoch, True)]

    # Model checkpoints (save best model and retrieve it when training is complete)
    restore_model = RestoreBest(model, monitor="val_binary_io_u")
    callbacks.append(restore_model)

    history = model.fit(train_gen,
                        epochs=epochs,
                        steps_per_epoch=steps_per_epoch,
                        validation_steps=val_steps,
                        validation_data=val_gen,
                        callbacks=callbacks)
    print_history_stats(history)


def evaluate_akida_model(model, val_gen, val_steps):
    """ Evaluates Akida model.

    Args:
        model (akida.Model): model to evaluate
        val_gen (generator): validation data
        val_steps (int): validation steps
    """
    # Initialize to None to allow different shapes depending on the caller
    labels = None
    pots = None

    for _ in range(val_steps):
        batch, label_batch = next(val_gen)
        pots_batch = model.predict(batch.astype('uint8'))

        if labels is None:
            labels = label_batch
            pots = pots_batch
        else:
            labels = np.concatenate((labels, label_batch))
            pots = np.concatenate((pots, pots_batch))
    preds = tf.keras.activations.sigmoid(pots)

    m_binary_iou = tf.keras.metrics.BinaryIoU(target_class_ids=[0, 1], threshold=0.5)
    m_binary_iou.update_state(labels, preds)
    binary_iou = m_binary_iou.result().numpy()

    m_accuracy = tf.keras.metrics.Accuracy()
    m_accuracy.update_state(labels, preds > 0.5)
    accuracy = m_accuracy.result().numpy()
    print(f"Akida BinaryIoU/pixel accuracy: {binary_iou:.4f}/{100*accuracy:.2f}%")


def main():
    """ Entry point for script and CLI usage.

    Note: Download the Portrait-Segmentation dataset from
    [Portrait128website](https://github.com/anilsathyan7/Portrait-Segmentation)
    """
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("-d", "--data", type=str,
                               required=True,
                               help="Path to the Portrait128 data.")

    parsers = get_training_parser(batch_size=32, tune=True, extract=True,
                                  global_parser=global_parser)
    args = parsers[0].parse_args()

    # Load the source model
    model = load_model(args.model)

    # Compile model
    learning_rate = 3e-5
    if args.action == "tune":
        learning_rate /= 10

    compile_model(model, learning_rate=learning_rate, loss='binary_crossentropy',
                  metrics=[BinaryIoU(), 'accuracy'])

    # Load data
    train_gen, val_gen, steps_per_epoch, val_steps = get_data(args.data, args.batch_size)

    # Disable QuantizeML assertions
    os.environ["ASSERT_ENABLED"] = "0"

    # Train model
    if args.action in ["train", "tune"]:
        train_model(model, train_gen, steps_per_epoch, val_gen,
                    val_steps, args.epochs, learning_rate)
        save_model(model, args.model, args.savemodel, args.action)
    elif args.action == "eval":
        # Evaluate model accuracy
        if args.akida:
            model = convert(model)
            evaluate_akida_model(model, val_gen, val_steps)
        else:
            evaluate_model(model, val_gen, steps=val_steps, print_history=True)
    elif args.action == 'extract':
        # Extract samples from dataset
        extract_samples(args.savefile, train_gen, args.batch_size)


if __name__ == "__main__":
    main()
