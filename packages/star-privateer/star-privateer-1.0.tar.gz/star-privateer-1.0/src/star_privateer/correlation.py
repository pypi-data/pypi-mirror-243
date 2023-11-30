import star_privateer as sp
import numpy as np
import matplotlib.pyplot as plt
import numba
import pandas as pd
from scipy.signal import correlate

'''
Functions to compute correlation
and autocorrelation functions.

This collection of functions are dedicated
to achieve the task of the PLATO module
MSAP4-02.
'''

def period_to_lag (dt, size, periods_in=None) :
  '''
  Compute from sampling and input periods
  closest lag index in the data and 
  corresponding output periods.

  Parameters 
  ----------
  
  dt : float
    sampling, in day

  periods_in : ndarray
    input periods, in day
  '''

  if periods_in is None :
    lags = np.arange (0, size)
  else :
    lags = np.rint (periods_in/dt).astype (int)
  lags = np.unique (lags)
  periods_out = lags * dt
  periods_out = periods_out[lags<size]
  lags = lags[lags<size]
    
  return lags, periods_out

@numba.jit (nopython=True)
def cross_correlation (y1, y2, lag) :
  '''
  Compute cross correlation value between two 
  vectors of same size for a given lag.
  '''

  y1 = y1[:y1.size-lag]
  y2 = y2[lag:]

  ccorr = np.sum (y1*np.conj (y2))

  return ccorr 

@numba.jit (nopython=True)
def compute_ccf (y1, y2, lags) :
  '''
  Wrapper to compute cross correlation
  for an ensemble of lags.
  ''' 

  ccf = np.zeros (lags.size)
  for ii, lag in enumerate (lags) :
    ccf[ii] = cross_correlation (y1, y2, lag)

  return ccf

def select_smooth_period_acf (periods, acf,
                              shortest_searched_period=0.1) :
  '''
  Select the period to consider for the Gaussian
  smoothing of the ACF. 
  '''
  dt = np.abs (np.median (np.diff (periods)))*86400
  p_ls, ls = sp.series_to_psd (acf, dt, return_periods=True)
  smooth_period = 0.1*p_ls[np.argmax (ls)]
  freq = 1/p_ls
  dfreq = np.median (np.abs (np.diff (freq)))
  if 1/smooth_period > 1/shortest_searched_period + 5*dfreq :
    smooth_period = shortest_searched_period 

  return smooth_period

def compute_acf (s, dt, periods_in=None, normalise=True,
                 use_scipy_correlate=True, smooth=False,
                 pcutoff=None, pthresh=None, smooth_period=None,
                 win_type='gaussian', verbose=False,
                 cutoff_filter_acf=None) :
  '''
  Compute autocorrelation function for 
  a uniformly sampled timeseries.
  '''
  if cutoff_filter_acf is not None :
    s = sp.preprocess (dt, s, cut=cutoff_filter_acf)
  lags, periods_out = period_to_lag (dt, s.size, periods_in)
  if not use_scipy_correlate :
    acf = compute_ccf (s, s, lags)
  else :
    acf = correlate(s, s, mode='full', method='fft')
    acf = acf[s.size-1:]
    acf = acf[lags] 
  if smooth :
    dt = np.median (np.diff (periods_out))
    if smooth_period is None :
      smooth_period = select_smooth_period_acf (periods_out, acf)
    sizebox = int (smooth_period / dt)
    if sizebox > 0 :
      acf = apply_smoothing (acf, sizebox, 
                             win_type=win_type, std=sizebox)
      if verbose :
        print ("ACF was smoothed with a period {:.2f} days".format (smooth_period))
  if normalise :
    if smooth :
      acf = acf / acf[0]
    else :
      acf = acf / np.sum (s*np.conj (s)) 
  
  return periods_out, acf  

def plot_acf (periods, acf, ax=None, figsize=(8, 4),
              lw=1, filename=None, dpi=300,
              prot=None, xlim=None,
              acf_additional=None,
              color_additional=None) :
  '''
  Plot autocorrelation function (ACF).
  '''

  if ax is None :
    fig, ax = plt.subplots (1, 1, figsize=figsize)
  else :
    fig = None

  ax.plot (periods, acf, color='black', lw=lw)
  if acf_additional is not None :
    for acf_a, color_a in zip (acf_additional, color_additional) :
      ax.plot (periods, acf_a, color=color_a, lw=lw)
  ax.set_xlabel ('Period (day)')
  ax.set_ylabel ('ACF')
  if prot is not None :
    prot = np.atleast_1d (prot)
    for elt in prot :
      ax.axvline (elt, color='grey', lw=lw, ls='--')

  if xlim is not None :
    ax.set_xlim (xlim)

  if fig is not None :
    fig.tight_layout ()

  if filename is not None :
    fig.savefig (filename, dpi=dpi)

  return fig

def apply_smoothing (a, sizebox, win_type='triang', std=None) :
  '''
  Smoothing function. Uses triangle smoothing by default

  Parameters
  ----------
  vector: ndarray 
    vector to smooth.

  smoothing: int
    size of the rolling window used for the smooth.

  win_type: str 
    see ``scipy.signal.windows``. Optional, default ``triang``.

  Returns
  -------
  smoothed vector
  '''
  smoothed = pd.Series (data=a)
  if win_type=='gaussian' :
    smoothed = smoothed.rolling (sizebox, min_periods=1,
                                 center=True, win_type=win_type).mean (std=std)
  else :
    smoothed = smoothed.rolling (sizebox, min_periods=1,
                                 center=True, win_type=win_type).mean ()
  return smoothed.to_numpy ()

def find_global_maximum (p_acf, acf, 
                         pcutoff=None, pthresh=None) :
  """
  Find period of the global maximum of an ACF
  function (ignoring the zero-lag maximum 
  and first decreasing slope)
  """ 
  if pcutoff is not None :
    acf = acf[p_acf<pcutoff]
    p_acf = p_acf[p_acf<pcutoff]
  if pthresh is not None :
    acf = acf[p_acf>pthresh]
    p_acf = p_acf[p_acf>pthresh]

  if np.any (acf<0) :
    indexes = np.nonzero (acf<0)[0]
    index_max = np.argmax (acf[indexes[0]:]) + acf[:indexes[0]].size
  else :
    index_max = np.argmax (acf)
  glob_max = p_acf[index_max]
  return glob_max

def find_local_extrema (data) : 
  """
  Find the maxima and minima in a given array.

  Parameters
  −−−−−−−−−−
  
  data : ndarray
    input array to explore

  Returns 
  −−−−−−−
  a_min, a_max : tuple of ndarray
    maxima and minima of the array
  """
  a_min = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1 # local min
  a_max = (np.diff(np.sign(np.diff(data))) < 0).nonzero()[0] + 1 # local max
  return a_min, a_max

def compute_all_hacf (acf, a_max, a_min) :
  """
  Compute all H_ACF values from local extrema
  values. 
  """
  a_max = a_max[:a_min.size-1]
  a1 = acf[a_max] - acf[a_min[:-1]] 
  a2 = acf[a_max] - acf[a_min[1:]]
  all_hacf = (a1 + a2) / 2

  return all_hacf

def find_period_acf (periods, acf,
                     pcutoff=None, pthresh=None) : 
  '''
  Find significant periodicities identified by the ACF
  function computation and related control parameters.

  Parameters
  ----------
  periods : ndarray
      Period value on which the autocorrelation
      function has been computed.

  acf : ndarray
      Autocorrelation function.

  Returns
  -------
  tuple
      Tuple with ``prot``, ``hacf``, ``gacf``, ``all_prots``, ``all_hacf``
      and ``all_gacf``. 
  '''
  a_min, a_max = find_local_extrema (acf)
  if a_max.size > 0 and a_min.size > 1 :
    all_gacf = acf[a_max]
    all_hacf = compute_all_hacf (acf, a_max, a_min)
    all_prots = periods[a_max]
    # Checking the relative heights of the two first 
    # peaks to see if first peak must be ignored
    if all_hacf.size>1 and all_hacf[1]>2*all_hacf[0] : 
      index_prot = a_max[1]
      all_prots = all_prots[1:]
      all_gacf = all_gacf[1:]
      all_hacf = all_hacf[1:]
    else :
      index_prot = a_max[0]
    # Ensure that all_hacf is the same size as all_prots
    if all_prots.size > all_hacf.size :
      all_hacf = np.concatenate ((all_hacf, 
                 np.full(all_prots.size-all_hacf.size, -1)))
    hacf = all_hacf[0]
    gacf = all_gacf[0]
    prot = all_prots[0]
    # Selecting only values with positive G_ACF
    mask = all_gacf>0
    all_prots = all_prots[mask]
    all_hacf = all_hacf[mask]
    all_gacf = all_gacf[mask]
    
    if pcutoff is not None :
      if prot > pcutoff :
        prot, hacf, gacf = -1, -1, -1
      all_hacf = all_hacf[all_prots<pcutoff]
      all_gacf = all_gacf[all_prots<pcutoff]
      all_prots = all_prots[all_prots<pcutoff]
    if pthresh is not None :
      if prot < pthresh :
        prot, hacf, gacf = -1, -1, -1
      all_hacf = all_hacf[all_prots>pthresh]
      all_gacf = all_gacf[all_prots>pthresh]
      all_prots = all_prots[all_prots>pthresh]
    return (prot, hacf, gacf, index_prot, 
           all_prots, all_hacf, all_gacf)
  else :
    return -1, -1, -1, -1, np.array ([-1]), np.array([-1]), np.array ([-1])

if __name__=='__main__' :

  y1 = np.zeros (6)
  y2 = np.zeros (6)
  y1[0] = 1
  y2[3] = 1
  ccorr = cross_correlation (y1, y2, 3)
  assert ccorr==1
  ccorr = cross_correlation (y1, y2, 2)
  assert ccorr==0
  lags = np.array ([1, 2, 3])
  ccf = compute_ccf (y1, y2, lags) 
  print (ccf)
