import unittest
import os
import glob
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings 
import apollinaire as apn
from apollinaire.peakbagging import *
import apollinaire.peakbagging.templates as templates
import apollinaire.test.test_data as test_data
import apollinaire.timeseries as timeseries
import importlib.resources
import pandas as pd

# Defining some environment variables
ignore_deprecation = os.environ.get('APN_TEST_IGNORE_DEPRECATION_WARNING', 'True')

class TestDataManipulation (unittest.TestCase) :
  '''
  A collection of tests to check that data manipulation
  methods behave correctly.
  '''

  def setUp (self) :
    '''
    Load data for test and proceed for a first a2z check.
    '''
    if ignore_deprecation :
      #Ignore deprecation warning 
       warnings.simplefilter('ignore', category=DeprecationWarning)
    f1 = importlib.resources.path (templates, 'test.a2z')
    f2 = importlib.resources.path (templates, 'verif.pkb')
    with f1 as filename :
      self.df_a2z = read_a2z (filename)
      check_a2z (self.df_a2z, verbose=False)
      self.pkb = a2z_to_pkb (self.df_a2z)
    with f2 as filename :
      self.verif_pkb = np.loadtxt (filename)

  def test_a2z_pkb_validity (self) :
    self.assertTrue (~np.any (np.isnan (self.pkb)))
    self.assertTrue (np.all (get_list_order (self.df_a2z)==[5, 21, 22]))
    # Test if the pkb array contains the expected values.'
    residual = np.abs (self.pkb - self.verif_pkb)
    error = np.linalg.norm (residual.ravel(), ord=np.inf)
    self.assertTrue (error < 1.e-6,) 

  def test_compute_model (self) :
    freq = np.linspace (0, 5000, 10000)
    model = compute_model (freq, self.pkb)
    # Test if the model built from the test pkb array contains NaN.
    self.assertTrue (~np.any (np.isnan (model)))

  def test_light_curve_and_guess (self) :
    # Test importation and light curves management function
    t, v = apn.timeseries.load_light_curve (star='006603624')
    self.assertEqual (t.shape, (1684776,))
    self.assertEqual (v.shape, (1684776,))
    self.assertTrue (~np.any (np.isnan (t)))
    self.assertTrue (~np.any (np.isnan (v)))
    dt = np.median (t[1:] - t[:-1]) * 86400
    freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
    freq, psd = freq*1e6, psd*1e-6
    guess, low_bounds, up_bounds, labels = create_background_guess_arrays (freq, psd, r=1.162, m=1.027, teff=5671.,
                                                                           n_harvey=2, spectro=False, power_law=False,
                                                                           high_cut_plaw=100., return_labels=True)
    # Test if the background guess array contains NaN
    self.assertTrue (~np.any (np.isnan (guess))) 
    # Test if the background low bounds array contains NaN
    self.assertTrue (~np.any (np.isnan (low_bounds))) 
    # Test if the background up bounds array contains NaN
    self.assertTrue (~np.any (np.isnan (up_bounds))) 
    # Test if the resulting background model contains NaN
    back = build_background(freq, guess, n_harvey=2, apodisation=False, remove_gaussian=True)
    self.assertTrue (~np.any (np.isnan (back))) 

  def test_load_golf_timeseries (self) :
    v = apn.timeseries.load_golf_timeseries ()
    self.assertTrue (~np.any (np.isnan (v)))

  def test_formatting (self) :
    labels=['freq', 'freq', 'freq', 'freq', 
             'width', 'height', 'angle', 
             'width', 'height', 'amplitude', 
             'split', 'proj_split',
             'background', 'asym',
             'amp_l']
    orders=['18', '19', '20', '21',
            'a', 'a', 'a',
            '18', '18', '18',
            'a', 'a', 
            'a', '20',
            'a']
    degrees=['0', '1', '2', '3', 
             'a', 'a', 'a',
             '1', '1', 'a',
             'a', 'a', 
             'a', 'a',
             '1']
    formatted = param_array_to_latex (labels, orders, degrees)
    expected = ['$\\nu_{18,0}$', '$\\nu_{19,1}$', '$\\nu_{20,2}$', '$\\nu_{21,3}$', 
                '$\\Gamma_{n,\\ell}$', '$H_{n,\\ell}$', '$i$', 
                '$\\Gamma_{18,1}$', '$H_{18,1}$', '$A_{18,\\ell}$', 
                '$s_{n,\\ell}$', '$\\sin i . s_{n,\\ell}$', 
                '$B$', '$\\alpha_{20,\\ell}$', '$V_{1} / V_0$']
    self.assertEqual (formatted, expected)
     

class ChainReadingTests (unittest.TestCase) :
  '''
  A class to test chain reading methods.
  '''

  def setUp (self) :
    if ignore_deprecation :
      #Ignore deprecation warning 
       warnings.simplefilter('ignore', category=DeprecationWarning)
    if not os.path.exists ('tmp') :
      os.mkdir ('tmp')

  def tearDown (self) :
    list_files = glob.glob ('tmp/*')
    for filename in list_files :
      os.remove (filename)
    os.rmdir ('tmp')

  def test_chain_reading (self) :
    f1 = importlib.resources.path (test_data, 'mcmc_background.h5')
    f2 = importlib.resources.path (test_data, 'mcmc_pattern.h5')
    f3 = importlib.resources.path (test_data, 'mcmc_sampler_order_20.h5')
    with f1 as filename :
      flatchain, labels = read_chain (filename, thin=1, discard=0, read_order=True,
                                      chain_type='background', fit_amp=False,
                                      projected_splittings=False)
      self.assertTrue (np.all (labels==['A_H_1', 'nuc_H_1', 'alpha_H_1', 
                                        'A_H_2', 'nuc_H_2', 'alpha_H_2', 
                                        'A_Gauss', 'numax', 'Wenv', 'noise']))
    with f2 as filename :
      flatchain, labels = read_chain (filename, thin=1, discard=0, read_order=True,
                                      chain_type='pattern', fit_amp=False,
                                      projected_splittings=False)
      self.assertTrue (np.all (labels==['eps', 'alpha', 'Dnu', 'numax', 'Hmax',
                                        'Wenv', 'w', 'd02', 'b02', 'd01', 'b01', 'd13', 'b03']))
    with f3 as filename :
      flatchain, labels, degrees, order = read_chain (filename, thin=1, discard=0, read_order=True,
                                                      chain_type='peakbagging', fit_amp=False,
                                                      projected_splittings=False)
      self.assertTrue (np.all (labels==['freq', 'freq', 'freq', 'freq', 'width', 'height', 'background']))
      self.assertTrue (np.all (degrees==['0', '1', '2', '3', 'a', 'a', 'a']))
      self.assertEqual (order, 20)

  def test_hdf5_to_a2z (self) :
    pkb = hdf5_to_pkb (workDir=os.path.dirname (test_data.__file__), 
                       pkbname=None, discard=0, thin=10, 
                       instr='geometric', extended=False)
    self.assertTrue (~np.any (np.isnan (pkb)))
    self.assertEqual (pkb.shape[1], 14)
    pkb = hdf5_to_pkb (workDir=os.path.dirname (test_data.__file__), 
                       pkbname=None, discard=0, thin=10, 
                       instr='geometric', extended=True)
    self.assertTrue (~np.any (np.isnan (pkb)))
    self.assertEqual (pkb.shape[1], 20)
    
@unittest.skipIf(os.environ.get('APN_TEST_SKIP_INTEGRATION', 'True')=='True',
                 "skipped integration tests")
class IntegrationTests (unittest.TestCase) :
  '''
  A class to execute integration tests and check that they
  finish without raising any exception. 
  '''

  def setUp (self) :
    if ignore_deprecation :
      #Ignore deprecation warning 
       warnings.simplefilter('ignore', category=DeprecationWarning)
    if not os.path.exists ('tmp') :
      os.mkdir ('tmp')

  def tearDown (self) :
    list_files = glob.glob ('tmp/*')
    for filename in list_files :
      os.remove (filename)
    os.rmdir ('tmp')

  def test_stellar_framework (self) :
    #Test stellar_framework execution 
    t, v = apn.timeseries.load_light_curve (star='006603624')
    dt = np.median (t[1:] - t[:-1]) * 86400
    freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
    freq = freq*1e6
    psd = psd*1e-6
    r, m, teff = 1.162, 1.027, 5671
    apn.peakbagging.stellar_framework (freq, psd, r, m, teff, n_harvey=2, low_cut=50., filename_back='tmp/background.png',
                                   filemcmc_back='tmp/mcmc_background.h5', nsteps_mcmc_back=10, n_order=3, 
                                   n_order_peakbagging=3, filename_pattern='tmp/pattern.png', fit_l3=True,
                                   filemcmc_pattern='tmp/mcmc_pattern.h5', nsteps_mcmc_pattern=10, parallelise=True, 
                                   quickfit=True, num=500, discard_back=1, discard_pattern=1, discard_pkb=1, 
                                   progress=True, bins=50, extended=True, mcmcDir='tmp', 
                                   a2z_file='tmp/modes_param.a2z', format_cornerplot='png', nsteps_mcmc_peakbagging=10, 
                                   filename_peakbagging='tmp/summary_peakbagging.png', dpi=100, plot_datapoints=False)

if __name__ == '__main__' :
  print ('Testing apollinaire v{}, located at {}'.format (apn.__version__, apn.__file__))
  unittest.main(verbosity=2)





