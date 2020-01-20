# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2012-2020 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.

from openquake.hazardlib.gsim.base import CoeffsTable
from openquake.hazardlib.imt import PGA, PGV, SA

#: Coefficient table constructed from the electronic suplements of the
#: original paper.

COEFFS_FS_ROCK_SWISS01 = CoeffsTable(sa_damping=5, table="""\
 IMT     k_adj           a1              a2              b1              b2              Rm             phi_11   phi_21   C2       Mc1  Mc2 Rc11    Rc21  mean_phi_ss
 pga     0.770968000     6.308282E+00    1.000000E+00    9.814496E-01    -7.784689E-01   7.056087E+01   0.58000  0.47000  0.35000  5    7   16      36    0.46000
 0.010   0.770968000     6.308282E+00    1.000000E+00    9.814496E-01    -7.784689E-01   7.056087E+01   0.58000  0.47000  0.35000  5    7   16      36    0.46000
 0.050   0.781884504     6.242341E+00    1.000000E+00    9.792917E-01    -7.239180E-01   7.736220E+01   0.55204  0.44903  0.40592  5    7   16      36    0.45301
 0.100   0.745908877     5.332961E+00    1.000000E+00    9.742506E-01    -1.092188E+00   4.880096E+01   0.54000  0.44000  0.43000  5    7   16      36    0.45000
 0.150   0.744117229     4.545627E+00    1.000000E+00    9.824773E-01    -9.934861E-01   5.436996E+01   0.58095  0.47510  0.40075  5    7   16      36    0.46755
 0.200   0.744577747     3.987006E+00    1.000000E+00    9.883142E-01    -9.234564E-01   5.832123E+01   0.61000  0.50000  0.38000  5    7   16      36    0.48000
 0.250   0.748103885     3.824292E+00    1.000000E+00    9.902861E-01    -8.590989E-01   6.387936E+01   0.62651  0.50000  0.37450  5    7   16      36    0.48000
 0.300   0.755136175     3.691346E+00    1.000000E+00    9.918973E-01    -8.065151E-01   6.842068E+01   0.64000  0.50000  0.37000  5    7   16      36    0.48000
 0.400   0.767879693     4.056852E+00    1.000000E+00    9.932212E-01    -8.277473E-01   6.639628E+01   0.61747  0.48874  0.37000  5    7   16      36    0.46874
 0.500   0.778052686     3.955542E+00    1.000000E+00    9.943901E-01    -7.686919E-01   7.702964E+01   0.60000  0.48000  0.37000  5    7   16      36    0.46000
 0.750   0.796961618     3.771458E+00    1.000000E+00    9.965141E-01    -6.613849E-01   9.635109E+01   0.56490  0.46245  0.38755  5    7   16      36    0.45415
 1.000   0.804115657     3.640847E+00    1.000000E+00    9.980211E-01    -5.852493E-01   1.100599E+02   0.54000  0.45000  0.40000  5    7   16      36    0.45000
 1.500   0.806238935     3.010737E+00    1.000000E+00    9.987325E-01    -5.862774E-01   1.098648E+02   0.53631  0.43155  0.40000  5    7   16      36    0.43524
 2.000   0.809163942     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53369  0.41845  0.40000  5    7   16      36    0.42476
 3.000   0.822779154     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36    0.41000
 4.000   0.835713694     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36    0.41000
 5.000   0.847331737     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36    0.41000
 7.500   0.874425160     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36    0.41000
 10.00   0.894172022     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36    0.41000
    """)

COEFFS_FS_ROCK_SWISS06 = CoeffsTable(sa_damping=5, table="""\
 IMT     k_adj                   a1              a2              b1              b2              Rm     phi_11   phi_21   C2       Mc1  Mc2 Rc11    Rc21 mean_phi_ss
 pga     0.907406000     6.308282E+00    1.000000E+00    9.814496E-01    -7.784689E-01   7.056087E+01   0.58000  0.47000  0.35000  5    7   16      36   0.46000
 0.010   0.907406000     6.308282E+00    1.000000E+00    9.814496E-01    -7.784689E-01   7.056087E+01   0.58000  0.47000  0.35000  5    7   16      36   0.46000
 0.050   1.052062325     6.242341E+00    1.000000E+00    9.792917E-01    -7.239180E-01   7.736220E+01   0.55204  0.44903  0.40592  5    7   16      36   0.45301
 0.100   0.903944171     5.332961E+00    1.000000E+00    9.742506E-01    -1.092188E+00   4.880096E+01   0.54000  0.44000  0.43000  5    7   16      36   0.45000
 0.150   0.846557682     4.545627E+00    1.000000E+00    9.824773E-01    -9.934861E-01   5.436996E+01   0.58095  0.47510  0.40075  5    7   16      36   0.46755
 0.200   0.8152693       3.987006E+00    1.000000E+00    9.883142E-01    -9.234564E-01   5.832123E+01   0.61000  0.50000  0.38000  5    7   16      36   0.48000
 0.250   0.797908534     3.824292E+00    1.000000E+00    9.902861E-01    -8.590989E-01   6.387936E+01   0.62651  0.50000  0.37450  5    7   16      36   0.48000
 0.300   0.789245393     3.691346E+00    1.000000E+00    9.918973E-01    -8.065151E-01   6.842068E+01   0.64000  0.50000  0.37000  5    7   16      36   0.48000
 0.400   0.78042074      4.056852E+00    1.000000E+00    9.932212E-01    -8.277473E-01   6.639628E+01   0.61747  0.48874  0.37000  5    7   16      36   0.46874
 0.500   0.777925382     3.955542E+00    1.000000E+00    9.943901E-01    -7.686919E-01   7.702964E+01   0.60000  0.48000  0.37000  5    7   16      36   0.46000
 0.750   0.786471408     3.771458E+00    1.000000E+00    9.965141E-01    -6.613849E-01   9.635109E+01   0.56490  0.46245  0.38755  5    7   16      36   0.45415
 1.000   0.804234088     3.640847E+00    1.000000E+00    9.980211E-01    -5.852493E-01   1.100599E+02   0.54000  0.45000  0.40000  5    7   16      36   0.45000
 1.500   0.839944334     3.010737E+00    1.000000E+00    9.987325E-01    -5.862774E-01   1.098648E+02   0.53631  0.43155  0.40000  5    7   16      36   0.43524
 2.000   0.865068228     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53369  0.41845  0.40000  5    7   16      36   0.42476
 3.000   0.893179655     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36   0.41000
 4.000   0.904833501     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36   0.41000
 5.000   0.911805616     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36   0.41000
 7.500   0.929535851     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36   0.41000
 10.00   0.942324350     2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02   0.53000  0.40000  0.40000  5    7   16      36   0.41000
    """)

COEFFS_FS_ROCK_SWISS04 = CoeffsTable(sa_damping=5, table="""\
IMT     k_adj                   a1              a2              b1              b2              Rm      phi_11   phi_21   C2       Mc1  Mc2 Rc11    Rc21  mean_phi_ss
pga     1.144220000    6.308282E+00    1.000000E+00    9.814496E-01    -7.784689E-01   7.056087E+01     0.58000  0.47000  0.35000  5    7   16      36    0.46000
0.010   1.144220000    6.308282E+00    1.000000E+00    9.814496E-01    -7.784689E-01   7.056087E+01     0.58000  0.47000  0.35000  5    7   16      36    0.46000
0.050   1.582364006    6.242341E+00    1.000000E+00    9.792917E-01    -7.239180E-01   7.736220E+01     0.55204  0.44903  0.40592  5    7   16      36    0.45301
0.100   1.134260083    5.332961E+00    1.000000E+00    9.742506E-01    -1.092188E+00   4.880096E+01     0.54000  0.44000  0.43000  5    7   16      36    0.45000
0.150   0.997131538    4.545627E+00    1.000000E+00    9.824773E-01    -9.934861E-01   5.436996E+01     0.58095  0.47510  0.40075  5    7   16      36    0.46755
0.200   0.931483355    3.987006E+00    1.000000E+00    9.883142E-01    -9.234564E-01   5.832123E+01     0.61000  0.50000  0.38000  5    7   16      36    0.48000
0.250   0.896609692    3.824292E+00    1.000000E+00    9.902861E-01    -8.590989E-01   6.387936E+01     0.62651  0.50000  0.37450  5    7   16      36    0.48000
0.300   0.879037052    3.691346E+00    1.000000E+00    9.918973E-01    -8.065151E-01   6.842068E+01     0.64000  0.50000  0.37000  5    7   16      36    0.48000
0.400   0.861457717    4.056852E+00    1.000000E+00    9.932212E-01    -8.277473E-01   6.639628E+01     0.61747  0.48874  0.37000  5    7   16      36    0.46874
0.500   0.853567498    3.955542E+00    1.000000E+00    9.943901E-01    -7.686919E-01   7.702964E+01     0.60000  0.48000  0.37000  5    7   16      36    0.46000
0.750   0.848145374    3.771458E+00    1.000000E+00    9.965141E-01    -6.613849E-01   9.635109E+01     0.56490  0.46245  0.38755  5    7   16      36    0.45415
1.000   0.842662116    3.640847E+00    1.000000E+00    9.980211E-01    -5.852493E-01   1.100599E+02     0.54000  0.45000  0.40000  5    7   16      36    0.45000
1.500   0.831445701    3.010737E+00    1.000000E+00    9.987325E-01    -5.862774E-01   1.098648E+02     0.53631  0.43155  0.40000  5    7   16      36    0.43524
2.000   0.827607473    2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02     0.53369  0.41845  0.40000  5    7   16      36    0.42476
3.000   0.835774855    2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02     0.53000  0.40000  0.40000  5    7   16      36    0.41000
4.000   0.848240349    2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02     0.53000  0.40000  0.40000  5    7   16      36    0.41000
5.000   0.861360769    2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02     0.53000  0.40000  0.40000  5    7   16      36    0.41000
7.500   0.892087590    2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02     0.53000  0.40000  0.40000  5    7   16      36    0.41000
10.00   0.914551086    2.563667E+00    1.000000E+00    9.992372E-01    -5.870069E-01   1.097264E+02     0.53000  0.40000  0.40000  5    7   16      36    0.41000
    """)
