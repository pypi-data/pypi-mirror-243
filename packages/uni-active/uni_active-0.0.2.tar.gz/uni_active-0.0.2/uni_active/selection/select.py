import numpy as np
import sklearn
from mgetool.tool import parallelize
from scipy import stats

from uni_active.utils.log import log


def unpack(X, y, label_index, unlabel_index):
    train_x = X[label_index]
    train_y = y[label_index]
    grid_x = X[unlabel_index]
    return train_x, train_y, grid_x


def pack(train_x, train_y, grid_x):
    assert isinstance(train_x, np.ndarray)

    X = np.concatenate((train_x, grid_x), axis=0)
    if train_y.ndim == 1:
        grid_y = np.zeros(grid_x.shape[0])
    else:
        grid_y = np.zeros((grid_x.shape[0], *train_y.shape[1:]))
    y = np.concatenate((train_y, grid_y), axis=0)

    return X, y, grid_x


class EGOSelection:
    """The base class for the selection method which imposes a constraint on the parameters of select()"""

    def __init__(self, train_x, train_y, grid_x, n_jobs=1, target_value="inf", **kwargs):
        self.train_x = train_x
        self.train_y = train_y
        self.grid_x = grid_x
        self.n_jobs = n_jobs
        self.target_value = target_value

    def predict_grid_x(self, model, resample_times=20):

        train_y = self.train_y.ravel() if self.train_y.ndim == 2 and self.train_y.shape[1] == 1 else self.train_y

        def fit_parllize(random_state):
            data_train, y_train = sklearn.utils.resample(self.train_x, train_y, n_samples=None,
                                                         replace=True,
                                                         random_state=random_state)
            model.fit(data_train, y_train)

            predict_data = model.predict(self.grid_x)

            predict_data = predict_data.ravel()
            return predict_data

        predict_y = parallelize(n_jobs=self.n_jobs, func=fit_parllize, iterable=range(resample_times))
        predict_y = np.array(predict_y).T
        return predict_y

    @staticmethod
    def y_with_sign(target_value, y):
        if isinstance(target_value, (int, float)):
            assert np.isfinite(target_value)
            y = - np.abs(y - target_value)
        elif target_value == "-inf":
            y = -y
        return y

    @staticmethod
    def mean_and_std(predict_y):
        """calculate meanandstd."""
        mean = np.mean(predict_y, axis=1)
        std = np.std(predict_y, axis=1)
        return mean, std

    def calculate_ei(self, mean, std, flexibility=0.0):
        """calculate EI."""
        y = self.y_with_sign(self.target_value, self.train_y)
        my = max(y)
        mean0 = self.y_with_sign(self.target_value, mean)

        ego = (mean0 - (my - flexibility)) / std
        ei_ego = std * ego * stats.norm.cdf(ego) + std * stats.norm.pdf(ego)
        kg = (mean0 - max(max(mean0), my - flexibility)) / std
        ei_kg = std * kg * stats.norm.cdf(kg) + std * stats.norm.pdf(kg)
        max_P = stats.norm.cdf(ego)
        ei = np.column_stack((mean, std, ei_ego, ei_kg, max_P))
        return ei

    def select_index(self, model, batch_size=1, flexibility=0.0, resample_number=20):

        tm = model.fitted_times if hasattr(model, "fitted_times") else 0
        log(f"Start training model with resample method ({resample_number} times) and get predict value.")
        predict_y = self.predict_grid_x(model, resample_times=resample_number)
        mean, std = self.mean_and_std(predict_y)
        model.fitted_times = tm + 1
        log(f"Calculate mean and std ({resample_number} times) of predict value to evaluate robustness.")

        self.res = self.calculate_ei(mean, std, flexibility=flexibility)
        self.rank = np.argsort(self.res[:, 2])[::-1]

        res_rank = self.res[self.rank]
        index = self.rank[:batch_size]

        log(f"Calculate Expectation Improvement (EI) and select top {batch_size} index.")

        return self.rank[:batch_size]

    def result_rank(self):
        return self.res[self.rank]
