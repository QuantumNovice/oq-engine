
| Test ID | Description |
|---------|-------------|
| case_1  | Test the MultiGMPE functionality| 
| case_2  | Test the use of a rather small discretisation for MFDs | 
| case_3  | Source model with one point source and two GMMs | 
| case_4  | Source model with one simple fault source | 
| case_5  | Test the option of discarding some TR using the `job.ini` file. See example [here](https://github.com/gem/oq-engine/blob/20200312_table/openquake/qa_tests_data/event_based/case_5/job.ini#L33s)  | 
| case_6  | Check we calculate only hazard curves | 
| case_7  | Test a simple case with logic tree sampling | 
| case_8  | Test EB with a non-parametric source | 
| case_9  | Test ground motion correlation | 
| case_10 | Test with logic tree sampling | 
| case_11 | *missing :^)* |
| case_12 | Test hazard_curves_from_gmfs with 2 GMPEs | 
| case_13 | Test hazard_curves_from_gmfs| 
| case_14 | Test source specific logic tree (like South Africa) |
| case_15 | Test calculation using a reduced model similar to the Japan one | 
| case_16 | Test calculation using a reduced model similar to the Italy one | 
| case_17 | Test that the ruptures are read correctly with --hc functionality| 
| case_18 | Test with oversampling | 
| case_19 | Test the NRCan15SiteTerm| 
| case_20 | Test the NRCan15SiteTerm with --hc| 
| case_21 | Test the use of a source model containing a cluster | 
| case_22 | Test the use of the [SplitSigmaGMPE](https://github.com/gem/oq-engine/blob/master/openquake/hazardlib/gsim/mgmpe/split_sigma_gmpe.py) modifiable GMPE | 
| case_23 | Test gridding from the exposure model + site model | 
| case_24 | Test the use of the `shift_hypo` option in the `job.ini` | 
| case_25 | Test the `extendModel` feature in the logic tree| 
| case_26 |  |
| case_27 |  |
| case_28 | Test the add between and within std in the modifiable GMPE |
| mutex   | Test the use of a source model with mutually exclusive sources | 
| spatial_correlation | Test the use spatial_correlation for the calculation of GMFs | 
| gmep_tables | Test the usage of GMPETable |
