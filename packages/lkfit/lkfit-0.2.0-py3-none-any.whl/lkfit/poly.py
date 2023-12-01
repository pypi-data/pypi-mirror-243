"""lkfit - a Python library for fitting.

This module contains plotting routines for polynomial fitting.

Copyright 2015-2022 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

from lkcom.util import find_closest, extend_range, get_color
from lkcom.standard_func import gaussian_1D, gaussian_1D_arglist, \
    plot_gaussian_1D_arglist
from lkcom.plot import add_y_marker


def fit_poly_2(X=None, Y=None, plot=False, plot_fit=False, color=None):
    if(isnone(color)):
        color = 'r'

    popt, pcov = optimize.curve_fit(poly_2, X, Y, p0=[-1, 0, 0])

    if(plot):
        plt.plot(X, Y, '.')

    if(plot or plot_fit):
        X_fit = np.linspace(min(X), max(X), 1000)
        plt.plot(X_fit, poly_2(X_fit, popt[0], popt[1], popt[2]),
                 c=color, ls='-')
        plt.draw()

    return [popt, pcov]


def get_poly_2_max_x(k):
    return -k[1]/(2*k[0])
