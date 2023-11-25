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
"""Vision datasets module"""
import os
from pathlib import Path
from typing import Tuple

import gdown
import numpy as np
import torch
import torchvision
from sklearn.model_selection import train_test_split


def load_dataset(
    name: str,
    data_folder: str = "~/datasets",
    augment: bool = False,
    normalize: bool = False,
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads an image benchmark classification dataset.

    Parameters
    ----------
    name: str
        The name of the dataset to load.
        The following are the supported datasets:
            1. mnist
            2. emnist
            3. fashion_mnist
            4. kmnist
            5. usps
            6. cifar10
            7. svhn
            8. malimg
    data_folder: str
        The path to the folder for the datasets.
    augment: bool
        Whether to augment the dataset or not.
    normalize: bool
        Whether to normalize the features or not.

    Returns
    -------
    Tuple
        train_dataset: torch.utils.data.Dataset
            The training dataset object.
        test_dataset: torch.utils.data.Dataset
            The test dataset object
    """
    if name == "mnist":
        train_dataset, test_dataset = load_mnist(
            data_folder=data_folder, augment=augment, normalize=normalize
        )
    elif name == "emnist":
        train_dataset, test_dataset = load_emnist(
            data_folder=data_folder, augment=augment
        )
    elif name == "fashion_mnist":
        train_dataset, test_dataset = load_fashion_mnist(
            data_folder=data_folder, augment=augment
        )
    elif name == "kmnist":
        train_dataset, test_dataset = load_kmnist(
            data_folder=data_folder, augment=augment
        )
    elif name == "usps":
        train_dataset, test_dataset = load_usps(data_folder=data_folder)
    elif name == "cifar10":
        train_dataset, test_dataset = load_cifar10(
            data_folder=data_folder, normalize=normalize
        )
    elif name == "svhn":
        train_dataset, test_dataset = load_svhn(data_folder=data_folder)
    elif name == "malimg":
        train_dataset, test_dataset = load_malimg()
    return train_dataset, test_dataset


def load_mnist(
    data_folder: str = "~/datasets", augment: bool = False, normalize: bool = False
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the MNIST training and test datasets.

    Parameters
    ----------
    data_folder: str
        The path to the folder for the datasets.
    augment: bool
        Whether to perform data augmentation or not.
    normalize: bool
        Whether to normalize data or not.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set.
    """
    train_transform = torchvision.transforms.Compose(
        [torchvision.transforms.ToTensor()]
    )
    test_transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    if augment:
        train_transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToTensor(),
                torchvision.transforms.RandomHorizontalFlip(),
                torchvision.transforms.RandomVerticalFlip(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,)),
            ]
        )
    elif normalize:
        train_transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize((0.1307,), (0.3081,)),
            ]
        )
    train_dataset = torchvision.datasets.MNIST(
        root=data_folder, train=True, download=True, transform=train_transform
    )
    test_dataset = torchvision.datasets.MNIST(
        root=data_folder, train=False, download=True, transform=test_transform
    )
    return train_dataset, test_dataset


def load_fashion_mnist(
    data_folder: str = "~/dataset", augment: bool = False
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the Fashion-MNIST training and test datasets.

    Parameters
    ----------
    data_folder: str
        The path to the folder for the datasets.
    augment: bool
        Whether to perform data augmentation or not.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set.
    """
    train_transform = torchvision.transforms.Compose(
        [torchvision.transforms.ToTensor()]
    )
    test_transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    if augment:
        train_transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToTensor(),
                torchvision.transforms.RandomHorizontalFlip(),
                torchvision.transforms.RandomVerticalFlip(),
            ]
        )
    train_dataset = torchvision.datasets.FashionMNIST(
        root=data_folder, train=True, download=True, transform=train_transform
    )
    test_dataset = torchvision.datasets.FashionMNIST(
        root=data_folder, train=False, download=True, transform=test_transform
    )
    return train_dataset, test_dataset


def load_emnist(
    data_folder: str = "~/dataset", augment: bool = False
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the EMNIST training and test datasets.


    Parameters
    ----------
    data_folder: str
        The path to the folder for the datasets.
    augment: bool
        Whether to perform data augmentation or not.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set.
    """
    train_transform = torchvision.transforms.Compose(
        [torchvision.transforms.ToTensor()]
    )
    test_transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    if augment:
        train_transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToTensor(),
                torchvision.transforms.RandomHorizontalFlip(),
                torchvision.transforms.RandomVerticalFlip(),
            ]
        )
    train_dataset = torchvision.datasets.EMNIST(
        root=data_folder,
        train=True,
        split="balanced",
        download=True,
        transform=train_transform,
    )
    test_dataset = torchvision.datasets.EMNIST(
        root=data_folder,
        train=False,
        split="balanced",
        download=True,
        transform=test_transform,
    )
    return (train_dataset, test_dataset)


def load_kmnist(
    data_folder: str = "~/datasets", augment: bool = False
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the KMNIST training and test datasets.

    Parameter
    ---------
    data_folder: str
        The path to the folder for the datasets.
    normalize: bool
        Whether to normalize the dataset or not.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set.
    """
    train_transform = torchvision.transforms.Compose(
        [torchvision.transforms.ToTensor()]
    )
    test_transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    if augment:
        train_transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToTensor(),
                torchvision.transforms.RandomHorizontalFlip(),
                torchvision.transforms.RandomVerticalFlip(),
            ]
        )
    train_dataset = torchvision.datasets.KMNIST(
        root=data_folder, train=True, download=True, transform=train_transform
    )
    test_dataset = torchvision.datasets.KMNIST(
        root=data_folder, train=False, download=True, transform=test_transform
    )
    return (train_dataset, test_dataset)


def load_usps(
    data_folder: str = "~/datasets",
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the USPS training and test datasets.

    Parameter
    ---------
    data_folder: str
        The path to the folder for the datasets.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set.
    """
    train_transform = torchvision.transforms.Compose(
        [torchvision.transforms.ToTensor()]
    )
    test_transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    train_dataset = torchvision.datasets.USPS(
        root=data_folder, train=True, download=True, transform=train_transform
    )
    test_dataset = torchvision.datasets.USPS(
        root=data_folder, train=False, download=True, transform=test_transform
    )
    return (train_dataset, test_dataset)


def load_cifar10(data_folder: str = "~/datasets", normalize: bool = False):
    """
    Loads the CIFAR10 training and test datasets.

    Parameter
    ---------
    data_folder: str
        The path to the folder for the datasets.
    normalize: bool
        Whether to normalize the dataset or not.

    Returns
    -------
    train_dataset: torch.utils.data.Dataset
        The training set.
    test_dataset: torch.utils.data.Dataset
        The test set.
    """
    transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    if normalize:
        transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize(
                    (0.4914, 0.4822, 0.4465), (0.2471, 0.2435, 0.2616)
                ),
            ]
        )
    train_dataset = torchvision.datasets.CIFAR10(
        root=data_folder, train=True, download=True, transform=transform
    )
    test_dataset = torchvision.datasets.CIFAR10(
        root=data_folder, train=False, download=True, transform=transform
    )
    return train_dataset, test_dataset


def load_svhn(
    data_folder: str = "~/datasets",
) -> Tuple[torch.utils.data.Dataset, torch.utils.data.Dataset]:
    """
    Loads the SVHN training and test datasets.

    Parameter
    ---------
    data_folder: str
        The path to the folder for the datasets.

    Returns
    -------
    Tuple
        train_dataset: torch.utils.data.Dataset
            The training set.
        test_dataset: torch.utils.data.Dataset
            The test set.
    """
    train_transform = torchvision.transforms.Compose(
        [torchvision.transforms.ToTensor()]
    )
    test_transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    train_dataset = torchvision.datasets.SVHN(
        root=data_folder, split="train", download=True, transform=train_transform
    )
    test_dataset = torchvision.datasets.SVHN(
        root=data_folder, split="test", download=True, transform=test_transform
    )
    return train_dataset, test_dataset


def load_malimg(
    test_size: float = 0.3, seed: int = 42
) -> Tuple[torch.utils.data.DataLoader, torch.utils.data.DataLoader]:
    """
    Returns a tuple of tensor datasets for the
    training and test splits of MalImg dataset.

    Parameters
    ----------
    test_size: float
        The size of the test set.
    seed: int
        The random seed to use for splitting.

    Returns
    -------
    Tuple[torch.utils.data.DataLoader, torch.utils.data.DataLoader]
        train_dataset
            The training set of MalImg dataset.
        test_dataset
            The test set of MalImg dataset.
    """
    download_url = "https://drive.google.com/uc?id=1Y6Ha5Jir8EI726KdwAKWHVU-oWmPqNDT"
    malimg_filename = "malimg_dataset_32x32.npy"
    dataset_path = os.path.join(str(Path.home()), "datasets")
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    if not os.path.isfile(os.path.join(dataset_path, malimg_filename)):
        gdown.download(
            download_url, os.path.join(dataset_path, malimg_filename), quiet=True
        )
    dataset = np.load(os.path.join(dataset_path, malimg_filename), allow_pickle=True)
    train_data, test_data = train_test_split(
        dataset, test_size=test_size, random_state=seed
    )
    train_features, train_labels = train_data[:, : (32**2)], train_data[:, -1]
    test_features, test_labels = test_data[:, : (32**2)], test_data[:, -1]
    train_dataset = torch.utils.data.TensorDataset(
        torch.from_numpy(train_features), torch.from_numpy(train_labels)
    )
    test_dataset = torch.utils.data.TensorDataset(
        torch.from_numpy(test_features), torch.from_numpy(test_labels)
    )
    return train_dataset, test_dataset
