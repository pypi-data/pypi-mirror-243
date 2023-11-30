import apollinaire as apn
import numpy as np
import matplotlib.pyplot as plt
import star_privateer as sp

'''
Background analysis for MSAP4-01.

A three-Harvey-law model is applied on
the PSD.

All this functions requires frequency in
muHz and PSD in ppm**2/muHz.
'''

def compute_guess (freq, psd, r=1, m=1, teff=5770,
                   dnu=None, numax=None) :
  '''
  Create guess for the 3-Harvey law model.  
  '''
  # Create the apollinaire standard 2-Harvey law guess
  guess, low_bounds, up_bounds = apn.peakbagging.create_background_guess_arrays(freq, psd, r=r, m=m, teff=teff, 
                                                                           dnu=dnu, numax=numax, n_harvey=2) 
  # Add guess parameters for the third Harvey law.
  res = np.median (np.diff (freq))
  # setting the cut arbitrarily at 80 muHz for now
  nu_c = 5 
  nbin = 30
  A = np.mean (psd[(freq>nu_c-nbin*res)&(freq<nu_c+nbin*res)])
  param = np.array ([A, nu_c, 4])
  low, up = (np.array([0.1*param[0], 0.1, 3]),
             np.array([10*param[0], 30, 5]))
  guess = np.concatenate ((param, guess))
  low_bounds = np.concatenate ((low, low_bounds))
  up_bounds = np.concatenate ((up, up_bounds))

  return guess, low_bounds, up_bounds

def remove_harmonics (freq, psd, nurot, width=1, n_harmonics=5) :
    '''
    Remove PSD regions close to rotation harmonics.

    Parameters
    ----------
    freq : ndarray
      frequency array 

    psd : ndarray
      psd array

    prot : float
      rotation period, in days

    width : float, optional
      frequency width around which datapoints will be removed, by default 1e-6

    n_harmonics : int 
      number of harmonic to consider 
     
    Returns
    -------
    tuple of array
      frequency and PSD array without datapoints close to harmonics
    '''

    for ii in range (1, n_harmonics+1) :
        psd = psd[(freq<ii*nurot-width)|(freq>ii*nurot+width)]
        freq = freq[(freq<ii*nurot-width)|(freq>ii*nurot+width)]

    return freq, psd

def normalise_amplitude (freq, param) :
  '''
  Renormalise an amplitude parameter in power
  spectral density into its equivalent ppm-amplitude.
  '''
  res = np.median (np.abs (np.diff (freq)))
  param = np.sqrt (2 * param / res)
  return param

def fit_background_model (freq, psd, quickfit=False, 
                          remove_rotation_harmonics=False,
                          r=1, m=1, teff=5770, dnu=None,
                          numax=None, nwalkers=64, nsteps=1000,
                          discard=200, parallelise=True, progress=True,
                          filename=None, filemcmc=None,
                          num=5000, num_numax=500) :
  '''
  Perform the MSAP4-01 background analysis.
  '''
  guess, low_bounds, up_bounds = compute_guess (freq, psd, r=r, m=m, teff=teff,
                                                dnu=dnu, numax=numax)


  if remove_rotation_harmonics :
    nurot = freq[np.argmax (psd)]
    freq, psd = remove_harmonics (freq, psd, nurot)
 
  back, param, sigma = apn.peakbagging.explore_distribution_background(freq, psd, n_harvey=3, guess=guess, 
               frozen_harvey_exponent=False, low_cut=0.1, fit_log=False, 
               low_bounds=low_bounds, up_bounds=up_bounds, spectro=False, 
               show=True, show_guess=True, show_corner=True, nsteps=nsteps, 
               discard=discard, filename=filename, parallelise=parallelise, progress=progress, nwalkers=nwalkers, 
               filemcmc=filemcmc, thin=1, quickfit=quickfit, num=num, num_numax=num_numax, 
               reboxing_behaviour='advanced_reboxing', format_cornerplot='png', 
               apodisation=False, bins=20, existing_chains='read')

  return param, sigma


