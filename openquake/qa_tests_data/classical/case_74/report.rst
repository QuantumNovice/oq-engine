Test the calculation of hazard with EAS
=======================================

+----------------+----------------------+
| checksum32     | 3_370_060_175        |
+----------------+----------------------+
| date           | 2022-03-17T11:25:21  |
+----------------+----------------------+
| engine_version | 3.14.0-gitaed816bf7b |
+----------------+----------------------+
| input_size     | 3_395                |
+----------------+----------------------+

num_sites = 1, num_levels = 20, num_rlzs = 1

Parameters
----------
+---------------------------------+--------------------------------------------+
| parameter                       | value                                      |
+---------------------------------+--------------------------------------------+
| calculation_mode                | 'preclassical'                             |
+---------------------------------+--------------------------------------------+
| number_of_logic_tree_samples    | 0                                          |
+---------------------------------+--------------------------------------------+
| maximum_distance                | {'default': [[2.5, 200.0], [10.2, 200.0]]} |
+---------------------------------+--------------------------------------------+
| investigation_time              | 50.0                                       |
+---------------------------------+--------------------------------------------+
| ses_per_logic_tree_path         | 1                                          |
+---------------------------------+--------------------------------------------+
| truncation_level                | 3.0                                        |
+---------------------------------+--------------------------------------------+
| rupture_mesh_spacing            | 2.0                                        |
+---------------------------------+--------------------------------------------+
| complex_fault_mesh_spacing      | 2.0                                        |
+---------------------------------+--------------------------------------------+
| width_of_mfd_bin                | 0.1                                        |
+---------------------------------+--------------------------------------------+
| area_source_discretization      | 5.0                                        |
+---------------------------------+--------------------------------------------+
| pointsource_distance            | {'default': '1000'}                        |
+---------------------------------+--------------------------------------------+
| ground_motion_correlation_model | None                                       |
+---------------------------------+--------------------------------------------+
| minimum_intensity               | {}                                         |
+---------------------------------+--------------------------------------------+
| random_seed                     | 23                                         |
+---------------------------------+--------------------------------------------+
| master_seed                     | 123456789                                  |
+---------------------------------+--------------------------------------------+
| ses_seed                        | 42                                         |
+---------------------------------+--------------------------------------------+

Input files
-----------
+-------------------------+--------------------------------------------------------------+
| Name                    | File                                                         |
+-------------------------+--------------------------------------------------------------+
| gsim_logic_tree         | `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                 |
+-------------------------+--------------------------------------------------------------+
| job_ini                 | `job.ini <job.ini>`_                                         |
+-------------------------+--------------------------------------------------------------+
| source_model_logic_tree | `source_model_logic_tree.xml <source_model_logic_tree.xml>`_ |
+-------------------------+--------------------------------------------------------------+

Required parameters per tectonic region type
--------------------------------------------
+----------------------+-------------------------+-----------+------------+---------------+
| trt_smr              | gsims                   | distances | siteparams | ruptparams    |
+----------------------+-------------------------+-----------+------------+---------------+
| Active Shallow Crust | [BaylessAbrahamson2018] | rrup      | vs30 z1pt0 | mag rake ztor |
+----------------------+-------------------------+-----------+------------+---------------+

Slowest sources
---------------
+-----------+------+-----------+-----------+--------------+
| source_id | code | calc_time | num_sites | eff_ruptures |
+-----------+------+-----------+-----------+--------------+
| 3         | S    | 0.0       | 5         | 548          |
+-----------+------+-----------+-----------+--------------+

Computation times by source typology
------------------------------------
+------+-----------+-----------+--------------+--------+
| code | calc_time | num_sites | eff_ruptures | weight |
+------+-----------+-----------+--------------+--------+
| S    | 0.0       | 5         | 548          | 564.0  |
+------+-----------+-----------+--------------+--------+

Information about the tasks
---------------------------
+--------------------+--------+---------+--------+-----------+---------+---------+
| operation-duration | counts | mean    | stddev | min       | max     | slowfac |
+--------------------+--------+---------+--------+-----------+---------+---------+
| preclassical       | 2      | 0.05012 | 99%    | 2.136E-04 | 0.10002 | 1.99574 |
+--------------------+--------+---------+--------+-----------+---------+---------+
| read_source_model  | 1      | 0.00165 | nan    | 0.00165   | 0.00165 | 1.00000 |
+--------------------+--------+---------+--------+-----------+---------+---------+

Data transfer
-------------
+-------------------+------------------------------------------+----------+
| task              | sent                                     | received |
+-------------------+------------------------------------------+----------+
| read_source_model |                                          | 1.66 KB  |
+-------------------+------------------------------------------+----------+
| split_task        | args=1.02 MB elements=1.34 KB func=132 B | 0 B      |
+-------------------+------------------------------------------+----------+
| preclassical      |                                          | 2.33 KB  |
+-------------------+------------------------------------------+----------+

Slowest operations
------------------
+---------------------------+----------+-----------+--------+
| calc_50560, maxmem=1.9 GB | time_sec | memory_mb | counts |
+---------------------------+----------+-----------+--------+
| importing inputs          | 0.10523  | 0.0       | 1      |
+---------------------------+----------+-----------+--------+
| total preclassical        | 0.10002  | 0.60547   | 1      |
+---------------------------+----------+-----------+--------+
| composite source model    | 0.09931  | 0.0       | 1      |
+---------------------------+----------+-----------+--------+
| weighting sources         | 0.05337  | 0.0       | 5      |
+---------------------------+----------+-----------+--------+
| splitting sources         | 0.01012  | 0.60547   | 1      |
+---------------------------+----------+-----------+--------+
| total read_source_model   | 0.00165  | 0.0       | 1      |
+---------------------------+----------+-----------+--------+