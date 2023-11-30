ROOSTER training framework (MSAP4-03)
=====================================

This notebook provide an example of an analysis by the PLATO MSAP4
demonstrator of a set of stars with catalog-existing reference
:math:`P_\mathrm{rot}`, and use the set to train an instance of ROOSTER.

First we need to import the demonstrator module and the auxiliary module
containing the dataset we are going to work with.

**Note:** This notebook has been designed for the purpose of scientific
justification of MSAP4-03. The notebook illustrated the precise
flowchart envisaged for MSAP4-03 is cs_rooster_sph_analysis.ipynb

.. code:: ipython3

    import plato_msap4_demonstrator as msap4
    import plato_msap4_demonstrator_datasets.kepler_dataset as kepler_dataset

We also need to import some other modules to run the notebook and to
check that the outputs directory that we need exist

.. code:: ipython3

    import importlib
    import tqdm
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    
    if not os.path.exists ('rooster_training_features') :
        os.mkdir ('rooster_training_features')
    if not os.path.exists ('rooster_training_plots') :
        os.mkdir ('rooster_training_plots')
    if not os.path.exists ('rooster_instances') :
        os.mkdir ('rooster_instances')

Running the analysis pipeline
-----------------------------

We are going to work with a sample of 1991 *Kepler* stars analysed by
Santos et al. (2019, 2021). The light curves have been calibrated with
the KEPSEISMIC method (see García et al. 2011, 2014), and all of them
have been filtered with a 55-day high-pass filter. We can get the
identifiers of the stars in the dataset with the following instruction:

.. code:: ipython3

    list_kic = msap4.get_list_targets (kepler_dataset)

The next step is to run the analysis pipeline on every light curve in
the dataset. The analysis pipeline in its default behaviour will compute
the Lomb-Scargle periodogram (LSP) of the light curve as well as its
auto-correlation function (ACF). ACF and LSP will then be used to
compute a composite spectrum (CS), obtained by multiplying one by
another. The feature computed for each stars are stored in a dedicated
csv file identified by the star identifier (in this case, the KIC of the
star).

.. code:: ipython3

    p_in = np.linspace (0, 100, 1000)
    for kic in tqdm.tqdm (list_kic) :
        str_kic = str (kic).zfill (9)
        fileout = 'rooster_training_features/{}.csv'.format(str_kic)
        filename = msap4.get_target_filename (kepler_dataset, str_kic)
        if not os.path.exists (fileout) :
            t, s, dt = msap4.load_resource (filename)
            (p_ps, p_acf, ps, acf, 
             cs, features, feature_names) = msap4.analysis_pipeline (t, s, periods_in=p_in,
                                                                     wavelet_analysis=False, plot=True,
                                                                     filename='rooster_training_plots/{}.png'.format(str_kic),
                                                                     figsize=(10,16),
                                                                     lw=1, dpi=300, smooth_acf=True)
            df = msap4.save_features (fileout, kic, features, feature_names)


.. parsed-literal::

    100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1991/1991 [1:10:07<00:00,  2.11s/it]


After running the analysis pipeline, it is possible to concatenate the
feature obtained for each star into one big DataFrame.

.. code:: ipython3

    df = msap4.build_catalog_features ('rooster_training_features')

This is typically what the DataFrame is going to look like:

.. code:: ipython3

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
          <th>891901</th>
          <td>73.598094</td>
          <td>5.006284</td>
          <td>52.030213</td>
          <td>0.882710</td>
          <td>0.904334</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>5.793131</td>
          <td>5.793131</td>
          <td>782.552118</td>
          <td>604.416480</td>
          <td>773.134552</td>
          <td>0.121354</td>
          <td>0.0</td>
          <td>0.633684</td>
          <td>0.265200</td>
          <td>0.095594</td>
        </tr>
        <tr>
          <th>1162339</th>
          <td>73.048392</td>
          <td>39.232722</td>
          <td>52.151892</td>
          <td>11.328352</td>
          <td>16.348211</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.334090</td>
          <td>1.334090</td>
          <td>2266.134459</td>
          <td>2082.090930</td>
          <td>2150.902737</td>
          <td>0.285520</td>
          <td>0.0</td>
          <td>-0.568057</td>
          <td>0.001484</td>
          <td>0.069160</td>
        </tr>
        <tr>
          <th>1163248</th>
          <td>73.048768</td>
          <td>59.666638</td>
          <td>91.054034</td>
          <td>10.510133</td>
          <td>14.697001</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>4.333272</td>
          <td>4.333272</td>
          <td>541.300214</td>
          <td>541.808769</td>
          <td>551.965885</td>
          <td>0.092878</td>
          <td>0.0</td>
          <td>0.169691</td>
          <td>0.373241</td>
          <td>0.883819</td>
        </tr>
        <tr>
          <th>1164583</th>
          <td>50.378386</td>
          <td>43.850828</td>
          <td>46.669255</td>
          <td>12.525927</td>
          <td>25.164926</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>5.712886</td>
          <td>5.712886</td>
          <td>1650.421415</td>
          <td>1644.008810</td>
          <td>1698.895451</td>
          <td>0.124362</td>
          <td>0.0</td>
          <td>0.342296</td>
          <td>0.678006</td>
          <td>0.467618</td>
        </tr>
        <tr>
          <th>1433067</th>
          <td>73.048497</td>
          <td>35.329934</td>
          <td>47.031731</td>
          <td>11.612365</td>
          <td>16.946332</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.743159</td>
          <td>1.743159</td>
          <td>1219.810610</td>
          <td>1192.928427</td>
          <td>1197.588777</td>
          <td>0.175185</td>
          <td>0.0</td>
          <td>-0.559881</td>
          <td>0.000288</td>
          <td>0.140650</td>
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
          <th>12647815</th>
          <td>10.435607</td>
          <td>10.400735</td>
          <td>10.457896</td>
          <td>0.403142</td>
          <td>0.436987</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>0.152860</td>
          <td>0.152860</td>
          <td>4727.467867</td>
          <td>4733.483163</td>
          <td>4721.753966</td>
          <td>0.262546</td>
          <td>0.0</td>
          <td>0.627364</td>
          <td>1.026059</td>
          <td>0.532050</td>
        </tr>
        <tr>
          <th>12737258</th>
          <td>40.582931</td>
          <td>77.586648</td>
          <td>69.544323</td>
          <td>4.159244</td>
          <td>5.218136</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>3.577753</td>
          <td>3.577753</td>
          <td>2135.495994</td>
          <td>2155.693110</td>
          <td>2164.787863</td>
          <td>0.146861</td>
          <td>0.0</td>
          <td>0.431254</td>
          <td>-1.000000</td>
          <td>0.542491</td>
        </tr>
        <tr>
          <th>12784167</th>
          <td>18.262306</td>
          <td>12.505398</td>
          <td>91.216340</td>
          <td>0.824439</td>
          <td>0.905366</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>3.206358</td>
          <td>3.206358</td>
          <td>632.040500</td>
          <td>609.092436</td>
          <td>650.432771</td>
          <td>0.072066</td>
          <td>0.0</td>
          <td>0.102950</td>
          <td>0.000197</td>
          <td>2.136317</td>
        </tr>
        <tr>
          <th>12834290</th>
          <td>52.692311</td>
          <td>56.049453</td>
          <td>53.100597</td>
          <td>10.789249</td>
          <td>18.146115</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>1.528117</td>
          <td>1.528117</td>
          <td>528.632031</td>
          <td>525.789101</td>
          <td>531.063571</td>
          <td>0.079475</td>
          <td>0.0</td>
          <td>0.100199</td>
          <td>0.262818</td>
          <td>0.675579</td>
        </tr>
        <tr>
          <th>12834663</th>
          <td>89.966120</td>
          <td>13.118167</td>
          <td>91.094432</td>
          <td>8.178801</td>
          <td>9.996320</td>
          <td>-1.0</td>
          <td>-1.0</td>
          <td>8.888001</td>
          <td>8.888001</td>
          <td>1084.671035</td>
          <td>996.803485</td>
          <td>1084.671035</td>
          <td>0.280246</td>
          <td>0.0</td>
          <td>0.147318</td>
          <td>0.006072</td>
          <td>1.505906</td>
        </tr>
      </tbody>
    </table>
    <p>1991 rows × 17 columns</p>
    </div>



Training and testing ROOSTER
----------------------------

Now that we have analysed a large sample of stars, we are able to use it
to train the random forest ROOSTER methodology (see Breton et al. 2021).
First, let’s (arbitrarily) divide our DataFrame into a training set and
a test set.

.. code:: ipython3

    df_train = df.loc[df.index[::2]]
    df_test = df.loc[df.index[1::2]]

The DataFrames let us obtain all the input we require to train and test
ROOSTER:

.. code:: ipython3

    training_id, training_p_candidates, training_features, feature_names = msap4.create_rooster_feature_inputs (df_train)
    test_id, test_p_candidates, test_features, test_feature_names = msap4.create_rooster_feature_inputs (df_test)

Now, let’s instantiate a new ROOSTER object. The main attributes of
ROOSTER are its two random forest classifiers, ``RotClass`` and
``PeriodSel``. The properties of these classifiers can be specified by
the user by passing the optional arguments of
``sklearn.ensemble.RandomForestClassifier`` to the created ROOSTER
instance.

.. code:: ipython3

    seed = 104359357
    chicken = msap4.ROOSTER (n_estimators=100, random_state=np.random.RandomState (seed=seed))
    chicken.RotClass, chicken.PeriodSel




.. parsed-literal::

    (RandomForestClassifier(random_state=RandomState(MT19937) at 0x2761FD240),
     RandomForestClassifier(random_state=RandomState(MT19937) at 0x2761FD240))



The training is performed as follows:

.. code:: ipython3

    chicken.train (training_id, training_p_candidates,
                   training_features, feature_names=feature_names,
                   catalog='santos-19-21', verbose=True)


.. parsed-literal::

    Training RotClass with 405 stars with detected rotation and 494 without detected rotation.
    Training PeriodSel with 405 stars.


Once properly trained, ROOSTER performances can be assessed with our
test set:

.. code:: ipython3

    results = chicken.test (test_id, test_p_candidates, test_features, 
                            feature_names=test_feature_names, 
                            catalog='santos-19-21', verbose=True)


.. parsed-literal::

    Testing RotClass with 393 stars with detected rotation and 501 without detected rotation.
    Testing PeriodSel with 393 stars.


The score obtained during the test set can be accessed through the
``getScore`` function, as well as the number of elements used for the
training and the test steps.

.. code:: ipython3

    chicken.getScore ()




.. parsed-literal::

    (0.9261744966442953, 0.905852417302799)



.. code:: ipython3

    chicken.getNumberEltTrain ()




.. parsed-literal::

    (899, 405)



.. code:: ipython3

    chicken.getNumberEltTest ()




.. parsed-literal::

    (894, 393)



The :math:`P_\mathrm{rot}` computed by ROOSTER for the test set are
returned when calling the function and it can be interesting to plot the
distribution to compare it to the reference catalog values.

.. code:: ipython3

    prot_rooster = results[3]
    prot_ref = msap4.get_prot_ref (results[2], catalog='santos-19-21')

Let’s take a look at the corresponding histogram

.. code:: ipython3

    fig, ax = plt.subplots (1, 1)
    
    bins = np.linspace (0, 80, 20, endpoint=False)
    
    ax.hist (prot_rooster, bins=bins, color='darkorange', label='ROOSTER')
    ax.hist (prot_ref, bins=bins, facecolor='none',
            edgecolor='black', label='Ref')
    
    ax.set_xlabel (r'$P_\mathrm{rot}$ (day)')
    ax.set_ylabel (r'Number of stars')
    
    ax.legend ()




.. parsed-literal::

    <matplotlib.legend.Legend at 0x275957280>




.. image:: rooster_training_framework_files/rooster_training_framework_30_1.png


Finally, let’s save our trained ROOSTER instance to be able to use it
again later (for example in the next tutorial notebook !)

.. code:: ipython3

    chicken.save ('rooster_instances/rooster_tutorial')

