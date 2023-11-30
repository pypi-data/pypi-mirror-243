Analysis framework for rotation period extraction (MSAP4-03)
============================================================

This notebook provide an example of the analysis performed by the PLATO
MSAP4-03 submodules: results from Lomb-Scargle periodogram,
autocorrelation functions and composite spectrum are used to produce a
set of features exploited by an existing instance of ROOSTER to return
the final rotation period of the analysed target. You will find that
what is done here is very similar to the ROOSTER tutorial notebook
(``rooster_training_framework``, you should run it before doing this
tutorial), the only big difference is actually that we will use here a
pre-trained ROOSTER instance !

Here, the MSAP4-01A and MSAP4-02 steps required to feed MSAP4-03 are
included in order to be able to run this notebook independently from the
MSAP4-01A and MSAP4-02 notebooks.

Note that, due its significant computing time, the MSAP4-01B component
dedicated to background analysis is executed independently in another
notebook.

**Note:** This notebook has been designed for the purpose of scientific
justification of MSAP4-03. The notebook illustrated the precise
flowchart envisaged for MSAP4-03 is cs_rooster_sph_analysis.ipynb

.. code:: ipython3

    import star_privateer as sp

A simple example
----------------

.. code:: ipython3

    import importlib
    import tqdm
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    
    if not os.path.exists ('stellar_analysis_features') :
        os.mkdir ('stellar_analysis_features')
    if not os.path.exists ('stellar_analysis_plots') :
        os.mkdir ('stellar_analysis_plots')    

Our working case is KIC 3733735, a well-known *Kepler* fast rotating
star.

.. code:: ipython3

    filename = sp.get_target_filename (sp.timeseries, '003733735')
    t, s, dt = sp.load_resource (filename)

The first thing we have to do is run the analysis pipeline. In
particular, we can take a look at the plots made from the different
analysis methods.

.. code:: ipython3

    p_in = np.linspace (0, 100, 1000)
    (p_ps, p_acf, ps, acf, 
     cs, features, feature_names, _) = sp.analysis_pipeline (t, s, periods_in=p_in, figsize=(8,10),
                                                                wavelet_analysis=False, plot=True,
                                                                filename='stellar_analysis_plots/003733735.png',
                                                            )



.. image:: stellar_analysis_framework_files/stellar_analysis_framework_7_0.png


We then save the results to a csv file:

.. code:: ipython3

    fileout = 'stellar_analysis_features/003733735.csv'
    df = sp.save_features (fileout, 3733735, features, feature_names)

As in the previous tutorial, let’s build a feature catalog. This is
actually not required here because we are analysing only one star, but
this step allows to ROOSTER-analyse several stars together with a simple
framework.

.. code:: ipython3

    df = sp.build_catalog_features ('stellar_analysis_features')

Then, let’s load the ROOSTER instance that we have trained in the
previous tutorial:

.. code:: ipython3

    chicken = sp.load_rooster_instance (filename='rooster_instances/rooster_tutorial')

As previously, let’s split the DataFrame into ROOSTER required inputs:

.. code:: ipython3

    (target_id, p_candidates, 
     e_p_candidates, E_p_candidates, 
     features, feature_names) = sp.create_rooster_feature_inputs (df, return_err=True)

Here, we can see that there is actually (almost) nothing to do, as the
three methods have yielded the same :math:`P_\mathrm{rot}` estimate.
However, we need ROOSTER to provide us with the rotation score of the
target. ROOSTER will also select one of the three ``p_candidates`` as
the final estimate for our target.

.. code:: ipython3

    p_candidates




.. parsed-literal::

    array([[2.55994471, 2.59507401, 2.49247385]])



The ``analyseSet`` function implemented in ROOSTER allows to analyse the
features we extracted with the analysis pipeline. By providing
``feature_names``, we ensure that ROOSTER was trained with the same
features that those we extracted.

.. code:: ipython3

    rotation_score, prot, e_p, E_p = chicken.analyseSet (features, p_candidates, e_p_err=e_p_candidates,
                                                         E_p_err=E_p_candidates, feature_names=feature_names)

We finally get the rotation score and the final :math:`P_\mathrm{rot}`.
A rotation score above 0.5 means that the ROOSTER analysis favours a
detection of stellar surface rotation signal.

.. code:: ipython3

    rotation_score, prot, e_p, E_p




.. parsed-literal::

    (array([0.82]), array([2.55994471]), array([0.0604509]), array([0.0634239]))



Analysing a PLATO simulated light curves dataset
------------------------------------------------

In order to illustrate the pipeline features described above, we can
apply the pipeline to a larger dataset of 255 PLATO simulated light
curves in order to check what we recover.

.. code:: ipython3

    import plato_msap4_demonstrator_datasets.plato_sim_dataset as plato_sim_dataset
    
    if not os.path.exists ('plato_sim_features') :
        os.mkdir ('plato_sim_features')
    if not os.path.exists ('plato_sim_plots') :
        os.mkdir ('plato_sim_plots')

.. code:: ipython3

    list_id = sp.get_list_targets (plato_sim_dataset)

Note that in the current version of the demonstrator, we apply a 55-day
high-pass finite impulse response filter to the simulated light curves
(``preprocess``) function in order to remove low-frequency systematics
while preserving at most the signature of stellar activity in the data.
In the future, data product calibrated specifically for MSAP4 or
dedicated calibration step aimed at reducing systematics at most would
allow to significantly improve the analysis performances.

.. code:: ipython3

    for elt in tqdm.tqdm (list_id) :
        str_elt = str (elt).zfill (3)
        fileout = 'plato_sim_features/{}.csv'.format(str_elt)
        filename = sp.get_target_filename (plato_sim_dataset, str_elt, filetype='csv')
        if not os.path.exists (fileout) :
            t, s, dt = sp.load_resource (filename)
            s = sp.preprocess (t, s, cut=55)
            (p_ps, p_acf, ps, acf, 
             cs, features, feature_names, _) = sp.analysis_pipeline (t, s, periods_in=p_in,
                                                                        wavelet_analysis=False, plot=True,
                                                                        filename='plato_sim_plots/{}.png'.format(str_elt),
                                                                        figsize=(10,16),
                                                                        lw=1, dpi=300, smooth_acf=True)
            df = sp.save_features (fileout, str_elt, features, feature_names)


.. parsed-literal::

    100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 255/255 [00:00<00:00, 44256.53it/s]


We can now analyse the obtained features with ROOSTER to provide our
final results.

.. code:: ipython3

    df = sp.build_catalog_features ('plato_sim_features')
    (target_id, p_candidates, 
     e_p_candidates, E_p_candidates, 
     features, feature_names) = sp.create_rooster_feature_inputs (df, return_err=True)
    rotation_score, prot, e_p, E_p = chicken.analyseSet (features, p_candidates, e_p_err=e_p_candidates,
                                                         E_p_err=E_p_candidates, feature_names=feature_names)
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
          <th>prot_ps</th>
          <th>prot_acf</th>
          <th>prot_cs</th>
          <th>e_prot_ps</th>
          <th>E_prot_ps</th>
          <th>e_prot_acf</th>
          <th>E_prot_acf</th>
          <th>e_prot_cs</th>
          <th>E_prot_cs</th>
          <th>sph_ps</th>
          <th>sph_acf</th>
          <th>sph_cs</th>
          <th>h_ps</th>
          <th>fa_prob_ps</th>
          <th>hacf</th>
          <th>gacf</th>
          <th>hcs</th>
        </tr>
        <tr>
          <th>target_id</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>43.384664</td>
          <td>32.631736</td>
          <td>29.219674</td>
          <td>1.152496</td>
          <td>1.216480</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.242817</td>
          <td>1.242817</td>
          <td>754.547891</td>
          <td>747.270985</td>
          <td>722.371710</td>
          <td>0.243752</td>
          <td>0.000000e+00</td>
          <td>0.204530</td>
          <td>0.417558</td>
          <td>0.457579</td>
        </tr>
        <tr>
          <th>1</th>
          <td>33.054982</td>
          <td>11.208262</td>
          <td>16.348645</td>
          <td>4.861871</td>
          <td>6.916978</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>3.874861</td>
          <td>3.874861</td>
          <td>196.002432</td>
          <td>197.573001</td>
          <td>217.818959</td>
          <td>0.016114</td>
          <td>0.000000e+00</td>
          <td>-0.154258</td>
          <td>0.000649</td>
          <td>0.489209</td>
        </tr>
        <tr>
          <th>2</th>
          <td>17.353865</td>
          <td>18.215161</td>
          <td>17.308824</td>
          <td>2.362525</td>
          <td>3.234358</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.424494</td>
          <td>0.424494</td>
          <td>130.530199</td>
          <td>132.035535</td>
          <td>130.541438</td>
          <td>0.083866</td>
          <td>0.000000e+00</td>
          <td>0.271299</td>
          <td>0.626426</td>
          <td>0.889873</td>
        </tr>
        <tr>
          <th>3</th>
          <td>21.034988</td>
          <td>20.923477</td>
          <td>20.924822</td>
          <td>2.248453</td>
          <td>2.852080</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.727613</td>
          <td>0.727613</td>
          <td>107.469907</td>
          <td>107.619504</td>
          <td>107.619504</td>
          <td>0.152170</td>
          <td>0.000000e+00</td>
          <td>0.552096</td>
          <td>1.054497</td>
          <td>0.983289</td>
        </tr>
        <tr>
          <th>4</th>
          <td>28.923109</td>
          <td>7.708284</td>
          <td>8.893554</td>
          <td>0.722536</td>
          <td>0.760135</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>2.896222</td>
          <td>2.896222</td>
          <td>156.269982</td>
          <td>149.832641</td>
          <td>149.472409</td>
          <td>0.011790</td>
          <td>4.780577e-250</td>
          <td>-0.077873</td>
          <td>0.002125</td>
          <td>0.357145</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>250</th>
          <td>31.552483</td>
          <td>29.027592</td>
          <td>31.219175</td>
          <td>5.676881</td>
          <td>8.918001</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>3.982823</td>
          <td>3.982823</td>
          <td>215.787517</td>
          <td>205.336661</td>
          <td>202.222122</td>
          <td>0.160314</td>
          <td>0.000000e+00</td>
          <td>0.561387</td>
          <td>1.081777</td>
          <td>0.855115</td>
        </tr>
        <tr>
          <th>251</th>
          <td>20.416312</td>
          <td>19.117933</td>
          <td>20.219246</td>
          <td>2.109279</td>
          <td>2.665563</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.734646</td>
          <td>1.734646</td>
          <td>184.403461</td>
          <td>175.416258</td>
          <td>184.363934</td>
          <td>0.160625</td>
          <td>0.000000e+00</td>
          <td>0.397343</td>
          <td>0.852581</td>
          <td>0.851365</td>
        </tr>
        <tr>
          <th>252</th>
          <td>36.534454</td>
          <td>37.638648</td>
          <td>36.899833</td>
          <td>4.307302</td>
          <td>5.618974</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>4.736251</td>
          <td>4.736251</td>
          <td>1353.429169</td>
          <td>1370.863674</td>
          <td>1358.401532</td>
          <td>0.250936</td>
          <td>0.000000e+00</td>
          <td>0.752538</td>
          <td>1.515209</td>
          <td>0.986710</td>
        </tr>
        <tr>
          <th>253</th>
          <td>17.353865</td>
          <td>17.416555</td>
          <td>17.478516</td>
          <td>3.479639</td>
          <td>5.770656</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>2.233398</td>
          <td>2.233398</td>
          <td>163.173697</td>
          <td>163.119816</td>
          <td>163.063621</td>
          <td>0.078761</td>
          <td>0.000000e+00</td>
          <td>0.332430</td>
          <td>0.760885</td>
          <td>0.981911</td>
        </tr>
        <tr>
          <th>254</th>
          <td>18.760936</td>
          <td>18.819324</td>
          <td>19.007517</td>
          <td>2.696398</td>
          <td>3.768938</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.604807</td>
          <td>0.604807</td>
          <td>1162.545259</td>
          <td>1161.618942</td>
          <td>1157.821920</td>
          <td>0.253955</td>
          <td>0.000000e+00</td>
          <td>0.343084</td>
          <td>0.878379</td>
          <td>0.973676</td>
        </tr>
      </tbody>
    </table>
    <p>255 rows × 17 columns</p>
    </div>



Next, let’s load the reference catalog for these simulated light curves
in order to compare the results from our pipeline with what was injected
in the data.

.. code:: ipython3

    prot_ref = sp.get_prot_ref (target_id, catalog='plato-sim')
    cond_0 = (rotation_score>0.5)
    cond_1 = (np.abs (prot - prot_ref) < 0.1 * prot_ref) 
    cond_2 = (np.abs (prot - prot_ref) < 0.1 * prot_ref) & (rotation_score>0.5)
    score_0 = target_id[cond_0].size / target_id.size
    score_1 = target_id[cond_1].size / target_id.size
    score_2 = target_id[cond_2].size / target_id.size
    score_0, score_1, score_2




.. parsed-literal::

    (0.9450980392156862, 0.6274509803921569, 0.6078431372549019)



The score computed here means that we were able to successfully detect a
rotation signal and recover the correct rotation period for about **61%
of the stars** in the sample. We can take a look at histograms to check
the rotation score of our population and to compare the input rotation
periods distribution to the one we recover.

.. code:: ipython3

    fig, (ax1, ax2) = plt.subplots (1, 2, figsize=(10, 4))
    
    bins = np.linspace (0, 1, 20, endpoint=False)
    ax1.hist (rotation_score, bins=bins, color='darkorange')
    ax1.axvline (0.5, ls='--', color='blue', lw=2)
    bins = np.linspace (0, 80, 20, endpoint=False)
    ax2.hist (prot, bins=bins, color='darkorange')
    ax2.hist (prot_ref, bins=bins, facecolor='none',
             edgecolor='black', label='Ref')
    
    ax1.set_ylabel (r'Number of stars')
    ax1.set_xlabel (r'Rotation score')
    ax2.set_xlabel (r'$P_\mathrm{rot}$ (day)')
    
    ax1.set_xlim (0, 1)
    ax2.set_xlim (0, 80)




.. parsed-literal::

    (0.0, 80.0)




.. image:: stellar_analysis_framework_files/stellar_analysis_framework_32_1.png

