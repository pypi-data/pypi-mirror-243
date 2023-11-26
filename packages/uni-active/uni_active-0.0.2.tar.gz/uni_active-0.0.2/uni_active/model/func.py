import copy
import importlib
import inspect
import os
import pathlib
import warnings

import joblib

from uni_active.utils.file_io import load_info, save_info
from uni_active.utils.log import log


def check_fitted(estimator):
    """
    The function `check_fitted` checks if an estimator instance is fitted and raises an error if it is
    not.
    For both BaseModel or sklearn.base.BaseEstimator.

    Args:
      estimator: The `estimator` parameter is an object that represents a machine learning model or
    estimator. It can be any object that has a `fit` method, which is used to train the model on a given
    dataset. The purpose of the `check_fitted` function is to check whether the `est
    """

    if not hasattr(estimator, "fit"):
        raise TypeError("%s is not an estimator instance." % (estimator))
    else:
        from sklearn.base import BaseEstimator, check_is_fitted
        if isinstance(estimator, BaseEstimator):
            check_is_fitted(estimator)
        else:
            if hasattr(estimator, "is_fitted"):
                if estimator.is_fitted is False:
                    msg = """This %(name)s instance is not fitted yet. Call 'fit' with "
                    "appropriate arguments before using this estimator."""
                    raise TypeError(msg % {"name": type(estimator).__name__})
                else:
                    pass
            else:
                msg = """This %(name)s instance is not one proper model. 
                Accept: model with ``register_model`` to decorate."""
                raise TypeError(msg % {"name": type(estimator).__name__})


def fitted(estimator):
    try:
        check_fitted(estimator=estimator)
    except:
        return False
    else:
        return True


def clone(obj):
    """Construct a new unfitted estimator with the same parameters.
    For both BaseModel or sklearn.base.BaseEstimator.
    """
    estimator_type = type(obj)
    # XXX: not handling dictionaries
    if estimator_type in (list, tuple, set, frozenset):
        return estimator_type([clone(e) for e in obj])

    elif not hasattr(obj, "get_params"):
        return copy.deepcopy(obj)
    else:
        klass = obj.__class__
        new_object_params = obj.get_params(deep=False)
        for name, param in new_object_params.items():
            new_object_params[name] = clone(param)
        new_object = klass(**new_object_params)

        params_set = new_object.get_params(deep=False)

        # quick sanity check of the parameters of the clone
        for name in new_object_params:
            param1 = new_object_params[name]
            param2 = params_set[name]
            if param1 is not param2:
                raise RuntimeError(
                    "Cannot clone object %s, as the constructor "
                    "either does not set or modifies parameter %s" % (obj, name)
                )

    if hasattr(new_object, "is_fitted"):
        new_object.is_fitted = False

    return new_object


def model_to_json(obj, path_file, label, save_fitted=True, mode="a"):
    path_file = pathlib.Path(path_file).with_suffix(".json")
    pt = path_file.parent
    main_file_path = os.path.abspath(inspect.getfile(obj.__class__))

    msg = {"Model": obj.__class__.__name__,
           "Model_Module": str(obj.__class__.__module__),
           "Model_Module_Path": str(main_file_path),
           "Model_Path": None,
           "Params": {k: v for k, v in obj.get_params().items() if k != "sub_model"}
           }

    if hasattr(obj, "feature_names_in_"):
        msg.update({"feature_names_in_": [str(i) for i in obj.feature_names_in_]})

    if hasattr(obj, "n_features_in_"):
        msg.update({"n_features_in_": obj.n_features_in_})

    if hasattr(obj, "sub_model"):
        msg.update({"Sub_Model": obj.sub_model.__class__.__name__})
        msg.update({"Sub_Model_Module": obj.sub_model.__class__.__module__})
        msg.update({"Sub_Params": obj.sub_model.get_params()})

    if save_fitted:
        import tempfile
        temp_name = next(tempfile._get_candidate_names())
        if not fitted(obj):
            warnings.warn("No fitted model would be store!")

        pt = pathlib.Path(pt) / "model_pkl"

        if not pt.is_dir():
            pt.mkdir()

        pt = (pt / temp_name).with_suffix(".pth")

        joblib.dump(obj, pt)

        msg["Model_Path"] = str(pt)

        log(f"Save model to pickle file: {pt}.")

    info = {label: msg}

    save_info(info, path_file, mode=mode)

    log(f"Save model info in json: {path_file}, with key: '{label}'.")


def model_from_json(cls=None, path_file="a.json", label=-1, load_fitted=True, load_sub_model=True):
    path_file = pathlib.Path(path_file).with_suffix(".json")

    info = load_info(path_file)
    if label in info:
        msg = info[label]
        name = label
        fitted_times = int(str(label).split("-")[-1])
    else:
        ks = list(info.keys())
        if len(ks) > 0:
            if not isinstance(label, int):
                label = -1
            msg = info[ks[label]]
            fitted_times = int(str(ks[label]).split("-")[-1])
            name = ks[label]

        else:
            raise KeyError(f"No model labeled {label}, available:{[i for i in info.keys()]} or index number.")

    if load_fitted and msg["Model_Path"] and pathlib.Path(msg["Model_Path"]).is_file():
        pt_m = pathlib.Path(msg["Model_Path"])
        temp = joblib.load(pt_m)
        log(f"Load model from pickle file: {pt_m}.")
    else:

        if "Sub_Model" in msg:
            try:
                lib = importlib.import_module(msg["Sub_Model_Module"])
                sub_model = getattr(lib, str(msg["Sub_Model"]))(**msg["Sub_Params"])
            except:
                sub_model = None
        else:
            sub_model = None

        if cls is None:
            if msg["Model_Module"] == "__main__":
                import sys
                pt = pathlib.Path(msg["Model_Module_Path"])
                p = pt.parent
                name = pt.name.removesuffix(".py")
                sys.path.append(str(p))
                lib = importlib.import_module(name)
            else:
                lib = importlib.import_module(str(msg["Model_Module"]))

            temp = getattr(lib, str(msg["Model"]))(**msg["Params"])
        else:
            lib = cls.__module__
            assert str(msg["Model"]) == cls.__name__, \
                f"The model in local file {msg['Model']}, is not consisted with {cls}," \
                f"Using ``{msg['Model']}.from_json(...)`` or ``model_from_json(cls=None,...)`` to load from file."
            temp = cls(**msg["Params"])

        if load_sub_model and sub_model is not None:
            temp.sub_model = sub_model

        temp.fitted_times = fitted_times

        log(f"Load model from code: {lib}. This is not fitted usually.", level="warning")

    if not fitted(temp):
        warnings.warn("Load no fitted model!")

    log(f"Load model info from json: {path_file}, with key '{name}'.")

    return temp
