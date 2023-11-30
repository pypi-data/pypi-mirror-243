Time series analysis (MSAP4-02)
===============================

.. code:: ipython3

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

.. code:: ipython3

    import plato_msap4_demonstrator as msap4
    import plato_msap4_demonstrator_datasets.plato_sim_dataset as plato_sim_dataset

K2: Preprocessing
-----------------

This first part include preprocessing tasks that are not actually
included in MSAP4-02 but are useful for the subsequent analysis.

.. code:: ipython3

    t, s0, dt = msap4.load_k2_example ()

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

    p_acf, acf = msap4.compute_acf (s0, dt, normalise=True,
                                    use_scipy_correlate=True, smooth=True, verbose=True)
    _, _, _, _, prots, hacf, gacf = msap4.find_period_acf (p_acf, acf, pcutoff=pcutoff)
    fig = msap4.plot_acf (p_acf, acf, prot=prots, filename='figures/acf_k2.png')


.. parsed-literal::

    /Users/sbreton/miniconda3/envs/main-3.9/lib/python3.9/site-packages/plato_msap4_demonstrator/correlation.py:80: RuntimeWarning: divide by zero encountered in true_divide
      freq = 1/p_ls


.. parsed-literal::

    ACF was smoothed with a period 0.10 days



.. image:: timeseries_analysis_files/timeseries_analysis_10_2.png


We can take a look at the values we have extracted from the ACF. Most
often, the rotation period can be linked to the first value of the
``prots`` array.

.. code:: ipython3

    prots[0], hacf[0], gacf[0]




.. parsed-literal::

    (2.6765510971308686, 0.8254231148777905, 1.250446358444243)



Finally we create the intermediate data product.

.. code:: ipython3

    IDP_123_ACF_TIMESERIES = np.c_[p_acf, acf]
    IDP_123_PROT_TIMESERIES = np.c_[prots, np.full (prots.size, -1), np.full (prots.size, -1),
                                    hacf, gacf, np.arange (prots.size)+1]
    np.savetxt ('data_products/IDP_123_PROT_TIMESERIES_K2.dat', 
                IDP_123_PROT_TIMESERIES)
    np.savetxt ('data_products/IDP_123_ACF_TIMESERIES_K2.dat', 
                IDP_123_ACF_TIMESERIES)
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
          <td>0.825423</td>
          <td>1.250446</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>5.271375</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.783692</td>
          <td>1.170875</td>
          <td>2.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>7.947927</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.657622</td>
          <td>1.006760</td>
          <td>3.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10.583614</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.603111</td>
          <td>0.933207</td>
          <td>4.0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>13.301029</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.494050</td>
          <td>0.760850</td>
          <td>5.0</td>
        </tr>
        <tr>
          <th>5</th>
          <td>15.854990</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.448485</td>
          <td>0.760193</td>
          <td>6.0</td>
        </tr>
        <tr>
          <th>6</th>
          <td>18.592836</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.420432</td>
          <td>0.737416</td>
          <td>7.0</td>
        </tr>
        <tr>
          <th>7</th>
          <td>21.187660</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.358807</td>
          <td>0.656044</td>
          <td>8.0</td>
        </tr>
        <tr>
          <th>8</th>
          <td>23.884643</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.361433</td>
          <td>0.638998</td>
          <td>9.0</td>
        </tr>
        <tr>
          <th>9</th>
          <td>26.499899</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.287491</td>
          <td>0.446773</td>
          <td>10.0</td>
        </tr>
        <tr>
          <th>10</th>
          <td>29.156018</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.281729</td>
          <td>0.523091</td>
          <td>11.0</td>
        </tr>
        <tr>
          <th>11</th>
          <td>31.791706</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.219678</td>
          <td>0.436155</td>
          <td>12.0</td>
        </tr>
        <tr>
          <th>12</th>
          <td>34.447826</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.205879</td>
          <td>0.390640</td>
          <td>13.0</td>
        </tr>
        <tr>
          <th>13</th>
          <td>36.960923</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.155496</td>
          <td>0.311252</td>
          <td>14.0</td>
        </tr>
        <tr>
          <th>14</th>
          <td>39.657906</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.145735</td>
          <td>0.275303</td>
          <td>15.0</td>
        </tr>
        <tr>
          <th>15</th>
          <td>42.109708</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.125178</td>
          <td>0.238814</td>
          <td>16.0</td>
        </tr>
        <tr>
          <th>16</th>
          <td>44.806691</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.121583</td>
          <td>0.226077</td>
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


.. parsed-literal::

    /var/folders/z1/83qr1p117c53sns4d4msv6kdw50fz0/T/ipykernel_5268/2750549929.py:1: FutureWarning: In future versions `DataFrame.to_latex` is expected to utilise the base implementation of `Styler.to_latex` for formatting and rendering. The arguments signature may therefore change. It is recommended instead to use `DataFrame.style.to_latex` which also contains additional functionality.
      df.to_latex (buf='data_products/idp_msap4_02_idp_prot_timeseries.tex',


Note that, due to the short length of this light curve, we do not show
for this first case the analysis of long term modulations.

PLATO simulation: Preprocessing
-------------------------------

This first part include preprocessing tasks that are not actually
included in MSAP4-02 but are useful for the subsequent analysis.

.. code:: ipython3

    filename = msap4.get_target_filename (plato_sim_dataset, '040', filetype='csv')
    t, s0, dt = msap4.load_resource (filename)

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

    s = msap4.preprocess (t, s0, cut=55)
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

    p_acf, acf = msap4.compute_acf (s, dt, normalise=True,
                                    use_scipy_correlate=True, smooth=True)
    _, _, _, _, prots, hacf, gacf = msap4.find_period_acf (p_acf, acf, pcutoff=pcutoff)
    fig = msap4.plot_acf (p_acf, acf, prot=prots, filename='figures/acf_plato_short.png')


.. parsed-literal::

    /Users/sbreton/miniconda3/envs/main-3.9/lib/python3.9/site-packages/plato_msap4_demonstrator/correlation.py:80: RuntimeWarning: divide by zero encountered in true_divide
      freq = 1/p_ls



.. image:: timeseries_analysis_files/timeseries_analysis_25_1.png


.. code:: ipython3

    IDP_123_ACF_TIMESERIES = np.c_[p_acf, acf]
    IDP_123_PROT_TIMESERIES = np.c_[prots, np.full (prots.size, -1), np.full (prots.size, -1),
                                    hacf, gacf, np.arange (prots.size)+1]
    np.savetxt ('data_products/IDP_123_PROT_TIMESERIES_PLATO.dat', 
                IDP_123_PROT_TIMESERIES)
    np.savetxt ('data_products/IDP_123_ACF_TIMESERIES_PLATO.dat', 
                IDP_123_ACF_TIMESERIES)

PLATO simulation: Long term modulation analysis
-----------------------------------------------

This time, we do not consider filtered out the data in order to consider
long term modulations. We put a period threshold at 90 days to consider
only long period in the postprocessing of our analysis.

.. code:: ipython3

    p_acf, acf = msap4.compute_acf (s0, dt, normalise=True, pthresh=pthresh, smooth_period=30,
                                    use_scipy_correlate=True, smooth=True, verbose=True)
    _, hacf, gacf, _, pmods, hacf, gacf = msap4.find_period_acf (p_acf, acf, pthresh=pthresh)
    fig = msap4.plot_acf (p_acf, acf, prot=pmods, filename='figures/acf_plato_long.png')


.. parsed-literal::

    ACF was smoothed with a period 30.00 days



.. image:: timeseries_analysis_files/timeseries_analysis_29_1.png


.. code:: ipython3

    IDP_123_LONGTERM_MODULATION_TIMESERIES = np.c_[pmods, np.full (pmods.size, -1), np.full (pmods.size, -1),
                                                                    hacf, gacf, np.arange (pmods.size)+1]
    np.savetxt ('data_products/IDP_123_LONGTERM_MODULATION_TIMESERIES_PLATO.dat', 
                IDP_123_PROT_TIMESERIES)
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
          <td>0.329725</td>
          <td>0.462692</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>328.845118</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.320247</td>
          <td>0.282649</td>
          <td>2.0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>603.628081</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.127609</td>
          <td>0.180539</td>
          <td>3.0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>654.579144</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.070637</td>
          <td>0.010281</td>
          <td>4.0</td>
        </tr>
        <tr>
          <th>4</th>
          <td>671.849867</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.050842</td>
          <td>-1.000000</td>
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


.. parsed-literal::

    /var/folders/z1/83qr1p117c53sns4d4msv6kdw50fz0/T/ipykernel_5268/3697175569.py:1: FutureWarning: In future versions `DataFrame.to_latex` is expected to utilise the base implementation of `Styler.to_latex` for formatting and rendering. The arguments signature may therefore change. It is recommended instead to use `DataFrame.style.to_latex` which also contains additional functionality.
      df.to_latex (buf='data_products/idp_msap4_02_idp_longterm_modulation_timeseries.tex',

