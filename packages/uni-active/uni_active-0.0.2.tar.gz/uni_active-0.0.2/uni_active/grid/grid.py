import numpy as np


def search_space(*arg):
    """
    Generate grid.

    Note
    ------
        Parameters should be no more than 6.

    Parameters
    ----------
    arg: np.ndarray
        Examples:
            arg = [
            np.arange(0.1,0.35,0.1),
            np.arange(0.1, 2.1, 0.5),
            np.arange(0,1.3,0.3),
            np.array([0.5,1,1.2,1.3]),]

    Returns
    -------
    result: np.ndarray
    """
    meshes = np.meshgrid(*arg)
    meshes = [_.ravel() for _ in meshes]
    meshes = np.array(meshes).T
    return meshes


class UniGrid:
    def __init__(self, X, X_steps:[np.ndarray, float]=0.1, **kwargs):
        self.X_max = np.max(X, axis=0)
        self.X_min = np.min(X, axis=0)
        if isinstance(X_steps, (float, int)):
            self.X_steps = [X_steps] * len(self.X_max)
        else:
            self.X_steps = X_steps

    def grid(self):
        arg = [np.arange(i, j, s) for i, j, s in zip(self.X_min, self.X_max, self.X_steps)]
        return search_space(*arg)


class Grid:
    def __init__(self, *args):
        self.args =args

    def grid(self):
        return search_space(*self.args)


grid_methods = {"UniGrid": UniGrid, "Grid":Grid}
