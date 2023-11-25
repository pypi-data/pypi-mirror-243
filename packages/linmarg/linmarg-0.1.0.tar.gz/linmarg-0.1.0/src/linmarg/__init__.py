# -*- coding: utf-8 -*-

# Copyright 2022-2023 Jean-Baptiste Delisle
#
# This file is part of linmarg.
#
# linmarg is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# linmarg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the
# GNU Lesser General Public License along with linmarg.
# If not, see <http://www.gnu.org/licenses/>.
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import block_diag, cholesky, solve, solve_triangular

__all__ = ['CBV', 'Bspline']


@dataclass
class LinearMarginalizer:
  r"""
  Linear model for which we want to marginalize the likelihood over its parameters.

  Parameters
  ----------
  size : float
    Size (n) of the dataset.
  nparam : int
    Number of linear parameters.
  indices: (c, 2) ndarray
    Start/end indices of the parameters corresponding to each component of the model.
  icovprior : (nparam, nparam) ndarray
    Inverse of the covariance matrix of the prior on linear parameters.
  logsqdetcovprior: float
    log of the square-root of the determinant of the covariance matrix.
  """

  size: int
  nparam: int
  indices: np.ndarray
  At: np.ndarray
  icovprior: np.ndarray
  logsqdetcovprior: float

  def __add__(self, b: 'LinearMarginalizer') -> 'LinearMarginalizer':
    assert self.size == b.size
    return LinearMarginalizer(
      self.size,
      self.nparam + b.nparam,
      np.concatenate((self.indices, b.indices + self.nparam)),
      np.concatenate((self.At, b.At)),
      block_diag(self.icovprior, b.icovprior),
      self.logsqdetcovprior + b.logsqdetcovprior,
    )

  def loglike(self, y: np.ndarray, sig: np.ndarray, m: np.ndarray | float = 1) -> float:
    r"""
    Marginalized log-likelihood over all linear parameters.

    Parameters
    ----------
    y : (n,) ndarray
      Timeseries to be detrended.
    sig : (n,) ndarray
      Measurements errors.
    m : (n,) ndarray or float
      Multiplicative model.

    Returns
    -------
    loglike : float
      The marginalized log-likelihood.
    """
    Gt = self.At * m / sig
    u = y / sig
    icov = Gt @ Gt.T + self.icovprior
    x = Gt @ u
    L = cholesky(icov, lower=True)
    z = solve_triangular(L, x, lower=True)
    return (
      -np.sum(np.log(np.diag(L)))
      - self.logsqdetcovprior
      - np.sum(np.log(sig))
      - y.size / 2 * np.log(2 * np.pi)
      + np.sum(z * z) / 2
      - np.sum(u * u) / 2
    )

  def mean(
    self, y: np.ndarray, sig: np.ndarray, m: np.ndarray | float = 1, split: bool = False
  ) -> np.ndarray | tuple:
    r"""
    Conditional expectation of the model given y and m.

    Parameters
    ----------
    y : (n,) ndarray
      Timeseries to be detrended.
    sig : (n,) ndarray
      Measurements errors.
    m : (n,) ndarray or float
      Multiplicative model.
    split: bool
      Wheter to split the contributions of each component of the model or to merge them.

    Returns
    -------
    mu : (n,) ndarray or tuple of (n,) ndarray
      Conditional expectation of the model, or of each component.
    """

    Gt = self.At * m / sig
    u = y / sig
    icov = Gt @ Gt.T + self.icovprior
    x = Gt @ u
    mu_eta = solve(icov, x)
    if split:
      return (mu_eta[sk:ek] @ self.At[sk:ek] for sk, ek in self.indices)
    else:
      return mu_eta @ self.At


class CBV(LinearMarginalizer):
  r"""
  Cotrending basis vectors.

  Parameters
  ----------
  cbv: (m, n) ndarray
    Matrix of m cotrending basis vectors for a time series of size n.
  prior : (m, m) ndarray or (m,) ndarray or float or None
    Scale of the Gaussian prior on the CBV parameters.
    If a matrix is provided, this should be the covariance matrix.
    If a vector (or single value) is provided, this should be the scales for each (all) coefficient.
    If None, we assume unbounded uniform priors and ignore the normalization factor.
  """

  def __init__(self, cbv: np.ndarray, prior: np.ndarray | float | None = None):
    nparam = cbv.shape[0]
    if isinstance(prior, np.ndarray):
      if prior.ndim == 2:
        self._add(nparam, cbv, np.linalg.inv(prior), np.linalg.slogdet(prior)[1] / 2)
      else:
        self._add(nparam, cbv, np.diag(1 / prior**2), np.sum(np.log(prior)))
    else:
      icovprior = np.zeros((nparam, nparam))
      logsqdetcovprior = 0
      if prior is not None:
        icovprior[np.diag_indices(nparam)] = 1 / prior**2
        logsqdetcovprior = nparam * np.log(prior)
    super().__init__(
      size=cbv.shape[1],
      nparam=nparam,
      indices=np.array([[0, nparam]]),
      At=cbv,
      icovprior=icovprior,
      logsqdetcovprior=logsqdetcovprior,
    )


class Bspline(LinearMarginalizer):
  r"""
  Uniform cubic B-spline.

  Parameters
  ----------
  t : (n,) ndarray
    Times of measurements.
  tau : float or None
    Timescale of the B-spline (lag between two knots).
    This parameter is ignored if P (and nknot) is provided.
  P : float or None
    Period of the B-spline.
    If provided, the parameter tau is ignored but nknot should be provided instead.
    If None, the spline is not periodic.
  nknot : int or None:
    Number of knots over a period for a periodic B-spline.
  prior : float or None
    Scale of the Gaussian prior on the B-spline parameters.
    If None, we assume unbounded uniform priors and ignore the normalization factor.
  """

  def __init__(
    self,
    t: np.ndarray,
    tau: float | None = None,
    P: float | None = None,
    nknot: int | None = None,
    prior: float | None = None,
  ):
    if P is None:
      t0 = tau * np.floor(t.min() / tau)
      s = (t - t0) / tau
    else:
      tau = P / nknot
      s = (t % P) / tau

    k = np.floor(s).astype(int)
    ds = s - k
    ds2 = ds * ds
    ds3 = ds2 * ds

    uk = np.unique(k)
    if P is None:
      ukdef = np.unique(np.concatenate((uk, uk + 1, uk + 2, uk + 3)))
    else:
      ukdef = np.unique(
        np.concatenate((uk, (uk + 1) % nknot, (uk + 2) % nknot, (uk + 3) % nknot))
      )
    nparam = ukdef.size
    iuk = np.empty(ukdef[-1] + 1, dtype=int)
    iuk[ukdef] = np.arange(nparam)
    ik = iuk[k]
    inds = np.arange(t.size)
    At = np.zeros((nparam, t.size))
    At[ik, inds] = 1 - ds3 + 3 * (ds2 - ds)
    At[(ik + 1) % nparam, inds] = 3 * ds3 - 6 * ds2 + 4
    At[(ik + 2) % nparam, inds] = 3 * (ds + ds2 - ds3) + 1
    At[(ik + 3) % nparam, inds] = ds3

    icovprior = np.zeros((nparam, nparam))
    logsqdetcovprior = 0
    if prior is not None:
      icovprior[np.diag_indices(nparam)] = 1 / prior**2
      logsqdetcovprior = nparam * np.log(prior)

    super().__init__(
      size=t.size,
      nparam=nparam,
      indices=np.array([[0, nparam]]),
      At=At,
      icovprior=icovprior,
      logsqdetcovprior=logsqdetcovprior,
    )
