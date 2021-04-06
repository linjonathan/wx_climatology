import matplotlib.pyplot as plt
import numpy as np

def hist_plot(xvar, rnd, xlab, title):
    b_min = np.floor(np.nanmin(xvar) / rnd) * rnd
    b_max = np.ceil(np.nanmax(xvar) / rnd) *  rnd

    var_bins = np.arange(b_min, b_max+rnd, rnd)

    counts, bins, bars = plt.hist(xvar, density=True, bins=var_bins, rwidth=0.9)
    #plt.scatter([np.nanmean(xvar)], [np.nanmax(counts)], c='k', linestyle='-')

    pcts = [5, 25, 50, 75, 95]
    for pct in pcts:
        plt.scatter([np.nanpercentile(xvar, pct)], [np.nanmax(counts)], c='k', linestyle='-')
        plt.plot([np.percentile(xvar, pct), np.percentile(xvar, pct)], [0, np.max(counts)], c='k', linestyle='--')

    plt.xlabel(xlab)
    plt.ylabel('Density')
    plt.title('%s' % title)
    plt.savefig('fig/%s.png' % xlab)
    plt.close()

def cdf_plot(xvar, rnd, xlab, title):
    b_min = np.floor(np.min(xvar) / rnd) * rnd
    b_max = np.ceil(np.max(xvar) / rnd) *  rnd

    #var_bins = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5]
    var_bins = np.arange(0, 1.01, 0.01)
    counts, bins, bars = plt.hist(xvar, density=True, bins=var_bins, rwidth=0.9, cumulative=True, histtype='step')
    plt.grid()
    plt.xlabel(xlab)
    plt.ylabel('Density')
    plt.ylim([0.2, 1])
    plt.title('%s' % title)
    plt.savefig('fig/%s.png' % xlab)
    plt.close()
