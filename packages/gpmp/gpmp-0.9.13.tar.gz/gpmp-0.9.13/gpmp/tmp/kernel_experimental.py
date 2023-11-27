## --------------------------------------------------------------
# Author: Emmanuel Vazquez <emmanuel.vazquez@centralesupelec.fr>
# Copyright (c) 2022-2023, CentraleSupelec
# License: GPLv3 (see LICENSE)
## --------------------------------------------------------------
import time
import numpy as np
import gpmp.numpy as gnp

if gnp._gpmp_backend_ == "numpy":
    
    class jax:
        @staticmethod
        def jit(f, *args, **kwargs):
            return f

        @staticmethod
        def grad(f):
            return None

elif gnp._gpmp_backend_ == "torch":

    class jax:
        @staticmethod
        def jit(f, *args, **kwargs):
            return f

        @staticmethod
        def grad(f):
            return None

elif gnp._gpmp_backend_ == "jax":
    import jax
from functools import partial
from scipy.special import gammaln
from scipy.optimize import minimize
from math import exp, log, sqrt


## -- distance


def scale(x, invrho):
    """Scale input points

    Parameters
    ----------
    x : ndarray(n, d)
        Observation points
    invrho : ndarray(d), or scalar
        Inverse of scaling factors

    Returns
    -------
    xs : ndarray(n, d)
        [ x_{1,1} * invrho_1 ... x_{1,d} * invrho_d
          ...
          x_{n,1} * invrho_1 ... x_{n,d} * invrho_d ]

    Note : If invrho is a scalar the scaling is isotropic
    """
    return invrho * x


def distance(x, y):
    if gnp._gpmp_backend_ == "jax":
        return distance_jax_jit(x, y)
    if gnp._gpmp_backend_ == "numpy" or gnp._gpmp_backend_ == "torch":
        return gnp.cdist(x, y)


def distance_pairwise(x, y):
    if gnp._gpmp_backend_ == "jax":
        return distance_pairwise_jax_jit(x, y)
    if gnp._gpmp_backend_ == "numpy" or gnp._gpmp_backend_ == "torch":
        return distance_pairwise_numpy(x, y)


def distance_jax(x, y, alpha=100*gnp.eps):
    """Compute a distance matrix

    Parameters
    ----------
    x : numpy.array(n,dim)
        _description_
    y : numpy.array(m,dim)
        If y is None, it is assumed y is x, by default None
    alpha : float, optional
        a small number to prevent auto-differentation problems
        with the derivative of sqrt at zero, by default 1e-8

    Returns
    -------
    numpy.array(n,m)
        distance matrix such that
    .. math:: d_{i,j} = (alpha + sum_{k=1}^dim (x_{i,k} - y_{i,k})^2)^(1/2)

    Notes
    -----
    in practice however, it seems that it makes no performance
    improvement; FIXME: investigate memory and CPU usage

    """
    if y is None:
        y = x

    y2 = gnp.sum(y**2, axis=1)

    # Debug: check if x is y
    # print("&x = {}, &y = {}".format(hex(id(x)), hex(id(y))))

    if x is y:
        d = gnp.sqrt(alpha + gnp.reshape(y2, [-1, 1]) + y2 - 2 * gnp.inner(x, y))
    else:
        x2 = gnp.reshape(gnp.sum(x**2, axis=1), [-1, 1])
        d = gnp.sqrt(alpha + x2 + y2 - 2 * gnp.inner(x, y))

    return d


distance_jax_jit = jax.jit(distance_jax)


def distance_pairwise_jax(x, y, alpha=1e-8):
    """Compute a distance vector between the pairs (xi, yi)

    Inputs
      * x: numpy array n x dim
      * y: numpy array n x dim or None
      * alpha: a small number to prevent auto-differentation problems
        with the derivative of sqrt at zero

    If y is None, it is assumed y is x

    Output
      * distance vector of size n x 1 such that
        d_i = (alpha + sum_{k=1}^dim (x_{i,k} - y_{i,k})^2)^(1/2)
        or
        d_i = 0 if y is x or None

    """
    if x is y or y is None:
        d = gnp.zeros((x.shape[0],))
    else:
        d = gnp.sqrt(alpha + gnp.sum((x - y) ** 2, axis=1))
    return d


distance_jax_pairwise_jit = jax.jit(distance_pairwise_jax)


def distance_pairwise_numpy(x, y):
    if x is y or y is None:
        d = gnp.zeros((x.shape[0],))
    else:
        d = gnp.sqrt(gnp.sum((x - y) ** 2, axis=1))
    return d


## -- kernels


def exponential_kernel(h):
    """exponential kernel

    Parameters
    ----------
    h : numpy.array
        _description_

    Returns
    -------
    numpy.array
        _description_
    """
    return gnp.exp(-h)


def matern32_kernel(h):
    """Matérn 3/2 kernel

    Parameters
    ----------
    h : numpy.array
        _description_

    Returns
    -------
    numpy.array
        _description_
    """
    nu = 3 / 2
    c = 2 * sqrt(nu)
    t = c * h

    return (1 + t) * gnp.exp(-t)


@partial(jax.jit, static_argnums=0)
def maternp_kernel(p, h):
    """Matérn kernel with half-integer regularity nu = p + 1/2

    See Stein, M. E., 1999, pp. 50, and Abramowitz and Stegun 1965,
    pp. 374-379, 443-444, Rasmussen and Williams 2006, pp. 85

    Parameters
    ----------
    p : int
        order
    h : ndarray(n)
        distance

    Returns
    -------
    k : ndarray(n)
        Values of the Matérn kernel at h

    """
    c = 2 * sqrt(p + 1 / 2)
    polynomial = 0
    a = gammaln(p + 1) - gammaln(2 * p + 1)
    for i in range(p + 1):
        polynomial = polynomial + (2 * c * h) ** (p - i) * exp(
            a
            + gammaln(p + i + 1)
            - gammaln(i + 1)
            - gammaln(p - i + 1)
        )
    return gnp.exp(-c * h) * polynomial


def maternp_covariance_ii_or_tt(x, p, param, pairwise=False):
    """Covariance between observations or predictands at x

    Parameters
    ----------
    x : ndarray(nx, d)
        observation points
    p : int
        half-integer regularity nu = p + 1/2
    param : ndarray(1 + d)
        sigma2 and range parameters
    pairwise : boolean
        whether to return a covariance matrix k(x_i, x_j),
        for i and j = 1 ... nx, if pairwise is False, or a covariance
        vector k(x_i, x_i) if pairwise is True
    """
    sigma2 = gnp.exp(param[0])
    invrho = gnp.exp(param[1:])
    nugget = 10 * gnp.finfo(gnp.float64).eps

    if pairwise:
        K = sigma2 * gnp.ones((x.shape[0],))  # nx x 0
    else:
        xs = scale(x, invrho)
        K = distance(xs, xs)  # nx x nx
        K = sigma2 * maternp_kernel(p, K) + nugget * gnp.eye(K.shape[0])

    return K


def maternp_covariance_it(x, y, p, param, pairwise=False):
    """Covariance between observations and prediction points

    Parameters
    ----------
    x : ndarray(nx, d)
        observation points
    y : ndarray(ny, d)
        observation points
    p : int
        half-integer regularity nu = p + 1/2
    param : ndarray(1 + d)
        log(sigma2) and log(1/range) parameters
    pairwise : boolean
        whether to return a covariance matrix k(x_i, y_j),
        for i in 1 ... nx and j in 1 ... ny, if pairwise is False,
        or a covariance vector k(x_i, y_i) if pairwise is True
    """
    sigma2 = gnp.exp(param[0])
    invrho = gnp.exp(param[1:])

    xs = scale(x, invrho)
    ys = scale(y, invrho)
    if pairwise:
        K = distance_pairwise(xs, ys)  # nx x 0
    else:
        K = distance(xs, ys)  # nx x ny

    K = sigma2 * maternp_kernel(p, K)

    return K


def maternp_covariance(x, y, p, param, pairwise=False):
    """Matérn covariance function with half-integer regularity nu = p + 1/2

    Parameters
    ----------
       x : ndarray(nx, d)
           Observation points
       y : ndarray(ny, d) or None
           Observation points. If None, it is assumed that y is x
       p : int
           Half-integer regularity nu = p + 1/2
       param : ndarray(1 + d)
           Covariance parameters
           [log(sigma2) log(1/rho_1) log(1/rho_2) ...]
       pairwise : boolean
           Whether to return a covariance matrix k(x_i, y_j),
           for i in 1 ... nx and j in 1 ... ny, if pairwise is False,
           or a covariance vector k(x_i, y_i) if pairwise is True

    Returns
    -------
    Covariance matrix (nx , ny) or covariance vector if pairwise is True

    Notes
    -----
    An isotropic covariance is obtained if param = [log(sigma2) log(1/rho)]
    (only one length scale parameter)
    """
    sigma2 = gnp.exp(param[0])
    invrho = gnp.exp(param[1:])
    nugget = 10 * gnp.finfo(gnp.float64).eps

    if y is x or y is None:
        return maternp_covariance_ii_or_tt(x, p, param, pairwise)
    else:
        return maternp_covariance_it(x, y, p, param, pairwise)


## -- parameters


def anisotropic_parameters_initial_guess_with_zero_mean(model, xi, zi):
    """anisotropic initialization strategy with zero mean

    Parameters
    ----------
    model : _type_
        _description_
    xi : _type_
        _description_
    zi : _type_
        _description_

    Returns
    -------
    _type_
        _description_

    References
    ----------
    .. [1] Basak, S., Petit, S., Bect, J., & Vazquez, E. (2021).
       Numerical issues in maximum likelihood parameter estimation for
       Gaussian process interpolation. arXiv:2101.09747.
    """
    rho = gnp.std(xi, axis=0)
    covparam = gnp.concatenate((gnp.array([gnp.log(1.0)]), -gnp.log(rho)))
    n = xi.shape[0]
    sigma2_GLS = (
        1 / n * model.norm_k_sqrd_with_zero_mean(xi, zi.reshape((-1,)), covparam)
    )

    return gnp.concatenate((gnp.array([gnp.log(sigma2_GLS)]), -gnp.log(rho)))


def anisotropic_parameters_initial_guess(model, xi, zi):
    """anisotropic initialization strategy

    Parameters
    ----------
    model : _type_
        _description_
    xi : _type_
        _description_
    zi : _type_
        _description_

    Returns
    -------
    _type_
        _description_

    References
    ----------
    [1] Basak, S., Petit, S., Bect, J., & Vazquez, E. (2021).
       Numerical issues in maximum likelihood parameter estimation for
       Gaussian process interpolation. arXiv:2101.09747.
    """

    xi_ = gnp.asarray(xi)
    zi_ = gnp.asarray(zi)

    rho = gnp.std(xi_, axis=0)
    covparam = gnp.concatenate((gnp.array([log(1.0)]), -gnp.log(rho)))
    n = xi_.shape[0]
    sigma2_GLS = 1 / n * model.norm_k_sqrd(xi_, zi_.reshape((-1,)), covparam)

    return gnp.concatenate((gnp.array([gnp.log(sigma2_GLS)]), -gnp.log(rho)))


def make_selection_criterion_with_gradient(selection_criterion, xi, zi):
    
    xi_ = gnp.asarray(xi)
    zi_ = gnp.asarray(zi)

    # selection criterion
    def crit_(covparam_):
        l = selection_criterion(xi_, zi_, covparam_)
        return l

    crit_jit = jax.jit(crit_)

    def crit(covparam):
        covparam_ = gnp.asarray(covparam)
        l = crit_jit(covparam_)
        return gnp.to_np(l)

    # gradient
    dcrit_ = gnp.grad(crit_)

    dcrit_jit = jax.jit(dcrit_)

    def dcrit(covparam):
        covparam_ = gnp.asarray(covparam)
        dl = dcrit_jit(covparam_)
        return gnp.to_np(dl)

    return crit, dcrit


def make_reml_criterion(model, xi, zi):
    """restricted maximum likelihood criterion

    Parameters
    ----------
    xi : ndarray(ni, d)
        points
    zi : ndarray(ni, 1)
        values

    Returns
    -------
    _type_
        restricted maximum likelihood criterion
    _type_
        restricted maximum likelihood criterion's gradient
    """
    xi_ = gnp.asarray(xi)
    zi_ = gnp.asarray(zi)

    # selection criterion
    def nlrel_(covparam_):
        l = model.negative_log_restricted_likelihood(xi_, zi_, covparam_)
        return l
    
    nlrel_jit = jax.jit(nlrel_)
    
    def nlrel(covparam):
        covparam_ = gnp.asarray(covparam)
        l = nlrel_jit(covparam_)
        return gnp.to_np(l)

    # gradient
    dnlrel_ = gnp.grad(nlrel_)

    dnlrel_jit = jax.jit(dnlrel_)
    
    def dnlrel(covparam):
        covparam_ = gnp.asarray(covparam)
        dl = dnlrel_jit(covparam_)
        return gnp.to_np(dl)
 
    return nlrel, dnlrel


def autoselect_parameters(p0, criterion, gradient, silent=True, info=False):
    """Automatic parameters selection

    Parameters
    ----------
    p0 : _type_
        _description_
    criterion : _type_
        _description_
    gradient : _type_
        _description_
    silent : Boolean
    info : Boolean

    Returns
    -------
    _type_
        _description_
    """
    tic = time.time()
    if gnp._gpmp_backend_ == 'jax':
        # scipy.optimize.minimize cannot use jax arrays
        if isinstance(p0, jax.numpy.ndarray):
            p0 = gnp.asarray(p0)
        gradient_asnumpy = lambda p: np.array(gnp.asarray(gradient(p)))
    elif gnp._gpmp_backend_ == 'torch':
        gradient_asnumpy = gradient

    options = {
        "disp": False,
        "maxcor": 20,
        "ftol": 1e-06,
        "gtol": 1e-05,
        "eps": 1e-08,
        "maxfun": 15000,
        "maxiter": 15000,
        "iprint": -1,
        "maxls": 40,
        "finite_diff_rel_step": None,
    }
    if silent is False:
        options["disp"] = True

    r = minimize(
        criterion,
        p0,
        args=(),
        method="L-BFGS-B",
        jac=gradient_asnumpy,
        bounds=None,
        tol=None,
        callback=None,
        options=options,
    )

    best = r.x
    r.covparam0 = p0
    r.covparam = best
    r.selection_criterion = criterion
    r.time = time.time() - tic

    if info:
        return best, r
    else:
        return best


def select_parameters_with_reml(model, xi, zi, info=False, silent=True):
    """Parameters selection with REML

    Parameters
    ----------
    model : _type_
        _description_
    xi : _type_
        _description_
    zi : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    tic = time.time()

    covparam0 = anisotropic_parameters_initial_guess(model, xi, zi)

    nlrl, dnlrl = make_selection_criterion_with_gradient(
        model.negative_log_restricted_likelihood,
        xi,
        zi
    )

    covparam_reml, info_ret = autoselect_parameters(
        covparam0, nlrl, dnlrl, silent=silent, info=True
    )
    # NB: info is essentially a dict with attribute accessors

    model.covparam = gnp.asarray(covparam_reml)

    if info:
        info_ret["covparam0"] = covparam0
        info_ret["covparam"] = covparam_reml
        info_ret["selection_criterion"] = nlrl
        info_ret["time"] = time.time() - tic
        return model, info_ret
    else:
        return model


def update_parameters_with_reml(model, xi, zi, info=False):
    """Parameters selection with REML

    Parameters
    ----------
    model : _type_
        _description_
    xi : _type_
        _description_
    zi : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    tic = time.time()

    covparam0 = model.covparam

    nlrl, dnlrl = make_selection_criterion_with_gradient(
        model.negative_log_restricted_likelihood,
        xi,
        zi
    )

    covparam_reml, info_ret = autoselect_parameters(
        covparam0, nlrl, dnlrl, silent=True, info=True
    )

    model.covparam = covparam_reml

    if info:
        info_ret["covparam0"] = covparam0
        info_ret["covparam"] = covparam_reml
        info_ret["selection_criterion"] = nlrl
        info_ret["time"] = time.time() - tic
        return model, info_ret
    else:
        return model
