import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import importlib.resources
import h5py
from .correlation import *
from .wavelets import *
from .lomb_scargle import *
from scipy.interpolate import interp1d
from astropy.timeseries import LombScargle
import star_privateer as sp

'''
Function to compute the composite spectrum (CS)
and run the complete rotation pipeline
with WPS, ACF and CS.

This collection of functions combine the ability
if MSAP4-01 and MSAP4-02 to get the rotation periods
estimate from a given time series. Combined with
the ROOSTER implementation, they constitute
MSAP4-03.
'''

def compute_cs (ps, acf, p_acf=None, p_ps=None,
                normalise=False, smooth_cs=False,
                smooth_ps=False, index_prot_acf=-1) :
  '''
  Compute CS from PS (from wavelets or Lomb-Scargle) 
  and ACF (sampled at same periods by default). By default,
  the CS is normalised with its maximal value.
  '''
  #Renormalising step
  ps = ps / np.amax (ps)
  if index_prot_acf!=-1 :
    acf = acf / acf[index_prot_acf]
  else :
    acf = acf / np.amax (acf)

  if smooth_ps :
    glob_max = p_ps[np.argmax (ps)]
    sizebox = int (glob_max / np.median (-np.diff (p_ps)))
    ps = apply_smoothing (ps, sizebox)

  if p_acf is not None and p_ps is not None :
   fun = interp1d (p_ps, ps, fill_value=0, bounds_error=False)
   ps = fun (p_acf) 

  cs = ps * acf

  if smooth_cs :
    if p_acf is None :
      p_acf = np.arange (acf.size)
    glob_max = find_global_maximum (p_acf, cs)
    sizebox = int (glob_max / np.median (np.diff (p_acf)))
    cs = apply_smoothing (cs, sizebox)

  if normalise :
   cs /= np.amax (cs)

  return cs

def find_prot_cs (periods, cs) :
  '''
  Compute Prot from Lomb-Scargle periodogram
  as the maximum of the spectrum.

  Returns
  -------
    Tuple with ``prot`` and ``hcs``. 
  '''
  prot = periods[np.argmax (cs)]
  hcs = np.amax (cs)
  return prot, hcs

def plot_cs (periods, cs, ax=None, figsize=(8, 4),
             lw=1, filename=None, dpi=300, param_gauss=None,
             xlim=None) :
  '''
  Plot composite spectrum (CS).
  '''

  if ax is None :
    fig, ax = plt.subplots (1, 1, figsize=figsize)
  else :
    fig = None

  ax.plot (periods, cs, color='black', lw=lw)
  ax.set_xlabel ('Period (day)')
  ax.set_ylabel ('CS')

  if param_gauss is not None :
    n_gauss = param_gauss.shape[0]
    model = np.zeros (periods.size)
    for ii in range (n_gauss) :
      if param_gauss[ii,0]!=-1 :
        model += sp.gauss (periods, *param_gauss[ii,:])
    ax.plot (periods, model, color='darkorange', lw=2*lw)

  if xlim is not None :
    ax.set_xlim (xlim)

  if fig is not None :
    fig.tight_layout ()

  if filename is not None :
    plt.savefig (filename, dpi=dpi)
  
  return fig

def plot_analysis (t, s, periods, ps, acf, cs, 
                   periods_wps=None, wps=None, coi=None,
                   p_ps=None, figsize=(6, 12), filename=None, lw=1,
                   cmap='Blues', dpi=200, vmin=None, vmax=None,
                   normscale='log', param_gauss_cs=None,
                   param_profile_ps=None, xlim=None, show_kepler_quarters=False,
                   tref=0, ylogscale=False, show_light_curve=True, 
                   contourf_plot_wps=False, show_contour=False, levels=None,
                   ylim_wps=(0.1,100), shading='auto') :
   """
   Plot pipeline analysis results.

   Parameters
   ----------
   t : ndarray
       Time stamps of the time series.
   s : ndarray
       Times series
   periods :
       Periods vector for the auto-correlation function and the composite
       spectrum. 
   ps : ndarray
       Power spectrum (Lomb-Scargle or
       GWPS)
   acf : ndarray
       Auto-correlation function.
   cs : ndarray
       Composite spectrum
   periods_wps : ndarray
       Periods on which the WPS was computed.
   wps : ndarray
       Wavelet power spectrum. If provided, a color
       mesh plot using the WPS will be created. 
       Optional, default ``None``.
   coi : ndarray
       Cone of influence of the WPS
   p_ps : ndarray 
       Period vector of the Lomb-Scargle power spectrum. 
   figsize : tuple
       Figure size.
   lw : float
       Linewidth
   cmap : str or ``ColorMap`` object
       Colormap to use for the WPS.
   filename : str or ``Path``
       Path where to save the generated figure.
   dpi : int
       Dot-per-inch of the figure.
   normscale : str
       Colormap scaling: ``linear`` or ``log``.
   vmin : float
       Minimal value to consider for the colormap.
   vmax : float
       Maximal value to consider for the colormap.
   param_gauss_cs : array-like
       Parameters of the Gaussian profiles fitted 
       on the composite spectrum.
   param_profile_ps : array-like
       Parameters of the Gaussian profiles fitted
       on the power spectrum (Lomb-Scargle or
       WPS)
   xlim : tuple
       Bounds to consider for the panel having the 
       period shown on the x-axis.
   show_kepler_quarters : bool
       For Kepler light curves, whether to show or
       not the boundary of the quarters.
   tref : float
       Reference time for the Kepler quarters.
   ylogscale : bool
       Whether to use or not a logarithmic scale for
       the y-axis (period axis) of the WPS and GWPS panels.
   show_light_curve : bool
       If set to ``True``, the light curve will be shown
       using an additional panel.
   contourf_ploti_wps : bool
       If set to ``True``, a contour-filled plot will
       be produced for the WPS panel.
   show_contour : bool
       Whether to show or not contour of the WPS.
   levels : array-like
       Level on which draw the contour of the WPS
       on the figure.
   ylim_wps : tuple
       Limit of the y-axis of the WPS and GWPS panels.
   shading : str
       Shading to consider for the WPS.

   Returns
   -------
     The corresponding ``matplotlib.pyplot.Figure``.
   """
   if xlim is None :
     xlim = (0, 100)

   if wps is not None :
     gs_kw = dict(width_ratios=[3, 1])
     if show_light_curve :
       fig, axs = plt.subplots (4, 2, figsize=figsize, gridspec_kw=gs_kw)
       i_ps = 1
     else :
       fig, axs = plt.subplots (3, 2, figsize=figsize, gridspec_kw=gs_kw)
       i_ps = 0
     plot_wps (t, periods_wps, wps, ps, coi,
                cmap=cmap, shading=shading,
                color_coi='black', ylogscale=ylogscale, contourf_plot=contourf_plot_wps,
                ax1=axs[i_ps,0], ax2=axs[i_ps,1], lw=lw, param_gauss=param_profile_ps,
                normscale=normscale, vmin=vmin, vmax=vmax, show_contour=show_contour, 
                show_kepler_quarters=show_kepler_quarters, tref=tref, levels=levels,
                ylim=ylim_wps)
   else :
     gs_kw = dict(width_ratios=[3, 0])
     if show_light_curve :
       fig, axs = plt.subplots (4, 2, figsize=figsize, gridspec_kw=gs_kw)
       i_ps = 1
     else :
       fig, axs = plt.subplots (3, 2, figsize=figsize, gridspec_kw=gs_kw)
       i_ps = 0
     axs[i_ps,1].axis ('off')
     plot_ls (p_ps, ps, ax=axs[i_ps,0], lw=lw, param_profile=param_profile_ps,
              logscale=False)
     axs[i_ps,0].set_xlim (xlim)

   if show_light_curve :
     axs[0,0].plot (t, s, lw=lw, color='black')
     if show_kepler_quarters :
       start, _ = sp.get_kepler_quarters ()
       for elt in start :
         axs[0,0].axvline(elt - tref, 
                          color='grey', ls='--')
     axs[0,0].set_xlim (t[0], t[-1])
     axs[0,0].set_xlabel ('Time (day)')
     axs[0,0].set_ylabel ('Flux (ppm)')
     axs[0,1].axis ('off')
   plot_acf (periods, acf, ax=axs[i_ps+1,0], lw=lw)
   plot_cs (periods, cs, ax=axs[i_ps+2,0], lw=lw,  
            param_gauss=param_gauss_cs)
    
   axs[i_ps+1,1].axis ('off')
   axs[i_ps+2,1].axis ('off')

   axs[i_ps+1,0].set_xlim (xlim)
   axs[i_ps+2,0].set_xlim (xlim)

   fig.tight_layout ()

   if filename is not None :
     plt.savefig (filename, dpi=dpi)

   return fig

def compute_sph (t, s, prot, 
                 return_timeseries=False) :
  '''
  Compute photometric activity index
  of the light curve. See Mathur et al. (2014).

  Returns
  -------
  ndarray
    Sph computed according to the provided ``prot``
    value.
  '''
  if prot==-1 :
    return -1
  dt = np.median (np.diff (t))
  size_slice = int (5 * prot / dt)
  n_slice = s.size // size_slice
  if n_slice==0 :
    if return_timeseries :
      list_t = np.atleast_1d (np.mean (t))
      list_sph = np.atleast_1d (np.std (s))
      return np.std (s), list_t, list_sph
    else :
      return np.std (s)
  list_sph = []
  list_t = []
  for ii in range (n_slice) :
    list_sph.append (np.std (s[ii*size_slice:(ii+1)*size_slice]))
    list_t.append (np.mean (t[ii*size_slice:(ii+1)*size_slice]))
  # Only use the last slice if it is arbitrary large enough
  # compared to prot
  if (s.size - n_slice*size_slice)*dt > 2 * prot :
    list_sph.append (np.std (s[n_slice*size_slice:]))
    list_t.append (np.mean (t[n_slice*size_slice:]))
  list_sph = np.array (list_sph)
  list_t = np.array (list_t)
  sph = np.mean (list_sph)
  if return_timeseries :
    return sph, list_t, list_sph
  else :
    return sph

def compute_lomb_scargle_sph (t_sph, sph, method='slow') :
  '''
  Compute the Lomb-Scargle periodogram of the provided Sph
  time series.

  Returns
  -------
  tuple
    Tuple with the periods and the power vectors
  '''

  dt_sph = np.median (np.diff (t_sph)) 
  ps_object = LombScargle(t_sph*86400, sph, center_data=False, fit_mean=True)
  res = t_sph[-1] - t_sph[0]
  freq = np.linspace (0, 1/(dt_sph*86400*2), (t_sph.size+1)//2)
  freq = freq[freq!=0]
  ps_object.power_standard_norm = ps_object.power(freq, normalization='standard',
                                                  method=method, assume_regular_frequency=True)
  ls = ps_object.power_standard_norm
  p_ps = 1 / (freq*86400)
  return p_ps, ls, ps_object

def create_feature_from_fitted_param (param, method='CS') :
  '''
  Create feature array from fitted param 
  obtained with the different methods. The function
  expect the three first parameters for each fitted
  profile to be, in this order, amplitude, central period
  (or frequency) and fwhm.
  '''
  param = param[:,:3]
  features =  np.ravel (param)
  n = param.shape[0]
  feature_names = []
  for ii in range (n) :
    feature_names.append ('{}_{}_1'.format (method, ii)) 
    feature_names.append ('{}_{}_2'.format (method, ii)) 
    feature_names.append ('{}_{}_3'.format (method, ii)) 

  feature_names = np.array (feature_names)

  return features, feature_names

def analysis_pipeline (t, s, periods_in=None, 
                       wavelet_analysis=True, plot=True,  
                       filename=None, figsize=(6,12), show_light_curve=True,
                       cmap='jet', normscale='log', ylogscale=False,
                       vmin=None, vmax=None, lw=1, mother=None, xlim=None,
                       dpi=200, smooth_acf=True, 
                       cutoff_global=None, cutoff_filter_acf=None, 
                       fit_lomb_scargle=True, show_kepler_quarters=False, tref=0,
                       add_profile_parameters_to_features=False,
                       smooth_period=True, contourf_plot_wps=False, 
                       show_contour_wps=False, levels_wps=None,
                       mode_wps=None, ylim_wps=(0.1, 100), 
                       shading='auto', n_profile=5, threshold=0.1) : 
   '''
   Analysis pipeline combining Lomb-Scargle (or wavelet analysis), ACF and CS.

   The pipeline compute Lomb-Scargle periodogram (or Wavelet Power Spectrum and Global 
   Wavelet Power Spectrum), Auto-Correlation function, and Composite spectrum of 
   the provided light curves, as well as a set of relevant features for each method
   of analysis.  

   Parameters
   ----------
   t : ndarray
     timestamps 

   s : ndarray
     timeseries

   period_in : ndarray
     value which will be used as input to compute
     the ACF lags. A ``periods`` vector corresponding
     to the exact position of the lags will be returned
     by the function.  
     If ``None``, a ``lags`` vector (and corresponding period
     vector) from ``0`` to ``s.size`` will be generated.
     Optional, default ``None``. 

   wavelet_analysis : bool
     if set to ``True`` the timeseries will be analysed
     with a wavelet analysis. Otherwise the Lomb-Scargle
     periodogram will be computed and used to compute
     the composite spectrum

   plot : bool
     if set to ``True`` a summary plot will be made.
     Optional, default ``None``. 

   filename : str
     the ``filename`` under which the summary plot will
     be saved. Optional, default ``None``.

   figsize : tuple 
     Figure size for the summary plot. Optional, default
     ``(10, 16)``.

   mother : object
     mother wavelet to consider. Optional, if set
     to ``None``, ``pycwt.Morlet (6)`` will be used.

   cutoff_global : float
     Cutoff for the high pass filter to apply on time series
     before making any computation, in days. Optional, default `None`, 
     in this case no filtering is applied.

   cutoff_filter_acf : float
     Cutoff for the high pass filter to apply on time series
     before computing ACF, in days. Optional, default `None`, 
     in this case no filtering is applied.

   fit_lomb_scargle : bool
     if set to ``True``, the rotation peaks in the 
     Lomb-Scargle periodograms will be fitted using
     a Lorentzian profile.

   show_kepler_quarters : bool 
     start time of Kepler quarters will be shown on 
     the light curves and WPS (if ``wavelet_analysis`` is ``True``)

   tref : float
     reference time to use for the start of the series 
     when showing Kepler quarters.

   add_profile_parameters_to_features : bool
     if set to ``True``, the parameters of the fitted profiles
     for the PS and CS will be included in ``features``.
     The corresponding ``feature_names`` are named
     with the following pattern: ``CS_i_j`` or ``PS_i_j``,
     with ``i`` is an integer greater or equal to zero denoting
     the profile index.  
     with ``j=1`` for the amplitude parameter of the profile
     ``j=2`` for the central period (CS) or frequency (PS)
     and ``j=3`` for the fwhm parameter of the profile.

   mode_wps : string
     alternative ways to compute and filter the WPS.
     ``mm`` for a mathematical morphology filter trying to
     remove brief high frequency systematical noise.
     ``ssq`` to reassign the WPS according to the
     synchrosqueezing method (Daubechies et al. 2000).
     ``ssqmm`` for both methods combined.
     Default to ``None`` to use the standard wavelet approach.
     Will only use a Morlet wavelet with w=6 

   Returns
   -------
   tuple
     Tuple of arrays containing output ``periods``, ``gwps``, 
     ``wps``, ``acf``, ``cs``, ``coi``, ``features``, and ``feature_names``
     arrays if ``wavelet_analysis`` is set to ``True``, ``periods``, ``ps``, 
     ``acf``, ``cs``, ``features``, and ``feature_names``,
     otherwise.
   '''
   if cutoff_global is not None :
     s = sp.preprocess (t, s, cut=cutoff_global)
   dt = np.median (np.diff (t))
   p_acf, acf = compute_acf (s, dt, periods_in, normalise=True,
                             smooth=smooth_acf, smooth_period=smooth_period,
                             cutoff_filter_acf=cutoff_filter_acf)
   # In the future, it will be possible to use the
   # additional outputs of find_period_acf to make
   # features for ROOSTER.
   prot_acf, hacf, gacf, index_prot_acf, _, _, _ = find_period_acf (p_acf, acf)
   if wavelet_analysis :
     p_ps, wps, gwps, coi, scles = compute_wps (s, dt*86400, periods=None, 
                                                mother=mother, mode=mode_wps)
     ps = gwps
     prot_ps = find_prot_gwps (p_ps, gwps)
     # Setting to minus -1 parameters that are not computed
     # when using the wavelets
     h_ps, fa_prob_ps = -1, -1
     prot_ps, E_prot_ps, param_profile_ps = compute_prot_err_gaussian_fit (p_ps, gwps, verbose=False,
                                                                          n_profile=n_profile, 
                                                                          threshold=threshold)
     # Setting symmetric errors
     e_prot_ps = E_prot_ps
     
   else :
     p_ps, ps_object = compute_lomb_scargle (t, s)
     ps = ps_object.power_standard_norm
     prot_ps, e_prot_ps, E_prot_ps, fa_prob_ps, h_ps = find_prot_lomb_scargle (p_ps, 
                                                                ps_object, return_uncertainty=True)
     if fit_lomb_scargle :
       prot, e_prot_ps, E_prot_ps, param_profile_ps, list_h_ps = compute_prot_err_gaussian_fit_chi2_distribution (p_ps, ps,
                                                                                                n_profile=n_profile, 
                                                                                                threshold=threshold)
   cs = compute_cs (ps, acf, p_acf=p_acf, p_ps=p_ps, index_prot_acf=index_prot_acf) 
   prot_cs, hcs = find_prot_cs (p_acf, cs)
   prot_cs, E_prot_cs, param_gauss_cs = compute_prot_err_gaussian_fit (p_acf, cs, verbose=False,
                                                                       n_profile=n_profile, 
                                                                       threshold=threshold)

   # Compute sph for different methods
   sph_ps = compute_sph (t, s, prot_ps)
   sph_acf = compute_sph (t, s, prot_acf)
   sph_cs = compute_sph (t, s, prot_cs)

   if plot :
     if wavelet_analysis :
       fig = plot_analysis (t, s, p_acf, ps, acf, cs, periods_wps=p_ps, wps=wps, coi=coi,
                            figsize=figsize, cmap=cmap, lw=lw,
                            filename=filename, dpi=dpi, vmin=vmin, show_light_curve=show_light_curve,
                            vmax=vmax, normscale=normscale, xlim=xlim,
                            param_gauss_cs=param_gauss_cs, param_profile_ps=param_profile_ps,
                            contourf_plot_wps=contourf_plot_wps, show_contour=show_contour_wps, levels=levels_wps, 
                            show_kepler_quarters=show_kepler_quarters, tref=tref, 
                            ylogscale=ylogscale, ylim_wps=ylim_wps, shading=shading)
     else :
       fig = plot_analysis (t, s, p_acf, ps, acf, cs, p_ps=p_ps, 
                            figsize=figsize, cmap=cmap, lw=lw,
                            filename=filename, dpi=dpi,
                            param_gauss_cs=param_gauss_cs, xlim=xlim,
                            param_profile_ps=param_profile_ps,
                            show_light_curve=show_light_curve)
   else :
     fig = None

   features = np.array ([prot_ps, prot_acf, prot_cs,
                         e_prot_ps, E_prot_ps, 
                         -1, -1, 
                         E_prot_cs, E_prot_cs,
                         sph_ps, sph_acf, sph_cs, 
                         h_ps, fa_prob_ps, hacf, gacf, hcs])
   feature_names = np.array(['prot_ps', 'prot_acf', 'prot_cs',
                             'e_prot_ps', 'E_prot_ps', 
                             'e_prot_acf', 'E_prot_acf',
                             'e_prot_cs', 'E_prot_cs',
                             'sph_ps', 'sph_acf', 'sph_cs',
                             'h_ps', 'fa_prob_ps', 
                             'hacf', 'gacf', 'hcs'])
   if add_profile_parameters_to_features :
     feat_cs, name_cs = create_feature_from_fitted_param (param_gauss_cs, method='CS')
     feat_ps, name_ps = create_feature_from_fitted_param (param_profile_ps, method='PS')
     features = np.concatenate ((features, feat_ps, feat_cs))
     feature_names = np.concatenate ((feature_names, name_ps, name_cs))
   if wavelet_analysis :
     return p_acf, gwps, wps, acf, cs, coi, features, feature_names, fig
   else : 
     return p_ps, p_acf, ps, acf, cs, features, feature_names, fig

def save_features (filename, star_id, features, feature_names) :
  '''
  Save feature and corresponding names to 
  a dedicated csv file. 

  Returns
  -------
  The pandas DataFrame that has been saved as a
  csv file. 
  '''

  df = pd.DataFrame (index=[star_id], 
                     data=features.reshape ((1, -1)), 
                     columns=feature_names)
  df.to_csv (filename, index_label='target_id')
  return df

def build_catalog_features (dirFeatures) :
  '''
  Read the csv files stored in the provided
  ``dirFeatures`` directory to build a csv 
  catalog summarising the feature of all 
  targets. The procedure will fail if any of 
  the available csv file does not have the 
  correct feature format.
  '''
  list_csv = glob.glob (os.path.join (dirFeatures, '*.csv'))
  list_df = []
  for csv in list_csv :
    list_df.append (pd.read_csv (csv, index_col='target_id')) 
  df = pd.concat (list_df)
  df = df.sort_index ()

  return df

def compute_rossby (prot, teff, prot_sun=25.38, 
                    teff_sun=None) :
  '''
  Compute an estimate of the fluid Rossby number
  of the target according to the prescription from
  Noraz et al. 2022. 
  '''
  if teff_sun is None :
    filename = importlib.resources.path (sp.constants, 'constants.hdf5')
    with filename as f :
      with h5py.File(f, "r") as hf:
        teff_sun = hf["SI/solar/Teff"][()]
  ro = prot / prot_sun * (teff / teff_sun)**3.29
  if ro > 1.67 :
    flag =  1
  elif ro > 1.1 :
    flag = 2 
  elif ro > 0.25 :
    flag = 3
  elif ro > 0.167 :
    flag = 4
  else :
    flag = 5
  return ro, flag

def compute_delta_prot (prot, diffrot_candidates, low_err,
                        up_err, delta_min=1/3, delta_max=5/3, 
                        tol_harmonic=0.05, min_shear=0.01) :
  '''
  Analyse list of differential rotation period
  candidates.

  Only candidate values verifying 
  ``delta_min < candidate/prot < delta_max``
  are retained. First harmonic of prot are also filtered
  considering ``tol_harmonic``.
  '''
  cond = (diffrot_candidates!=prot) & (diffrot_candidates / prot > delta_min) & (diffrot_candidates / prot < delta_max)
  # Applying minimal shear condition
  cond = cond & ((diffrot_candidates / prot < 1 - min_shear)|(diffrot_candidates / prot > 1 + min_shear))
  # Removing harmonics
  cond = cond & ((diffrot_candidates<prot/(2+tol_harmonic))|(diffrot_candidates>prot/(2-tol_harmonic)))
  diffrot_validated = diffrot_candidates[cond]
  low_err = low_err[cond]
  up_err = up_err[cond]
  shear = np.abs (diffrot_validated-prot) / prot
  if diffrot_validated.size > 0 :  
    return diffrot_validated, low_err, up_err, shear
  else :
    return -1, -1, -1, -1

def build_long_term_modulation (idp_fourier, idp_acf,
                                idp_sph_fourier, idp_sph_acf,
                                h_acf_min=None, g_acf_min=None) :
  '''
  Build the long term modulation data product
  following the prescriptions from the MSAP4-06
  documentation.
  '''
  dp = []
  for elt in idp_fourier : 
    cond = (idp_acf[:,0]>elt[0]-3*elt[1])&(idp_acf[:,0]<elt[0]+3*elt[2])
    if h_acf_min is not None :
      cond = cond&(idp_acf[:,3]>h_acf_min)
    if g_acf_min is not None :
      cond = cond&(idp_acf[:,4]>g_acf_min)
    if idp_acf[cond].size > 0 :
      aux = idp_acf[cond,:]
      ii = np.argmin (np.abs (aux[:,0]-elt[0]))
      v_acf, e_acf, E_acf = aux[ii,0], aux[ii,1], aux[ii,2] 

      cond = (idp_sph_fourier[:,0]>elt[0]-3*elt[1])&(idp_sph_fourier[:,0]<elt[0]+3*elt[2])
      if idp_sph_fourier[cond].size > 0 :
        aux = idp_sph_fourier[cond,:]
        ii = np.argmin (np.abs (aux[:,0]-elt[0]))
        v_sph_fourier, e_sph_fourier, E_sph_fourier = aux[ii,0], aux[ii,1], aux[ii,2] 
      else :
        v_sph_fourier, e_sph_fourier, E_sph_fourier = -1, -1, -1 

      cond = (idp_sph_acf[:,0]>elt[0]-3*elt[1])&(idp_sph_acf[:,0]<elt[0]+3*elt[2])
      if idp_sph_acf[cond].size > 0 :
        aux = idp_sph_acf[cond,:]
        ii = np.argmin (np.abs (aux[:,0]-elt[0]))
        v_sph_acf, e_sph_acf, E_sph_acf = aux[ii,0], aux[ii,1], aux[ii,2] 
      else :
        v_sph_acf, e_sph_acf, E_sph_acf = -1, -1, -1 
      dp.append ([elt[0], elt[1], elt[2], v_acf, e_acf, E_acf,
                  v_sph_fourier, e_sph_fourier, E_sph_fourier,
                  v_sph_acf, e_sph_acf, E_sph_acf])

  dp = np.array (dp)
  if dp.size==0 :
    dp = np.full ((1,12), -1)
  return dp
