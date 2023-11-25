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
"""PyTorch dataset loader repository"""
from pt_datasets.create_dataloader import create_dataloader
from pt_datasets.create_dataset import create_dataset
from pt_datasets.encode_features import encode_features
from pt_datasets.load_dataset import load_dataset

__author__ = "Abien Fred Agarap"
__version__ = "0.19.2"


def list_datasets() -> str:
    datasets = [
        "MNIST",
        "Fashion-MNIST",
        "EMNIST",
        "KMNIST",
        "SVHN",
        "CIFAR10",
        "AG News",
        "20 Newsgroups",
        "IMDB",
        "Yelp",
        "Malware Image",
        "Wisconsin Diagnostic Breast Cancer",
        "Binary COVID19",
        "Multi COVID19",
        "USPS",
        "Pima Indians Diabetes",
    ]
    return datasets
