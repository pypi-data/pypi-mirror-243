import numpy as np

import math

from pyvest.general.portfolio import Portfolio
from pyvest.general.general import calculate_portfolio_standard_deviation
from pyvest.general.general import calculate_portfolio_sharpe_ratio
from pyvest.investment_universe.investment_universe_visualizer import \
    InvestmentUniverseVisualizer

from scipy.optimize import minimize
from scipy.optimize import LinearConstraint
from scipy.optimize import Bounds

from pyvest.investment_universe.investor import Investor


class InvestmentUniverse:
    MAX_NB_ITERATIONS = 100

    def __init__(self, assets, mu, cov, r_f=None, min_weight=0,
                 min_weight_r_f=None, parameters=None):

        self.__assign_parameters(parameters)

        self.__assets = assets

        self.__nb_risky_assets = len(mu)
        self.__nb_assets = self.__nb_risky_assets if r_f is None \
            else self.__nb_risky_assets + 1

        self.__assign_r_f(r_f)
        self.__assign_mu(mu)
        self.__assign_cov(cov)
        self.__assign_min_weight(min_weight)
        self.__assign_min_weight_r_f(min_weight_r_f)

        self.__investors = {}
        self.__nb_unnamed_investors = 0

        self.__calculate_assets_std()

        self.__feasible_portfolios = None
        self.__feasible_portfolios_with_r_f = None
        self.__mvp = None
        self.__efficient_frontier = None
        self.__tangency_portfolio = None
        self.__cal = self.__cal_mu_list = self.__cal_std_list = None
        self.__other_portfolios = None
        self.__market_portfolio = None
        self.__total_wealth = None
        self.__investors = {}

        self.__min_weights_bound = None
        self.__sum_weights_assets_equals_one_constraint = None

        self.__efficient_mu_min = None
        self.__efficient_mu_max = None

        self.__visualizer = None

    ################################# ATTRIBUTES ##############################

    @property
    def assets(self):
        return self.__assets

    @assets.setter
    def assets(self, value):
        self.__assets = value

    @property
    def mu(self):
        return self.__mu

    @mu.setter
    def mu(self, value):
        self.__mu = np.array(value)

    @property
    def augmented_mu(self):
        return self.__augmented_mu

    @augmented_mu.setter
    def augmented_mu(self, value):
        self.__augmented_mu = np.array(value)

    @property
    def cov(self):
        return self.__cov

    @cov.setter
    def cov(self, value):
        self.__cov = np.array(value)

    @property
    def augmented_cov(self):
        return self.__augmented_cov

    @augmented_cov.setter
    def augmented_cov(self, value):
        self.__augmented_cov = np.array(value)

    @property
    def r_f(self):
        return self.__r_f

    @r_f.setter
    def r_f(self, value):
        self.__assign_r_f(value)

    @property
    def min_weight(self):
        return self.__min_weights

    @min_weight.setter
    def min_weight(self, value):
        self.__assign_min_weight(value)

    @property
    def min_weight_r_f(self):
        return self.__min_weight_r_f

    @min_weight_r_f.setter
    def min_weight_r_f(self, value):
        self.__assign_min_weight_r_f(value)

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__assign_parameters(value)

    @property
    def std(self):
        return self.__std

    @property
    def feasible_portfolios(self):
        return self.__feasible_portfolios

    @property
    def feasible_portfolios_with_r_f(self):
        return self.__feasible_portfolios_with_r_f

    @property
    def mvp(self):
        return self.__mvp

    @property
    def efficient_frontier(self):
        return self.__efficient_frontier

    @property
    def tangency_portfolio(self):
        return self.__tangency_portfolio

    @property
    def cal(self):
        return self.__cal

    @property
    def other_portfolios(self):
        return self.__other_portfolios

    @property
    def visualizer(self):
        return self.__visualizer

    @property
    def investors(self):
        return self.__investors

    @property
    def market_portfolio(self):
        return self.__market_portfolio

    @property
    def total_wealth(self):
        return self.__total_wealth

    ################################# PUBLIC FUNCTIONS #################################

    def calculate_feasible_portfolios(self, nb_portfolios=20000,
                                      return_portfolios=False):
        self.__feasible_portfolios = []
        for i in range(1, nb_portfolios):
            risky_assets_portfolio_weights = \
                self.__calculate_random_portfolio_weights(
                    self.__min_weights)

            if self.__r_f is not None:
                portfolio_weights = \
                    np.append(risky_assets_portfolio_weights, [0])
            else:
                portfolio_weights = risky_assets_portfolio_weights

            portfolio = Portfolio(portfolio_weights, self.__mu, self.__cov,
                                  r_f=self.__r_f, assets=self.__assets)
            self.__feasible_portfolios.append(portfolio)

        if return_portfolios:
            return self.__feasible_portfolios

    def calculate_feasible_portfolios_with_r_f(self, nb_portfolios=100000,
                                      return_portfolios=False):

        if self.r_f is None:
            min_weights = self.min_weight
        else:
            min_weights = np.append(self.min_weight, self.min_weight_r_f)

        self.__feasible_portfolios_with_r_f = []
        for i in range(1, nb_portfolios):
            portfolio_weights = \
                self.__calculate_random_portfolio_weights(min_weights)

            portfolio = Portfolio(portfolio_weights, self.__mu, self.__cov,
                                  r_f=self.__r_f, assets=self.__assets)
            self.__feasible_portfolios_with_r_f.append(portfolio)

        if return_portfolios:
            return self.__feasible_portfolios_with_r_f

    def calculate_mvp(self, x0=None):

        # Initial guess (seed value)
        if x0 is None:
            x0 = np.ones(self.__nb_risky_assets) / self.__nb_risky_assets

        # Assign results
        self.__mvp = self.__calculate_mvp(x0)

        return self.__mvp

    def calculate_efficient_portfolio(self, mu=None, sigma=None, name=None,
                                      x0=None, tolerance=None):

        tolerance = self.__parameters["optimization_tolerance"] \
            if tolerance is None else tolerance

        # Initial guess (seed value)
        if x0 is None:
            x0 = np.ones(self.__nb_risky_assets) / self.__nb_risky_assets

        mvp = self.__calculate_mvp(x0) if not self.__mvp else self.__mvp

        self.__calculate_efficient_mu_min_max(mvp)

        if mu is not None and sigma is not None:
            raise ValueError("Only one of 'mu' and 'sigma' must be passed as "
                             "argument.")
        elif mu is not None:
            efficient_portfolio = \
                self.__calculate_efficient_portfolio_from_mu(mu, x0, tolerance)
        elif sigma is not None:
            efficient_portfolio = \
                self.__calculate_efficient_portfolio_from_sigma(sigma, x0,
                                                                tolerance)
        else:
            raise ValueError("Either 'mu' or 'sigma' must be passed as "
                             "argument.")

        self.calculate_portfolio(efficient_portfolio, name)

        return efficient_portfolio

    def calculate_efficient_frontier(self, nb_portfolios=1000, x0=None,
                                     tolerance=None,
                                     return_portfolios=False):

        tolerance = self.__parameters["optimization_tolerance"] \
            if tolerance is None else tolerance

        # Initial guess (seed value)
        if x0 is None:
            x0 = np.ones(self.__nb_risky_assets) / self.__nb_risky_assets

        mvp = self.__calculate_mvp(x0) if not self.__mvp else self.__mvp

        self.__calculate_efficient_mu_min_max(mvp)
        efficient_mu_array = self.__calculate_efficient_mu_array(nb_portfolios)

        # Calculate the efficient portfolios
        self.__efficient_frontier = []
        for efficient_mu in efficient_mu_array:
            efficient_portfolio = \
                self.__calculate_efficient_portfolio_from_mu(efficient_mu, x0,
                                                             tolerance)
            self.__efficient_frontier.append(efficient_portfolio)

        if return_portfolios:
            return self.__efficient_frontier

    def calculate_tangency_portfolio(self, x0=None, tolerance=None):

        tolerance = self.__parameters["optimization_tolerance"] \
            if tolerance is None else tolerance

        if self.__r_f is None:
            raise ValueError("You need to add a risk-free asset first!")

        # Initial guess (seed value)
        if x0 is None:
            x0 = np.ones(self.__nb_risky_assets) / self.__nb_risky_assets

        # Sum portfolio weights equals 1 constraint
        self.__sum_weights_assets_equals_one_constraint = LinearConstraint(
            np.ones(self.__nb_risky_assets), 1, 1)

        tangency_portfolio_result = minimize(
            lambda x: -calculate_portfolio_sharpe_ratio(x, self.__mu,
                                                        self.__cov,
                                                        self.__r_f),
            x0,
            bounds=self.__min_weights_bound,
            constraints=[self.__sum_weights_assets_equals_one_constraint],
            tol=tolerance)

        if self.__r_f is not None:
            tangency_portfolio_weights = \
                np.append(tangency_portfolio_result.x, [0])
        else:
            tangency_portfolio_weights = tangency_portfolio_result.x

        self.__tangency_portfolio = Portfolio(tangency_portfolio_weights,
                                              self.__mu, self.__cov,
                                              r_f=self.__r_f,
                                              assets=self.__assets)

        return self.__tangency_portfolio

    def calculate_cal(self, return_portfolios=False):

        min_fraction, max_fraction, step_fraction = self.__get_cal_parameters()

        if not self.__tangency_portfolio:
            self.calculate_tangency_portfolio()

        self.__cal = []
        for tangency_weight in np.arange(min_fraction,
                                         max_fraction,
                                         step_fraction):
            cal_portfolio_weights = tangency_weight \
                                    * self.__tangency_portfolio.weights
            cal_portfolio_weights[-1] = 1 - tangency_weight

            cal_portfolio = Portfolio(cal_portfolio_weights, self.__mu,
                                      self.__cov, self.__r_f,
                                      assets=self.__assets)
            self.__cal.append(cal_portfolio)

        if return_portfolios:
            return self.__cal

    def calculate_portfolio(self, portfolio, name=None):

        if isinstance(portfolio, Portfolio):
            portfolio_obj = portfolio
        elif (isinstance(portfolio, list)
              or isinstance(portfolio, np.ndarray)
              or isinstance(portfolio, tuple)) \
                and ((len(portfolio) == self.__nb_risky_assets
                      and self.__r_f is None)
                     or (len(portfolio) == self.__nb_risky_assets + 1
                         and self.__r_f is not None)):
            portfolio_obj = Portfolio(portfolio, self.__mu, self.__cov,
                                      r_f=self.__r_f, assets=self.__assets)
        else:
            raise TypeError("The variable 'portfolio' must be an object of "
                            "type Portfolio or a list of weights of dimension "
                            "{}.".format(self.__nb_risky_assets))

        if self.__other_portfolios is None:
            self.__other_portfolios = {}

        self.__other_portfolios[tuple(portfolio_obj.weights)] = \
            (portfolio_obj, name)

        return portfolio_obj

    def remove_portfolio(self, portfolio=None):
        if portfolio is None:
            self.__other_portfolios = None
        elif isinstance(portfolio, list) or isinstance(portfolio, tuple) \
                or isinstance(portfolio, np.ndarray):
            del self.__other_portfolios[tuple(portfolio)]
        elif isinstance(portfolio, Portfolio):
            del self.__other_portfolios[portfolio.weights]
        elif isinstance(portfolio, str):
            keys_to_delete = []
            for key, value in self.__other_portfolios.items():
                if value[1] == portfolio:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                del self.__other_portfolios[key]
        else:
            raise TypeError("The parameter 'portfolio' must be either a "
                            "Portfolio, a list of weights, or a string!")

    def plot(self, compare_with=None, labels=None, weights_visible=True,
             zoom_individual=False, min_mu=None, max_mu=None, min_std=None,
             max_std=None, investors=None, indifference_curves=None,
             legend='upper left'):
        investment_universes = [self]
        if isinstance(compare_with, InvestmentUniverse):
            investment_universes.append(compare_with)
        elif isinstance(compare_with, list):
            investment_universes.extend(compare_with)

        if self.__visualizer is None:
            self.__visualizer = InvestmentUniverseVisualizer(
                investment_universes, labels=labels,
                weights_visible=weights_visible)
        else:
            self.__visualizer.investment_universes = investment_universes
            self.__visualizer.labels = labels
            self.__visualizer.reset_colors()
        self.__visualizer.plot(zoom_individual=zoom_individual, min_mu=min_mu,
                               max_mu=max_mu, min_std=min_std, max_std=max_std,
                               investors=investors,
                               indifference_curves=indifference_curves,
                               legend=legend)

    def add_investor(self, wealth, portfolio=None, gamma=None,
                     utility_function=None, name=None):

        investor = Investor(self, wealth, portfolio, gamma, utility_function)

        if name is None:
            self.__nb_unnamed_investors += 1
            name = "Investor {}".format(self.__nb_unnamed_investors)

        self.__investors[name] = investor

        return investor

    def calculate_market_portfolio(self):

        nb_weights = self.__nb_risky_assets + 1 if self.__r_f is not None \
            else self.__nb_risky_assets

        market_assets_value = np.zeros(nb_weights)
        self.__total_wealth = 0
        for investor in self.__investors.values():
            self.__total_wealth += investor.wealth
            weights = investor.portfolio.weights
            market_assets_value += np.array(weights) * investor.wealth

        market_weights = market_assets_value / self.__total_wealth

        if self.__r_f is not None:
            market_weights = \
                market_weights / sum(market_weights[:self.__nb_risky_assets])
            market_weights[-1] = 0.0

        self.__market_portfolio = Portfolio(market_weights, self.__mu,
                                            self.__cov, r_f=self.__r_f,
                                            assets=self.__assets)

        return self.__market_portfolio

    ########################## PRIVATE ##########################

    def __assign_mu(self, mu):
        self.mu = mu
        if self.__r_f is not None:
            self.__augmented_mu = np.concatenate((self.__mu,
                                                  [self.__r_f]))
        else:
            self.__augmented_mu = self.mu

    def __assign_cov(self, cov):
        self.cov = cov
        if self.__r_f is not None:
            zeros_column = (np.zeros((len(self.__cov), 1)))
            zeros_row = (np.zeros((1, len(self.__cov) + 1)))
            self.__augmented_cov = \
                np.concatenate(
                    (np.concatenate((self.__cov, zeros_column), axis=1),
                     zeros_row))
        else:
            self.__augmented_cov = self.cov

    def __assign_r_f(self, r_f):
        if r_f is None or type(r_f) is float or type(r_f) is int:
            self.__r_f = r_f
        else:
            raise TypeError(
                "The parameter 'r_f' must be of type float or int.")

    def __assign_min_weight(self, min_weight):
        if type(min_weight) is float or type(min_weight) is int:
            self.__min_weights = min_weight * np.ones(self.__nb_risky_assets)
        elif type(min_weight) is list or type(min_weight) is np.array:
            self.__min_weights = min_weight
        else:
            raise TypeError(
                "The parameter 'min_weight' must be of type float ,int or "
                "list.")

    def __assign_min_weight_r_f(self, min_weight_r_f):
        if min_weight_r_f is None:
            self.__min_weight_r_f = self.__parameters["min_weight_r_f"]
        else:
            self.__min_weight_r_f = min_weight_r_f

    def __assign_parameters(self, parameters):
        if parameters is None:
            self.__assign_default_parameters()
        else:
            self.__check_parameters(parameters)
            self.__parameters = parameters

    def __assign_default_parameters(self):
        self.__parameters = {
            "optimization_tolerance": 1e-8,
            "cal_min_fraction": 0,
            "cal_step_fraction": 0.001,
            "min_weight_r_f": -4,
            "cal_max_std": 10
        }

    def __check_parameters(self, parameters):
        if type(parameters) is not dict:
            raise TypeError(
                "The variable 'parameters' must be a dictionary.")

        if "optimization_tolerance" not in parameters:
            raise ValueError(
                "The dictionary parameters must contain the key "
                "'optimization_tolerance'.")
        if type(optimization_tolerance) is not float:
            raise TypeError(
                "The value of 'optimization_tolerance' must be of type float.")

    # Portfolio weights generator
    def __calculate_random_portfolio_weights(self, smallest_weights_list):
        # This function adds random portfolio weights
        # The argument "smallest_weight" denotest the smallest weight admissible for a given asset
        # For example, "smallest_weight=0" indicates that short sales are not allowed,
        # and "smallest_weight=-1" implies that the weight of each asset in the portfolio must be equal or greater to -1
        # The function returns an array of portfolio weights

        weights = np.random.dirichlet(np.ones(len(smallest_weights_list)),
                                      size=1)[0]
        norm_weights = \
            weights * (1 - sum(smallest_weights_list)) + smallest_weights_list

        return norm_weights

    def __calculate_assets_std(self):
        std = []
        for i in range(0, len(self.__assets)):
            std.append(math.sqrt(self.__cov[i][i]))
        self.__std = np.array(std)
        return self.__std

    def __calculate_mvp(self, x0):

        # Sum portfolio weights equals 1 constraint
        self.__sum_weights_assets_equals_one_constraint = LinearConstraint(
            np.ones(self.__nb_risky_assets), 1, 1)
        self.__min_weights_bound = Bounds(self.__min_weights,
                                          np.inf)

        # Minimize
        mvp_result = minimize(
            lambda x: calculate_portfolio_standard_deviation(x, self.__cov),
            x0,
            bounds=self.__min_weights_bound,
            constraints=[self.__sum_weights_assets_equals_one_constraint],
            tol=self.__parameters["optimization_tolerance"])

        if self.__r_f is not None:
            mvp_weights = \
                np.append(mvp_result.x, [0])
        else:
            mvp_weights = mvp_result.x

        return Portfolio(mvp_weights, self.__mu, self.__cov, r_f=self.__r_f,
                         assets=self.__assets)

    def __calculate_efficient_mu_min_max(self, mvp):
        mu_argmax = np.argmax(self.__mu)
        mu_max = self.__mu[mu_argmax]
        others_mu = np.delete(self.__mu, mu_argmax)
        others_min_weight = np.delete(self.__min_weights,
                                      mu_argmax)

        self.__efficient_mu_min = mvp.expected_return
        self.__efficient_mu_max = (1 - sum(
            others_min_weight)) * mu_max + np.dot(
            others_mu, others_min_weight)

    def __calculate_efficient_mu_array(self, nb_portfolios):
        # Define the range of expected return over which to calculate the
        # efficient frontier.
        delta_mu = self.__efficient_mu_max - self.__efficient_mu_min
        step = delta_mu / nb_portfolios
        efficient_mu_array = np.arange(self.__efficient_mu_min,
                                       self.__efficient_mu_max, step)

        return efficient_mu_array

    def __calculate_efficient_portfolio_from_mu(self, mu, x0, tolerance):
        efficient_mu_constraint = LinearConstraint(self.__mu.T, mu, mu)
        efficient_portfolio_result = minimize(
            lambda x: calculate_portfolio_standard_deviation(x,
                                                             self.__cov),
            x0,
            bounds=self.__min_weights_bound,
            constraints=[self.__sum_weights_assets_equals_one_constraint,
                         efficient_mu_constraint],
            tol=tolerance)
        if not efficient_portfolio_result.success:
            raise ValueError(
                "minimize was not successful with bounds={} and constraints={}!"
                .format(self.__min_weights_bound, mu))

        if self.__r_f is not None:
            efficient_portfolio_weights = \
                np.append(efficient_portfolio_result.x, [0])
        else:
            efficient_portfolio_weights = efficient_portfolio_result.x

        efficient_portfolio = Portfolio(efficient_portfolio_weights, self.__mu,
                                        self.__cov, r_f=self.__r_f,
                                        assets=self.__assets)

        return efficient_portfolio

    def __calculate_efficient_portfolio_from_sigma(self, sigma, x0, tolerance):

        nb_iter = 0

        mu_min = self.__efficient_mu_min
        mu_max = self.__efficient_mu_max
        tentative_mu = (mu_min + mu_max) / 2
        tentative_portfolio = \
            self.__calculate_efficient_portfolio_from_mu(tentative_mu, x0,
                                                         tolerance)
        tentative_sigma = tentative_portfolio.standard_deviation
        while abs(tentative_sigma - sigma) >= tolerance:
            if sigma - tentative_sigma > 0:
                mu_min = tentative_mu
                tentative_mu = (tentative_mu + mu_max) / 2
            else:
                mu_max = tentative_mu
                tentative_mu = (mu_min + tentative_mu) / 2
            tentative_portfolio = \
                self.__calculate_efficient_portfolio_from_mu(tentative_mu, x0,
                                                             tolerance)
            tentative_sigma = tentative_portfolio.standard_deviation
            nb_iter += 1
            if nb_iter > self.MAX_NB_ITERATIONS:
                raise StopIteration("Number of iterations exceeded "
                                    "MAX_NB_ITERATIONS ({})"
                                    .format(self.MAX_NB_ITERATIONS))

        return tentative_portfolio

    def __get_cal_parameters(self):

        min_fraction = self.__parameters["cal_min_fraction"]
        step_fraction = self.__parameters["cal_step_fraction"]

        if self.__efficient_frontier is not None:
            max_std = max([ptf.standard_deviation
                           for ptf in self.__efficient_frontier])
        else:
            max_std = self.__parameters["cal_max_std"]

        max_fraction = min(
            1.0 - self.min_weight_r_f,
            max_std / self.__tangency_portfolio.standard_deviation)

        return min_fraction, max_fraction, step_fraction
