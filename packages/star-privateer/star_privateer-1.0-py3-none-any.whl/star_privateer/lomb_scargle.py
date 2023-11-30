import pickle, os
import numpy as np
from astropy.timeseries import LombScargle
from scipy.integrate import simps
import matplotlib.pyplot as plt
import star_privateer as sp
from scipy.optimize import minimize
import warnings

'''
Lomb-Scargle periodogram functions.

This collection of functions are dedicated
to achieve the task of the PLATO module
MSAP4-01.
'''

class powerspectrum():
    """ 
    Asteroseismology wrapper for Astropy Lomb-Scargle

    Uses the Astropy.LombScargle class to compute the power spectrum of a given
    time series. A variety of choices for computing the spectrum are available.
    The recommended methods are either `fast' or `Cython'.

    The variable list includes Parameters which are input parameters and
    Attributes, which are class attributes set when the class instance is
    either initalized or called.

    Notes
    -----
    The Cython implementation is very slow for time series longer than about
    1 month (array size of ~1e5). The Fast implementation is similar to a
    FFT, but at a very slight loss of accuracy.

    The adjustments to the frequency resolution, due to gaps, performed in the
    KASOC filter may not be beneficial the statistics we use in the detection
    algorithm.  This has not been thoroughly tested yet though. So recommend
    leaving it in, but with a switch to turn it off for testing.

    Parameters
    ----------
    time : array
        Time stamps of the time series.
    flux : array
        Flux values of the time series.
    flux_error : array
        Flux value errors of the time series.
    fit_mean : bool, optional
        Keyword for Astropy.LombScargle. If True, uses the generalized
        Lomb-Scargle approach and fits with a floating mean. Default is False.
    timeConversion : float
        Factor to convert the time series such that it is in seconds. Note, all
        stored time values, e.g. cadence or duration, are kept in the input
        units. Default is 86400 to convert from days to seconds.

    Attributes
    ----------
    dt : float
        Cadence of the time series.
    dT : float
        Total length of the time series.
    NT : int
        Number of data points in the time series.
    dutyCycle : float
        Duty cycle of the time series.
    nyquist : float
        Nyquist frequency in Hz.
    df : float
        Fundamental frequency spacing in Hz.
    ls : astropy.timeseries.LombScargle object:
        Astropy Lomb-Scargle class instance used in computing the power
        spectrum.
    indx: array, bool
        Mask array for removing nan and/or -inf values from the time series.
    freqHz : array, float
        Frequency range in Hz.
    freq : array, float
        Freqeuency range in muHz.
    normfactor : float
        Normalization factor to ensure the power conforms with Parseval.
    power : array, float
        Power spectrum of the time series in ppm^2.
    powerdensity : array float
        Power density spectrum of the time series in ppm^2/muHz
    amplitude : array, float
        Amplitude spectrum of the time series in ppm.
    """

    def __init__(self, time, flux, flux_err=None, fit_mean=False, timeConversion=86400):


        self.time = time

        self.flux = flux

        self.flux_err = flux_err

        self.fit_mean = fit_mean

        self.timeConversion = timeConversion

        self._getBadIndex()

        self.dt = self._getSampling()

        self.dT = self.time[-1]-self.time[0]

        self.NT = len(self.time)

        self.dutyCycle = self._getDutyCycle()


        if flux_err is None:
            #self.indx = np.invert(np.isnan(time) | np.isnan(flux) | np.isinf(time) | np.isinf(flux))

            # Init Astropy LS class without weights
            self.ls = LombScargle(self.time[self.indx]*self.timeConversion,
                                  self.flux[self.indx],
                                  center_data=True,
                                  fit_mean=self.fit_mean)

        else:
            #self.indx = np.invert(np.isnan(time) | np.isnan(flux) | np.isnan(flux_err) | np.isinf(time) | np.isinf(flux) | np.isinf(flux_err))

            # Init Astropy LS class with weights
            self.ls = LombScargle(self.time[self.indx]*self.timeConversion,
                                  self.flux[self.indx],
                                  dy=self.flux_err[self.indx],
                                  center_data=True,
                                  fit_mean=self.fit_mean)

        self.Nyquist = 1/(2*self.timeConversion*self.dt) # Hz

        self.df = self._fundamental_spacing_integral()


    def __call__(self, oversampling=1, nyquist_factor=1.1, method='fast',
                 periods=None):
        """ 
       Compute power spectrum

        Computes the power spectrum and normalizes it to conform with Parseval's
        theorem. The output is available as the power in ppm^2, powerdensity in
        ppm^2/muHz and the amplitude spectrum in ppm.

        The frequency range is transformed to muHz as this is customarily used
        in asteroseismology of main sequence stars.

        Parameters
        ----------
        oversampling : int
            The number of times the frequency range should be oversampled. This
            equates to zero-padding when using the FFT.

        nyquist_factor : float
            Factor by which to extend the spectrum past the Nyquist frequency.
            The default is 10% greater than the true Nyquist frequency. We use
            this to get a better handle on the background level at high
            frequency.

        method : str
            The recommended methods are either `fast' or `Cython'. Cython is
            a bit more accurate, but significantly slower.

        periods : ndarray
            Input periods in days. Optional, default ``None``.
        """
        
        if periods is None :
          self.freqHz = np.arange(self.df/oversampling, nyquist_factor*self.Nyquist, self.df/oversampling, dtype='float64')
        else :
          freqHz = 1 / (86400*periods) 
          freqHz = np.sort (freqHz)
          self.freqHz = freqHz

        self.freq = self.freqHz*1e6 # muHz is usually used in seismology

        # Calculate power at frequencies using fast Lomb-Scargle periodiogram:
        power = self.ls.power(self.freqHz, normalization='psd', method=method, assume_regular_frequency=True)
        power_standard_norm = self.ls.power(self.freqHz, normalization='standard', 
                                            method=method, assume_regular_frequency=True)

        # Due to numerical errors, the "fast implementation" can return power < 0.
        # Replace with random exponential values instead of 0?
        power = np.clip(power, 0, None)

        self._getNorm(power)

        self.power_standard_norm = power_standard_norm

        self.power = power * self.normfactor * 2

        self.powerdensity = power * self.normfactor / (self.df * 1e6)

        self.amplitude = power * np.sqrt(power * self.normfactor * 2)

    def _getBadIndex(self):
        """ Identify indices with nan/inf values

        Flags array indices where either the timestamps, flux values, or flux errors
        are nan or inf.

        """

        if self.flux_err is not None:
            self.indx = np.invert(np.isnan(self.time) | np.isnan(self.flux) | np.isnan(self.flux_err) | np.isinf(self.time) | np.isinf(self.flux) | np.isinf(self.flux_err))
        else:
            self.indx = np.invert(np.isnan(self.time) | np.isnan(self.flux) | np.isinf(self.time) | np.isinf(self.flux))

    def getTSWindowFunction(self, tmin=None, tmax=None, cadenceMargin=1.01):

        if tmin is None:
            tmin = min(self.time)
        if tmax is None:
            tmax = max(self.time)

        t = self.time.copy()[self.indx]

        w = np.ones_like(t)

        break_counter = 0
        epsilon = 0.0001 # this is a tiny scaling of dt to avoid numerical issues

        while any(np.diff(t) > cadenceMargin*self.dt):

            idx = np.where(np.diff(t)>cadenceMargin*self.dt)[0][0]

            t_gap_fill = np.arange(t[idx], t[idx+1]-epsilon*self.dt, self.dt)

            w_gap_fill = np.zeros(len(t_gap_fill))
            w_gap_fill[0] = 1

            t = np.concatenate((t[:idx], t_gap_fill, t[idx+1:]))

            w = np.concatenate((w[:idx], w_gap_fill, w[idx+1:]))

            break_counter +=1
            if break_counter == 100:
                break


        if (tmin is not None) and (tmin < t[0]):
            padLow = np.arange(tmin, t[0], self.dt)
            t = np.append(padLow, t)
            w = np.append(np.zeros_like(padLow), w)

        if (tmax is not None) and (t[0] < tmax):
            padHi = np.arange(t[-1], tmax, self.dt)
            t = np.append(t, padHi)
            w = np.append(w, np.zeros_like(padHi))

        return t, w


    def _getDutyCycle(self, cadence=None):
        """ Compute the duty cycle

        If cadence is not provided, it is assumed to be the median difference
        of the time stamps in the time series.

        Parameters
        ----------
        cadence : float
            Nominal cadence of the time series. Units should be the
            same as t.

        Returns
        -------
        dutyCycle : float
            Duty cycle of the time series
        """

        if cadence is None:
            cadence = self._getSampling()

        nomLen = np.ceil((np.nanmax(self.time) - np.nanmin(self.time)) / cadence)

        idx = np.invert(np.isnan(self.time) | np.isinf(self.time))

        dutyCycle = len(self.time[idx]) / nomLen

        return dutyCycle

    def _getSampling(self):
        """ Compute sampling rate

        Computes the average sampling rate in the time series.

        This should approximate the nominal sampling rate,
        even with gaps in the time series.

        Returns
        ----------
        dt : float
            Cadence of the time stamps.
        """
        idx = np.invert(np.isnan(self.time) | np.isinf(self.time))

        dt = np.median(np.diff(self.time[idx]))

        return dt

    def _getNorm(self, power):
        """ Parseval normalization

        Computes the normalization factor for the power spectrum such that it
        conforms with Parseval's theorem.

        power : array
            Unnormalized array of power.
        """

        N = len(self.ls.t)

        if self.ls.dy is None:
            tot_MS = np.sum((self.ls.y - np.nanmean(self.ls.y))**2)/N
        else:
            tot_MS = np.sum(((self.ls.y - np.nanmean(self.ls.y))/self.ls.dy)**2)/np.sum((1/self.ls.dy)**2)

        self.normfactor = tot_MS/np.sum(power)

    def _fundamental_spacing_integral(self):
        """ Estimate fundamental frequency bin spacing

        Computes the frequency bin spacing using the integral of the spectral
        window function.

        For uniformly sampled data this is given by df=1/T. Which under ideal
        circumstances ensures that power in neighbouring frequency bins is
        independent. However, this fails when there are gaps in the time series.
        The integral of the spectral window function is a better approximation
        for ensuring the bins are less correlated.

        """

        # The nominal frequency resolution
        df = 1/(self.timeConversion*(np.nanmax(self.time[self.indx]) - np.nanmin(self.time[self.indx]))) # Hz

        # Compute the window function
        freq, window = self.windowfunction(df, width=None, oversampling=5) # oversampling for integral accuracy

        # Integrate the windowfunction to get the corrected frequency resolution
        df = simps(window, freq)

        return df*1e-6

    def windowfunction(self, df, width=None, oversampling=10):
        """ Spectral window function.

        Parameters
        ----------
		 width : float, optional
            The width in Hz on either side of zero to calculate spectral window.
            Default is None.
        oversampling : float, optional
            Oversampling factor. Default is 10.
        """

        freq_cen = 0.5*self.Nyquist
        if width is None:
            width = np.minimum (100*df, freq_cen)
        Nfreq = int(oversampling*width/df)
        freq = freq_cen + (df/oversampling) * np.arange(-Nfreq, Nfreq, 1)
        x = 0.5*np.sin(2*np.pi*freq_cen*self.ls.t) + 0.5*np.cos(2*np.pi*freq_cen*self.ls.t)
        # Calculate power spectrum for the given frequency range:
        ls = LombScargle(self.ls.t, x, center_data=True, fit_mean=self.fit_mean)
        power = ls.power(freq, method='fast', normalization='psd', assume_regular_frequency=True)
        power /= power[int(len(power)/2)] # Normalize to have maximum of one
        freq -= freq_cen
        freq *= 1e6

        return freq, power


def squish(time, dt, gapSize=27):
    """ Remove gaps

    Adjusts timestamps to remove gaps of a given size. Large gaps influence
    the statistics we use for the detection quite strongly.

    Parameters
    ----------
    gapSize : float
        Size of the gaps to consider, in units of the timestamps. Gaps
        larger than this will be removed. Default is 27 days.

    Returns
    -------
    t : array
        Adjusted timestamps
    """

    tsquish = time.copy()

    for i in np.where(np.diff(tsquish) > gapSize)[0]:
        diff = tsquish[i] - tsquish[i+1]

        tsquish[i+1:] = tsquish[i+1:] + diff + dt

    return tsquish

def compute_lomb_scargle (t, s, periods=None, 
                          renormalise=False, 
                          normalisation='standard',
                          return_object=True) : 
  '''
  Compute Lomb Scargle for a given timeseries.
  Default normalisation follows the ``standard`` 
  normalisation described in ``astropy`` documentation.

  Returns
  -------
  tuple
    Tuple of array with periods (in days) and Lomb-Scargle
    power spectrum. Return the Lomb-Scargle object
    if ``return_object`` is set to ``True``.
  '''

  ps = powerspectrum (t, s, flux_err=None, fit_mean=False, timeConversion=86400)
  ps (periods=periods)
  periods = 1 / (86400 * ps.freqHz)
  if normalisation=='standard':
    ls = ps.power_standard_norm
  elif normalisation=='psd':
    ls = ps.powerdensity
  else :
    raise Exception ("Requested normalisation is not available.")
  if renormalise :
    ls = ls / np.amax (ls)

  if return_object :
    return periods, ps
  else :
    return periods, ls

def compute_uncertainty_smoothing (periods, power, filename=None) :
  '''
  Smooth the power spectrum (sampled in frequency) and estimate
  from this smoothing the width of the selected peak at period
  ``prot``. 

  Note
  ----
    Even if there are caveat to keep in mind, this method
    is computationnally efficient and not model dependent.
  '''
  index = np.argmax (power)
  prot = periods[index]
  freq = 1 / (periods*86400)
  f_rot = 1 / (prot*86400)
  res = np.abs (freq[2]-freq[1])
  sizebox = max (1, int (f_rot / res))
  smoothed = sp.apply_smoothing (power, sizebox, win_type='triang')
  hmax = smoothed[index]
  aux = periods[smoothed<hmax/2] 
  try :
    e_prot = aux[aux<prot][0]
  except IndexError :
    e_prot = prot
  try :
    E_prot = aux[aux>prot][-1]
  except IndexError :
    E_prot = prot

  if filename is not None :
    fig, ax = plt.subplots (1, 1)
    ax.plot (periods, power, color='grey')
    ax.plot (periods, smoothed, color='black')
    ax.axvline (e_prot, lw=2, color='darkorange')
    ax.axvline (E_prot, lw=2, color='darkorange')
    ax.set_xlabel ('Periods (day)')
    ax.set_ylabel ('Power')
    ax.set_yscale ('log')
    ax.set_xlim (e_prot-prot, E_prot+prot)
    plt.savefig (filename, dpi=300)
    plt.close ()

  e_prot = prot - e_prot
  E_prot = E_prot - prot

  return prot, e_prot, E_prot

def find_prot_lomb_scargle (periods, ps_object,
                            method='naive',  
                            return_uncertainty=False) :
  '''
  Compute Prot from Lomb-Scargle periodogram
  as the maximum of the spectrum. Corresponding
  false alarm probability (see e.g. Scargle 1982)
  is also computed.

  Returns
  -------
    Rotation period and false alarm probability.
  '''
  prot, e_prot, E_prot = compute_uncertainty_smoothing (periods, 
                                                        ps_object.power_standard_norm)
  h_ps = ps_object.power_standard_norm.max()
  fa_prob = ps_object.ls.false_alarm_probability(h_ps,
                                                 method=method)  
  if return_uncertainty :
    return prot, e_prot, E_prot, fa_prob, h_ps
  else :
    return prot, fa_prob, h_ps


def plot_ls (periods, ls, ax=None, lw=1,
             filename=None, dpi=300,
             xlim=None, ylim=None, logscale=False,
             param_profile=None, figsize=(8,4)) :
  '''
  Plot Lomb-Scargle periodogram.
  '''

  if ax is None :
    fig, ax = plt.subplots (1, 1, figsize=figsize)
  else :
    fig = None

  ax.plot (periods, ls, color='black') 
  ax.set_xlabel ('Period (day)')
  ax.set_ylabel ('Power')
  if xlim is not None :
    ax.set_xlim (xlim)
  if ylim is not None :
    ax.set_ylim (ylim)
  if logscale :
    ax.set_xscale ('log')
    ax.set_yscale ('log')

  if param_profile is not None and param_profile.size>0:
    param_profile = np.atleast_2d (param_profile)
    # Removing cells corresponding to unfitted profiles
    n_profile = param_profile.shape[0]
    model = np.zeros (periods.size)
    prot = 1e6 / (param_profile[0,1]*86400)
    cond = (periods>max(0.1, 0.1*prot))&(periods<3*prot)
    model = model[cond] 
    x = 1e6 / (periods[cond]*86400)
    for ii in range (n_profile) :
      model += compute_model (param_profile[ii,:], x, back=np.ones (x.size)) 
    ax.plot (periods[cond], model, color='darkorange', lw=2*lw)

  if fig is not None :
    fig.tight_layout ()

  if filename is not None :
    plt.savefig (filename, dpi=dpi)

  return fig

def compute_model (param, x, profile=0, back=None) :
  if back is None :
    trend = - param[3]*x + param[4]
    back = np.ones (x.size) 
  else :
    trend = 0
  if profile==0 :
    model = sp.gauss (x, param[0], param[1], param[2])*back + trend
  elif profile==1 :
    model = sp.lor (x, param[0], param[1], param[2])*back  + trend
  else :
    raise Exception ("Unknown profile.")
  return model

def log_likelihood (param, x, ps, back=None) :
  '''
  The model is a Gaussian or Lorentzian profile summed 
  with an affine law to take the background into
  account if ``back`` is ``None``, otherwise the background
  is removed. 
  '''
  with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    model = compute_model (np.exp (param), x, back=back)
    log_l = ps / model + np.log (model)
    log_l = np.sum (log_l)
  return log_l

def fit_gaussian_lomb_scargle (x, ps, x_init, back=None,
                               mask=None) :
  '''
  Perform a least-square fit with a Gaussian profile.
  '''
  if mask is not None :
    x_fit, ps = x[mask], ps[mask]
  else :
    x_fit = x
  if back is None :
    a = np.amax (ps) 
    beta = np.median (ps) 
    param0 = np.array ([a,
                       x_init,
                       0.1*x_init, 
                       1e-12, 
                       beta])
    
    bounds = [(0.1*a, 2*a),
              (.99*x_init, 1.01*x_init),
              (0.01*x_init, 2*x_init),
              (1e-15, 1),
              (1e-15, 1)]
  else :
    a = np.amax (ps / back) 
    param0 = np.array ([a,
                       x_init,
                       0.1*x_init])
    
    bounds = [(0.1*a, 2*a),
              (.5*x_init, 2*x_init),
              (0.01*x_init, 2*x_init)]
  result = minimize (log_likelihood, np.log (param0),
                     args=(x_fit, ps, back), bounds=np.log (bounds))

  fitted = np.exp (result.x)
  model = compute_model (fitted, x, back=np.ones (x.size))
  return fitted, model, result.success, result.message


def compute_prot_err_gaussian_fit_chi2_distribution (periods, ps,
                                                     n_profile=5, threshold=0.1,
                                                     verbose=False, back=None,
                                                     plot_procedure=False) :
  '''
  Fit a series of gaussian profiles on a power 
  spectrum following a chi2 distribution and use it to extract 
  the rotation period estimate and corresponding error.
 
  Returns
  -------
  tuple
    The rotation period, its uncertainty and the parameters
    fitted for the ``n_profile`` profiles (in this order for
    each profile: amplitude, central frequency, width, a, b, with
    a and b the parameters for the affine background law).
  '''
  param = np.full ((n_profile,5), -1.)
  h_ps = np.zeros (n_profile)
  p_init = periods[np.argmax (ps)]
  cond = (periods>0.1)
  ps = ps[cond]
  aux_ps = np.copy (ps)
  periods = periods[cond]
  if back is not None :
    back = back[cond]
  x = 1e6 / (periods*86400)
  x_init = 1e6 / (p_init*86400)
  # Ensuring that even if fitting does not work
  # we will get a prot value.
  max_init = np.amax (ps)
  param[0,1], h_ps[0] = x_init, max_init
  ii = 0
  while ii < n_profile and np.amax (ps) > threshold*max_init :
    mask = (periods>0.5*p_init)&(periods<1.5*p_init)
    fitted_param, model, success, message = fit_gaussian_lomb_scargle (x, ps, x_init,
                                                                       back=back, mask=mask)
    if verbose :
      print ('Fitted profile {}, param obtained:{}, success: {}'.format (ii, fitted_param, success))
    if not success :
      if verbose :
        print (message)
      break
    h_ps[ii] = aux_ps[np.argmax (ps)]
    if plot_procedure :
      plot_ls (periods, ps, param_profile=fitted_param)
    ps = ps - model
    ps[ps<0] = 1e-6 
    p_init = periods[np.argmax (ps)]
    x_init = 1e6/(p_init*86400)
    param[ii,:] = fitted_param
    ii += 1

  h_ps = h_ps[param[:,0]!=-1]
  param = param[param[:,0]!=-1,:]
  if param.size > 0 :
    prot = 1e6/(param[0,1]*86400)
    e_p = prot - 1e6/((param[0,1] + param[0,2])*86400)
    E_p = 1e6/((param[0,1] - param[0,2])*86400) - prot
  else :
    prot, e_p, E_p = p_init, -1, -1
  return prot, e_p, E_p, param, h_ps

def false_alarm_zk_2009 (h_ps, ls_size) :
  """
  False alarm probability as expressed by Eq. 24 of Zechmeister & Kurster
  2009, considering a Lomb-Scargle periodogram normalised according to
  their Eq. 4. 
  """
  proba_p_p0 = (1 - h_ps)**((ls_size*2-3)/2)
  proba_fa = 1 - (1 - proba_p_p0)**ls_size
  return proba_fa

def prepare_idp_fourier (param, h_ps, ls_size, 
                         ps_object=None,
                         pcutoff=None, pthresh=None,
                         fapcutoff=None, 
                         clean_residual=True,
                         cleaning=0.02) :
  '''
  Take as input the result of the peak fitting to
  compute false alarm probability and return and
  array formatted to be written as one of the
  requested intermediate data product. 
  '''
  if param.size==0 :
    return np.full ((1,5), -1)
  param = np.atleast_2d (param)
  idp = np.zeros ((param.shape[0], 5))
  p = 1e6/(param[:,1]*86400)
  e_p = p - 1e6/((param[:,1] + param[:,2])*86400)
  E_p = 1e6/((param[:,1] - param[:,2])*86400) - p
  if ps_object is not None :
    try :
      fa_prob = ps_object.ls.false_alarm_probability(h_ps,
                                                   method='baluev')
    except AttributeError :
      fa_prob = ps_object.false_alarm_probability(h_ps,
                                                  method='baluev')
  else :
    fa_prob = false_alarm_zk_2009 (h_ps, ls_size)
  
  fa_prob[fa_prob<1e-16] = 1e-16
  idp[:,0] = p
  idp[:,1] = e_p
  idp[:,2] = E_p
  idp[:,3] = h_ps
  idp[:,4] = fa_prob

  if pcutoff is not None :
    idp = idp[idp[:,0]<pcutoff,:]    
  if pthresh is not None :
    idp = idp[idp[:,0]>pthresh,:]    
  if fapcutoff is not None :
    idp = idp[idp[:,4]<fapcutoff,:]    

  indexes = np.argsort (idp[:,3])
  idp = idp[indexes,:]
  idp = np.flip (idp, axis=0)

  if clean_residual :
    # Clean prot that are too close
    ii = 0
    low, up = 1-cleaning, 1+cleaning
    while ii < idp.shape[0] :
      mask = (idp[:,0]<low*idp[ii,0])|(idp[:,0]>up*idp[ii,0])
      mask[ii] = True
      idp = idp[mask,:]
      ii += 1
   
  return idp

def series_to_psd (series, dt, correct_dc=True,
                   return_periods=False, 
                   periods_in_day=True) :

  """
  Take a regularly sampled timeseries and compute 
  its PSD through a FFT.

  This snippet of code can be used as an alternative
  for the Lomb-Scargle object provided above in this file.
  """
  freq = np.fft.rfftfreq (series.size, d=dt)
  tf = np.fft.rfft (series) / (series.size / 2.)
  T = series.size * dt
  psd = np.abs (tf) * np.abs (tf) * T / 2.

  if correct_dc :
    dc = np.count_nonzero (series) / series.size
    psd = psd / dc

  if not return_periods :
    return freq, psd
  else :
    periods = 1/freq[freq!=0]
    psd = psd[freq!=0]
    if periods_in_day :
      periods /= 86400
    return periods, psd

