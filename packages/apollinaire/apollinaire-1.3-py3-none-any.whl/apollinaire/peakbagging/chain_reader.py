import numpy as np
import pandas as pd
import glob
import emcee
from os import path
import os
from .fit_tools import *
from .a2z_no_pandas import wrapper_cf_to_pkb_extended_nopandas

def read_chain (filename, thin=1, discard=0, read_order=True,
                chain_type='peakbagging', fit_amp=False, 
                projected_splittings=False) :
  '''
  Read a chain created by ``apollinaire`` and return flattened 
  sampled chain with auxiliary informations.

  :param filename: name of the hdf5 file with the stored chain.
  :type filename: str

  :param thin: the returned chain will be thinned according to this factor. Optional, default 1.
  :type thin: int

  :param discard: number of iteration step to discard. Optional, default 0.
  :type discard: int

  :param read_order: set to ``False`` when reading a ``peakbagging`` chain created
    with the ``strategy=global``. The ``order`` output will be ``-9999``
    in this case.  
  :type read_order: bool 

  :param chain_type: can be ``peakbagging``, ``pattern`` or ``background``.
    Optional, default ``peakbagging``.
  :type chain_type: str

  :param fit_amp: set to ``True`` if amplitudes were fitted instead of heights.
  :type fit_amp: bool

  :param projected_splittings: set to ``True`` if projected splittings were 
    fitted instead of splittings.
  :type projected_splittings: bool

  :return: tuple with flatchain, param labels, degrees of param and order of modes
    if ``chain_type=peakbagging``, flatchain and labels otherwise.
  :rtype: tuple of ndarrays
  ''' 
  reader = emcee.backends.HDFBackend(filename, read_only=True)

  if chain_type=='peakbagging' :
    labels = np.loadtxt (path.splitext (filename)[0]+'.dat', dtype=str, usecols=0)
    degrees = np.loadtxt (path.splitext (filename)[0]+'.dat', dtype=str, usecols=2)
    norm = np.loadtxt (path.splitext (filename)[0]+'.dat', usecols=1)

    if fit_amp :
      labels[labels=='height'] = 'amplitude'
    if projected_splittings :
      labels[labels=='split'] = 'proj_split'
    if read_order :
      order = path.basename (filename)[19:21]
      order = int (order)
    else :
      order = -9999

    flatchain = reader.get_chain(flat=True, thin=thin, discard=discard) * norm
    return flatchain, labels, degrees, order 

  else :
    norm = np.loadtxt (path.splitext (filename)[0]+'.dat', usecols=0)
    labels = np.loadtxt (path.splitext (filename)[0]+'.dat', dtype=str, usecols=1)
    flatchain = reader.get_chain(flat=True, thin=thin, discard=discard) * norm 
    return flatchain, labels 

def make_cornerplot (flatchain, labels=None, filename=None, 
                     bins=10, figsize=(24,24), labelsize=20, 
                     use_formatter=False, reverse=False, 
                     title_fmt='.4f',
                     **kwargs) : 
  '''
  Make a cornerplot from a flattened chain. 
  This is simply a wrapper for ``corner.corner``.

  :param flatchain: the flattened chain.
  :type flatchain: ndarray

  :param labels: parameters labels
  :type labels: array-like

  :param filename: name of the file where the cornerplot will 
    be saved.
  :type filename: str

  :param bins: number of bins in the histograms.
    Optional, default ``10``. 
  :type bins: int
  '''

  ndim = flatchain.shape[1]
  fig = corner.corner(flatchain, bins=bins, labels=labels, 
                      quantiles=[0.16,0.84], show_titles=True, title_fmt=title_fmt,
                      reverse=reverse, **kwargs)
  fig.set_size_inches(figsize)
  axes = np.array(fig.axes).reshape((ndim, ndim))
  if filename is not None :
    plt.savefig (filename)
  else :
    plt.show ()
  plt.close ()

  return fig

def complete_df_with_ampl (df, instr='geometric') :

  a_amp = [['a', '2', 'amp_l', 'global', 0.7, 0.0, 1, 0.0, 0.0],
           ['a', '3', 'amp_l', 'global', 0.2, 0.0, 1, 0.0, 0.0],
           ['a', '1', 'amp_l', 'global', 1.5, 0.0, 1, 0.0, 0.0],
           ['a', '0', 'amp_l', 'global', 1.0, 0.0, 1, 0.0, 0.0]]
  df_amp = pd.DataFrame (data=a_amp) 

  if instr=='golf' :
    df_amp.loc[df[1]=='1', 4] = 1.69
    df_amp.loc[df[1]=='2', 4] = 0.81
    df_amp.loc[df[1]=='3', 4] = 0.17
  if instr=='virgo' :
    df_amp.loc[df[1]=='1', 4] = 1.53
    df_amp.loc[df[1]=='2', 4] = 0.59
    df_amp.loc[df[1]=='3', 4] = 0.09

  df = pd.concat ([df, df_amp])

  return df

def chain_element_to_a2z (param, labels, degrees, order, add_ampl=False, instr='geometric') :
  '''
  Build and a2z DataFrame with any set of parameters taken from a MCMC.

  :return: a2z DataFrame
  :rtype: pandas DataFrame
  '''

  columns = list (range (9))
  aux_index = list (range (labels.size))

  # Initialise with a float type to have the correct
  # type for columns on which numerical operations 
  # are performed
  df = pd.DataFrame (index=aux_index, columns=columns)
  df[0] = order
  df[1] = degrees
  df[2] = labels
  df.loc[labels!='a',3] = 'mode'
  df.loc[labels=='a',3] = 'order'
  df[4] = param
  df[[5,6,7,8]] = 0

  # If fit_amp, the keyword in the chain is "amplitude"
  # but a2z deals only with "heights" as a column name
  df.loc[df[2]=='amplitude'] = 'height'

  #retransforming width and heights
  cond_exp = (df[2]=='height')|(df[2]=='width')
  df.loc[cond_exp,4] = np.exp (df.loc[cond_exp,4])

  df.loc[(df[1]=='2')|(df[1]=='3'), 0] = (df.loc[(df[1]=='2')|(df[1]=='3'), 0].astype (np.int_) - 1).astype (np.str_)
  df.loc[(df[1]=='4')|(df[1]=='5'), 0] = (df.loc[(df[1]=='4')|(df[1]=='5'), 0].astype (np.int_) - 2).astype (np.str_)

  if add_ampl :
    df = complete_df_with_ampl (df, instr='geometric')

  return df

def chain_to_a2z (filename, thin=1, discard=0, add_ampl=False, instr='geometric') :
  '''
  Function to create an a2z dataframe from a sampled chain.

  :param filename: name of the chain. The name format is the following
    ``mcmc_sampler_order_[n_order]_degrees_[n_degrees].h5`` with ``n_degrees`` being ``13`` or ``02``.
  :type filename: str

  :param instr: instrument to consider. Possible argument : ``geometric``, ``kepler``, ``golf``, ``virgo``.
    Optional, default ``geometric``. 
  :type instr: str

  :return: a2z style dataframe.
  :rtype: pandas DataFrame
  '''

  flatchain, labels, degrees, order = read_chain (filename, thin=thin, discard=discard)

  centiles = np.percentile (flatchain, [16, 50, 84], axis=0) 
  bounds = np.percentile (flatchain, [0,100], axis=0) 

  columns = list (range (9))
  aux_index = list (range (labels.size))

  df = pd.DataFrame (index=aux_index, columns=columns)
  df[0] = order
  df[1] = degrees
  df[2] = labels
  df.loc[labels!='a',3] = 'mode'
  if 'degrees_02' in path.basename (filename) :  
    df.loc[labels=='a',3] = 'even'
  elif 'degrees_13' in path.basename (filename) :  
    df.loc[labels=='a',3] = 'odd'
  else :
    df.loc[labels=='a',3] = 'order'
  df[4] = centiles[1,:]

  #retransforming width and heights
  cond_exp = (df[2]=='height')|(df[2]=='width')
  a_cond_exp = cond_exp.to_numpy ()
  for ii in range (centiles.shape[0]) :
    centiles[ii,a_cond_exp] = np.exp (centiles[ii,a_cond_exp])
  df.loc[cond_exp,4] = np.exp (df.loc[cond_exp,4])

  #Computing (symmetric) sigmas
  sigma_1 = centiles[1,:] - centiles[0,:]
  sigma_2 = centiles[2,:] - centiles[1,:]
  sigma = np.maximum (sigma_1, sigma_2)

  df[5] = sigma
  df[6] = 0.

  #Adding bounds
  df[7] = bounds[0,:]
  df[8] = bounds[1,:]

  df.loc[(df[1]=='2')|(df[1]=='3'), 0] = (df.loc[(df[1]=='2')|(df[1]=='3'), 0].astype (np.int_) - 1).astype (np.str_)
  df.loc[(df[1]=='4')|(df[1]=='5'), 0] = (df.loc[(df[1]=='4')|(df[1]=='5'), 0].astype (np.int_) - 2).astype (np.str_)

  if add_ampl :
    df = complete_df_with_ampl (df, instr='geometric')

  return df

def complete_df_centile_with_ampl (df, instr='geometric') :

  a_amp = [['a', '2', 'amp_l', 'global', 0.7, 0.0, 0.0],
           ['a', '3', 'amp_l', 'global', 0.2, 0.0, 0.0],
           ['a', '1', 'amp_l', 'global', 1.5, 0.0, 0.0],
           ['a', '0', 'amp_l', 'global', 1.0, 0.0, 0.0]]
  df_amp = pd.DataFrame (data=a_amp)

  if instr=='golf' :
    df_amp.loc[df[1]=='1', 4] = 1.69
    df_amp.loc[df[1]=='2', 4] = 0.81
    df_amp.loc[df[1]=='3', 4] = 0.17
  if instr=='virgo' :
    df_amp.loc[df[1]=='1', 4] = 1.53
    df_amp.loc[df[1]=='2', 4] = 0.59
    df_amp.loc[df[1]=='3', 4] = 0.09

  df = pd.concat ([df, df_amp])

  return df

def chain_to_centile_frame (filename, thin=1, discard=0, add_ampl=False, instr='geometric') :
  '''
  Function to create a centile frame from a sampled chain.

  :param discard: the number of elements to ignore at the beginning of the chain.
  :type discard: int

  :param thin: one element of the chain every ``thin`` elements will be considered.
  :type thin: int

  :param filename: name of the chain. The name format is the following
    'mcmc_sampler_order_[n_order]_degrees_[n_degrees].h5' with n_degrees being '13' or '02'.
  :type filename: str

  :return: centile frame
  :rtype: pandas DataFrame
  '''

  flatchain, labels, degrees, order = read_chain (filename, thin=thin, discard=discard)

  centiles = np.percentile (flatchain, [16, 50, 84], axis=0) 
  bounds = np.percentile (flatchain, [0,100], axis=0) 

  columns = list (range (6))
  aux_index = list (range (labels.size))

  df = pd.DataFrame (index=aux_index, columns=columns)
  df[0] = order
  df[1] = degrees
  df[2] = labels
  df.loc[labels!='a',3] = 'mode'
  if 'degrees_02' in path.basename (filename) :  
    df.loc[labels=='a',3] = 'even'
  elif 'degrees_13' in path.basename (filename) :  
    df.loc[labels=='a',3] = 'odd'
  else :
    df.loc[labels=='a',3] = 'order'
  df[4] = centiles[1,:]

  #retransforming width and heights
  cond_exp = (df[2]=='height')|(df[2]=='width')
  a_cond_exp = cond_exp.to_numpy ()
  for ii in range (centiles.shape[0]) :
    centiles[ii,a_cond_exp] = np.exp (centiles[ii,a_cond_exp])
  df.loc[cond_exp,4] = np.exp (df.loc[cond_exp,4])

  #Adding sigmas
  sigma_1 = centiles[1,:] - centiles[0,:]
  sigma_2 = centiles[2,:] - centiles[1,:]

  df[5] = sigma_1
  df[6] = sigma_2

  df.loc[(df[1]=='2')|(df[1]=='3'), 0] = (df.loc[(df[1]=='2')|(df[1]=='3'), 0].astype (np.int_) - 1).astype (np.str_)
  df.loc[(df[1]=='4')|(df[1]=='5'), 0] = (df.loc[(df[1]=='4')|(df[1]=='5'), 0].astype (np.int_) - 2).astype (np.str_)

  if add_ampl :
    df = complete_df_centile_with_ampl (df, instr='geometric')

  return df

def cf_to_pkb_extended (df_centile, nopandas=True) :
  '''
  Take centile frame and return pkb extended array. Frequency units are given in µHz and not Hz. pkb format is the following: 

  +------------+---+---+-----+---------------+-----------+-----------+-----------+-------+------+------+--------+--------+--------+-------+------+------+----------------+---------+
  | parameters | n | l | nu  | nu_e- | nu_e+ | height    | height_e- | height_e+ | width | w_e- | w_e+ | angle  | a_e-   | a_e+   | split | s_e- | s_e+ | asym | asym_e- | asym_e+ |
  +------------+---+---+-----+---------------+-----------+-----------+-----------+-------+------+------+--------+--------+--------+-------+--------------------+---------+---------+
  | units      | . | . | µHz | µHz   | µHz   | power/µHz | power/µHz | power/µHz | µHz   | µHz  | µHz  | degree | degree | degree | µHz   | µHz  | µHz  | .    | .       | .       |
  +------------+---+---+-----+---------------+-----------+-----------+-----------+-------+------+------+--------+--------+--------+-------+------+------+------+---------+---------+

  :param df_centile: input parameters as a centile frame.
  :type df_centile: pandas DataFrame

  :return: array extended pkb. 
  :rtype: ndarray
  '''

  if nopandas :
    return wrapper_cf_to_pkb_extended_nopandas (df_centile)
  else :
    raise Exception ('nopandas=False option is no longer available in version {}.'.format (apollinaire.__version__))
  

def hdf5_to_a2z (workDir='.', a2zname='summary_fit.a2z', 
                 discard=0, thin=10, instr='geometric', centile=False,
                 verbose=False) :

  '''
  Create a a2z file with the hdf5 files stored in a given folder.

  :param workDir: the directory where the hdf5 file will be read.
  :type workDir: str

  :param a2zname: the name of the output file. Set to ``None`` if you do not want to save any file.
  :type pkbname: str

  :param discard: the number of elements to ignore at the beginning of the chain.
  :type discard: int

  :param thin: one element of the chain every ``thin`` elements will be considered.
  :type thin: int

  :param centile: if set to True, change the structure of the output to write a centile frame.
    Optional, default ``False``.
  :type centile: bool

  :param instr: instrument to consider. Possible argument : ``geometric``, ``kepler``, ``golf``, ``virgo``.
    Optional, default ``geometric``. 
  :type instr: str

  :param verbose: if set to ``True``, print the name of the considered files.
    Optional, default ``False``.
  :type verbose: bool

  :return: a2z DataFrame
  :rtype: pandas DataFrame
  '''

  listHDF5 = glob.glob (path.join (workDir, 'mcmc_sampler_order_*.h5'))
  listHDF5.sort ()
  df = pd.DataFrame ()
  add_ampl = False
  for ii, filename in enumerate (listHDF5) :
    if verbose :
      print (filename)
    if ii==len (listHDF5) - 1 :
      add_ampl=True
    if not centile :
      aux = chain_to_a2z (filename, thin=thin, discard=discard, add_ampl=add_ampl, instr=instr)
    else :
      aux = chain_to_centile_frame (filename, thin=thin, discard=discard, add_ampl=add_ampl, instr=instr)
    df = pd.concat ([df, aux])

  if a2zname is not None :
    save_a2z (path.join (workDir, a2zname), df)

  df = sort_a2z (df)

  return df

def hdf5_to_pkb (workDir='.', pkbname='summary_fit.pkb', discard=0, 
                 thin=10, instr='geometric', extended=False, verbose=False) :

  '''
  Create a pkb file with the hdf5 files stored in a given folder.

  :param workDir: the directory where the hdf5 file will be read.
  :type workDir: str

  :param pkbname: the name of the output pkb. Set to ``None`` if you do not want to save a file.
  :type pkbname: str

  :param discard: the number of elements to ignore at the beginning of the chain.
  :type discard: int

  :param thin: one element of the chain every ``thin`` elements will be considered.
  :type thin: int

  :param extended: if set to True, change the structure of the output to write a pkb extended.
    Optional, default ``False``.
  :type extended: bool

  :param instr: instrument to consider. Possible argument : ``geometric``, ``kepler``, ``golf``, ``virgo``.
    Optional, default ``geometric``. 
  :type instr: str

  :param verbose: if set to ``True``, print the name of the considered files.
    Optional, default ``False``.
  :type verbose: bool

  :return: pkb array
  :rtype: ndarray
  '''

  centile = False
  if extended :
    centile = True

  df = hdf5_to_a2z (workDir=workDir, a2zname=None, discard=discard, 
                    thin=thin, instr=instr, centile=centile, verbose=verbose)

  df = df.loc[(df[1]!='4')&(df[1]!='5')]
  if extended :
    pkb = cf_to_pkb_extended (df)
  else :
    pkb = a2z_to_pkb (df)

  pkb = sort_pkb (pkb)

  if pkbname is not None :
    np.savetxt (path.join (workDir, pkbname), pkb, fmt='%-s')

  return pkb
