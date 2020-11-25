import numpy as np

def estimate_rw(y):
    # yt = b[0] + yt_1 + e
    e = np.diff(y)
    b = np.mean(e)
    e = e - b
    b = [b, 1]
    return b, e

def estimate_ar1(y):
    # yt = b[0] + b[1]*yt_1 + e
    n = len(y)-1
    X = np.vstack([np.ones(n), y[:-1]]).T
    y = y[1:]
    b = np.linalg.inv(X.T @ X) @ (X.T @ y) # Linear regression
    e = y - b @ X.T # residuals
    return b, e

class UnivariateModels():

    def __init__(self, models):
        self.models = models

    def estimate(self):

        B0 = []
        B1 = []
        E = []
        starting_value = []

        for d in self.models:
            b, e = d['estimator'](d['data'])

            # impose b0 for simulation if parameter specified
            if 'b0' in d:
                b[0] = d['b0']

            B0.append(b[0])
            B1.append(b[1])
            E.append(e)
            starting_value.append(d['data'][-1])

        self.B0 = np.array(B0)
        self.B1 = np.diag(np.array(B1))
        self.E = np.array(E)
        self.starting_value = np.array(starting_value)

    def simulate(self, n_steps, n_paths):
        C = np.cov(self.E) # covariance matrix of shocks, e
        R = np.linalg.cholesky(C) # cholesky decomposition ("square root" of matrix)

        n_models = len(self.models)

        starting_value = np.repeat(np.atleast_3d(self.starting_value.T), n_paths, axis=2) # setup starting values for factors in correct size
        Y = np.zeros((n_steps, n_models, n_paths)) # initialize array
        Y = np.concatenate((starting_value, Y))
        for k in range(0, n_paths):
            for j in range(0, n_steps):
                Y[j+1, :, k] = self.B0 + self.B1 @ Y[j, :, k] + R @ np.random.randn(n_models)

        return Y