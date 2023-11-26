# pyENSDF

This project [[1]](#1) is a Python package providing access to, as well as manipulation and analysis methods for, the decay data from the Evaluated Nuclear Structure Data File (ENSDF) library [[2]](#2).  A total of 3226 data sets encompassing &alpha; (826), &beta;<sup>-</sup> (1124 + 6 double-&beta;<sup>-</sup>), and &epsilon;/&beta;<sup>+</sup> (1270) have been extracted from the ENSDF archive [[2]](#2), parsed and translated into a representative JavaScript Object Notation (JSON) format (descibed below).  The JSON-formatted data sets constitute a total of 92,782 deexcitation &gamma; rays associated with 40,638 levels.  Additionally, we also provide a Reference Input Parameter Library [[3]](#3) RIPL-translated format of the corresponding decay-scheme data.  These data sets are bundled together with the analysis toolkit.  A schematic illustrating the portion of the nuclear chart of relevance to the aforementioned decay data from ENSDF is shown in the figure below.

![ENSDF Nuclides](decay_nuclides.png?raw=true "Schematic showing portion of nuclear chart of relevance to the ENSDF-decay data sets")

The `pyENSDF` package provides users with a convenient means to access and manipulate the decay data from ENSDF [[2]](#2) with various methods to return all associated nuclear structure decay-scheme data including levels, spins, parities, &gamma;-ray information, etc.  An overview of some the methods available is provided in `Jupyter` notebook distributed with this package in the `notebook` folder.

All ENSDF decay-scheme data sets containing &gamma;-ray information have also been used to generate coincidence &gamma;-&gamma; and &gamma;-*X*-ray JSON data structures from the corresponding decay data set [[1]](#1).  In addition to the coincidence energies and absolute intensities, together with uncertainties, these data structures contain additional meta data parsed from the original ENSDF data structure allowing users to search for single energies (both &gamma; and *X*-ray) as well as coincidence pairs.  Refer to the corresponding `Jupyter` notebook provided with this project to see example use cases.

### Notes on ENSDF quantities

Although most quantities in ENSDF are normally-distributed symmetrical quantities associated with the equality `=` operator, the following exceptions (frequent in many cases) are also accounted for:

* All asymmetric quantities parsed in the original ENSDF dataset are symmetrized and their associated median-symmertized values and uncertainties are reported in the derived JSON data structures.
* All approximate `AP` values parsed in the original ENSDF dataset are reported with an assumed 50% uncertainty.
* All values parsed as limits (i.e., `LT`, `GT`, `GE`, `GE`) in the original ENSDF dataset are reported with an assumed 100% uncertainty.

# Building and installation

This project should be built and installed by executing the `installation.sh` script at the terminal command line of the project directory:

```Bash
$ git clone https://github.com/AaronMHurst/python_ensdf.git
$ cd python_ensdf
$ sh installation.sh
```

# Testing

A suite of Python modules containing 283 unit tests have been written for this project and are located in the `tests` folder.  To run the test suite and ensure they work with the Python environment, run `tox` in the project directory where the `tox.ini` file is also located:

```Bash
$ tox -r
```

This project has the following Python-package dependencies: `numpy`, `pandas`, and `pytest`.  The test session is automatically started after building against the required Python environment.

# Running the software

After the installation the `pyENSDF` scripts can be ran from any location by importing the package and making an instance of the `ENSDF` class:

```Bash
$ python
```
```python
>>> import pyENSDF as ensdf
>>> e = ensdf.ENSDF()
```

Most methods also require passing the `JSON`-formatted source data set as a list object.  To use the ENSDF decay-data sets:

```python
>>> edata = e.load_ensdf()
```

A `Jupyter` notebook is provided illustrating use of the various methods for access and manipulation of the ENSDF data.  To run the notebook from the terminal command line:

```Bash
$ cd notebook
$ jupyter notebook decay_pyENSDF.ipynb
```

Alternatively, To use the coincidence &gamma;-&gamma; and &gamma;-*X*-ray data sets:

```python
>>> cdata = e.load_coinc()
```

Again, a `Jupyter` notebook is also provided illustrating use of the various methods for access and manipulation of the coincidence data:

```Bash
$ cd notebook
$ jupyter notebook coinc_pyENSDF.ipynb
```

Inline plotting methods are supported in the notebooks using the `matplotlib` Python package.

# Docstrings

All `pyENSDF` classes and functions have supporting docstrings.  Please refer to the individual dosctrings for more information on any particular function including how to use it.  The dosctrings for each method generally have the following structure:

* A short explanation of the function.
* A list and description of arguments that need to be passed to the function.
* The return value of the function.
* An example(s) invoking use of the function.

To retrieve a list of all available methods simply execute the following command in a Python interpreter:

```python
>>> help(e)
```

Or, to retrieve the docstring for a particular method, e.g., the callable `get_gg`:

```python
>>> help(e.get_gg)
```

## RIPL format

Because many nuclear reaction codes source decay-scheme information in a particular Reference Input Parameter Library (RIPL) [[3]](#3) format, representative RIPL-translated data sets have also been generated for each corresponding ENSDF-decay data set and these files are also bundled with the software.  The RIPL-formatted ENSDF-decay data sets are located in their respective `python_ensdf/pyENSDF/ENSDF_RIPL/<decay_mode>` directories, where `<decay_mode>` corresponds to `alpha`, `beta_minus`, `beta_plus`, or `ecbp`.


## JSON format

All original ENSDF radioactive-decay data sets have been translated into a representative JavaScript Object Notation (JSON) format using an intuitive syntax to describe the quantities sourced from the primary and continuation records of the ENSDF-formatted data sets [[2]](#2).  The corresponding JSON-formatted radioative-decay data sets are bundled with this software package together with JSON-formatted coincidence $\gamma-\gamma$ and $\gamma-X$-ray data sets derived from the respective decay information in the original ENSDF library.  These JSON data structures are located in project folders:
```Bash
python_ensdf/pyENSDF/ENSDF_JSON
```
for the radioactive-decay data sets, and
```Bash
python_ensdf/pyENSDF/COINC_JSON
```
for the coincidence data sets.

The JSON data structures support the following data types:

* *string*
* *number*
* *boolean*
* *null*
* *object* (JSON object)
* *array*

The JSON-formatted schemas are described below.

## (1) JSON-formatted ENSDF-decay schema

| JSON key | Explanation |
| --- | --- |
| `"parentAtomicNumber"` | A number type denoting the atomic number of the parent nucleus.|
| `"parentAtomicMass"` | A number type denoting the mass number of the parent nucleus.|
| `"parentNeutronNumber"` | A number type denoting the neutron number of the parent nucleus.|
| `"daughterAtomicNumber"` | A number type denoting the atomic number of the daughter nucleus.|
| `"daughterAtomicMass"` | A number type denoting the mass number of the daughter nucleus.|
| `"daughterNeutronNumber"` | A number type denoting the neutron number of the daughter nucleus.|
| `"levelEnergyParentDecay"` | Usually a number type (float or integer) representing the decay-level energy of the parent.  String types are also acceptable, e.g., 'X', to indicate an unknown or imprecise value.  Values greater than zero are isomer decays.|
| `"parentID"` | A string type identification value of the parent nucleus `<symbol><mass>`.|
| `"daughterID"` | A string type identification value of the daughter nucleus `<symbol><mass>`.|
| `"decayMode"` | A string type representation of the decay mode: `"alphaDecay"`, `"betaMinusDecay"`, and `"electronCaptureBetaPusDecay"` values are acceptable.|
| `"totalNumberLevels"` | A number type value (integer) denoting the total number of levels observed in the daughter nucleus.|
| `"totalNumberGammas"` | A number type value (integer) denoting the total number of gammas observed in the daughter nucleus.|
| `"totalNumberParticleDecays` | A number type value (integer) denoting the number of particle decays observed to levels the daughter nucleus.|
| `"decayIndex"` | A number type value (integer) to indicate whether the parent nucleus decays from its ground state (0) or from an isomeric level (>0).|
| `"decaySchemeNormalization"` | An array type containing the two normalization arrays from ENSDF.|
| `"parentDecay"` | An array type containing several JSON objects related to the decay properties of the parent nucleus.|
| `"levelScheme"` | An array type containing several JSON objects related to the level scheme properties of the daughter nucleus populated following radioactive decay.|

The JSON arrays are described below:

### 1.1 `"decaySchemeNormalization"` array

| JSON key | Explanation |
| --- | --- |
| `"normalizationRecord"` | An array type containing all the information from the ENSDF primary *Normalization Record*.|
| `"productionNormalizationRecord"` | An array type containing all the information from the ENSDF primary *Production Normalization Record*.|

##### 1.1.1 `"normalizationRecord"` array
| JSON key | Explanation |
| --- | --- |
| `"recordExists"`| A boolean type to indicate whether the *Normalization Record* is present in the original ENSDF document.|
| `"multiplerPhotonIntensity"`| A number type representing the photon-intensity multiplier.|
| `"dMultiplerPhotonIntensity"`| A number type representing the associated uncertainty of the photon-intensity multiplier.|
| `"recordExistsNR"`| A boolean type to indicate whether the photon-intensity multiplier is parsed from the original ENSDF document.|
| `"multiplerTransitionIntensity"`| A number type representing the transition-intensity multiplier.|
| `"dMultiplerTransitionIntensity"`| A number type representing the associated uncertainty of the transition-intensity multiplier.|
| `"recordExistsNT"`| A boolean type to indicate whether the transition-intensity multiplier is parsed from the original ENSDF document.|
| `"multiplerBranchingRatio"`| A number type representing the branching-ratio multiplier.|
| `"dMultiplerBranchingRatio"`| A number type representing the associated uncertainty of the branching-ratio multiplier.|
| `"recordExistsBR"`| A boolean type to indicate whether the branching-ratio multiplier is parsed from the original ENSDF document.|
| `"multiplerLeptonIntensity"`| A number type representing the lepton-intensity multiplier.|
| `"dMultiplerLeptonIntensity"`| A number type representing the associated uncertainty of the lepton-intensity multiplier.|
| `"recordExistsNB"`| A boolean type to indicate whether the lepton-intensity multiplier is parsed from the original ENSDF document.|
| `"multiplierDelayedParticleIntensity"`| A number type representing the delayed-particle intensity multiplier.|
| `"dMultiplierDelayedParticleIntensity"`| A number type representing the associated uncertainty of the delayed-particle intensity multiplier.|
| `"recordExistsNP"`| A boolean type to indicate whether the delayed-particle intensity multiplier is parsed from the original ENSDF document.|

#### 1.1.2 `"productionNormalizationRecord"` array
| JSON key | Explanation |
| --- | --- |
| `"recordExists"`| A boolean type to indicate whether the *Production Normalization Record* is present in the original ENSDF document.|
| `"multiplierPhotonIntensityBranchingRatioCorrected"`| A number type representing the branching-ratio corrected photon-intensity multiplier.|
| `"dMultiplierPhotonIntensityBranchingRatioCorrected"`| A number type representing the associated uncertainty of the branching-ratio corrected photon-intensity multiplier.|
| `"recordExistsPNR"`| A boolean type to indicate whether the branching-ratio corrected photon-intensity multiplier is parsed from the original ENSDF document.|
| `"multiplierTransitionIntensityBranchingRatioCorrected"`| A number type representing the branching-ratio corrected transition-intensity multiplier.|
| `"dMultiplierTransitionIntensityBranchingRatioCorrected"`| A number type representing the associated uncertainty of the branching-ratio corrected transition-intensity multiplier.|
| `"recordExistsPNT"`| A boolean type to indicate whether the branching-ratio corrected transition-intensity multiplier is parsed from the original ENSDF document.|
| `"multiplierLeptonIntensityBranchingRatioCorrected"`| A number type representing the branching-ratio corrected lepton-intensity multiplier.|
| `"dMultiplierLeptonIntensityBranchingRatioCorrected"`| A number type representing the associated uncertainty of the branching-ratio corrected lepton-intensity multiplier.|
| `"recordExistsPNB"`| A boolean type to indicate whether the branching-ratio corrected lepton-intensity multiplier is parsed from the original ENSDF document.|
| `"multiplierDelayedParticleIntensity"`| A number type representing the delayed-particle intensity multiplier.  This quantity should be identical to that given in the corresponding `normalizationRecord`.|
| `"dMultiplierDelayedParticleIntensity"`| A number type representing the associated uncertainty of the delayed-particle intensity multiplier.  This quantity should be identical to that given in the corresponding `normalizationRecord`.|
| `"recordExistsPNP"`| A boolean type to indicate whether the delayed-particle intensity multiplier is parsed from the original ENSDF document.  This quantity should be identical to that given in the corresponding `normalizationRecord`.|

### 1.1 `"parentDecay"` array
| JSON key | Explanation |
| --- | --- |
| `"parentIsIsomer"`| A boolean type to indicate isomeric decay.|
| `"parentDecayLevelEnergy"`| A number type<sup>*</sup> (float or integer) corresponding to the excitation energy associated with the decay of the parent.|
| `"dParentDecayLevelEnergy"`| A number type (float or integer) corresponding to the associated uncertainty of parent-decay excitation energy.|
| `"parentDecayLevelEnergyIsKnown"`| A boolean type<sup>*</sup> to indicate whether or not the parent-decay level energy is known.|
| `"parentDecayLevelEnergyThreshold"`| If `"parentDecayLevelEnergyIsKnown": true` the value is a `null` type.  Otherwise number or string type values are allowed.|
| `"parentDecayLevelEnergyOffset"`|
| `"parentDecayLevelEnergyOffsetDirection"`|
| `"valueQ"`|
| `"dValueQ"`|
| `"atomicIonizationState"`|
| `"halfLife"`|
| `"decayWidth"`|
| `"numberOfSpins"`|
| `"spins"`|


## References

<a id="1">[1]</a>
A.M. Hurst, B.D. Pierson, B.C. Archambault, L.A. Bernstein, S.M. Tannous,
*"A decay datababase of coincident $\gamma - \gamma$ and $\gamma - X$-ray branching ratios for in-field spectroscopy applications"*,
Eur. Phys. J. (Web of Conf.) **284**, 18002 (2023);
https://doi.org/10.1051/epjconf/202328418002

<a id="2">[2]</a>
J.K. Tuli,
*"Evaluated Nuclear Structure Data File"*, BNL-NCS-51655-01/02-Rev (2001);
https://www.nndc.bnl.gov/ensdf/

<a id="3">[3]</a>
R. Capote *et al*.,
*"RIPL - Reference Input Parameter Library for Calculation of Nuclear Reactions and Nuclear Data Evaluations"*,
Nucl. Data Sheets **110**, 3107 (2009).



