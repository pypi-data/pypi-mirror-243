import star_privateer as sp
from astropy.io import fits
from scipy import signal
import importlib.resources
import numpy as np
import pandas as pd
import os

'''
Auxiliary functions for the module
'''

def closest_odd (a) :
  if a%2==1:
    return a
  else :
    return a-1

def gauss (x, a, mu, sigma) :
  return a * np.exp (- (x-mu)**2 / sigma**2)

def lor (x, a, mu, sigma) :
  return a / (1 + 4 * ((x-mu)**2 / sigma**2))

def rebin (a, nrebin=4) :
    """
    Rebin a vector according to ``nrebin`` factor.
    """
    if a.size%nrebin!= 0 :
        a = a[:-(a.size%nrebin)]
        a = np.mean (a.reshape (-1, nrebin), axis=1)
    return a

def apply_fir (t, s, cut=55, numtaps=10001,
               desired=None, bands=None) :
  '''
  Apply high-pass finite impulse response
  filter.

  Parameters
  ----------
  t : float or array-like
    Vector of time stamps (if array) or sampling time (if float).
  '''
  if type (t) in [float, np.float_, np.float64,
                      np.float32] :
    dt = t
  else :
    dt = np.median (np.diff (t))
  numtaps = np.minimum (closest_odd(s.size//3 - 1), numtaps) 
  fs = 1 / (dt*86400)  
  f_cut = 1 / (cut*86400)
  if bands is None :
    bands=[0, f_cut, f_cut]
  else :
    bands = bands.copy ()
  bands.append (fs/2) 
  if desired is None :
    desired=[0,0,1,1] 
  b = signal.firls (numtaps, bands, desired, fs=fs)
  s = signal.filtfilt (b, [1.0], s)
  return s

def preprocess (t, s, cut=55, numtaps=10001,
                bands=None, desired=None) :
  '''
  Preprocess a time series by substracting
  median and applying a FIR filter.

  Parameters
  ----------
  t : float or array-like
    Vector of time stamps (if array) or sampling time (if float).
  '''
  # Setting median to 0.
  s = s - np.mean (s)
  # The low-frequency trend need to be filtered out.
  # Applying a FIR.
  s = apply_fir (t, s, cut=cut, numtaps=numtaps,
                 bands=bands, desired=desired)
  # Setting median to 0.
  s = s - np.mean (s)
  return s

def load_k2_example () :
    '''
    Load K2 light curve example for MSAP4-01
    and MSAP4-02 demonstrators.
    '''
    filename = get_target_filename (sp.timeseries, 
                      'epic211015853', filetype='fits')
    with filename as f :
      hdul = fits.open (f)
      hdu = hdul[1]
      t = np.array (hdu.data['TIME'])
      s = np.array (hdu.data['PDCSAP_FLUX'])
      mask = ~(np.isnan (t) | np.isnan (s))
      t = t[mask]
      s = s[mask]
      dt = np.median (np.diff (t))
      hdul.close ()
    s = s - np.mean (s)
    s[np.isnan (s)] = 0
    return t, s, dt

def load_resource (filename) :
    '''
    Load data from a given light_curve.
    Assume that the fits file correspond to 
    KESPEISMIC product and the csv file to
    simulated data provided by Suzanne Aigrain.
    '''
    with filename as f :
      ext = os.path.splitext (f)[1] 
      if ext=='.fits' or ext=='.fit' :
            hdul = fits.open (f)
            hdu = hdul[0]
            data = np.array (hdu.data).astype (float)
            hdul.close ()
      elif ext=='.csv' :
            df = pd.read_csv (f)
            data= df[['time', 'fcor3']].to_numpy ()
      else :
        raise Exception ("Unkown filename extension.")
    t = data[:,0]
    s = data[:,1]
    if ext=='.csv' :
      s = s - np.mean (s)
      # Normalise the flux variation to ppm
      s = s*1e6
    dt = np.median (np.diff (t))
    return t, s, dt

def get_list_targets (dataset) :
  '''
  Get list of targets for a given dataset.
  '''
  with importlib.resources.path (dataset, 'list_target.dat') as f :
      list_targets = np.loadtxt (f, dtype=int)
  return list_targets

def get_target_filename (dataset, str_id, filetype='fits') :
  '''
  Get filename corresponding to a given target
  in the required ``dataset``.
  '''
  if filetype=='fits':
    filename = importlib.resources.path (dataset, '{}.{}'.format (str_id, filetype))
  elif filetype=='csv':
    filename = importlib.resources.path (dataset, 'plato_brightbinned{}_cor.{}'.format (str_id, filetype))
  else :
    raise Exception ("Unknown requested file extension.")
  return filename

def get_kepler_quarters () :
  '''
  Return a tuple with start and end date of the 
  Kepler quarters.
  '''
  start = np.array([54953.0, 54964.5, 55002.5, 55093.5, 
                    55185.3, 55276.4, 55372.4, 55463.1, 
                    55568.3, 55641.5, 55739.8, 55834.1,
                    55932.3, 56015.6, 56106.6, 56205.9,
                    56306,56391.71]) 
  end = np.array([54963.25, 54997.99, 55091.47, 55182.5, 
                  55275.3, 55371.2, 55462.3, 55552.55,
                  55635.35, 55738.93, 55833.27, 55931.34,
                  56015.031, 56106.1, 56203.8294, 56303.64,
                  56391,56423.5120])
  return start, end
