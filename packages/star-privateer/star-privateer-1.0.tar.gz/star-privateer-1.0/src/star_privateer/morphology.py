"""
Created on Thu Jun 15 11:26:27 2023

@author: emile carinos
"""
import star_privateer as sp
import numpy as np
import ssqueezepy as ssq 
import skimage
from scipy.signal import find_peaks_cwt

def get_coi(n0,dt): #coi for a Morlet(6) wavelet
    coi = (n0 / 2 - np.abs(np.arange(0, n0) - (n0 - 1) / 2))
    coi = (4 * np.pi) / (6 + np.sqrt(2 + 6 ** 2)) * (1/np.sqrt(2)) * dt * coi
    return coi

def find_mmkernel(wps,minw,maxw,step): #Identifies the typical size of systematic peaks in TESS data
    peaks = find_peaks_cwt(np.sum(wps,axis=0),widths=np.arange(minw,maxw,step))
    return np.ones((1,int(np.floor(np.nanmedian(np.diff(peaks))))),np.uint8)
    
def cwt_modes(f, dt=None, periods=None, mode=None): 
   """
   Compute Wavelet Power Spectrum and corresponding
   cone of influence for a Morlet(6) wavelet, based on
   ssqueezepy wavelet transform and synschrosqueezing
   reassignment. Depending on the mode, it can also 
   automatically filter out certain morphological details
   in the WPS using mathematical morphology.
   
   Paremeters
   ----------
   f : ndarray
     time series to analyse
     
   dt : float
     sampling of the time series (in s)
     
   periods : ndarray
     Periods on which to compute the WPS. 
     Optional, if not given, WPS will be computed for
     periods ranging from 2*dt to dt*len(f) in days. Must be
     given in days.
     
   mode : string
     Alternative ways to compute and filter the WPS.
     'mm' for a mathematical morphology filter trying to
     remove brief high frequency systematical noise.
     'ssq' to reassign the WPS according to the
     synchrosqueezing method (Daubechies et al. 2000).
     'ssqmm' for both methods combined.
     default None to use none of them
   
   Returns
   -------
   tuple
       Tuple with the selected WPS, 
       periods it was computed on 
       and corresponding COI
   
   """
   
   if periods is None: 
       #Setup period range if not provided, way bigger than actually needed
       periods = sp.compute_periods_wavelet (f, dt)

   widths = 6 * (1/np.amin (periods)) * periods / np.pi #morlet with w=6  
   ssqwt, cwt, ssq_freq, scales = ssq.ssq_cwt(x=f, wavelet=('morlet', 
                                              {'mu': 6,'dtype': 'float32'}), scales=widths)
   ssqwps = np.abs(ssqwt)**2 #synchrosqueezed power spectrum
   wps = np.abs(cwt)**2 #regular power spectrum
   coi = get_coi(len(f),dt)

   if mode is None:
       rwps=ssqwps
   if mode=='ssq':
       rwps=ssqwps
   else:
       # Define an appropriate structuring element, 
       # see https://clouard.users.greyc.fr/Pantheon/experiments/morphology/index-en 
       # for instance or Haralick et al. 1987
       #fine tuned parameters to search optimal kernel 
       # to filter out TESS systematics. Will most lilely not work at all for other data.
       low_bound = int(0.001 * len(f)) 
       high_bound = int(0.05 * len(f)) #
       step = (high_bound-low_bound)/10 #

       if mode=='mm':
           kernel = find_mmkernel(wps, low_bound, high_bound,step)
           tophatcwt = skimage.morphology.white_tophat(wps, kernel) 
           rwps = wps - tophatcwt

       if mode=='ssqmm':
           kernel = find_mmkernel(ssqwps, low_bound, high_bound,step)
           tophatssq = skimage.morphology.white_tophat(ssqwps, kernel) 
           rwps = ssqwps - tophatssq

   return rwps, periods, coi, scales
