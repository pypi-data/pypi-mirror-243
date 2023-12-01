#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
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
"""Sample extraction from datasets"""

import numpy as np
import tensorflow as tf
from typing import Iterable
import itertools


def extract_samples(out_file, dataset, nb_samples=1024):
    """Extracts samples from dataset and save them to a npz file.

    Args:
        out_file (str): name of output file
        dataset (numpy.ndarray or tf.data.Dataset): dataset for extract samples
        nb_samples (int, optional): number of samples. Defaults to 1024.
    """
    # The expected number of samples
    if isinstance(dataset, np.ndarray):
        if len(dataset) < nb_samples:
            raise ValueError("Not enough samples in the dataset.")
        samples_x = dataset[0:nb_samples].astype('float32')
    elif isinstance(dataset, tf.data.Dataset):
        samples_x, _ = next(dataset.as_numpy_iterator())
    elif isinstance(dataset, Iterable):
        dataset = itertools.islice(dataset, nb_samples)
        # drop labels
        xs, _ = itertools.tee(dataset)
        xs = (x[0] for x in xs)
        samples_x = next(xs)
    else:
        raise ValueError("Dataset format not supported.")
    samples = {"data": samples_x}
    np.savez(out_file, **samples)
    print(f"Samples saved as {out_file}")
