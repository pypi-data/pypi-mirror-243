Fourier analysis (MSAP4-01A)
============================

.. code:: ipython3

    import plato_msap4_demonstrator as msap4
    import plato_msap4_demonstrator_datasets.plato_sim_dataset as plato_sim_dataset

K2: Rotation period analysis
----------------------------

.. code:: ipython3

    t, s, dt = msap4.load_k2_example ()

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s!=0]-t[0], s[s!=0], color='black', 
                marker='o', s=1)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    fig.tight_layout ()



.. image:: fourier_analysis_files/fourier_analysis_4_0.png


As we want to recover rotation periods below 45 days, we only consider
the section of the periodogram verifying
:math:`P < P_\mathrm{cutoff} = 45` days.

.. code:: ipython3

    pcutoff = 45

As a preprocessing step, we compute the Lomb-Scargle periodogram (in the
SAS framework, it will be directyly provided by MSAP1).

.. code:: ipython3

    p_ps, ps_object = msap4.compute_lomb_scargle (t, s)
    ls = ps_object.power_standard_norm

Now we perform the periodogram analysis.

.. code:: ipython3

    cond = p_ps < pcutoff
    prot, e_p, E_p, param, h_ps = msap4.compute_prot_err_gaussian_fit_chi2_distribution (p_ps[cond], ls[cond], n_profile=20, 
                                                                                         threshold=0.1, plot_procedure=False,
                                                                                         verbose=False)
    msap4.plot_ls (p_ps, ls, filename='figures/fourier_k2.png', param_profile=param, 
                   logscale=False, xlim=(0.1, 5))
    IDP_123_PROT_FOURIER = msap4.prepare_idp_fourier (param, h_ps, ls.size,
                                                      pcutoff=pcutoff, pthresh=None,
                                                      fapcutoff=1e-6)
    
    df = pd.DataFrame (data=IDP_123_PROT_FOURIER)
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
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2.787376</td>
          <td>0.027603</td>
          <td>0.028161</td>
          <td>0.422299</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1.393418</td>
          <td>0.013796</td>
          <td>0.014075</td>
          <td>0.216592</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>2</th>
          <td>0.779115</td>
          <td>0.007714</td>
          <td>0.007870</td>
          <td>0.057243</td>
          <td>1.000000e-16</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: fourier_analysis_files/fourier_analysis_10_1.png


.. code:: ipython3

    df.to_latex (buf='data_products/idp_123_prot_fourier_k2_211015853.tex', 
                 formatters=['{:.2f}'.format, '{:.2f}'.format, '{:.2f}'.format,
                             '{:.2f}'.format, '{:.0e}'.format],  
                 index=False, header=False)
    np.savetxt ('data_products/IDP_123_PROT_FOURIER_K2.dat', 
                 IDP_123_PROT_FOURIER)


.. parsed-literal::

    /var/folders/z1/83qr1p117c53sns4d4msv6kdw50fz0/T/ipykernel_4275/3364933883.py:1: FutureWarning: In future versions `DataFrame.to_latex` is expected to utilise the base implementation of `Styler.to_latex` for formatting and rendering. The arguments signature may therefore change. It is recommended instead to use `DataFrame.style.to_latex` which also contains additional functionality.
      df.to_latex (buf='data_products/idp_123_prot_fourier_k2_211015853.tex',


This time, we are interested in recovering long term modulations. We
consider the section of the periodogram verifying
:math:`P > P_\mathrm{tresh} = 90` days.

PLATO: Rotation period analysis
-------------------------------

.. code:: ipython3

    filename = msap4.get_target_filename (plato_sim_dataset, '040', filetype='csv')
    t, s, dt = msap4.load_resource (filename)

.. code:: ipython3

    fig, ax = plt.subplots (1, 1, figsize=(8,4))
    
    ax.scatter (t[s!=0]-t[0], s[s!=0], color='black', 
                marker='o', s=1)
    
    ax.set_xlabel ('Time (day)')
    ax.set_ylabel ('Flux (ppm)')
    
    fig.tight_layout ()



.. image:: fourier_analysis_files/fourier_analysis_15_0.png


As we want to recover rotation periods below 45 days, we only consider
the section of the periodogram verifying
:math:`P < P_\mathrm{cutoff} = 45` days.

.. code:: ipython3

    pcutoff = 45

As a preprocessing step, we compute the Lomb-Scargle periodogram (in the
SAS framework, it will be directyly provided by MSAP1).

.. code:: ipython3

    p_ps, ps_object = msap4.compute_lomb_scargle (t, s)
    ls = ps_object.power_standard_norm

Now we perform the periodogram analysis.

.. code:: ipython3

    cond = p_ps < pcutoff
    prot, e_p, E_p, param, h_ps = msap4.compute_prot_err_gaussian_fit_chi2_distribution (p_ps[cond], ls[cond], n_profile=20, 
                                                                                         threshold=0.1,
                                                                                         verbose=False)
    msap4.plot_ls (p_ps, ls, filename='figures/fourier_plato_short.png', param_profile=param, 
                   logscale=False, xlim=(1, pcutoff), ylim=(-0.01, 0.1))
    IDP_123_PROT_FOURIER = msap4.prepare_idp_fourier (param, h_ps, ls.size,
                                                      pcutoff=pcutoff, pthresh=None,
                                                      fapcutoff=1e-6)
    df = pd.DataFrame (data=IDP_123_PROT_FOURIER)
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
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>25.750841</td>
          <td>0.255524</td>
          <td>0.260698</td>
          <td>0.041200</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>1</th>
          <td>36.470886</td>
          <td>0.428032</td>
          <td>0.438321</td>
          <td>0.032378</td>
          <td>1.000000e-16</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: fourier_analysis_files/fourier_analysis_21_1.png


.. code:: ipython3

    df.to_latex (buf='data_products/idp_123_prot_fourier_plato_040.tex', 
                 formatters=['{:.2f}'.format, '{:.2f}'.format, '{:.2f}'.format,
                             '{:.2f}'.format, '{:.0e}'.format],  
                 index=False, header=False)
    np.savetxt ('data_products/IDP_123_PROT_FOURIER_PLATO.dat', 
                 IDP_123_PROT_FOURIER)


.. parsed-literal::

    /var/folders/z1/83qr1p117c53sns4d4msv6kdw50fz0/T/ipykernel_4275/1520620131.py:1: FutureWarning: In future versions `DataFrame.to_latex` is expected to utilise the base implementation of `Styler.to_latex` for formatting and rendering. The arguments signature may therefore change. It is recommended instead to use `DataFrame.style.to_latex` which also contains additional functionality.
      df.to_latex (buf='data_products/idp_123_prot_fourier_plato_040.tex',


PLATO: Long term modulation analysis
------------------------------------

This time, we are interested in recovering long term modulations. We
consider the section of the periodogram verifying
:math:`P > P_\mathrm{tresh} = 90` days.

.. code:: ipython3

    pthresh = 90

As a preprocessing step, we compute the Lomb-Scargle periodogram (in the
SAS framework, it will be directyly provided by MSAP1).

.. code:: ipython3

    p_ps, ps_object = msap4.compute_lomb_scargle (t, s)
    ls = ps_object.power_standard_norm

Now we perform the periodogram analysis.

.. code:: ipython3

    plongterm, e_p, E_p, param, h_ps = msap4.compute_prot_err_gaussian_fit_chi2_distribution (p_ps[p_ps>pthresh], ls[p_ps>pthresh], 
                                                                                              n_profile=5, threshold=0.1, verbose=False)
    fig = msap4.plot_ls (p_ps, ls, filename='figures/fourier_plato_long.png', param_profile=param, 
                        logscale=False, xlim=(1,8*pthresh))
    IDP_123_LONGTERM_MODULATION_FOURIER = msap4.prepare_idp_fourier (param, h_ps, ls.size,
                                                                     pcutoff=None, pthresh=pthresh,
                                                                     fapcutoff=1e-6)
    df = pd.DataFrame (data=IDP_123_LONGTERM_MODULATION_FOURIER)
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
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>347.127534</td>
          <td>31.561216</td>
          <td>38.575952</td>
          <td>0.500829</td>
          <td>1.000000e-16</td>
        </tr>
        <tr>
          <th>1</th>
          <td>700.965183</td>
          <td>64.289193</td>
          <td>78.730828</td>
          <td>0.130459</td>
          <td>1.000000e-16</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: fourier_analysis_files/fourier_analysis_29_1.png


.. code:: ipython3

    df.to_latex (buf='data_products/idp_123_longterm_modulation_fourier_plato_040.tex', 
                 formatters=['{:.2f}'.format, '{:.2f}'.format, '{:.2f}'.format,
                             '{:.2f}'.format, '{:.0e}'.format],  
                 index=False, header=False)
    np.savetxt ('data_products/IDP_123_LONGTERM_MODULATION_FOURIER_PLATO.dat', 
                 IDP_123_LONGTERM_MODULATION_FOURIER)


.. parsed-literal::

    /var/folders/z1/83qr1p117c53sns4d4msv6kdw50fz0/T/ipykernel_4275/2522956954.py:1: FutureWarning: In future versions `DataFrame.to_latex` is expected to utilise the base implementation of `Styler.to_latex` for formatting and rendering. The arguments signature may therefore change. It is recommended instead to use `DataFrame.style.to_latex` which also contains additional functionality.
      df.to_latex (buf='data_products/idp_123_longterm_modulation_fourier_plato_040.tex',

