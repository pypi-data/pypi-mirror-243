import inspect
from abc import ABCMeta, abstractmethod

import numpy as np
import sklearn
from sklearn.metrics import accuracy_score

from uni_active.model.func import model_to_json, model_from_json


class _BaseModel:

    @classmethod
    def _get_param_names(cls):
        """Get parameter names for the estimator"""
        # fetch the constructor or the original constructor before
        # deprecation wrapping if any
        init = getattr(cls.__init__, "deprecated_original", cls.__init__)
        if init is object.__init__:
            # No explicit constructor to introspect
            return []

        # introspect the constructor arguments to find the model parameters
        # to represent
        init_signature = inspect.signature(init)
        # Consider the constructor parameters excluding 'self'
        parameters = [
            p
            for p in init_signature.parameters.values()
            if p.name != "self" and p.kind != p.VAR_KEYWORD
        ]
        for p in parameters:
            if p.kind == p.VAR_POSITIONAL:
                raise RuntimeError(
                    "Model should always "
                    "specify their parameters in the signature"
                    " of their __init__ (no varargs)."
                    " %s with constructor %s doesn't "
                    " follow this convention." % (cls, init_signature)
                )
        # Extract and sort argument names excluding 'self'
        return sorted([p.name for p in parameters])

    def get_params(self, deep=False):
        """
        Get parameters for this estimator.

        Parameters
        ----------
        deep : bool, default=True
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.

        Returns
        -------
        params : dict
            Parameter names mapped to their values.
        """
        out = dict()
        for key in self._get_param_names():
            value = getattr(self, key)
            if deep and hasattr(value, "get_params") and not isinstance(value, type):
                deep_items = value.get_params().items()
                out.update((key + "__" + k, val) for k, val in deep_items)
            out[key] = value
        return out

    def to_json(self, path_file, step_label="tmp_model", step_mark=None, save_fitted=True, mode="a"):

        if step_mark is None and hasattr(self, "fitted_times"):
            step_mark = self.fitted_times
        step_label = f"{step_label}-{step_mark}"
        model_to_json(self, path_file=path_file, label=step_label, save_fitted=save_fitted, mode=mode)

    @classmethod
    def from_json(cls, path_file, step_label="tmp_model", step_mark=None, load_fitted=True):

        step_label = f"{step_label}-{step_mark}"
        # cls=None
        return model_from_json(cls, path_file, label=step_label, load_fitted=load_fitted)


class BaseModel(_BaseModel):
    fitted_times = 0
    is_fitted = False

    @abstractmethod
    def _fit(self, X, y=None, **kwargs):
        """"""

    def fit(self, X, y=None, **kwargs):
        self.is_fitted = True
        res = self._fit(X, y=y, **kwargs)
        self.fitted_times += 1
        return res

    def __repr__(self):
        return f"{self.__class__.__name__}(loop={self.fitted_times})"


class SKRegisterModel(_BaseModel):
    fitted_times = 0
    is_fitted = False

    def __init__(self, sub_model=None):
        if sub_model is not None:
            assert (sub_model, sklearn.base.BaseEstimator)
        self.sub_model = sub_model

    def fit(self, X, y=None, **kwargs):
        self.is_fitted = True
        res = self.sub_model.fit(X, y=y, **kwargs)
        self.fitted_times += 1
        return res

    def predict(self, X, **kwargs):
        res = self.sub_model.predict(X, **kwargs)
        return res

    def score(self, X, y=None, **kwargs):
        res = self.sub_model.score(X, y=y, **kwargs)
        return res

    def __repr__(self):
        return f"{self.__class__.__name__}(sub_model={self.sub_model},loop={self.fitted_times})"


class TestMyM(BaseModel):
    def _fit(self, X, y=None, **kwargs):
        pass

    def predict(self, X, **kwargs):
        return np.average(X, axis=1)

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))


def register_sk(model):
    return SKRegisterModel(sub_model=model)