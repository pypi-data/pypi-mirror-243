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
"""Medical datasets module"""
import os
from pathlib import Path
from typing import Tuple

import torch
import torchvision

from pt_datasets.datasets.COVID19Dataset import (
    BinaryCOVID19Dataset,
    MultiCOVID19Dataset,
)
from pt_datasets.datasets.Diabetes import Diabetes
from pt_datasets.datasets.WDBC import WDBC
from pt_datasets.download_covid_dataset import (
    download_binary_covid19_dataset,
    download_covidx5_dataset,
)
from pt_datasets.utils import unzip_dataset


def load_wdbc() -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the Wisconsin Diagnostic Breast Cancer dataset.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set for WDBC.
    test_dataset: torch.utils.data.Dataset
        The test set for WDBC.
    """
    train_dataset, test_dataset = WDBC(train=True), WDBC(train=False)
    return train_dataset, test_dataset


def load_binary_covid19(
    transform: torchvision.transforms,
    size: int = 64,
    preprocessed: bool = False,
    preprocessing_bsize: int = 2048,
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Returns a tuple of the tensor datasets for the
    train and test sets of the COVID19 binary classification dataset.

    Parameters
    ----------
    transform: torchvision.transform
        The transformation pipeline to use for image preprocessing.
    size: int
        The size to use for image resizing.
    preprocessed: bool
        Whether to load preprocessed dataset or not.
    preprocessing_bsize: int
        The batch size to use for preprocessing the dataset.

    Returns
    -------
    train_data: torch.utils.data.TensorDataset
        The training set of Binary COVID19 dataset.
    test_data: torch.utils.data.TensorDataset
        The test set of Binary COVID19 dataset.
    """
    dataset_path = os.path.join(str(Path.home()), "datasets")
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    if not os.path.exists(os.path.join(dataset_path, "BinaryCOVID19Dataset")):
        download_binary_covid19_dataset()
        unzip_dataset(os.path.join(dataset_path, "BinaryCOVID19Dataset.tar.xz"))
    (train_data, test_data) = (
        BinaryCOVID19Dataset(
            train=True,
            preprocessed=preprocessed,
            size=size,
            preprocessing_bsize=preprocessing_bsize,
        ),
        BinaryCOVID19Dataset(
            train=False,
            preprocessed=preprocessed,
            size=size,
            preprocessing_bsize=preprocessing_bsize,
        ),
    )
    return train_data, test_data


def load_multi_covid19(
    transform: torchvision.transforms,
    size: int = 64,
    preprocessed: bool = False,
    preprocessing_bsize: int = 2048,
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Returns a tuple of the tensor datasets for the
    train and test sets of the COVID19 multi-classification dataset.

    Parameters
    ----------
    transform: torchvision.transform
        The transformation pipeline to use for image preprocessing.
    size: int
        The size to use for image resizing.
    preprocessed: bool
        Whether to load preprocessed dataset or not.
    preprocessing_bsize: int
        The batch size to use for preprocessing the dataset.

    Returns
    -------
    train_data: torch.utils.data.TensorDataset
        The training set of COVIDx5 dataset.
    test_data: torch.utils.data.TensorDataset
        The test set of COVIDx5 dataset.
    """
    dataset_path = os.path.join(str(Path.home()), "datasets")
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    if not os.path.exists(os.path.join(dataset_path, "MultiCOVID19Dataset")):
        download_covidx5_dataset()
        unzip_dataset(os.path.join(dataset_path, "MultiCOVID19Dataset.tar.xz"))
    (train_data, test_data) = (
        MultiCOVID19Dataset(
            train=True,
            preprocessed=preprocessed,
            size=size,
            preprocessing_bsize=preprocessing_bsize,
        ),
        MultiCOVID19Dataset(
            train=False,
            preprocessed=preprocessed,
            size=size,
            preprocessing_bsize=preprocessing_bsize,
        ),
    )
    return train_data, test_data


def load_diabetes() -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the Pima Indians Diabetes dataset.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set.
    """
    train_dataset, test_dataset = Diabetes(train=True), Diabetes(train=False)
    return train_dataset, test_dataset
