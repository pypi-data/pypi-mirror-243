apollinaire
=======================================

**apollinaire** is a Python implementation of helio- and asteroseismic MCMC
peakbagging methods. You will find here all the necessary tools in order to
analyse the acoustic oscillations of your favourite solar-like star. 

The source code is hosted on a `GitLab repository
<https://gitlab.com/sybreton/apollinaire>`_ and is still in development.  To
find more details on the power spectrum modelling framework used by
**apollinaire**, you can take a look at `Breton et al. (2022)
<https://www.aanda.org/articles/aa/full_html/2022/07/aa43330-22/aa43330-22.html>`_. 

.. image:: https://anaconda.org/conda-forge/apollinaire/badges/version.svg/?style=plastic
  :target: https://anaconda.org/conda-forge/apollinaire
.. image:: https://anaconda.org/conda-forge/apollinaire/badges/license.svg/?style=plastic  
  :target: https://anaconda.org/conda-forge/apollinaire
.. image:: https://img.shields.io/badge/reference-paper-orange
  :target: https://www.aanda.org/articles/aa/abs/2022/07/aa43330-22/aa43330-22.html

|

.. toctree::
   :maxdepth: 1
   :caption: User guide

   usage/installation
   usage/quickstart/first_steps
   usage/advanced/advanced_peakbagging
   usage/format
   usage/synthetic_spectrum/synthetic_spectrum
   usage/quality_assurance/quality_assurance
   usage/citing_apollinaire

.. toctree::
   :maxdepth: 2
   :caption: Detailed API

   usage/psd_module
   usage/peakbagging_module
   usage/sim_module
   usage/songlib

Why naming a peakbagging code **apollinaire** ?
###################################################

Among the most famous French-language poets, Guillaume Apollinaire chose his
pseudonym (which is actually one of his many middle names) as a reference to
Apollo, Greek god of the Sun and light. Asteroseimology being often
metaphorically refered as a discipline devoted to elucidating `the music of
the Sun and stars
<https://exoplanets.nasa.gov/news/1516/symphony-of-stars-the-science-of-stellar-sound-waves/>`_,
the present module is named as a tribute to one of the greatest musician of
words of the XXth century.

	| *Et je cherche au ciel constellé*  
	| *Où sont nos étoiles jumelles* 
	| *Mon destin au tien est mêlé*
	| *Mais nos étoiles où sont-elles ?*
	| Guillaume Apollinaire
	| *Poèmes à Lou* 

