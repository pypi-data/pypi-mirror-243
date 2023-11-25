import csv
import os
import zipfile
from pathlib import Path
from typing import Any, List, Tuple

import gdown
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class Diabetes(torch.utils.data.Dataset):
    _path = os.path.join(str(Path.home()), "datasets")
    _dataset = os.path.join(_path, "diabetes.csv")
    _zipped_dataset = os.path.join(_path, "diabetes.zip")
    _url = "https://drive.google.com/uc?id=1kN1FeKs1LXYFFDeItbXN1GCc8buXoGAr"

    def __init__(self, train: bool = True):
        super().__init__()
        if not os.path.isfile(Diabetes._dataset):
            gdown.download(url=Diabetes._url, output=Diabetes._zipped_dataset)
            with zipfile.ZipFile(Diabetes._zipped_dataset, "r") as file:
                file.extractall(Diabetes._path)
        features, labels = Diabetes.load_data(Diabetes._dataset)
        train_features, test_features, train_labels, test_labels = train_test_split(
            features,
            labels,
            test_size=0.30,
            random_state=torch.random.initial_seed(),
            shuffle=True,
        )
        scaler = StandardScaler()
        if train:
            train_features = scaler.fit_transform(train_features)
            train_features = train_features.astype("float32")
            self.data = train_features
            self.targets = train_labels
        else:
            test_features = scaler.fit_transform(test_features)
            test_features = test_features.astype("float32")
            self.data = test_features
            self.targets = test_labels
        self.classes = ["Negative", "Positive"]

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        features, labels = self.data[index], self.targets[index]
        labels = labels.astype("int64")
        return (features, labels)

    def __len__(self) -> int:
        return len(self.data)

    @staticmethod
    def load_data(filename: str = "~/datasets/diabetes.csv") -> Tuple[Any, Any]:
        dataset = list()
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                else:
                    row = list(map(lambda element: float(element), row))
                    dataset.append(np.array(row))
        dataset = np.array(dataset)
        features, labels = dataset[:, :-1], dataset[:, -1]
        return features, labels
