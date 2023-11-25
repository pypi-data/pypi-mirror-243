import numpy as np
from linmarg import CBV, Bspline


def test_bspline():
  np.random.seed(0)

  nt = 1000
  D = nt // 4
  k0 = nt // 6
  R = 0.2
  gap = 0.6

  t = np.linspace(0, 12.45, nt)
  t[nt // 2 :] += gap + t[0] - t[1]
  tau = 1

  yact = 10 + np.cos(2 * np.pi * t / 5.7)

  ypla = np.ones(nt)
  ypla[k0 : k0 + D] = 1 - R

  sig = np.random.uniform(0.5, 1.5, nt)
  y = yact * ypla + np.random.normal(0, sig)

  bs = Bspline(t, tau)

  ll = np.empty(nt - D)
  for k in range(nt - D):
    m = np.ones(nt)
    m[k : k + D] = 1 - R
    ll[k] = bs.loglike(y, sig, m)
  kbest = np.argmax(ll)
  assert kbest == k0
  m = np.ones(nt)
  m[k0 : k0 + D] = 1 - R
  s = bs.mean(y, sig, m)
  chi2 = np.sum(((y - s * m) / sig) ** 2)
  assert chi2 < 1.1 * nt


def test_perbspline():
  np.random.seed(0)

  nt = 1000
  D = nt // 4
  k0 = nt // 6
  R = 0.2
  gap = 0.6

  t = np.linspace(0, 12.45, nt)
  t[nt // 2 :] += gap + t[0] - t[1]

  yact = 10 + np.cos(2 * np.pi * t / 5.7)

  ypla = np.ones(nt)
  ypla[k0 : k0 + D] = 1 - R

  sig = np.random.uniform(0.5, 1.5, nt)
  y = yact * ypla + np.random.normal(0, sig)

  bs = Bspline(t, P=5.7, nknot=10)

  ll = np.empty(nt - D)
  for k in range(nt - D):
    m = np.ones(nt)
    m[k : k + D] = 1 - R
    ll[k] = bs.loglike(y, sig, m)
  kbest = np.argmax(ll)
  assert kbest == k0
  m = np.ones(nt)
  m[k0 : k0 + D] = 1 - R
  s = bs.mean(y, sig, m)
  chi2 = np.sum(((y - s * m) / sig) ** 2)
  assert chi2 < 1.1 * nt


def test_bspline_CBV():
  np.random.seed(0)

  nt = 1000
  nCBV = 4
  D = nt // 4
  k0 = nt // 6
  R = 0.2
  gap = 0.6

  t = np.linspace(0, 12.45, nt)
  t[nt // 2 :] += gap + t[0] - t[1]
  tau = 1

  At = np.array(
    [
      np.cos(k * np.pi * t + np.random.uniform(0, 2 * np.pi)) ** 2
      for k in range(1, nCBV + 1)
    ]
  )
  etaA_true = np.random.uniform(0.5, 1.5, size=nCBV)

  yact = 10 + np.cos(2 * np.pi * t / 5.7) + At.T @ etaA_true

  ypla = np.ones(nt)
  ypla[k0 : k0 + D] = 1 - R

  sig = np.random.uniform(0.5, 1.5, nt)
  y = yact * ypla + np.random.normal(0, sig)

  bs = Bspline(t, tau) + CBV(At)

  ll = np.empty(nt - D)
  for k in range(nt - D):
    m = np.ones(nt)
    m[k : k + D] = 1 - R
    ll[k] = bs.loglike(y, sig, m)
  kbest = np.argmax(ll)
  assert kbest == k0
  m = np.ones(nt)
  m[k0 : k0 + D] = 1 - R
  s = bs.mean(y, sig, m)
  chi2 = np.sum(((y - s * m) / sig) ** 2)
  assert chi2 < 1.1 * nt
