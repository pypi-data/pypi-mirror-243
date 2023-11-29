"""GP Conditional Sample Paths

This script constructs a GP model using a Matérn kernel and a constant
mean function. The script generates sample paths from the GP prior,
and then generates conditional sample paths given the observed data.

Copyright (c) 2022-2023, CentraleSupelec
Author: Emmanuel Vazquez <emmanuel.vazquez@centralesupelec.fr>
License: GPLv3 (see LICENSE)

"""

import math
import numpy as np
import gpmp.num as gnp
import gpmp as gp
import matplotlib
import gpmp.misc.plotutils as plotutils
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor

matplotlib.rcParams['font.size'] = 18
matplotlib.rcParams["legend.loc"] = 'upper right'
figsize = (10, 6)

def generate_data():
    nt = 200
    xt = np.linspace(0, 1, nt).reshape(-1, 1)
    zt = None
    
    ind = np.array([1, 17, 42, 55, 60, 82, 85, 96]) * 2
    xi = xt[ind, :]  # np.array([ 0.01  0.17 0.42 0.55 0.6  0.82 0.85 0.96]).T 
    zi = np.array([ -0.3, -1.8,  1,   0.8,  1.25, 0.5,  -0.1, -0.4]).T

    return xt, zt, xi, zi, ind


def kernel(x, y, covparam, pairwise=False):
    p = 3
    return gp.kernel.maternp_covariance(x, y, p, covparam, pairwise)


def constant_mean(x, param):
    return gnp.ones((x.shape[0], 1))


def visualization(xt, zt, zsim, zpsim, xi, zi, zpm, zpv):
    # Figure 0
    fig = plotutils.Figure(isinteractive=True, figsize=figsize)
    fig.plot(xt, zsim, color='tab:blue')
    fig.xlim([0.0, 1.0001])
    fig.xylabels('$x$', '$z$')
    fig.show(grid=True)
    
    # Figure 0
    ymin, ymax = -3.0, 3.0
    # ymin, ymax = -4.0, 6.0
    fig = plotutils.Figure(isinteractive=True, figsize=figsize)
    fig.plot(xi, zi, 'rs', label='data')
    fig.xlim([0.0, 1.01])
    fig.ylim([ymin, ymax])
    fig.xylabels('x', 'z')
    fig.show(grid=True, legend=True, legend_fontsize='12')
    
    # Figure 1
    ymin, ymax = -4.0, 6.0
    fig = plotutils.Figure(isinteractive=True, figsize=figsize)
    fig.plot(xt, zpsim[:, 1], 'C0', linewidth=1, label='posterior sample paths')
    fig.plot(xt, zpsim[:, 1:], 'C0', linewidth=1)
    fig.plot(xi, zi, 'rs', label='data')
    fig.xlim([0.0, 1.0])
    fig.ylim([ymin, ymax])
    fig.xylabels('x', 'z')
    fig.show(grid=True, legend=True, legend_fontsize='12')
    
    # Figure 2a
    fig = plotutils.Figure(isinteractive=True, figsize=figsize)
    fig.plot(xt, zpsim[:, 1], 'C0', linewidth=1, label='posterior sample paths')
    fig.plot(xt, zpsim[:, 1:], 'C0', linewidth=1)
    fig.plot(xi, zi, 'rs', label='data')
    fig.plotgp(xt, zpm, zpv, ci=[], show_ci_labels=False)
    fig.xlim([0.0, 1.0])
    fig.ylim([ymin, ymax])
    fig.xylabels('x', 'z')
    fig.show(grid=True, legend=True, legend_fontsize='12')

    # Figure 2b
    fig = plotutils.Figure(isinteractive=True, figsize=figsize)
    fig.plot(xt, zpsim[:, 1], 'C0', linewidth=1, label='posterior sample paths')
    fig.plot(xt, zpsim[:, 1:], 'C0', linewidth=1)
    fig.plot(xi, zi, 'rs', label='data')
    fig.plotgp(xt, zpm, zpv, ci=[0.95, 0.95, 0.95], show_ci_labels=False)
    fig.xlim([0.0, 1.0])
    fig.ylim([ymin, ymax])
    fig.xylabels('x', 'z')
    fig.show(grid=True, legend=True, legend_fontsize='12')

    # Figure 2c
    fig = plotutils.Figure(isinteractive=True, figsize=figsize)
    fig.plot(xt, zpsim[:, 1], 'C0', linewidth=1, label='posterior sample paths')
    fig.plot(xt, zpsim[:, 1:], 'C0', linewidth=1)
    fig.plot(xi, zi, 'rs', label='data')
    fig.plotgp(xt, zpm, zpv, ci=[0.95, 0.99, 0.99], show_ci_labels=False)
    fig.xlim([0.0, 1.0])
    fig.ylim([ymin, ymax])
    fig.xylabels('x', 'z')
    fig.show(grid=True, legend=True, legend_fontsize='12')

    # Figure 2d
    fig = plotutils.Figure(isinteractive=True, figsize=figsize)
    fig.plot(xt, zpsim[:, 1], 'C0', linewidth=1, label='posterior sample paths')
    fig.plot(xt, zpsim[:, 1:], 'C0', linewidth=1)
    fig.plot(xi, zi, 'rs', label='data')
    fig.plotgp(xt, zpm, zpv, show_ci_labels=False)
    fig.xlim([0.0, 1.0])
    fig.ylim([ymin, ymax])
    fig.xylabels('x', 'z')
    fig.show(grid=True, legend=True, legend_fontsize='12')

    # Figure 3
    fig = plotutils.Figure(isinteractive=True, figsize=figsize)
    fig.plot(xi, zi, 'rs', label='data')
    fig.plotgp(xt, zpm, zpv)
    fig.xlim([0.0, 1.0])
    fig.ylim([ymin, ymax])
    fig.xylabels('x', 'z')
    fig.show(grid=True, legend=True, legend_fontsize='12')

def simple_plot(xi, zi, xt, zp, label=''):
    ymin, ymax = -3.0, 3.0
    fig = plotutils.Figure(isinteractive=True, figsize=figsize)
    fig.plot(xi, zi, 'rs', label='data')
    fig.plot(xt, zp, label=label)
    fig.xlim([0.0, 1.0])
    fig.ylim([ymin, ymax])
    fig.xylabels('x', 'z')
    fig.show(grid=True, legend=True, legend_fontsize='12')
    
def main():
    xt, zt, xi, zi, xi_ind = generate_data()

    mean = constant_mean
    meanparam = None
    covparam = gnp.array([math.log(2 ** 2), math.log(1 / .2)])
    model = gp.core.Model(mean, kernel, meanparam, covparam)

    n_samplepaths = 12
    zsim = model.sample_paths(xt, n_samplepaths, method='chol')

    zpm, zpv, lambda_t = model.predict(xi, zi, xt, return_lambdas=True)
    zpsim = model.conditional_sample_paths(zsim, xi_ind, zi, gnp.arange(xt.shape[0]), lambda_t)

    visualization(xt, zt, zsim, zpsim, xi, zi, zpm, zpv)
    
    zp = sklearn_linear(xi, zi, xt)
    simple_plot(xi, zi, xt, zp, 'quadratic fit')
    zp = sklearn_rf(xi, zi, xt)
    simple_plot(xi, zi, xt, zp, 'random forest')
    zp = sklearn_mlp(xi, zi, xt)
    simple_plot(xi, zi, xt, zp, 'MLP')

def sklearn_linear(xi, zi, xt):
    # Create polynomial features
    poly = PolynomialFeatures(degree=2)
    xi_poly = poly.fit_transform(xi)

    # Fit the model
    model = LinearRegression()
    model.fit(xi_poly, zi)

    # Predict on xt
    xt_poly = poly.transform(xt)
    zp = model.predict(xt_poly)

    return zp

def sklearn_rf(xi, zi, xt):
    # Create and fit the model
    model = RandomForestRegressor()
    model.fit(xi, zi)

    # Predict on xt
    zp = model.predict(xt)
    return zp

def sklearn_mlp(xi, zi, xt):
    # Create and fit the model
    model = MLPRegressor(hidden_layer_sizes=(50, 50, 50), max_iter=100000, random_state=1)
    model.fit(xi, zi)

    # Predict on xt
    zp = model.predict(xt)
    return zp

if __name__ == "__main__":
    main()
