#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
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
Convtiny model definition for DVS handy classification.
"""

__all__ = ["convtiny_dvs_handy", "convtiny_handy_samsung_pretrained"]

from keras import Model
from keras.layers import Input, Reshape, Dropout, Activation

from ..layer_blocks import conv_block, separable_conv_block, dense_block
from ..utils import fetch_file, get_params_by_version
from ..model_io import load_model, get_model_path

# Locally fixed config options
# The number of neurons in the penultimate dense layer
# This layer has binary output spikes, and could be a bottleneck
# if care isn't taken to ensure enough info capacity
NUM_SPIKING_NEURONS = 256


def convtiny_dvs_handy(input_shape=(120, 160, 2), classes=9):
    """Instantiates a CNN for "Brainchip dvs_handy" example.

    Args:
        input_shape (tuple, optional): input shape tuple of the model. Defaults to (120, 160, 2).
        classes (int, optional): number of classes to classify images into. Defaults to 9.

    Returns:
        keras.Model: a Keras convolutional model for DVS Gesture.
    """

    img_input = Input(input_shape, name="input")

    # Model version management
    fused, post_relu_gap, relu_activation = get_params_by_version()

    x = conv_block(img_input,
                   filters=16,
                   kernel_size=(3, 3),
                   name='conv_0',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='max',
                   pool_size=(2, 2),
                   relu_activation=relu_activation,
                   strides=(1, 1))

    x = conv_block(x,
                   filters=32,
                   kernel_size=(3, 3),
                   name='conv_1',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='max',
                   pool_size=(2, 2),
                   relu_activation=relu_activation,
                   strides=(1, 1))

    x = conv_block(x,
                   filters=64,
                   kernel_size=(3, 3),
                   name='conv_2',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='max',
                   pool_size=(2, 2),
                   relu_activation=relu_activation,
                   strides=(1, 1))

    x = conv_block(x,
                   filters=128,
                   kernel_size=(3, 3),
                   name='conv_3',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='max',
                   pool_size=(2, 2),
                   relu_activation=relu_activation,
                   strides=(1, 1))

    x = conv_block(x,
                   filters=256,
                   kernel_size=(3, 3),
                   name='conv_4',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='max',
                   pool_size=(2, 2),
                   relu_activation=relu_activation,
                   strides=(1, 1))

    x = conv_block(x,
                   filters=512,
                   kernel_size=(3, 3),
                   name='conv_5',
                   use_bias=False,
                   add_batchnorm=True,
                   padding='same',
                   pooling='global_avg',
                   relu_activation=relu_activation,
                   post_relu_gap=post_relu_gap,
                   strides=(1, 1))

    bm_outshape = (1, 1, 512)

    x = Reshape(bm_outshape, name='reshape_1')(x)
    x = Dropout(1e-3, name='dropout')(x)

    x = separable_conv_block(x,
                             filters=NUM_SPIKING_NEURONS,
                             kernel_size=(3, 3),
                             use_bias=False,
                             padding='same',
                             name='spiking_layer',
                             add_batchnorm=True,
                             pooling=None,
                             relu_activation=relu_activation,
                             fused=fused)

    x = dense_block(x,
                    units=classes,
                    name='dense',
                    add_batchnorm=False,
                    relu_activation=False,
                    use_bias=False)

    act_function = 'softmax' if classes > 1 else 'sigmoid'
    x = Activation(act_function, name=f'act_{act_function}')(x)
    x = Reshape((classes,), name='reshape_2')(x)

    return Model(inputs=img_input, outputs=x, name='dvs_network')


def convtiny_handy_samsung_pretrained(quantized=True):
    """ Helper method to retrieve a `convtiny_dvs_handy` model that was trained
    on samsung_handy dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
                quantized or not. Defaults to True.
    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v1 = 'convtiny_dvs_handy_samsung_iq4_wq4_aq4.h5'
        file_hash_v1 = 'ac5dbf1420fbedc402da4394bb22cf94ff5cff73adb428cca741d6550f663c71'
        model_name_v2 = 'convtiny_dvs_handy_samsung_i4_w4_a4.h5'
        file_hash_v2 = '29cd8beabcb0576312e8673e8bf7cc41b92f6be82685357f848dfae39a172076'
    else:
        model_name_v1 = None
        file_hash_v1 = None
        model_name_v2 = 'convtiny_dvs_handy_samsung.h5'
        file_hash_v2 = '6cfb0e120f51dbad4961eb9ebdec32449f7113ddc55f864c0374f72fc77ae664'

    model_path, model_name, file_hash = get_model_path("convtiny", model_name_v1, file_hash_v1,
                                                       model_name_v2, file_hash_v2)
    model_path = fetch_file(model_path,
                            fname=model_name,
                            file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)
