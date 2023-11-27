# --------------------------------------------------------------
# Author: Emmanuel Vazquez <emmanuel.vazquez@centralesupelec.fr>
# Copyright (c) 2022-2023, CentraleSupelec
# License: GPLv3 (see LICENSE)
# --------------------------------------------------------------
import warnings
import gpmp.numpy as gnp


class Model:
    """
    Model manager class

    Attributes
    ----------
    mean :
    covariance :
    meanparam :
    covparam :

    Methods
    -------
    """

    def __init__(self, mean, covariance, meanparam=None, covparam=None):
        self.mean = mean
        self.covariance = covariance

        self.meanparam = meanparam
        self.covparam = covparam

    def __repr__(self):
        output = str("<gpmp.core.Model object> " + hex(id(self)))
        return output

    def __str__(self):
        output = str("<gpmp.core.Model object>")
        return output

    def kriging_predictor_with_zero_mean(self, xi, xt, return_type=0):
        """Compute the kriging predictor with zero mean"""
        Kii = self.covariance(xi, xi, self.covparam)
        Kit = self.covariance(xi, xt, self.covparam)

        if gnp._gpmp_backend_ == 'jax' or gnp._gpmp_backend_ == 'numpy':
            lambda_t = gnp.solve(
                Kii, Kit, sym_pos=True, overwrite_a=True, overwrite_b=True
            )
        elif gnp._gpmp_backend_ == 'torch':
            lambda_t = gnp.solve(Kii, Kit)

        if return_type == -1:
            zt_posterior_variance = None
        elif return_type == 0:
            zt_prior_variance = self.covariance(xt, None, self.covparam, pairwise=True)
            zt_posterior_variance = zt_prior_variance - gnp.einsum(
                "i..., i...", lambda_t, Kit
            )
        elif return_type == 1:
            zt_prior_variance = self.covariance(xt, None, self.covparam, pairwise=False)
            zt_posterior_variance = zt_prior_variance - gnp.matmul(lambda_t.T, Kit)

        return lambda_t, zt_posterior_variance

    def kriging_predictor(self, xi, xt, return_type=0):
        """Compute the kriging predictor with non-zero mean

        Parameters
        ----------
        xi : ndarray(ni, d)
            Observation points
        xt : ndarray(nt, d)
            Prediction points
        return_type : -1, 0 or 1
            If -1, returned posterior variance is None. If 0
            (default), return the posterior variance at points xt. If
            1, return the posterior covariance.

        Notes
        -----
        If return_type==1, then the covariance function k must be
        built so that k(xi, xi, covparam) returns the covariance
        matrix of observations, and k(xt, xt, covparam) returns the
        covariance matrix of the predictands. This means that the
        information of which are the observation points and which are
        the prediction points must be coded in xi / xt

        """
        # LHS
        Kii = self.covariance(xi, xi, self.covparam)
        Pi = self.mean(xi, self.meanparam)
        (ni, q) = Pi.shape
        # build [ [K P] ; [P' 0] ]
        LHS = gnp.vstack(
            (gnp.hstack((Kii, Pi)), gnp.hstack((Pi.T, gnp.zeros((q, q)))))
        )

        # RHS
        Kit = self.covariance(xi, xt, self.covparam)
        Pt = self.mean(xt, self.meanparam)
        RHS = gnp.vstack((Kit, Pt.T))

        # lambdamu_t = RHS^(-1) LHS
        lambdamu_t = gnp.solve(LHS, RHS, overwrite_a=True, overwrite_b=True)

        lambda_t = lambdamu_t[0:ni, :]

        # posterior variance
        if return_type == -1:
            zt_posterior_variance = None
        elif return_type == 0:
            zt_prior_variance = self.covariance(xt, None, self.covparam, pairwise=True)
            zt_posterior_variance = zt_prior_variance - gnp.einsum(
                "i..., i...", lambdamu_t, RHS
            )
        elif return_type == 1:
            zt_prior_variance = self.covariance(xt, None, self.covparam, pairwise=False)
            zt_posterior_variance = zt_prior_variance - gnp.matmul(lambdamu_t.T, RHS)

        return lambda_t, zt_posterior_variance

    def predict(self, xi, zi, xt, return_lambdas=False, zero_neg_variances=True, convert_out=True):
        """Performs a prediction at target points xt given the data (xi, zi).

        Parameters
        ----------
        xi : ndarray(ni,dim)
            observation points
        zi : ndarray(ni,1)
            observed values
        xt : ndarray(nt,dim)
            prediction points
        return_lambdas : bool, optional
            Set return_lambdas=True if lambdas should be returned, by default False
        zero_neg_variances : bool, optional
            Whether to zero negative posterior variances (due to numerical errors), default=True
        convert : bool, optional
            Whether to return numpy arrays or keep _gpmp_backend_ types

        Returns
        -------
        z_posterior_mean : ndarray
            2d array of shape nt x 1
        z_posterior variance : ndarray
            2d array of shape nt x 1

        Notes
        -----
        From a Bayesian point of view, the outputs are
        respectively the posterior mean and variance of the
        Gaussian process given the data (xi, zi).
        """

        xi_ = gnp.asarray(xi)
        zi_ = gnp.asarray(zi)
        xt_ = gnp.asarray(xt)

        # posterior variance
        if self.mean is None:
            lambda_t, zt_posterior_variance_ = self.kriging_predictor_with_zero_mean(
                xi_, xt_
            )
        else:
            lambda_t, zt_posterior_variance_ = self.kriging_predictor(xi_, xt_)

        if gnp.any(zt_posterior_variance_ < 0):
            warnings.warn(
                "In predict: negative variances detected. Consider using jitter.", RuntimeWarning
            )
        if zero_neg_variances:
            zt_posterior_variance_ = gnp.maximum(zt_posterior_variance_, 0)

        # posterior mean
        zt_posterior_mean_ = gnp.einsum("i..., i...", lambda_t, zi_)

        # outputs
        if convert_out:
            zt_posterior_mean = gnp.to_np(zt_posterior_mean_)
            zt_posterior_variance = gnp.to_np(zt_posterior_variance_)
        else:
            zt_posterior_mean = zt_posterior_mean_
            zt_posterior_variance = zt_posterior_variance_

        if not return_lambdas:
            return (zt_posterior_mean, zt_posterior_variance)
        else:
            return (zt_posterior_mean, zt_posterior_variance, lambda_t)

    def loo_with_zero_mean(self, xi, zi):

        xi_ = gnp.asarray(xi)
        zi_ = gnp.asarray(zi)

        n = xi_.shape[0]
        K = self.covariance(xi_, xi_, self.covparam)

        # Use the "virtual cross-validation" formula
        if gnp._gpmp_backend_ == 'jax' or gnp._gpmp_backend_ == 'numpy':
            C, lower = gnp.cho_factor(K)
            Kinv = gnp.cho_solve((C, lower), gnp.eye(n))
        elif gnp._gpmp_backend_ == 'torch':
            C = gnp.cholesky(K)
            Kinv = gnp.cholesky_solve(gnp.eye(n), C, upper=False)

        # e_loo,i  = 1 / Kinv_i,i ( Kinv  z )_i
        Kinvzi = gnp.matmul(Kinv, zi_)
        Kinvdiag = gnp.diag(Kinv)
        eloo = Kinvzi / Kinvdiag

        # sigma2_loo,i = 1 / Kinv_i,i
        sigma2loo = 1 / Kinvdiag

        # zloo_i = z_i - e_loo,i
        zloo = zi_ - eloo

        return zloo, sigma2loo, eloo

    def loo(self, xi, zi):

        xi_ = gnp.asarray(xi)
        zi_ = gnp.asarray(zi)

        n = xi_.shape[0]
        K = self.covariance(xi_, xi_, self.covparam)
        P = self.mean(xi_, self.meanparam)

        # Use the "virtual cross-validation" formula
        # Qinv = K^-1 - K^-1P (Pt K^-1 P)^-1 Pt K^-1
        if gnp._gpmp_backend_ == 'jax' or gnp._gpmp_backend_ == 'numpy':
            C, lower = gnp.cho_factor(K)
            Kinv = gnp.cho_solve((C, lower), gnp.eye(n))
            KinvP = gnp.cho_solve((C, lower), P)
        elif gnp._gpmp_backend_ == 'torch':
            C = gnp.cholesky(K)
            Kinv = gnp.cholesky_solve(gnp.eye(n), C, upper=False)
            KinvP = gnp.cholesky_solve(P, C, upper=False)

        PtKinvP = gnp.einsum("ki, kj->ij", P, KinvP)

        R = gnp.solve(PtKinvP, KinvP.T)
        Qinv = Kinv - gnp.matmul(KinvP, R)

        # e_loo,i  = 1 / Q_i,i ( Qinv  z )_i
        Qinvzi = gnp.matmul(Qinv, zi_)
        Qinvdiag = gnp.diag(Qinv)
        eloo = Qinvzi / Qinvdiag

        # sigma2_loo,i = 1 / Qinv_i,i
        sigma2loo = 1 / Qinvdiag

        # z_loo
        zloo = zi_ - eloo

        return zloo, sigma2loo, eloo

    def negative_log_likelihood(self, xi, zi, covparam):
        """Computes the negative log-likelihood of the model

        Parameters
        ----------
        xi : ndarray(ni,d)
            points
        zi : ndarray(ni,1)
            values
        covparam : _type_
            _description_

        Returns
        -------
        nll : scalar
            negative log likelihood
        """
        K = self.covariance(xi, xi, covparam)
        n = K.shape[0]

        if gnp._gpmp_backend_ == 'jax' or gnp._gpmp_backend_ == 'numpy':
            C, lower = gnp.cho_factor(K)
            Kinv_zi = gnp.cho_solve((C, lower), zi)
        elif gnp._gpmp_backend_ == 'torch':
            C = gnp.cholesky(K)
            Kinv_zi = gnp.cholesky_solve(zi.reshape(-1, 1), C, upper=False)
        
        norm2 = gnp.einsum("i..., i...", zi, Kinv_zi)
    
        ldetK = 2 * gnp.sum(gnp.log(gnp.diag(C)))

        L = 1 / 2 * (n * gnp.log(2 * gnp.pi) + ldetK + norm2)

        return L.reshape(())

    def negative_log_restricted_likelihood(self, xi, zi, covparam):
        """Computes the negative log- restricted likelihood of the model

        Parameters
        ----------
        xi : ndarray(ni,d)
            points
        zi : ndarray(ni,1)
            values
        covparam : _type_
            _description_

        Returns
        -------
        nll : scalar
            negative log likelihood
        """
        K = self.covariance(xi, xi, covparam)
        P = self.mean(xi, self.meanparam)
        Pshape = P.shape
        n, q = Pshape

        # Compute a matrix of contrasts
        [Q, R] = gnp.qr(P, "complete")
        W = Q[:, q:n]

        # Contrasts (n-q) x 1
        Wzi = gnp.matmul(W.T, zi)

        # Compute G = W' * (K * W), the covariance matrix of contrasts
        G = gnp.matmul(W.T, gnp.matmul(K, W))

        # Cholesky factorization: G = U' * U, with upper-triangular U
        # Compute G^(-1) * (W' zi)
        if gnp._gpmp_backend_ == 'jax' or gnp._gpmp_backend_ == 'numpy':
            C, lower = gnp.cho_factor(G)
            WKWinv_Wzi = gnp.cho_solve((C, lower), Wzi)
        elif gnp._gpmp_backend_ == 'torch':
            C = gnp.cholesky(G)
            WKWinv_Wzi = gnp.cholesky_solve(Wzi.reshape(-1, 1), C, upper=False)

        # Compute norm2 = (W' zi)' * G^(-1) * (W' zi)
        norm2 = gnp.einsum("i..., i...", Wzi, WKWinv_Wzi)
    
        # Compute log(det(G)) using the Cholesky factorization
        ldetWKW = 2 * gnp.sum(gnp.log(gnp.diag(C)))

        L = 1 / 2 * ((n - q) * gnp.log(2 * gnp.pi) + ldetWKW + norm2)

        return L.reshape(())

    def norm_k_sqrd_with_zero_mean(self, xi, zi, covparam):
        """

        Parameters
        ----------
        xi : ndarray(ni, d)
            points
        zi : ndarray(ni, 1)
            values
        covparam : _type_
            _description_

        Returns
        -------
        _type_
            z' K^-1 z
        """
        K = self.covariance(xi, xi, covparam)
        if gnp._gpmp_backend_ == 'jax' or gnp._gpmp_backend_ == 'numpy':
            C, lower = gnp.cho_factor(K)
            Kinv_zi = gnp.cho_solve((C, lower), zi)
        elif gnp._gpmp_backend_ == 'torch':
            C = gnp.cholesky(K)
            Kinv_zi = gnp.cholesky_solve(zi.reshape(-1, 1), C, upper=False)
            
        norm_sqrd = gnp.einsum("i..., i...", zi, Kinv_zi)
        
        return norm_sqrd

    def norm_k_sqrd(self, xi, zi, covparam):
        """

        Parameters
        ----------
        xi : ndarray(ni, d)
            _description_
        zi : ndarray(ni, 1)
            _description_
        covparam : _type_
            _description_

        Returns
        -------
        _type_
            (Wz)' (WKW)^-1 Wz where W is a matrix of contrasts
        """
        K = self.covariance(xi, xi, covparam)
        P = self.mean(xi, self.meanparam)
        n, q = P.shape

        # Compute a matrix of contrasts
        [Q, R] = gnp.qr(P, "complete")
        W = Q[:, q:n]

        # Contrasts (n-q) x 1
        Wzi = gnp.matmul(W.T, zi)

        # Compute G = W' * (K * W), the covariance matrix of contrasts
        G = gnp.matmul(W.T, gnp.matmul(K, W))

        # Cholesky factorization: G = U' * U, with upper-triangular U
        # Compute G^(-1) * (W' zi)
        if gnp._gpmp_backend_ == 'jax' or gnp._gpmp_backend_ == 'numpy':
            C, lower = gnp.cho_factor(G)
            WKWinv_Wzi = gnp.cho_solve((C, lower), Wzi)
        elif gnp._gpmp_backend_ == 'torch':
            C = gnp.cholesky(G)
            WKWinv_Wzi = gnp.cholesky_solve(Wzi.reshape(-1, 1), C, upper=False)
            
        # Compute norm_2 = (W' zi)' * G^(-1) * (W' zi)
        norm_sqrd = gnp.einsum("i..., i...", Wzi, WKWinv_Wzi)

        return norm_sqrd

    def sample_paths(self, xt, nb_paths, method='chol', check_result=True):
        """Generates nb_paths sample paths on xt from the GP model GP(0, k),
        where k is the covariance specified by Model.covariance

        Parameters
        ----------
        xt : ndarray(nt, 1)
            _description_
        nb_paths : int
            _description_

        Returns
        -------
        _type_
            _description_

        """
        xt_ = gnp.asarray(xt)
        
        K = self.covariance(xt, xt, self.covparam)

        # Factorization of the covariance matrix
        if method == "chol":
            C = gnp.cholesky(K, lower=True, overwrite_a=True)
            if check_result:
                if gnp.isnan(C).any():
                    raise AssertionError(
                        "In sample_paths: Cholesky factorization failed. Consider using jitter or the sdv switch."
                    )
        elif method == "svd":
            u, s, vt = gnp.svd(K, full_matrices=True, hermitian=True)
            C = gnp.matmul(u * gnp.sqrt(s), vt)

        # Generates samplepaths
        zsim = gnp.matmul(C, gnp.randn(K.shape[0], nb_paths))

        return zsim

    def conditional_sample_paths(self, ztsim, xi_ind, zi, xt_ind, lambda_t):
        """Generates conditionnal sample paths on xt from unconditional
        sample paths ztsim, using the matrix of kriging weights
        lambda_t, which is provided by kriging_predictor() or predict().

        Conditioning is done with respect to ni observations, located
        at the indices given by xi_ind in ztsim, with corresponding
        observed values zi. xt_ind specifies indices in ztsim
        corresponding to conditional simulation points.

        NOTE: the function implements "conditioning by kriging" (see,
        e.g., Chiles and Delfiner, Geostatistics: Modeling Spatial
        Uncertainty, Wiley, 1999).

        Parameters
        ----------
        ztsim : ndarray(n, nb_paths)
            Unconditional sample paths
        zi : ndarray(ni, 1)
            Observed values
        xi_ind : ndarray(ni, 1, dtype=int)
            Observed indices in ztsim
        xt_ind : ndarray(nt, 1, dtype=int)
            Prediction indices in ztsim
        lambda_t : ndarray(ni, nt)
            Kriging weights

        Returns
        -------
        ztsimc : ndarray(nt, nb_paths)
            Conditional sample paths at xt

        """
        zi_ = gnp.asarray(zi)
        ztsim_ = gnp.asarray(ztsim)

        d = zi_.reshape((-1, 1)) - ztsim_[xi_ind, :]

        ztsimc = ztsim_[xt_ind, :] + gnp.einsum("ij,ik->jk", lambda_t, d)

        return ztsimc
