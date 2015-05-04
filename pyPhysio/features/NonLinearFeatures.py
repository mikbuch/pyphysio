# coding=utf-8
from __future__ import division

__author__ = 'AleB'
__all__ = ['ApproxEntropy', 'CorrelationDim', 'Fisher', 'FractalDimension', 'DFALongTerm', 'DFAShortTerm', 'Hurst',
           'PetrosianFracDim', 'PoinEll', 'PoinSD1', 'PoinSD12', 'PoinSD2', 'SVDEntropy', 'SampleEntropy']

from scipy.spatial.distance import cdist, pdist
from scipy.stats.mstats import mquantiles
import numpy as np

from pyPhysio.features.CacheOnlyFeatures import Diff, OrderedSubsets, PoincareSD, StandardDeviation
from pyPhysio.features.BaseFeatures import NonLinearFeature
from pyPhysio.features.TDFeatures import Mean
from pyPhysio.Utility import ordered_subsets
from pyPhysio.PyHRVSettings import MainSettings as Sett


class ApproxEntropy(NonLinearFeature):
    """
    Calculates the approx entropy of the data series.
    """

    def __init__(self, data=None):
        super(ApproxEntropy, self).__init__(data)
        if len(data) < 3:
            self._value = np.nan
        else:
            r = Sett.approx_entropy_r
            uj_m = OrderedSubsets.get(self._data, subset_size=2)
            uj_m1 = OrderedSubsets.get(self._data, subset_size=3)
            card_elem_m = uj_m.shape[0]
            card_elem_m1 = uj_m1.shape[0]

            r = r * np.std(self._data)
            d_m = cdist(uj_m, uj_m, 'chebyshev')
            d_m1 = cdist(uj_m1, uj_m1, 'chebyshev')

            cmr_m_apen = np.zeros(card_elem_m)
            for i in xrange(card_elem_m):
                vector = d_m[i]
                cmr_m_apen[i] = float(sum(1 for i in vector if i <= r)) / card_elem_m

            cmr_m1_apen = np.zeros(card_elem_m1)
            for i in xrange(card_elem_m1):
                vector = d_m1[i]
                cmr_m1_apen[i] = float(sum(1 for i in vector if i <= r)) / card_elem_m1

            phi_m = np.sum(np.log(cmr_m_apen)) / card_elem_m
            phi_m1 = np.sum(np.log(cmr_m1_apen)) / card_elem_m1

            self._value = phi_m - phi_m1


class SampleEntropy(NonLinearFeature):
    """
    Calculates the sample entropy of the data series.
    """

    def __init__(self, data=None):
        super(SampleEntropy, self).__init__(data)
        if len(data) < 4:
            self._value = np.nan
        else:
            r = Sett.sample_entropy_r
            uj_m = OrderedSubsets.get(self._data, subset_size=2)
            uj_m1 = OrderedSubsets.get(self._data, subset_size=3)

            num_elem_m = uj_m.shape[0]
            num_elem_m1 = uj_m1.shape[0]

            r = r * StandardDeviation.get(self._data)
            d_m = cdist(uj_m, uj_m, 'chebyshev')
            d_m1 = cdist(uj_m1, uj_m1, 'chebyshev')

            cmr_m_samp_en = np.zeros(num_elem_m)
            for i in xrange(num_elem_m):
                vector = d_m[i]
                cmr_m_samp_en[i] = (sum(1 for i in vector if i <= r) - 1) / (num_elem_m - 1)

            cmr_m1_samp_en = np.zeros(num_elem_m1)
            for i in xrange(num_elem_m1):
                vector = d_m1[i]
                cmr_m1_samp_en[i] = (sum(1 for i in vector if i <= r) - 1) / (num_elem_m1 - 1)

            cm = np.sum(cmr_m_samp_en) / num_elem_m
            cm1 = np.sum(cmr_m1_samp_en) / num_elem_m1

            self._value = np.log(cm / cm1)


class FractalDimension(NonLinearFeature):
    """
    Calculates the fractal dimension of the data series.
    """

    def __init__(self, data=None):
        super(FractalDimension, self).__init__(data)
        if len(data) < 3:
            self._value = np.nan
        else:
            uj_m = OrderedSubsets.get(self._data, subset_size=2)
            cra = Sett.fractal_dimension_cra
            crb = Sett.fractal_dimension_crb
            mutual_distance = pdist(uj_m, 'chebyshev')

            num_elem = len(mutual_distance)

            rr = mquantiles(mutual_distance, prob=[cra, crb])
            ra = rr[0]
            rb = rr[1]

            cmr_a = (sum(1 for i in mutual_distance if i <= ra)) / num_elem
            cmr_b = (sum(1 for i in mutual_distance if i <= rb)) / num_elem

            self._value = (np.log(cmr_b) - np.log(cmr_a)) / (np.log(rb) - np.log(ra))


class SVDEntropy(NonLinearFeature):
    """
    Calculates the SVD entropy of the data series.
    """

    def __init__(self, data=None):
        super(SVDEntropy, self).__init__(data)
        if len(data) < 2:
            self._value = np.nan
        else:
            uj_m = OrderedSubsets.get(self._data, subset_size=2)
            w = np.linalg.svd(uj_m, compute_uv=False)
            w /= sum(w)
            self._value = -1 * sum(w * np.log(w))


class Fisher(NonLinearFeature):
    """
    Calculates the Fisher index of the data series.
    """

    def __init__(self, data=None):
        super(Fisher, self).__init__(data)
        if len(data) < 2:
            self._value = np.nan
        else:
            uj_m = OrderedSubsets.get(self._data, subset_size=2)
            w = np.linalg.svd(uj_m, compute_uv=False)
            w /= sum(w)
            fi = 0
            for i in xrange(0, len(w) - 1):  # from Test1 to M
                fi += ((w[i + 1] - w[i]) ** 2) / (w[i])

            self._value = fi


class CorrelationDim(NonLinearFeature):
    """
    Calculates the correlation dimension of the data series.
    """

    def __init__(self, data=None):
        super(CorrelationDim, self).__init__(data)
        if len(self._data) < Sett.correlation_dimension_len:
            self._value = np.nan
        else:
            rr = self._data / 1000  # rr in seconds
            uj = ordered_subsets(rr, Sett.correlation_dimension_len)
            num_elem = uj.shape[0]
            r_vector = np.arange(0.3, 0.46, 0.02)  # settings
            c = np.zeros(len(r_vector))
            jj = 0
            n = np.zeros(num_elem)
            dj = cdist(uj, uj, 'euclidean')
            for r in r_vector:
                for i in xrange(num_elem):
                    vector = dj[i]
                    n[i] = float(sum(1 for i in vector if i <= r)) / num_elem
                c[jj] = np.sum(n) / num_elem
                jj += 1

            log_c = np.log(c)
            log_r = np.log(r_vector)

            self._value = (log_c[-1] - log_c[0]) / (log_r[-1] - log_r[0])


class PoinSD1(NonLinearFeature):
    """
    Calculates the SD1 Poincaré index of the data series.
    """

    def __init__(self, data=None):
        super(PoinSD1, self).__init__(data)
        sd1, sd2 = PoincareSD.get(self._data)
        self._value = sd1


class PoinSD2(NonLinearFeature):
    """
    Calculates the SD2 Poincaré index of the data series.
    """

    def __init__(self, data=None):
        super(PoinSD2, self).__init__(data)
        sd1, sd2 = PoincareSD.get(self._data)
        self._value = sd2


class PoinSD12(NonLinearFeature):
    """
    Calculates the ratio between SD1 and SD2 Poincaré features of the data series.
    """

    def __init__(self, data=None):
        super(PoinSD12, self).__init__(data)
        sd1, sd2 = PoincareSD.get(self._data)
        self._value = sd1 / sd2


class PoinEll(NonLinearFeature):
    """
    Calculates the Poincaré Ell. index of the data series.
    """

    def __init__(self, data=None):
        super(PoinEll, self).__init__(data)
        sd1, sd2 = PoincareSD.get(self._data)
        self._value = sd1 * sd2 * np.pi


class Hurst(NonLinearFeature):
    """
    Calculates the Hurst HRV index of the data series.
    """

    def __init__(self, data=None):
        super(Hurst, self).__init__(data)
        n = len(self._data)
        if n < 2:
            self._value = np.nan
        else:
            t = np.arange(1.0, n + 1)
            y = np.cumsum(self._data)
            ave_t = np.array(y / t)

            s_t = np.zeros(n)
            r_t = np.zeros(n)
            for i in xrange(n):
                s_t[i] = np.std(self._data[:i + 1])
                x_t = y - t * ave_t[i]
                r_t[i] = np.max(x_t[:i + 1]) - np.min(x_t[:i + 1])

            r_s = r_t / s_t
            r_s = np.log(r_s)
            n = np.log(t).reshape(n, 1)
            h = np.linalg.lstsq(n[1:], r_s[1:])[0]
            self._value = h[0]


class PetrosianFracDim(NonLinearFeature):
    """
    Calculates the petrosian's fractal dimension of the data series.
    """

    def __init__(self, data=None):
        super(PetrosianFracDim, self).__init__(data)
        d = Diff.get(self._data)
        n_delta = 0  # number of sign changes in derivative of the signal
        for i in xrange(1, len(d)):
            if d[i] * d[i - 1] < 0:
                n_delta += 1
        n = len(self._data)
        self._value = np.float(np.log10(n) / (np.log10(n) + np.log10(n / n + 0.4 * n_delta)))


class DFAShortTerm(NonLinearFeature):
    """
    Calculate the alpha1 (short term) component index of the De-trended Fluctuation Analysis.
    """

    def __init__(self, data=None):
        super(DFAShortTerm, self).__init__(data)
        # calculates De-trended Fluctuation Analysis: alpha1 (short term) component
        x = self._data
        if len(self._data) >= 16:
            ave = Mean.get(x)
            y = np.cumsum(x)
            y -= ave
            l = np.arange(4, 17, 4)
            f = np.zeros(len(l))  # f(n) of different given box length n
            for i in xrange(0, len(l)):
                n = int(l[i])  # for each box length l[i]
                for j in xrange(0, len(x), n):  # for each box
                    if j + n < len(x):
                        c = range(j, j + n)
                        c = np.vstack([c, np.ones(n)]).T  # coordinates of time in the box
                        z = y[j:j + n]  # the value of example_data in the box
                        f[i] += np.linalg.lstsq(c, z)[1]  # add residue in this box
                f[i] /= ((len(x) / n) * n)
            f = np.sqrt(f)
            self._value = np.linalg.lstsq(np.vstack([np.log(l), np.ones(len(l))]).T, np.log(f))[0][0]
        else:
            self._value = np.nan


class DFALongTerm(NonLinearFeature):
    """
    Calculate the alpha2 (long term) component index of the De-trended Fluctuation Analysis.
    """

    def __init__(self, data=None):
        super(DFALongTerm, self).__init__(data)
        # calculates De-trended Fluctuation Analysis: alpha2 (long term) component
        x = self._data
        if len(self._data) >= 16:
            ave = Mean.get(x)
            y = np.cumsum(x)
            y -= ave
            l_max = np.min([64, len(x)])
            l = np.arange(16, l_max + 1, 4)
            f = np.zeros(len(l))  # f(n) of different given box length n
            for i in xrange(0, len(l)):
                n = int(l[i])  # for each box length l[i]
                for j in xrange(0, len(x), n):  # for each box
                    if j + n < len(x):
                        c = range(j, j + n)
                        c = np.vstack([c, np.ones(n)]).T  # coordinates of time in the box
                        z = y[j:j + n]  # the value of example_data in the box
                        f[i] += np.linalg.lstsq(c, z)[1]  # add residue in this box
                f[i] /= ((len(x) / n) * n)
            f = np.sqrt(f)

            self._value = np.linalg.lstsq(np.vstack([np.log(l), np.ones(len(l))]).T, np.log(f))[0][0]
        else:
            self._value = np.nan