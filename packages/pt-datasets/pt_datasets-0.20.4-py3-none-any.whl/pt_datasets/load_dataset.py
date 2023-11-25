# PyTorch Datasets utility repository
# Copyright (C) 2020  Abien Fred Agarap
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Function for loading datasets"""
from typing import Tuple

from pt_datasets.life import (
    load_binary_covid19,
    load_diabetes,
    load_multi_covid19,
    load_wdbc,
)
from pt_datasets.text import load_dataset as load_text_dataset
from pt_datasets.vision import load_dataset as load_vision_dataset

__author__ = "Abien Fred Agarap"


SUPPORTED_DATASETS = [
    "mnist",
    "fashion_mnist",
    "emnist",
    "cifar10",
    "svhn",
    "malimg",
    "ag_news",
    "20newsgroups",
    "kmnist",
    "imdb",
    "yelp",
    "wdbc",
    "binary_covid",
    "multi_covid",
    "diabetes",
]


def load_dataset(
    name: str = "mnist",
    normalize: bool = True,
    augment: bool = False,
    data_folder: str = "~/datasets",
    vectorizer: str = "tfidf",
    ngram_range: Tuple = (1, 5),
    return_vectorizer: bool = False,
    image_size: int = 64,
    preprocessed_covidx: bool = False,
    preprocessing_bsize: int = 2048,
) -> Tuple[object, object]:
    """
    Returns a tuple of torchvision dataset objects.

    Parameters
    ----------
    name: str
        The name of the dataset to load. Current choices:
            1. mnist (MNIST)
            2. fashion_mnist (FashionMNIST)
            3. emnist (EMNIST/Balanced)
            4. cifar10 (CIFAR10)
            5. svhn (SVHN)
            6. malimg (Malware Image classification)
            7. ag_news (AG News)
            8. 20newsgroups (20 Newsgroups text classification)
            9. kmnist (KMNIST)
            10. wdbc (Wiscosin Diagnostic Breast Cancer classification)
            11. binary_covid (Binary COVID19)
            12. multi_covid (Multi COVID19)
            13. imdb
            14. yelp
            15. usps
            16. diabetes (Pima Indians Diabetes)
    normalize: bool
        Whether to normalize images or not.
    augment: bool
        Whether to perform image augmentation or not.
        This is only used for *MNIST datasets.
    data_folder: str
        The path to the folder for the datasets.
    vectorizer: str
        The vectorization method to use.
        Options: [tfidf (default) | ngrams]
        This is only used for datasets [name = ag_news | 20newsgroups].
    ngram_range: Tuple
        The lower and upper bound of ngram range to use.
        Default: [(3, 3)]
    return_vectorizer: bool
        Whether to return the vectorizer object or not.
        This is only used for datasets [name = ag_news | 20newsgroups].
    image_size: int
        The image size to use for COVID19 datasets.
    preprocessed_covidx: bool
        Whether to use the preprocessed COVID19 datasets or not.
        This requires the use of `modules/export_covid19_dataset`
        in the package repository.
    preprocessing_bsize: int
        The batch size to use for preprocessing the COVID19 dataset.

    Returns
    -------
    Tuple[object, object]
        A tuple consisting of the training dataset and the test dataset.
    """
    supported_datasets = [
        "mnist",
        "fashion_mnist",
        "emnist",
        "cifar10",
        "svhn",
        "malimg",
        "ag_news",
        "20newsgroups",
        "kmnist",
        "wdbc",
        "binary_covid",
        "multi_covid",
        "usps",
        "imdb",
        "yelp",
        "diabetes",
    ]

    name = name.lower()

    _supported = f"Supported datasets: {supported_datasets}"
    assert (
        name in supported_datasets
    ), f"[ERROR] Dataset {name} is not supported. {_supported}"

    if name in [
        "mnist",
        "emnist",
        "fashion_mnist",
        "kmnist",
        "usps",
        "cifar10",
        "svhn",
        "malimg",
    ]:
        train_dataset, test_dataset = load_vision_dataset(
            name=name, data_folder=data_folder, augment=augment, normalize=normalize
        )
    elif name in ["ag_news", "20newsgroups", "imdb", "yelp"]:
        datasets = load_text_dataset(
            name=name,
            vectorizer=vectorizer,
            return_vectorizer=return_vectorizer,
            ngram_range=ngram_range,
        )
        if return_vectorizer:
            train_dataset, test_dataset, vectorizer = datasets
        else:
            train_dataset, test_dataset = datasets
    elif name == "wdbc":
        train_dataset, test_dataset = load_wdbc()
    elif name == "binary_covid":
        train_dataset, test_dataset = load_binary_covid19(
            transform=None,
            size=image_size,
            preprocessed=preprocessed_covidx,
            preprocessing_bsize=preprocessing_bsize,
        )
    elif name == "multi_covid":
        train_dataset, test_dataset = load_multi_covid19(
            transform=None,
            size=image_size,
            preprocessed=preprocessed_covidx,
            preprocessing_bsize=preprocessing_bsize,
        )
    elif name == "diabetes":
        train_dataset, test_dataset = load_diabetes()
    return (
        (train_dataset, test_dataset, vectorizer)
        if return_vectorizer
        else (train_dataset, test_dataset)
    )
