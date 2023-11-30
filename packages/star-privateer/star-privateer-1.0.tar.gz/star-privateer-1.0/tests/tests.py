import unittest
import warnings
import importlib.resources
import star_privateer as sp
from scipy.signal import correlate
from astropy.io import fits
import numpy as np
import os

'''
Unitary test framework
'''

#@unittest.skip
class TestAnalysisMethods (unittest.TestCase) :
 
  def setUp (self) :
    '''
    Load data for test and proceed for a first a2z check.
    '''
    if not os.path.exists ('test_outputs') :
      os.mkdir ('test_outputs')
    filename = "kic003733735_longcadence_kepseismic.fits"
    filename = importlib.resources.path (sp.timeseries, filename)
    with filename as f :
     hdul = fits.open (f)
     hdu = hdul[0]
     data = np.array (hdu.data).astype (float)
     hdul.close ()
     self.t = data[:,0]
     self.s = data[:,1]
     self.dt = np.median (np.diff (self.t))

  @unittest.skip
  def testLombScargle (self) :
    p_ps, ps_object = sp.compute_lomb_scargle (self.t, self.s, renormalise=True,
                                              periods=None)
    ls = ps_object.power_standard_norm
    prot, fa_prob, h_ps = sp.find_prot_lomb_scargle (p_ps, ps_object)
    prot, e_prot, E_prot = sp.compute_uncertainty_smoothing (p_ps, ls,
                                                          filename='test_outputs/smoothing_uncertainty.png')
    prot, e_prot, E_prot, fa_prob, h_ps = sp.find_prot_lomb_scargle (p_ps, ps_object, return_uncertainty=True)
    prot, e_p, E_p, param, list_h_ps = sp.compute_prot_err_gaussian_fit_chi2_distribution (p_ps, ls,
                                                                        n_profile=5, threshold=0.1,
                                                                        verbose=True)
    self.assertTrue (e_p>0)
    self.assertTrue (E_p>0)
    idp = sp.prepare_idp_fourier (param, list_h_ps,
                                     ls.size, ps_object=ps_object,
                                     pcutoff=None, pthresh=None,
                                     fapcutoff=None)
    sp.plot_ls (p_ps, ls, filename='test_outputs/lomb_scargle.png', param_profile=param, logscale=True)
    print ('Power level to have false alarm below 1e-1, 1e-3 and 1e-8:', ps_object.ls.false_alarm_level([0.1, 1e-3, 1e-8]))
    print ('Rotation period found with Lomb-Scargle for KIC3733735: {:.2f} (- {:.2f}, +{:.2f}) days'.format (prot, e_p, E_p))

  @unittest.skip
  def testCCF (self) :
    y1 = np.array ([0, 1, 3, 4])
    y2 = np.array ([1, 2, 0, 1])
    lags = np.arange (y1.size)
    ccf = sp.compute_ccf (y1, y2, lags)
    self.assertTrue (np.all (ccf==np.array ([6, 3, 1, 0])))

  #@unittest.skip
  def testACF (self) :
    p_in = np.linspace (0, 9, 10)
    p_out, acf_1 = sp.compute_acf (self.s, self.dt, p_in, normalise=True,
                                      use_scipy_correlate=False)
    p_out, acf_2 = sp.compute_acf (self.s, self.dt, p_in, normalise=True,
                                      use_scipy_correlate=True)
    self.assertTrue (np.all (np.abs (acf_1 - acf_2) < 1e-6))

  #@unittest.skip
  def testFindPeriodACF(self) :
    p_in = np.linspace (0, 100, 5000)
    p_acf, acf = sp.compute_acf (self.s, self.dt, p_in, normalise=True,
                                    use_scipy_correlate=True, smooth=False)
    _, acf_a1 = sp.compute_acf (self.s, self.dt, p_in, normalise=True,
                                    use_scipy_correlate=True, smooth=True)
    _, acf_a2 = sp.compute_acf (self.s, self.dt, p_in, normalise=True,
                                   use_scipy_correlate=True, smooth=True,
                                   win_type='triang')
    _, acf_a3 = sp.compute_acf (self.s, self.dt, p_in, normalise=True,
                                   use_scipy_correlate=True, smooth=True,
                                   smooth_period=30)
    (prot, hacf, gacf, 
     index_prot_acf, prots, hacfs, gacfs) = sp.find_period_acf (p_acf, acf)
    a_min, a_max = sp.find_local_extrema (acf)
    sph, t_sph, sph_series = sp.compute_sph (self.t, self.s, prot,
                                                return_timeseries=True)
    sp.plot_acf (p_acf, acf, prot=prot, acf_additional=[acf_a1, acf_a2, acf_a3],
                    color_additional=['darkorange', 'blue', 'red'], 
                    filename='test_outputs/acf.png')
    print ('Rotation period found with ACF for KIC3733735: {:.2f} days'.format (prot))

  @unittest.skip
  def testCSImplementation(self) :
    t = np.linspace (0, 365, 36500)  
    dt = np.median (np.diff (t))
    omega = 2*np.pi
    s = np.sin (omega*t)
    p_ps, ls = sp.compute_lomb_scargle (t, s, return_object=False)
    p_acf, acf = sp.compute_acf (s, dt, normalise=True,
                                    use_scipy_correlate=True, smooth=True)
    cs = sp.compute_cs (ls, acf, p_ps=p_ps, p_acf=p_acf)
    prot, h_cs = sp.find_prot_cs (p_acf, cs)
    print ('CS maximum for sinus function: {:.2f} days'.format (prot))
    prot, E_p, param = sp.compute_prot_err_gaussian_fit (p_acf, cs, verbose=False,
                                                            n_profile=5, threshold=0.1)
    feature, feature_names = sp.create_feature_from_fitted_param (param, method='CS')
    self.assertTrue (feature_names[0]=='CS_0_1')
    self.assertTrue (np.abs (feature[feature_names=='CS_0_2']-prot)<1e-6)
    sp.plot_cs (p_acf, cs, filename='test_outputs/cs_implementation.png', param_gauss=param,
                   xlim=(0,10))
    print ('Period found after Gaussian fit on CS for sinus function: {:.2f} +/- {:.2f} days'.format (prot, E_p))

  @unittest.skip
  def testCSLightCurve(self) :
    p_ps, ls = sp.compute_lomb_scargle (self.t, self.s, return_object=False)
    p_in = np.linspace (0, 100, 5000)
    p_acf, acf = sp.compute_acf (self.s, self.dt, p_in, normalise=True,
                                    use_scipy_correlate=True, smooth=True)
    cs = sp.compute_cs (ls, acf, p_ps=p_ps, p_acf=p_acf)
    prot, h_cs = sp.find_prot_cs (p_acf, cs)
    prot, E_p, param = sp.compute_prot_err_gaussian_fit (p_acf, cs, verbose=True,
                                                            n_profile=5, threshold=0.1)
    sp.plot_cs (p_acf, cs, filename='test_outputs/cs.png', param_gauss=param)
    print ('Rotation period found with CS for KIC3733735: {:.2f} +/- {:.2f} days'.format (prot, E_p))

  @unittest.skip
  def testComputeDeltaProt (self) :
    prot = 5
    dr_candidates = np.array([1, 4, 5, 5.3, 12, 28])
    dr_err = np.array([0.1, 0.4, 0.5, 0.53, 1.2, 2.8])
    dr_err = np.array([0.1, 0.4, 0.5, 0.53, 1.2, 2.8])
    dr, dr_err, _ = sp.compute_delta_prot (prot, dr_candidates, dr_err,
                                              dr_err, delta_min=1/3, delta_max=5/3)
    state = np.full (dr.size, -1)
    IDP_123_DELTA_PROT_NOSPOT = np.c_[dr, dr_err, state]
    expected = np.array([[ 4.  ,  0.4  , -1 ],
                         [ 5.  ,  0.5  , -1 ],
                         [ 5.3 ,  0.53 , -1 ]])
    self.assertTrue (np.all (IDP_123_DELTA_PROT_NOSPOT - expected < 1e-6))

  @unittest.skip
  def testAnalysisPipeline (self) :
    p_in = np.linspace (0, 100, 5000)
    p_ps, p_acf, ps, acf, cs, features, feature_names = sp.analysis_pipeline (self.t, self.s, periods_in=p_in,
                                                                                 wavelet_analysis=False, plot=True,
                                                                                 filename='test_outputs/pipeline.png', 
                                                                                 lw=1, dpi=300, smooth_acf=True)
    df = sp.save_features ('test_outputs/3733735_features.csv', 3733735, features, feature_names)

  @unittest.skip
  def testWavelet (self) :
    p_in = np.linspace (0.1, 100, 200)
    _, wps, gwps, coi = sp.compute_wps (self.s, self.dt*86400, periods=p_in,
                                           normalise=True, mother=None)
    prot, E_p, param = sp.compute_prot_err_gaussian_fit (p_in, gwps, verbose=False,
                                                            n_profile=5, threshold=0.1)
    print ('Rotation period found with GWPS for KIC3733735: {:.2f} +/- {:.2f} days'.format (prot, E_p))
    sp.plot_wps (self.t, p_in, wps, gwps, coi,
              cmap='Blues', shading='auto', 
              filename='test_outputs/wavelet.png',
              color_coi='black', ylogscale=False, param_gauss=param,
              ax1=None, ax2=None, lw=1, normscale='linear',
              vmin=None, vmax=None, dpi=200)

  @unittest.skip
  def testAnalysisPipelineWavelet (self) :
    p_in = np.linspace (0, 100, 200)
    sp.analysis_pipeline (self.t, self.s, periods_in=p_in,
                             wavelet_analysis=True, plot=True,
                             filename='test_outputs/pipeline_wavelet.png', 
                             lw=1, dpi=200, smooth_acf=True)

 
#@unittest.skip
class TestRooster (unittest.TestCase) :

  @unittest.skip
  def testLoadReference (self) :
    df = sp.load_reference_catalog (catalog='santos-19-21')
    self.assertEqual (df.columns, ['prot'])

  @unittest.skip
  def testAttributeClass (self) :
    target_id = [3733735, 1245803]
    df = sp.attribute_rot_class (target_id, catalog='santos-19-21')
    self.assertEqual (df.loc[3733735, 'target_class'], 'rot')
    self.assertEqual (df.loc[1245803, 'target_class'], 'no_rot')

    p_candidates = np.array ([[2.6, 2.4, 5.1], [2, 2, 2]])
    df = sp.attribute_period_sel (target_id, p_candidates,
                                     catalog='santos-19-21')
    self.assertEqual (df.loc[3733735, 'target_class'], 0)

    p_candidates = np.array ([[5.6, 2.4, 5.1], [2, 2, 2]])
    df = sp.attribute_period_sel (target_id, p_candidates,
                                     catalog='santos-19-21')
    self.assertEqual (df.loc[3733735, 'target_class'], 1)

    p_candidates = np.array ([[5, 5, 2.5], [2, 2, 2]])
    df = sp.attribute_period_sel (target_id, p_candidates,
                                     catalog='santos-19-21')
    self.assertEqual (df.loc[3733735, 'target_class'], 2)

  @unittest.skip
  def testCreateRoosterInstance (self) :
    # Initiating ROOSTER without specifying any random forest option
    chicken = sp.ROOSTER ()
    # Specifying number of estimators
    chicken = sp.ROOSTER (n_estimators=50, max_leaf_nodes=10)
    self.assertEqual (chicken.RotClass.n_estimators, 50)
    self.assertEqual (chicken.isTrained (), False)
    self.assertEqual (chicken.isTested (), False)
    chicken.save ('test_outputs/rooster_instance')
    chicken = sp.load_rooster_instance (filename='test_outputs/rooster_instance')
    # Check that we can correctly access the loaded instance properties
    self.assertEqual (chicken.RotClass.n_estimators, 50)

if __name__ == '__main__' :
  print ('Testing star_privateer v{}, located at {}'.format (sp.__version__, sp.__file__))
  unittest.main(verbosity=2)
