Time series analysis (MSAP4-02)
===============================

.. code:: ipython3

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

.. code:: ipython3

    import star_privateer as sp
    import plato_msap4_demonstrator_datasets.plato_sim_dataset as plato_sim_dataset

K2: Preprocessing
-----------------

This first part include preprocessing tasks that are not actually
included in MSAP4-02 but are useful for the subsequent analysis.

.. code:: ipython3

    t, s0, dt = sp.load_k2_example ()

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s0!=0]-t[0], s0[s0!=0], color='black', 
                marker='o', s=1)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    fig.tight_layout ()
    
    plt.savefig ('figures/k2_lc.png', dpi=300)



.. image:: timeseries_analysis_files/timeseries_analysis_6_0.png


.. code:: ipython3

    pcutoff = 45
    pthresh = 90

K2: Rotation period analysis
----------------------------

In the next step, we compute the ACF and we analyse the characteristic
periodicities obtained from the function, considering only periods below
:math:`P_\mathrm{cutoff}`.

.. code:: ipython3

    p_acf, acf = sp.compute_acf (s0, dt, normalise=True,
                                    use_scipy_correlate=True, smooth=True, verbose=True)
    _, _, _, _, prots, hacf, gacf = sp.find_period_acf (p_acf, acf, pcutoff=pcutoff)
    fig = sp.plot_acf (p_acf, acf, prot=prots, filename='figures/acf_k2.png')


.. parsed-literal::

    ACF was smoothed with a period 0.26 days



.. image:: timeseries_analysis_files/timeseries_analysis_10_1.png


We can take a look at the values we have extracted from the ACF. Most
often, the rotation period can be linked to the first value of the
``prots`` array.

.. code:: ipython3

    prots[0], hacf[0], gacf[0]




.. parsed-literal::

    (2.6765510971308686, 1.2594916191360066, 0.8353126108493093)



Finally we create the intermediate data product.

.. code:: ipython3

    IDP_123_ACF_FILT_TIMESERIES = np.c_[p_acf, acf]
    IDP_123_PROT_TIMESERIES = np.c_[prots, np.full (prots.size, -1), np.full (prots.size, -1),
                                    hacf, gacf, np.arange (prots.size)+1]
    np.savetxt ('data_products/IDP_123_PROT_TIMESERIES_K2.dat', 
                IDP_123_PROT_TIMESERIES)
    np.savetxt ('data_products/IDP_123_ACF_FILT_TIMESERIES_K2.dat', 
                IDP_123_ACF_FILT_TIMESERIES)
    df = pd.DataFrame (data=IDP_123_PROT_TIMESERIES)
    df




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2.676551</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.259492</td>
          <td>0.835313</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>5.271375</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.180853</td>
          <td>0.786927</td>
          <td>2.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>7.947927</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.017210</td>
          <td>0.664006</td>
          <td>3.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10.583614</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.940327</td>
          <td>0.605458</td>
          <td>4.0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>13.280597</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.771528</td>
          <td>0.499477</td>
          <td>5.0</td>
        </tr>
        <tr>
          <th>5</th>
          <td>15.875421</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.768302</td>
          <td>0.452141</td>
          <td>6.0</td>
        </tr>
        <tr>
          <th>6</th>
          <td>18.592836</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.741704</td>
          <td>0.421836</td>
          <td>7.0</td>
        </tr>
        <tr>
          <th>7</th>
          <td>21.187660</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.663556</td>
          <td>0.363392</td>
          <td>8.0</td>
        </tr>
        <tr>
          <th>8</th>
          <td>23.884643</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.641628</td>
          <td>0.362309</td>
          <td>9.0</td>
        </tr>
        <tr>
          <th>9</th>
          <td>26.499899</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.551047</td>
          <td>0.292327</td>
          <td>10.0</td>
        </tr>
        <tr>
          <th>10</th>
          <td>29.156018</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.524945</td>
          <td>0.282007</td>
          <td>11.0</td>
        </tr>
        <tr>
          <th>11</th>
          <td>31.791706</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.440642</td>
          <td>0.222855</td>
          <td>12.0</td>
        </tr>
        <tr>
          <th>12</th>
          <td>34.427394</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.392308</td>
          <td>0.206277</td>
          <td>13.0</td>
        </tr>
        <tr>
          <th>13</th>
          <td>36.981355</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.314554</td>
          <td>0.157428</td>
          <td>14.0</td>
        </tr>
        <tr>
          <th>14</th>
          <td>39.637474</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.276499</td>
          <td>0.145753</td>
          <td>15.0</td>
        </tr>
        <tr>
          <th>15</th>
          <td>42.109708</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.240641</td>
          <td>0.126138</td>
          <td>16.0</td>
        </tr>
        <tr>
          <th>16</th>
          <td>44.786260</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.226810</td>
          <td>0.121512</td>
          <td>17.0</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    df.to_latex (buf='data_products/idp_msap4_02_idp_prot_timeseries.tex', 
                 formatters=['{:.2f}'.format, '{:.0f}'.format, '{:.0f}'.format,
                             '{:.2f}'.format, '{:.2f}'.format, '{:.0f}'.format,],  
                 index=False, header=False)

Note that, due to the short length of this light curve, we do not show
for this first case the analysis of long term modulations.

PLATO simulation: Preprocessing
-------------------------------

This first part include preprocessing tasks that are not actually
included in MSAP4-02 but are useful for the subsequent analysis.

.. code:: ipython3

    filename = sp.get_target_filename (plato_sim_dataset, '040', filetype='csv')
    t, s0, dt = sp.load_resource (filename)

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s0!=0]-t[0], s0[s0!=0], color='black', 
                marker='o', s=1)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    fig.tight_layout ()
    
    
    plt.savefig ('figures/plato_lc.png', dpi=300)



.. image:: timeseries_analysis_files/timeseries_analysis_20_0.png


.. code:: ipython3

    s = sp.preprocess (t, s0, cut=55)
    pcutoff = 45
    pthresh = 90

PLATO simulation: Rotation period analysis
------------------------------------------

This first part include preprocessing task that are not actually
included in MSAP4-02 but are useful for the subsequent analysis.

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s!=0]-t[0], s[s!=0], color='black', 
                marker='o', s=1)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    fig.tight_layout ()
    
    plt.savefig ('figures/plato_lc_filtered.png', dpi=300)



.. image:: timeseries_analysis_files/timeseries_analysis_24_0.png


.. code:: ipython3

    p_acf, acf = sp.compute_acf (s, dt, normalise=True,
                                    use_scipy_correlate=True, smooth=True)
    _, _, _, _, prots, hacf, gacf = sp.find_period_acf (p_acf, acf, pcutoff=pcutoff)
    fig = sp.plot_acf (p_acf, acf, prot=prots, filename='figures/acf_plato_short.png')



.. image:: timeseries_analysis_files/timeseries_analysis_25_0.png


.. code:: ipython3

    IDP_123_ACF_FILT_TIMESERIES = np.c_[p_acf, acf]
    IDP_123_PROT_TIMESERIES = np.c_[prots, np.full (prots.size, -1), np.full (prots.size, -1),
                                    hacf, gacf, np.arange (prots.size)+1]
    np.savetxt ('data_products/IDP_123_PROT_TIMESERIES_PLATO.dat', 
                IDP_123_PROT_TIMESERIES)
    np.savetxt ('data_products/IDP_123_ACF_FILT_TIMESERIES_PLATO.dat', 
                IDP_123_ACF_FILT_TIMESERIES)

PLATO simulation: Long term modulation analysis
-----------------------------------------------

This time, we do not consider filtered out the data in order to consider
long term modulations. We put a period threshold at 90 days to consider
only long period in the postprocessing of our analysis.

.. code:: ipython3

    p_acf, acf = sp.compute_acf (s0, dt, normalise=True, pthresh=pthresh, smooth_period=30,
                                    use_scipy_correlate=True, smooth=True, verbose=True)
    _, hacf, gacf, _, pmods, hacf, gacf = sp.find_period_acf (p_acf, acf, pthresh=pthresh)
    fig = sp.plot_acf (p_acf, acf, prot=pmods, filename='figures/acf_plato_long.png')


.. parsed-literal::

    ACF was smoothed with a period 30.00 days



.. image:: timeseries_analysis_files/timeseries_analysis_29_1.png


.. code:: ipython3

    IDP_123_ACF_TIMESERIES = np.c_[p_acf, acf]
    IDP_123_LONGTERM_MODULATION_TIMESERIES = np.c_[pmods, np.full (pmods.size, -1), np.full (pmods.size, -1),
                                                                    hacf, gacf, np.arange (pmods.size)+1]
    np.savetxt ('data_products/IDP_123_LONGTERM_MODULATION_TIMESERIES_PLATO.dat', 
                IDP_123_PROT_TIMESERIES)
    np.savetxt ('data_products/IDP_123_ACF_TIMESERIES_PLATO.dat', 
                IDP_123_ACF_TIMESERIES)
    df = pd.DataFrame (data=IDP_123_LONGTERM_MODULATION_TIMESERIES)
    df




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>310.678567</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.462692</td>
          <td>0.329725</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>328.845118</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.282649</td>
          <td>0.320247</td>
          <td>2.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>603.628081</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.180539</td>
          <td>0.127609</td>
          <td>3.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>654.579144</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.010281</td>
          <td>0.070637</td>
          <td>4.0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>671.849867</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>-1.000000</td>
          <td>0.050842</td>
          <td>5.0</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    df.to_latex (buf='data_products/idp_msap4_02_idp_longterm_modulation_timeseries.tex', 
                 formatters=['{:.2f}'.format, '{:.0f}'.format, '{:.0f}'.format,
                             '{:.2f}'.format, '{:.2f}'.format, '{:.0f}'.format,],  
                 index=False, header=False)
