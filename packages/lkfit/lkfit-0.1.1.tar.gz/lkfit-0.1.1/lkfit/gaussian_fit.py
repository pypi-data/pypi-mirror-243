"""lkfit - a Python library for fitting.

This module contains plotting routines for Gaussian fitting.

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


def fit_gaussian_1d(
        X, Y, fixed_a=None, fixed_y0=None, plot=False,
        y_scale='lin', main_axes=None, res_axes=None, y_axis_pos='left',
        center_z_axis_in_plot=False, xlim=None, show_y_zero_marker=True,
        plot_residuals=False, plot_fwhm=False, xlabel=None, ylabel=None):
    """Fit data to a 1D gaussian."""
    try:
        num_plot_pts = 1000
        if X is None:
            X = np.arange(Y.size)

        y0_g = np.min(Y)
        c_g = X[np.argmax(Y)]
        A_g = np.max(Y) - y0_g

        c_ind = find_closest(Y, A_g + y0_g)

        if c_ind > 1 and c_ind < len(Y)-1:
            w1_ind = find_closest(Y[0:c_ind], A_g/2 + y0_g)
            w2_ind = find_closest(Y[c_ind:-1], A_g/2 + y0_g) + c_ind
            w_g = abs(X[w2_ind] - X[w1_ind])
        else:
            w_g = (np.max(X) - np.min(X))/3
    except Exception:
        print("Fitting failed")
        fit_result = None

    try:
        if fixed_a is not None:
            if fixed_y0 is not None:
                def fit_func(x, w, c):
                    return gaussian_1D(x, A=fixed_a, w=w, c=c, y0=fixed_y0)
                p0 = [w_g, c_g]
            else:
                def fit_func(x, w, c, y0):
                    return gaussian_1D(x, A=fixed_a, w=w, c=c, y0=y0)
                p0 = [w_g, c_g, y0_g]
        else:
            if fixed_y0 is not None:
                def fit_func(x, w, c):
                    return gaussian_1D(x, A, w, c, y0=fixed_y0)
                p0 = [A_g, w_g, c_g]
            else:
                def fit_func(x, A, w, c, y0):
                    return gaussian_1D(x, A, w, c, y0)
                p0 = [A_g, w_g, c_g, y0_g]

        fit_result = optimize.curve_fit(fit_func, X, Y, p0=p0)[0]

        if fixed_a is not None:
            fit_result = np.append(fixed_a, fit_result)
        if fixed_y0 is not None:
            fit_result = np.append(fit_result, fixed_y0)
    except Exception as excpt:
        print("Fitting failed", excpt)
        plot = False
        fit_result = None

    if plot is True and fit_result:
        if center_z_axis_in_plot:
            X = X - fit_result[2]
            fit_result[2] = 0

        if plot_residuals:
            res = Y - gaussian_1D_arglist(fit_result, X)
            if main_axes is None:
                grid = plt.GridSpec(5, 1, wspace=0.1, hspace=0.1)
                main_axes = plt.subplot(grid[0:4, :])
                res_axes = plt.subplot(grid[4, :])
        else:
            if main_axes is None:
                main_axes = plt.gca()

        if xlim is None:
            xlim = [np.min(X), np.max(X)]

        plt.sca(main_axes)
        if y_axis_pos == 'right':
            main_axes.yaxis.set_label_position("right")
            main_axes.yaxis.tick_right()

        if y_scale == 'lin':
            plt.ylim(extend_range([np.min(Y), np.max(Y)], 0.1))
            if show_y_zero_marker:
                add_y_marker(0, xlim=xlim, ls='-')
            plt.plot(X, Y, '.-', c=get_color('db'))
        elif y_scale == 'log':
            plt.semilogy(X, Y, '.-', c=get_color('db'))
        X_fit = np.linspace(min(X), max(X), num_plot_pts)

        plot_gaussian_1D_arglist(fit_result, X=X_fit, c=get_color('dr'))

        if plot_fwhm:
            w = fit_result[1]
            A = fit_result[0]
            y0 = fit_result[3]
            plt.draw()
            xl = plt.xlim()
            x_span = xl[1] - xl[0]
            plt.text(w/2+x_span*0.02, A/2+y0, '{:.2f} um'.format(w))

        if ylabel is not None:
            plt.ylabel(ylabel)

        plt.xlim(xlim)
        plt.grid('on')

        if plot_residuals:
            plt.tick_params(axis="x", which="both", bottom=False, top=False)
            plt.sca(res_axes)
            add_y_marker(0, xlim=xlim, ls='-')
            plt.plot(X, res, c=get_color('db'))
            plt.grid('on')
            plt.xlim(xlim)

        if xlabel is not None:
            plt.xlabel(xlabel)

    return fit_result
