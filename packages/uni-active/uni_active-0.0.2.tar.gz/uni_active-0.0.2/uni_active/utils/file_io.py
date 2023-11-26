import json
import pathlib
from functools import wraps
from os import PathLike
from typing import Any, Union

import joblib
import pandas as pd


def check_path(func):
    """
    The `check_path` decorator ensures that the directory of the given file path exists before executing
    the decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) == 0:
            pt = kwargs[list(kwargs.keys())[1]]
        elif len(args) == 1:
            pt = kwargs[list(kwargs.keys())[0]]
        else:
            pt = args[1]  # 强制第二个参数是路径+文件名，并且不做检查。

        pt = pathlib.Path(pt).parent
        if not pt.is_dir():
            pt.mkdir(parents=True, exist_ok=True)
        result = func(*args, **kwargs)
        return result

    return wrapper


# For info json

@check_path
def save_info(obj, pt: Union[str, PathLike, pathlib.Path], mode="a"):
    """
    The `save_info` function saves a Python object as JSON to a specified file path, either appending to
    an existing file or creating a new file.
    
    Args:
      obj: The `obj` parameter is the object that you want to save as JSON. It can be any valid JSON
    serializable object, such as a dictionary, list, or string.
      pt (Union[str,PathLike,pathlib.Path]): The parameter `pt` is the path where the JSON file will be
    saved. It can be specified as a string, a `PathLike` object, or a `pathlib.Path` object.
      mode: The `mode` parameter specifies the mode in which the file should be opened. It has a default
    value of "a", which stands for append mode. This means that if the file already exists, the function
    will append the new samples to the existing samples in the file. If the file does not. Defaults to a
    """
    if mode == "a":
        pt = pathlib.Path(pt).with_suffix(".json")
        if pt.exists():
            with open(pt, 'r', encoding='utf-8') as fw:
                in_json = json.load(fw)
            in_json.update(obj)
        else:
            in_json = obj
    else:
        in_json = obj

    with open(pt, 'w', encoding='utf-8') as fw:
        json.dump(in_json, fw, )


def load_info(pt: Union[str, PathLike, pathlib.Path]) -> Any:
    """
    The function `load_info` loads JSON samples from a file specified by the input path.
    
    Args:
      pt (Union[str,PathLike,pathlib.Path]): The parameter `pt` is the path to the file that you want to
    load. It can be either a string, a `PathLike` object, or a `pathlib.Path` object.
    
    Returns:
      the contents of the JSON file as a Python object.
    """
    pt = pathlib.Path(pt).with_suffix(".json")
    with open(pt, 'r', encoding='utf-8') as fw:
        in_json = json.load(fw)
    return in_json


# For general model
@check_path
def save_model(obj, pt: Union[str, PathLike, pathlib.Path]):
    """
    The function `save_model` saves an object to a specified file path using the joblib library.
    
    Args:
      obj: The `obj` parameter is the object that you want to save. It can be any Python object that you
    want to persist, such as a trained machine learning model or any other custom object.
      pt (Union[str,PathLike,pathlib.Path]): The parameter `pt` is the path where the model object will
    be saved. It can be specified as a string, a `PathLike` object, or a `pathlib.Path` object. The
    function will automatically add the file extension `.pth` to the path if it is not already present
    """
    pt = pathlib.Path(pt).with_suffix(".pth")
    joblib.dump(obj, pt)


def load_model(pt: Union[str, PathLike, pathlib.Path]) -> Any:
    """
    The function `load_model` loads a model from a file specified by the input path.
    
    Args:
      pt (Union[str,PathLike,pathlib.Path]): The parameter `pt` is the path to the model file. It can be
    either a string, a `PathLike` object, or a `pathlib.Path` object.
    
    Returns:
      the loaded model.
    """
    pt = pathlib.Path(pt).with_suffix(".pth")
    return joblib.load(pt)


# For general samples
@check_path
def save_pkl(obj, pt: Union[str, PathLike, pathlib.Path]):
    """
    The function `save_pkl` saves a pandas DataFrame object as a pickle file at the specified path.
    
    Args:
      obj (pd.DataFrame): The `obj` parameter is a pandas DataFrame object that you want to save.
      pt (Union[str,PathLike,pathlib.Path]): The parameter `pt` is the path where you want to save the
    samples. It can be either a string representing the file path, or an object of type `PathLike` or
    `pathlib.Path`.
    """
    pt = pathlib.Path(pt).with_suffix(".pkl")
    pd.to_pickle(obj, pt)


def load_pkl(pt: Union[str, PathLike, pathlib.Path]) -> Any:
    """
    The function `load_pkl` loads samples from a pickle file given a file path.
    
    Args:
      pt (Union[str,PathLike,pathlib.Path]): The parameter `pt` is the path to the file that you want to
    load. It can be specified as a string, a `PathLike` object, or a `pathlib.Path` object.
    
    Returns:
      the samples loaded from the pickle file.
    """
    pt = pathlib.Path(pt).with_suffix(".pkl")
    return pd.read_pickle(pt)


# For csv
@check_path
def save_csv(obj: pd.DataFrame, pt: Union[str, PathLike, pathlib.Path]):
    """
    The function `save_csv` takes a pandas DataFrame object and a file path as input, and saves the
    DataFrame as a CSV file at the specified path.
    
    Args:
      obj (pd.DataFrame): The `obj` parameter is a pandas DataFrame object that you want to save as a
    CSV file.
      pt (Union[str,PathLike,pathlib.Path]): The parameter `pt` is the file path where you want to save
    the CSV file. It can be specified as a string, a `PathLike` object, or a `pathlib.Path` object.
    """
    pt = pathlib.Path(pt).with_suffix(".csv")
    obj.to_csv(pt)


def load_csv(pt: Union[str, PathLike, pathlib.Path]) -> Any:
    """
    The function `load_csv` loads a CSV file and returns a pandas DataFrame with the first column as the
    index and the first row as the header.
    
    Args:
      pt (Union[str,PathLike,pathlib.Path]): The parameter `pt` is the path to the CSV file that you
    want to load. It can be specified as a string, a `PathLike` object, or a `pathlib.Path` object.
    
    Returns:
      the contents of a CSV file as a pandas DataFrame.
    """
    pt = pathlib.Path(pt).with_suffix(".csv")
    return pd.read_csv(pt, index_col=0, header=0)  # index, columns force!


def load_excel(pt: Union[str, PathLike, pathlib.Path], sheet_name: Union[str, int] = 0) -> Any:
    try:
        pt = pathlib.Path(pt).with_suffix(".xlsx")
        data = pd.read_excel(pt, sheet_name=0, index_col=0, header=0)  # index, columns force!
    except FileNotFoundError:
        pt = pathlib.Path(pt).with_suffix(".xls")
        data = pd.read_excel(pt, sheet_name=sheet_name, index_col=0, header=0)  # index, columns force!
    return data


def load_data(pt: Union[str, PathLike, pathlib.Path]) -> Any:
    pt = pathlib.Path(pt)
    if pt.suffix == ".pkl":
        return load_pkl(pt)
    elif pt.suffix == ".csv":
        return load_csv(pt)
    elif pt.suffix in [".xlsx", ".xls"]:
        return load_excel(pt)
    else:
        raise TypeError("Un-supported file. Just accept [pkl,csv,xlsx,xls]")


if __name__ == "__main__":
    import numpy as np

    data = pd.DataFrame(np.array([1, 1, 1, 1.2]), )
    save_model(data, "test")
    a = load_model("test")
    print(a)

    save_pkl(data, "test")
    a = load_pkl("test")
    print(a)

    save_csv(data, "test")
    a = load_csv("test")
    print(a)
