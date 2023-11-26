import pathlib
from copy import copy
from os import PathLike
from typing import Union, Tuple, Any

import numpy as np
import pandas as pd

from uni_active.utils.file_io import save_model, load_model
from uni_active.utils.log import log

cat_method = {"np": np.concatenate, "pd": pd.concat,
              np.ndarray: np.concatenate, pd.DataFrame: pd.concat}


class DataSetLoop:

    def __repr__(self):
        return self.__str__()

    def __init__(self, data_train=None, data_test=None, targets: tuple = None, loop=0):
        self.data = {f"train-{loop}": data_train}
        self.data[f"test-{loop}"] = data_test
        self.max_loop = 0
        self.targets = targets

    @classmethod
    def from_xy(cls, data_train_x=None, data_train_y=None,
                data_test_x=None, data_test_y=None, loop=0):

        if data_train_x is not None and data_train_y is not None:
            if data_train_y.ndim == 1:
                data_train_y = data_train_y.reshape(-1, 1)
            data_train = cat_method[type(data_train_x)]((data_train_x, data_train_y), axis=1)
        else:
            data_train = None

        if data_test_x is not None and data_test_y is not None:
            if data_test_y.ndim == 1:
                data_test_y = data_test_y.reshape(-1, 1)
            data_test = cat_method[type(data_train_x)]((data_test_x, data_test_y), axis=1)
        else:
            data_test = None

        targets = tuple(list(np.arange(data_train_x.shape[1], data_train.shape[1])))
        return cls(data_train, data_test, targets, loop)

    def refresh(self, loop, new_data=None, is_train=True):
        if loop is None:
            self.max_loop += 1
        else:
            self.max_loop = loop
        if is_train:
            if new_data is not None:
                self.data[f"train-{loop}"] = new_data
        else:
            if new_data is not None:
                self.data[f"test-{loop}"] = new_data

    def refresh_from_xy(self, loop, new_data_x, new_data_y=None, is_train=True):
        if new_data_y is None:
            if isinstance(new_data_x, np.ndarray):
                y_d = 1 if self.targets is None else len(self.targets)
                new_data_y = np.full((new_data_x.shape[0], y_d), np.inf)
            else:
                raise NotImplementedError("new_data_y for pd.DataFrame should be offered.")

        data = cat_method[type(new_data_x)]((new_data_x, new_data_y), axis=1)
        self.refresh(loop, new_data=data, is_train=is_train)

    def collect_split_to_xy(self, loops=None):
        assert self.targets is not None
        train, test = self.collect(loops)
        index = np.ones(train.shape[1]) > 0
        index[self.targets] = False

        train_x, train_y, test_x, test_y = None, None, None, None

        if train is not None:
            if type(train) == pd.DataFrame:
                train_x = train.iloc[:, index]
                train_y = train.iloc[:, ~index]
            else:
                train_x = train[:, index]
                train_y = train[:, ~index]

        if test is not None:
            if type(test) == pd.DataFrame:
                test_x = test.iloc[:, index]
                test_y = test.iloc[:, ~index]
            else:
                test_x = test[:, index]
                test_y = test[:, ~index]

        return train_x, train_y, test_x, test_y

    def collect(self, loops=None) -> Tuple[Any, Any]:
        if loops is None:
            loops = list(range(0, self.max_loop + 1))
        train = []
        for i in loops:
            if f"train-{i}" in self.data:
                train.append(self.data[f"train-{i}"])

        test = []
        for i in loops:
            if f"test-{i}" in self.data:
                test.append(self.data[f"test-{i}"])

        train = cat_method[type(train[0])](train, axis=0) if len(train) > 1 else train[0]
        test = cat_method[type(test[0])](test, axis=0) if len(test) > 1 else test[0]

        return train, test

    def to_pickle(self, pt: Union[str, PathLike, pathlib.Path], loops=None):
        data = {}
        if loops is None:
            loops = list(range(0, self.max_loop + 1))
        data["data"] = {i: self.data[f"train-{i}"] for i in loops}
        data["data"].update({i: self.data[f"test-{i}"] for i in loops})
        data["max_loop"] = max(loops)
        data["targets"] = self.targets
        save_model(data, pt)
        log(f"Save samples from: {pt}.")

    def load_pickle(self, pt: Union[str, PathLike, pathlib.Path], mode="r"):
        res = load_model(pt)
        if mode == "r":
            self.__dict__ = copy(res)
        if mode == "a":
            for k, v in res.items():
                for ki, vi in v.items():
                    self.__dict__[k][ki] = vi
        log(f"Load samples from: {pt}.")
        return self

    def to_xlsx(self, pt: Union[str, PathLike, pathlib.Path], loops=None):

        assert isinstance(self.data["train-0"], (np.ndarray, pd.DataFrame))
        if loops is None:
            loops = list(range(0, self.max_loop + 1))

        data = {f"train-{i}": self.data[f"train-{i}"] for i in loops if f"train-{i}" in self.data}
        data.update({f"test-{i}": self.data[f"test-{i}"] for i in loops if f"test-{i}" in self.data})

        data = {k: pd.DataFrame(v) if isinstance(v, np.ndarray) else v for k, v in data.items()}

        with pd.ExcelWriter(pt) as excel_writer:

            for k, v in data.items():
                if "train" in k:
                    v.to_excel(excel_writer, sheet_name=k)
                if "test" in k:
                    v.to_excel(excel_writer, sheet_name=k)

            v = pd.DataFrame.from_dict({"targets": {i: j for i, j in enumerate(self.targets)}}).T
            v.to_excel(excel_writer, sheet_name=f"targets")

        log(f"Save samples to: {pt}.")

    def load_xlsx(self, pt: Union[str, PathLike, pathlib.Path], loops=None, mode="r", tp="np"):

        excel_file = pd.read_excel(pt, sheet_name=None, index_col=0)

        # if loops is None:
        # loops = list(range(0, self.max_loop+1))

        data = {}
        targets = None
        max_loop = 0

        for i in excel_file.keys():
            if "target" in i:
                targets = tuple(excel_file[i].values.ravel().tolist())
                continue
            try:
                mark, step = i.split("-")
            except:
                raise NotImplementedError("The sheet name should be like 'train-0','train-1','test-0' ...")
            step = int(step)
            if loops is None or (loops is None and float(step) in loops):
                if "train" in mark or "test" in mark:
                    data[i] = excel_file[i] if tp == "pd" else excel_file[i].values

            max_loop = max([max_loop, step])

        res = {"data": data, "max_loop": max_loop, "targets": targets}

        if mode == "r":
            self.__dict__ = copy(res)
        if mode == "a":
            for k, v in res.items():
                for ki, vi in v.items():
                    self.__dict__[k][ki] = vi

        log(f"Load samples from: {pt}.")

        return self

    def __str__(self):
        return f"{self.__class__.__name__}(loop={self.max_loop})"
