import pathlib
from typing import Union

import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor

from uni_active.data.dataset import DataSetLoop
from uni_active.grid.grid import UniGrid, grid_methods

from uni_active.model.func import model_from_json
from uni_active.selection.select import EGOSelection
from uni_active.utils.log import log


class ActiveLoopLocalTable:

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dsl.max_loop},path={self.local_path})"

    def __init__(self, local_path, dsl, model, grid_method: Union[str, UniGrid] = "UniGrid", **kwargs):

        self.model = model
        self.dsl = dsl
        self.local_path = local_path

        gd_params = {}
        for k, v in kwargs.items():
            if "grid_param_" in k:
                k = str(k).replace("grid_param_", "")
                gd_params[k] = v

        if isinstance(grid_method, str):
            self.grid_method = grid_method
            self.gd_params = gd_params
        else:
            self.grid_method = grid_method
        log(">>>> START NEXT LOOP >>>>")

    @classmethod
    def from_code(cls, local_path, dsl, model, grid_method="UniGrid", **kwargs):
        return cls(local_path, dsl, model, grid_method=grid_method, **kwargs)

    @classmethod
    def from_path(cls, local_path, dsl_path=None, model_path=None,
                  grid_method="UniGrid", tp="np",**kwargs):
        pt = pathlib.Path(local_path)
        if dsl_path is None:
            dsl_path = pt / "samples.xlsx"
        if model_path is None:
            model_path = pt / "model.json"
        if "xlsx" in dsl_path.name:
            dsl = DataSetLoop().load_xlsx(pt=dsl_path, tp=tp)
        else:
            dsl = DataSetLoop().load_pickle(pt=dsl_path)
        model = model_from_json(cls=None, path_file=model_path, label=None, load_fitted=True)

        return cls(local_path, dsl, model, grid_method=grid_method,**kwargs)

    def to_path(self, local_path=None, dsl_path=None, model_path=None):
        local_path = local_path if local_path else self.local_path
        pt = pathlib.Path(local_path)
        if not pt.is_dir():
            pt.mkdir()

        if dsl_path is None:
            dsl_path = pt / "samples.xlsx"
        if model_path is None:
            model_path = pt / "model.json"

        self.model.to_json(model_path, save_fitted=True)

        if "xlsx" in dsl_path.name:
            self.dsl.to_xlsx(dsl_path)
        else:
            self.dsl.to_pickle(dsl_path)

        log(f"Now, Please check the 'train-{self.dsl.max_loop}' in {dsl_path},"
            f" and make experimental evaluation.")
        log(f"After the fill missing value, start the next cycle.")

    def run(self, batch_size=10, resample_number=20,
            n_jobs=1,
            target_value="inf",debug_func=None):

        train_x0, train_y0, _, _ = self.dsl.collect_split_to_xy()

        if isinstance(train_x0, pd.DataFrame):
            tp = "pd"
        else:
            tp = "np"

        train_x = train_x0.values if isinstance(train_x0, pd.DataFrame) else train_x0
        train_y = train_y0.values if isinstance(train_y0, pd.DataFrame) else train_y0

        # model = self.model
        # model.fit(train_x0, train_y0)
        # score = model.score(train_x0, train_y0)
        # print(score)

        if isinstance(self.grid_method, str):
            gd = grid_methods[self.grid_method](train_x, **self.gd_params)
        else:
            gd = self.grid_method

        grid_x = gd.grid()

        log(f"Make grid with shape {grid_x.shape}.")

        def setdiff2d_set(arr1, arr2):
            set1 = set(map(tuple, arr1))
            set2 = set(map(tuple, arr2))
            return np.array(list(set1 - set2))

        grid_x = setdiff2d_set(grid_x, train_x)

        ego_search = EGOSelection(train_x, train_y, grid_x, n_jobs=n_jobs,
                                  target_value=target_value)
        index = ego_search.select_index(self.model, batch_size=batch_size,
                                        resample_number=resample_number)
        new_data_x = grid_x[index, :]

        if debug_func is not None:
            new_data_y = debug_func(*new_data_x.T)
            if new_data_y.ndim==1:
                new_data_y = new_data_y.reshape(-1,1)

        else:
            fill_value = 0

            if tp == "pd":  # todo new_data_y is for debug
                new_data_x = pd.DataFrame(new_data_x, columns=train_x0.columns)
                new_data_y = pd.DataFrame(np.full((new_data_x.shape[0], train_y0.shape[1]), fill_value),
                                          columns=train_y0.columns)
            else:
                new_data_y = np.full((new_data_x.shape[0], train_y0.shape[1]), fill_value)

        self.dsl.refresh_from_xy(self.dsl.max_loop + 1,
                                 new_data_x=new_data_x,
                                 new_data_y=new_data_y
                                 )

        log(f"Save new samples x to 'train-{self.dsl.max_loop + 1}'.")


if __name__ == "__main__":
    # sample samples
    from sklearn.linear_model import LinearRegression
    from uni_active.model.base import register_sk

    for loop in range(3):

        if loop == 0:
            X_train = np.random.randn(100, 3)
            y_train = np.random.randint(low=0, high=2, size=100)
            X_test = np.random.randn(50, 3)
            y_test = np.random.uniform(low=0, high=2, size=50)

            X_train = pd.DataFrame(X_train, columns=["A", "B", "C"])
            y_train = pd.DataFrame(y_train, columns=["T"])
            X_test = pd.DataFrame(X_test, columns=["A", "B", "C"])
            y_test = pd.DataFrame(y_test, columns=["T"])

            # sample model
            model  = GaussianProcessRegressor(alpha=1e-5)

            model.fit(X_train, y_train)
            score = model.score(X_test, y_test)

            dsl = DataSetLoop.from_xy(X_train, y_train, X_test, y_test, loop=loop)

            model = register_sk(model)
            # model = MyM()
            #
            al = ActiveLoopLocalTable.from_code("./debug", dsl, model, grid_method="UniGrid",grid_param_X_steps=0.1)

        else:
            al = ActiveLoopLocalTable.from_path("./debug", grid_method="UniGrid", tp="pd",grid_param_X_steps=0.1)

        al.run(batch_size=1)
        al.to_path()
