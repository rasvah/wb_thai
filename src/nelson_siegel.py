import matplotlib.pyplot as plt
import numpy as np

class NelsonSiegel():

    """ Estimation of Nelson-Siegel factors """

    def __init__(self, yields, mats, dates, lambda_ = 0.4):
        self.yields = yields   #yields: (n_periods, n_yields) np.array
        self.mats = mats       #mats: (n_mats x 1) np.array
        self.dates = dates     #dates: np.array
        self.lambda_ = lambda_ #lambda_: float
        
    def estimate_factors(self):
        T = self.yields.shape[0]
        loadings = self._get_loadings(self.mats)
        self.betas = np.zeros([T, loadings.shape[1]])
        self.sse = 0

        for j in range(T):
            beta, sse_ = self._estimate_OLS_factors(self.yields[j, :].T, loadings)
            self.betas[j, :] = beta.T
            self.sse = self.sse + sse_

        self.fit_err = self.yields - self.get_fitted_yields(self.mats)

    def get_fitted_yields(self, mats):
        loadings = self._get_loadings(mats)
        return self.betas @ loadings.T

    def _get_loadings(self, mats):
        # mats: (n_mats x 1) np.array
        # return:  (n_mats x 3) np.array
        scaled_mats = mats * self.lambda_
        loading0 = np.ones_like([mats])
        loading1 = (1 - np.exp(-scaled_mats)) / (scaled_mats)
        loading2 = (1 - np.exp(-scaled_mats)) / (scaled_mats) \
        - np.exp(-scaled_mats)
        return np.vstack([loading0, loading1, loading2]).T

    def _estimate_OLS_factors(self, yields, loadings):
        X = loadings
        Y = yields
        beta = np.linalg.inv(X.T @ X) @ (X.T @ Y)
        u_hat = Y - X @ beta
        SSE = np.sum([x**2 for x in u_hat])
        return (beta, SSE)

    def plot(self):
        plt.figure()
        for j in range(self.betas.shape[1]):
          plt.plot(self.dates, self.betas[:, j], label = f"beta {j}")

        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Factor level')

    def plot_fit(self, mat):
        if mat in self.mats:
          d = self.dates
          y = self.yields[:, mat == self.mats]
          y_hat = self.get_fitted_yields(mat)

          plt.figure()
          plt.subplot(2, 1, 1)
          plt.plot(d, y)
          plt.plot(d, y_hat)
          plt.ylabel('Yield')
          
          plt.subplot(2, 1, 2)
          plt.plot(d, y - y_hat)
          plt.ylabel('Fit error')
          plt.xlabel('Date')

        else:
          print(f"maturity of {mat} not in the data")

    def plot_factor_loadings(self):
        plot_mats = np.arange(1, 30)
        loads = self._get_loadings(plot_mats)
        for j in range(loads.shape[1]):
          plt.plot(plot_mats, loads[:, j], label = f"beta {j}" )
          plt.xlabel('Maturity')
          plt.ylabel('Factor loading on yield')
          plt.legend()