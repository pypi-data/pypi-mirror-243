"""
    This **module** gives the unit tests of targeted MD
"""

__all__ = ["test_tmd"]

def test_tmd():
    """ test targeted MD """
    import os
    from io import StringIO
    import Xponge
    import Xponge.forcefield.amber.tip3p
    import Xponge.forcefield.amber.ff14sb
    from Xponge.mdrun import run
    from Xponge.helper.cv import CVSystem

    pdb = StringIO("""ATOM      1  N   ASN A   1      -8.901   4.127  -0.555  1.00  0.00           N  
ATOM      2  CA  ASN A   1      -8.608   3.135  -1.618  1.00  0.00           C  
ATOM      3  C   ASN A   1      -7.117   2.964  -1.897  1.00  0.00           C  
ATOM      4  O   ASN A   1      -6.634   1.849  -1.758  1.00  0.00           O  
ATOM      5  CB  ASN A   1      -9.437   3.396  -2.889  1.00  0.00           C  
ATOM      6  CG  ASN A   1     -10.915   3.130  -2.611  1.00  0.00           C  
ATOM      7  OD1 ASN A   1     -11.269   2.700  -1.524  1.00  0.00           O  
ATOM      8  ND2 ASN A   1     -11.806   3.406  -3.543  1.00  0.00           N  
ATOM      9  H1  ASN A   1      -8.330   3.957   0.261  1.00  0.00           H  
ATOM     10  H2  ASN A   1      -8.740   5.068  -0.889  1.00  0.00           H  
ATOM     11  H3  ASN A   1      -9.877   4.041  -0.293  1.00  0.00           H  
ATOM     12  HA  ASN A   1      -8.930   2.162  -1.239  1.00  0.00           H  
ATOM     13  HB2 ASN A   1      -9.310   4.417  -3.193  1.00  0.00           H  
ATOM     14  HB3 ASN A   1      -9.108   2.719  -3.679  1.00  0.00           H  
ATOM     15 HD21 ASN A   1     -11.572   3.791  -4.444  1.00  0.00           H  
ATOM     16 HD22 ASN A   1     -12.757   3.183  -3.294  1.00  0.00           H  
ATOM     17  N   LEU A   2      -6.379   4.031  -2.228  1.00  0.00           N  
ATOM     18  CA  LEU A   2      -4.923   4.002  -2.452  1.00  0.00           C  
ATOM     19  C   LEU A   2      -4.136   3.187  -1.404  1.00  0.00           C  
ATOM     20  O   LEU A   2      -3.391   2.274  -1.760  1.00  0.00           O  
ATOM     21  CB  LEU A   2      -4.411   5.450  -2.619  1.00  0.00           C  
ATOM     22  CG  LEU A   2      -4.795   6.450  -1.495  1.00  0.00           C  
ATOM     23  CD1 LEU A   2      -3.612   6.803  -0.599  1.00  0.00           C  
ATOM     24  CD2 LEU A   2      -5.351   7.748  -2.084  1.00  0.00           C  
ATOM     25  H   LEU A   2      -6.821   4.923  -2.394  1.00  0.00           H  
ATOM     26  HA  LEU A   2      -4.750   3.494  -3.403  1.00  0.00           H  
ATOM     27  HB2 LEU A   2      -3.340   5.414  -2.672  1.00  0.00           H  
ATOM     28  HB3 LEU A   2      -4.813   5.817  -3.564  1.00  0.00           H  
ATOM     29  HG  LEU A   2      -5.568   6.022  -0.858  1.00  0.00           H  
ATOM     30 HD11 LEU A   2      -3.207   5.905  -0.146  1.00  0.00           H  
ATOM     31 HD12 LEU A   2      -2.841   7.304  -1.183  1.00  0.00           H  
ATOM     32 HD13 LEU A   2      -3.929   7.477   0.197  1.00  0.00           H  
ATOM     33 HD21 LEU A   2      -4.607   8.209  -2.736  1.00  0.00           H  
ATOM     34 HD22 LEU A   2      -6.255   7.544  -2.657  1.00  0.00           H  
ATOM     35 HD23 LEU A   2      -5.592   8.445  -1.281  1.00  0.00           H  
ATOM     36  N   TYR A   3      -4.354   3.455  -0.111  1.00  0.00           N  
ATOM     37  CA  TYR A   3      -3.690   2.738   0.981  1.00  0.00           C  
ATOM     38  C   TYR A   3      -4.102   1.256   1.074  1.00  0.00           C  
ATOM     39  O   TYR A   3      -3.291   0.409   1.442  1.00  0.00           O  
ATOM     40  CB  TYR A   3      -3.964   3.472   2.302  1.00  0.00           C  
ATOM     41  CG  TYR A   3      -2.824   3.339   3.290  1.00  0.00           C  
ATOM     42  CD1 TYR A   3      -2.746   2.217   4.138  1.00  0.00           C  
ATOM     43  CD2 TYR A   3      -1.820   4.326   3.332  1.00  0.00           C  
ATOM     44  CE1 TYR A   3      -1.657   2.076   5.018  1.00  0.00           C  
ATOM     45  CE2 TYR A   3      -0.725   4.185   4.205  1.00  0.00           C  
ATOM     46  CZ  TYR A   3      -0.639   3.053   5.043  1.00  0.00           C  
ATOM     47  OH  TYR A   3       0.433   2.881   5.861  1.00  0.00           O  
ATOM     48  H   TYR A   3      -4.934   4.245   0.120  1.00  0.00           H  
ATOM     49  HA  TYR A   3      -2.615   2.768   0.796  1.00  0.00           H  
ATOM     50  HB2 TYR A   3      -4.117   4.513   2.091  1.00  0.00           H  
ATOM     51  HB3 TYR A   3      -4.886   3.096   2.750  1.00  0.00           H  
ATOM     52  HD1 TYR A   3      -3.513   1.456   4.101  1.00  0.00           H  
ATOM     53  HD2 TYR A   3      -1.877   5.200   2.695  1.00  0.00           H  
ATOM     54  HE1 TYR A   3      -1.576   1.221   5.669  1.00  0.00           H  
ATOM     55  HE2 TYR A   3       0.033   4.952   4.233  1.00  0.00           H  
ATOM     56  HH  TYR A   3       1.187   3.395   5.567  1.00  0.00           H  
ATOM     57  N   ILE A   4      -5.342   0.925   0.689  1.00  0.00           N  
ATOM     58  CA  ILE A   4      -5.857  -0.449   0.613  1.00  0.00           C  
ATOM     59  C   ILE A   4      -5.089  -1.221  -0.470  1.00  0.00           C  
ATOM     60  O   ILE A   4      -4.621  -2.334  -0.226  1.00  0.00           O  
ATOM     61  CB  ILE A   4      -7.386  -0.466   0.343  1.00  0.00           C  
ATOM     62  CG1 ILE A   4      -8.197   0.540   1.197  1.00  0.00           C  
ATOM     63  CG2 ILE A   4      -7.959  -1.884   0.501  1.00  0.00           C  
ATOM     64  CD1 ILE A   4      -8.019   0.412   2.715  1.00  0.00           C  
ATOM     65  H   ILE A   4      -5.906   1.656   0.283  1.00  0.00           H  
ATOM     66  HA  ILE A   4      -5.670  -0.941   1.568  1.00  0.00           H  
ATOM     67  HB  ILE A   4      -7.554  -0.192  -0.697  1.00  0.00           H  
ATOM     68 HG12 ILE A   4      -7.900   1.531   0.912  1.00  0.00           H  
ATOM     69 HG13 ILE A   4      -9.257   0.424   0.964  1.00  0.00           H  
ATOM     70 HG21 ILE A   4      -7.509  -2.555  -0.232  1.00  0.00           H  
ATOM     71 HG22 ILE A   4      -7.759  -2.271   1.501  1.00  0.00           H  
ATOM     72 HG23 ILE A   4      -9.036  -1.871   0.332  1.00  0.00           H  
ATOM     73 HD11 ILE A   4      -8.306  -0.585   3.049  1.00  0.00           H  
ATOM     74 HD12 ILE A   4      -6.983   0.606   2.995  1.00  0.00           H  
ATOM     75 HD13 ILE A   4      -8.656   1.144   3.213  1.00  0.00           H  
ATOM     76  N   GLN A   5      -4.907  -0.601  -1.645  1.00  0.00           N  
ATOM     77  CA  GLN A   5      -4.122  -1.167  -2.743  1.00  0.00           C  
ATOM     78  C   GLN A   5      -2.629  -1.321  -2.390  1.00  0.00           C  
ATOM     79  O   GLN A   5      -1.986  -2.240  -2.884  1.00  0.00           O  
ATOM     80  CB  GLN A   5      -4.292  -0.313  -4.013  1.00  0.00           C  
ATOM     81  CG  GLN A   5      -4.244  -1.171  -5.290  1.00  0.00           C  
ATOM     82  CD  GLN A   5      -5.576  -1.860  -5.585  1.00  0.00           C  
ATOM     83  OE1 GLN A   5      -5.769  -3.044  -5.335  1.00  0.00           O  
ATOM     84  NE2 GLN A   5      -6.532  -1.146  -6.152  1.00  0.00           N  
ATOM     85  H   GLN A   5      -5.327   0.318  -1.763  1.00  0.00           H  
ATOM     86  HA  GLN A   5      -4.517  -2.162  -2.940  1.00  0.00           H  
ATOM     87  HB2 GLN A   5      -5.238   0.191  -3.969  1.00  0.00           H  
ATOM     88  HB3 GLN A   5      -3.492   0.429  -4.053  1.00  0.00           H  
ATOM     89  HG2 GLN A   5      -3.993  -0.539  -6.120  1.00  0.00           H  
ATOM     90  HG3 GLN A   5      -3.458  -1.923  -5.205  1.00  0.00           H  
ATOM     91 HE21 GLN A   5      -6.389  -0.184  -6.408  1.00  0.00           H  
ATOM     92 HE22 GLN A   5      -7.392  -1.635  -6.335  1.00  0.00           H  
ATOM     93  N   TRP A   6      -2.074  -0.459  -1.528  1.00  0.00           N  
ATOM     94  CA  TRP A   6      -0.716  -0.631  -0.993  1.00  0.00           C  
ATOM     95  C   TRP A   6      -0.631  -1.766   0.044  1.00  0.00           C  
ATOM     96  O   TRP A   6       0.295  -2.579  -0.004  1.00  0.00           O  
ATOM     97  CB  TRP A   6      -0.221   0.703  -0.417  1.00  0.00           C  
ATOM     98  CG  TRP A   6       1.148   0.652   0.194  1.00  0.00           C  
ATOM     99  CD1 TRP A   6       2.319   0.664  -0.482  1.00  0.00           C  
ATOM    100  CD2 TRP A   6       1.508   0.564   1.606  1.00  0.00           C  
ATOM    101  NE1 TRP A   6       3.371   0.560   0.411  1.00  0.00           N  
ATOM    102  CE2 TRP A   6       2.928   0.515   1.710  1.00  0.00           C  
ATOM    103  CE3 TRP A   6       0.779   0.524   2.812  1.00  0.00           C  
ATOM    104  CZ2 TRP A   6       3.599   0.445   2.938  1.00  0.00           C  
ATOM    105  CZ3 TRP A   6       1.439   0.433   4.053  1.00  0.00           C  
ATOM    106  CH2 TRP A   6       2.842   0.407   4.120  1.00  0.00           C  
ATOM    107  H   TRP A   6      -2.624   0.343  -1.242  1.00  0.00           H  
ATOM    108  HA  TRP A   6      -0.052  -0.908  -1.813  1.00  0.00           H  
ATOM    109  HB2 TRP A   6      -0.206   1.425  -1.211  1.00  0.00           H  
ATOM    110  HB3 TRP A   6      -0.921   1.044   0.344  1.00  0.00           H  
ATOM    111  HD1 TRP A   6       2.412   0.733  -1.558  1.00  0.00           H  
ATOM    112  HE1 TRP A   6       4.360   0.536   0.156  1.00  0.00           H  
ATOM    113  HE3 TRP A   6      -0.299   0.571   2.773  1.00  0.00           H  
ATOM    114  HZ2 TRP A   6       4.679   0.418   2.961  1.00  0.00           H  
ATOM    115  HZ3 TRP A   6       0.862   0.400   4.966  1.00  0.00           H  
ATOM    116  HH2 TRP A   6       3.334   0.360   5.081  1.00  0.00           H  
ATOM    117  N   LEU A   7      -1.600  -1.860   0.967  1.00  0.00           N  
ATOM    118  CA  LEU A   7      -1.641  -2.932   1.963  1.00  0.00           C  
ATOM    119  C   LEU A   7      -1.847  -4.319   1.342  1.00  0.00           C  
ATOM    120  O   LEU A   7      -1.144  -5.248   1.742  1.00  0.00           O  
ATOM    121  CB  LEU A   7      -2.710  -2.645   3.033  1.00  0.00           C  
ATOM    122  CG  LEU A   7      -2.301  -1.579   4.069  1.00  0.00           C  
ATOM    123  CD1 LEU A   7      -3.475  -1.323   5.018  1.00  0.00           C  
ATOM    124  CD2 LEU A   7      -1.093  -2.007   4.914  1.00  0.00           C  
ATOM    125  H   LEU A   7      -2.316  -1.137   0.994  1.00  0.00           H  
ATOM    126  HA  LEU A   7      -0.666  -2.978   2.445  1.00  0.00           H  
ATOM    127  HB2 LEU A   7      -3.600  -2.308   2.537  1.00  0.00           H  
ATOM    128  HB3 LEU A   7      -2.921  -3.571   3.572  1.00  0.00           H  
ATOM    129  HG  LEU A   7      -2.061  -0.649   3.560  1.00  0.00           H  
ATOM    130 HD11 LEU A   7      -4.343  -0.992   4.449  1.00  0.00           H  
ATOM    131 HD12 LEU A   7      -3.725  -2.237   5.560  1.00  0.00           H  
ATOM    132 HD13 LEU A   7      -3.211  -0.549   5.739  1.00  0.00           H  
ATOM    133 HD21 LEU A   7      -1.270  -2.989   5.354  1.00  0.00           H  
ATOM    134 HD22 LEU A   7      -0.195  -2.045   4.300  1.00  0.00           H  
ATOM    135 HD23 LEU A   7      -0.922  -1.286   5.712  1.00  0.00           H  
ATOM    136  N   LYS A   8      -2.753  -4.481   0.360  1.00  0.00           N  
ATOM    137  CA  LYS A   8      -3.024  -5.791  -0.269  1.00  0.00           C  
ATOM    138  C   LYS A   8      -1.796  -6.427  -0.937  1.00  0.00           C  
ATOM    139  O   LYS A   8      -1.719  -7.648  -1.030  1.00  0.00           O  
ATOM    140  CB  LYS A   8      -4.224  -5.697  -1.232  1.00  0.00           C  
ATOM    141  CG  LYS A   8      -3.930  -5.009  -2.577  1.00  0.00           C  
ATOM    142  CD  LYS A   8      -3.682  -5.986  -3.736  1.00  0.00           C  
ATOM    143  CE  LYS A   8      -3.494  -5.199  -5.039  1.00  0.00           C  
ATOM    144  NZ  LYS A   8      -4.563  -5.483  -6.023  1.00  0.00           N  
ATOM    145  H   LYS A   8      -3.321  -3.675   0.097  1.00  0.00           H  
ATOM    146  HA  LYS A   8      -3.309  -6.478   0.529  1.00  0.00           H  
ATOM    147  HB2 LYS A   8      -4.565  -6.694  -1.436  1.00  0.00           H  
ATOM    148  HB3 LYS A   8      -5.019  -5.143  -0.731  1.00  0.00           H  
ATOM    149  HG2 LYS A   8      -4.769  -4.390  -2.830  1.00  0.00           H  
ATOM    150  HG3 LYS A   8      -3.062  -4.368  -2.469  1.00  0.00           H  
ATOM    151  HD2 LYS A   8      -2.799  -6.562  -3.536  1.00  0.00           H  
ATOM    152  HD3 LYS A   8      -4.524  -6.674  -3.818  1.00  0.00           H  
ATOM    153  HE2 LYS A   8      -3.502  -4.150  -4.813  1.00  0.00           H  
ATOM    154  HE3 LYS A   8      -2.511  -5.439  -5.457  1.00  0.00           H  
ATOM    155  HZ1 LYS A   8      -4.621  -6.474  -6.211  1.00  0.00           H  
ATOM    156  HZ2 LYS A   8      -5.442  -5.124  -5.657  1.00  0.00           H  
ATOM    157  HZ3 LYS A   8      -4.382  -4.983  -6.881  1.00  0.00           H  
ATOM    158  N   ASP A   9      -0.828  -5.607  -1.355  1.00  0.00           N  
ATOM    159  CA  ASP A   9       0.466  -6.016  -1.905  1.00  0.00           C  
ATOM    160  C   ASP A   9       1.481  -6.464  -0.832  1.00  0.00           C  
ATOM    161  O   ASP A   9       2.545  -6.971  -1.194  1.00  0.00           O  
ATOM    162  CB  ASP A   9       1.033  -4.839  -2.724  1.00  0.00           C  
ATOM    163  CG  ASP A   9       0.672  -4.906  -4.210  1.00  0.00           C  
ATOM    164  OD1 ASP A   9      -0.532  -5.051  -4.522  1.00  0.00           O  
ATOM    165  OD2 ASP A   9       1.627  -4.815  -5.017  1.00  0.00           O  
ATOM    166  H   ASP A   9      -1.010  -4.616  -1.291  1.00  0.00           H  
ATOM    167  HA  ASP A   9       0.319  -6.867  -2.574  1.00  0.00           H  
ATOM    168  HB2 ASP A   9       0.644  -3.924  -2.320  1.00  0.00           H  
ATOM    169  HB3 ASP A   9       2.116  -4.837  -2.650  1.00  0.00           H  
ATOM    170  N   GLY A  10       1.185  -6.278   0.464  1.00  0.00           N  
ATOM    171  CA  GLY A  10       2.060  -6.618   1.593  1.00  0.00           C  
ATOM    172  C   GLY A  10       2.628  -5.412   2.353  1.00  0.00           C  
ATOM    173  O   GLY A  10       3.496  -5.594   3.208  1.00  0.00           O  
ATOM    174  H   GLY A  10       0.265  -5.908   0.693  1.00  0.00           H  
ATOM    175  HA2 GLY A  10       1.486  -7.214   2.304  1.00  0.00           H  
ATOM    176  HA3 GLY A  10       2.897  -7.228   1.252  1.00  0.00           H  
ATOM    177  N   GLY A  11       2.172  -4.187   2.055  1.00  0.00           N  
ATOM    178  CA  GLY A  11       2.626  -2.967   2.723  1.00  0.00           C  
ATOM    179  C   GLY A  11       4.157  -2.802   2.654  1.00  0.00           C  
ATOM    180  O   GLY A  11       4.710  -2.829   1.551  1.00  0.00           O  
ATOM    181  H   GLY A  11       1.481  -4.089   1.319  1.00  0.00           H  
ATOM    182  HA2 GLY A  11       2.164  -2.109   2.237  1.00  0.00           H  
ATOM    183  HA3 GLY A  11       2.280  -2.997   3.753  1.00  0.00           H  
ATOM    184  N   PRO A  12       4.871  -2.651   3.794  1.00  0.00           N  
ATOM    185  CA  PRO A  12       6.333  -2.533   3.806  1.00  0.00           C  
ATOM    186  C   PRO A  12       7.058  -3.729   3.165  1.00  0.00           C  
ATOM    187  O   PRO A  12       8.139  -3.562   2.601  1.00  0.00           O  
ATOM    188  CB  PRO A  12       6.740  -2.387   5.279  1.00  0.00           C  
ATOM    189  CG  PRO A  12       5.460  -1.952   5.987  1.00  0.00           C  
ATOM    190  CD  PRO A  12       4.362  -2.615   5.160  1.00  0.00           C  
ATOM    191  HA  PRO A  12       6.611  -1.626   3.267  1.00  0.00           H  
ATOM    192  HB2 PRO A  12       7.091  -3.323   5.670  1.00  0.00           H  
ATOM    193  HB3 PRO A  12       7.531  -1.647   5.403  1.00  0.00           H  
ATOM    194  HG2 PRO A  12       5.443  -2.302   7.001  1.00  0.00           H  
ATOM    195  HG3 PRO A  12       5.358  -0.867   5.929  1.00  0.00           H  
ATOM    196  HD2 PRO A  12       4.173  -3.609   5.516  1.00  0.00           H  
ATOM    197  HD3 PRO A  12       3.440  -2.042   5.246  1.00  0.00           H  
ATOM    198  N   SER A  13       6.463  -4.929   3.205  1.00  0.00           N  
ATOM    199  CA  SER A  13       7.049  -6.179   2.704  1.00  0.00           C  
ATOM    200  C   SER A  13       6.897  -6.369   1.185  1.00  0.00           C  
ATOM    201  O   SER A  13       7.025  -7.488   0.697  1.00  0.00           O  
ATOM    202  CB  SER A  13       6.458  -7.371   3.472  1.00  0.00           C  
ATOM    203  OG  SER A  13       6.763  -7.264   4.850  1.00  0.00           O  
ATOM    204  H   SER A  13       5.535  -4.999   3.613  1.00  0.00           H  
ATOM    205  HA  SER A  13       8.121  -6.159   2.903  1.00  0.00           H  
ATOM    206  HB2 SER A  13       5.393  -7.382   3.344  1.00  0.00           H  
ATOM    207  HB3 SER A  13       6.880  -8.302   3.093  1.00  0.00           H  
ATOM    208  HG  SER A  13       7.707  -7.394   4.970  1.00  0.00           H  
ATOM    209  N   SER A  14       6.637  -5.290   0.434  1.00  0.00           N  
ATOM    210  CA  SER A  14       6.389  -5.315  -1.015  1.00  0.00           C  
ATOM    211  C   SER A  14       7.332  -4.405  -1.823  1.00  0.00           C  
ATOM    212  O   SER A  14       7.082  -4.123  -2.993  1.00  0.00           O  
ATOM    213  CB  SER A  14       4.914  -4.993  -1.265  1.00  0.00           C  
ATOM    214  OG  SER A  14       4.431  -5.743  -2.358  1.00  0.00           O  
ATOM    215  H   SER A  14       6.509  -4.415   0.930  1.00  0.00           H  
ATOM    216  HA  SER A  14       6.562  -6.329  -1.378  1.00  0.00           H  
ATOM    217  HB2 SER A  14       4.344  -5.236  -0.389  1.00  0.00           H  
ATOM    218  HB3 SER A  14       4.778  -3.934  -1.457  1.00  0.00           H  
ATOM    219  HG  SER A  14       3.714  -6.324  -1.987  1.00  0.00           H  
ATOM    220  N   GLY A  15       8.419  -3.920  -1.202  1.00  0.00           N  
ATOM    221  CA  GLY A  15       9.451  -3.116  -1.870  1.00  0.00           C  
ATOM    222  C   GLY A  15       8.984  -1.725  -2.316  1.00  0.00           C  
ATOM    223  O   GLY A  15       9.539  -1.177  -3.267  1.00  0.00           O  
ATOM    224  H   GLY A  15       8.573  -4.210  -0.246  1.00  0.00           H  
ATOM    225  HA2 GLY A  15      10.297  -2.987  -1.194  1.00  0.00           H  
ATOM    226  HA3 GLY A  15       9.805  -3.652  -2.752  1.00  0.00           H  
ATOM    227  N   ARG A  16       7.956  -1.164  -1.660  1.00  0.00           N  
ATOM    228  CA  ARG A  16       7.289   0.084  -2.054  1.00  0.00           C  
ATOM    229  C   ARG A  16       6.855   0.916  -0.829  1.00  0.00           C  
ATOM    230  O   ARG A  16       6.222   0.366   0.076  1.00  0.00           O  
ATOM    231  CB  ARG A  16       6.110  -0.243  -2.994  1.00  0.00           C  
ATOM    232  CG  ARG A  16       5.046  -1.171  -2.378  1.00  0.00           C  
ATOM    233  CD  ARG A  16       3.923  -1.592  -3.338  1.00  0.00           C  
ATOM    234  NE  ARG A  16       4.251  -2.811  -4.100  1.00  0.00           N  
ATOM    235  CZ  ARG A  16       4.859  -2.914  -5.274  1.00  0.00           C  
ATOM    236  NH1 ARG A  16       5.289  -1.864  -5.937  1.00  0.00           N  
ATOM    237  NH2 ARG A  16       5.035  -4.095  -5.809  1.00  0.00           N  
ATOM    238  H   ARG A  16       7.579  -1.676  -0.874  1.00  0.00           H  
ATOM    239  HA  ARG A  16       8.009   0.663  -2.630  1.00  0.00           H  
ATOM    240  HB2 ARG A  16       5.634   0.678  -3.269  1.00  0.00           H  
ATOM    241  HB3 ARG A  16       6.524  -0.720  -3.880  1.00  0.00           H  
ATOM    242  HG2 ARG A  16       5.538  -2.059  -2.031  1.00  0.00           H  
ATOM    243  HG3 ARG A  16       4.579  -0.652  -1.549  1.00  0.00           H  
ATOM    244  HD2 ARG A  16       3.033  -1.774  -2.766  1.00  0.00           H  
ATOM    245  HD3 ARG A  16       3.669  -0.765  -4.003  1.00  0.00           H  
ATOM    246  HE  ARG A  16       3.963  -3.694  -3.698  1.00  0.00           H  
ATOM    247 HH11 ARG A  16       5.150  -0.962  -5.521  1.00  0.00           H  
ATOM    248 HH12 ARG A  16       5.761  -1.962  -6.815  1.00  0.00           H  
ATOM    249 HH21 ARG A  16       4.649  -4.894  -5.327  1.00  0.00           H  
ATOM    250 HH22 ARG A  16       5.508  -4.205  -6.684  1.00  0.00           H  
ATOM    251  N   PRO A  17       7.156   2.230  -0.780  1.00  0.00           N  
ATOM    252  CA  PRO A  17       6.782   3.088   0.345  1.00  0.00           C  
ATOM    253  C   PRO A  17       5.261   3.331   0.395  1.00  0.00           C  
ATOM    254  O   PRO A  17       4.586   3.165  -0.624  1.00  0.00           O  
ATOM    255  CB  PRO A  17       7.554   4.394   0.119  1.00  0.00           C  
ATOM    256  CG  PRO A  17       7.677   4.474  -1.401  1.00  0.00           C  
ATOM    257  CD  PRO A  17       7.820   3.010  -1.816  1.00  0.00           C  
ATOM    258  HA  PRO A  17       7.107   2.628   1.279  1.00  0.00           H  
ATOM    259  HB2 PRO A  17       7.009   5.234   0.505  1.00  0.00           H  
ATOM    260  HB3 PRO A  17       8.548   4.308   0.561  1.00  0.00           H  
ATOM    261  HG2 PRO A  17       6.800   4.914  -1.836  1.00  0.00           H  
ATOM    262  HG3 PRO A  17       8.540   5.066  -1.707  1.00  0.00           H  
ATOM    263  HD2 PRO A  17       7.349   2.844  -2.766  1.00  0.00           H  
ATOM    264  HD3 PRO A  17       8.876   2.739  -1.855  1.00  0.00           H  
ATOM    265  N   PRO A  18       4.710   3.739   1.555  1.00  0.00           N  
ATOM    266  CA  PRO A  18       3.287   4.031   1.686  1.00  0.00           C  
ATOM    267  C   PRO A  18       2.901   5.305   0.913  1.00  0.00           C  
ATOM    268  O   PRO A  18       3.684   6.256   0.871  1.00  0.00           O  
ATOM    269  CB  PRO A  18       3.035   4.190   3.187  1.00  0.00           C  
ATOM    270  CG  PRO A  18       4.385   4.655   3.729  1.00  0.00           C  
ATOM    271  CD  PRO A  18       5.393   3.949   2.823  1.00  0.00           C  
ATOM    272  HA  PRO A  18       2.719   3.181   1.316  1.00  0.00           H  
ATOM    273  HB2 PRO A  18       2.274   4.924   3.372  1.00  0.00           H  
ATOM    274  HB3 PRO A  18       2.781   3.223   3.618  1.00  0.00           H  
ATOM    275  HG2 PRO A  18       4.482   5.721   3.654  1.00  0.00           H  
ATOM    276  HG3 PRO A  18       4.518   4.377   4.775  1.00  0.00           H  
ATOM    277  HD2 PRO A  18       6.262   4.562   2.682  1.00  0.00           H  
ATOM    278  HD3 PRO A  18       5.662   2.983   3.253  1.00  0.00           H  
ATOM    279  N   PRO A  19       1.688   5.360   0.336  1.00  0.00           N  
ATOM    280  CA  PRO A  19       1.185   6.543  -0.353  1.00  0.00           C  
ATOM    281  C   PRO A  19       0.715   7.607   0.655  1.00  0.00           C  
ATOM    282  O   PRO A  19      -0.124   7.324   1.513  1.00  0.00           O  
ATOM    283  CB  PRO A  19       0.048   6.014  -1.229  1.00  0.00           C  
ATOM    284  CG  PRO A  19      -0.519   4.852  -0.412  1.00  0.00           C  
ATOM    285  CD  PRO A  19       0.716   4.275   0.272  1.00  0.00           C  
ATOM    286  HA  PRO A  19       1.961   6.966  -0.991  1.00  0.00           H  
ATOM    287  HB2 PRO A  19      -0.697   6.770  -1.389  1.00  0.00           H  
ATOM    288  HB3 PRO A  19       0.463   5.630  -2.162  1.00  0.00           H  
ATOM    289  HG2 PRO A  19      -1.232   5.201   0.310  1.00  0.00           H  
ATOM    290  HG3 PRO A  19      -1.019   4.114  -1.041  1.00  0.00           H  
ATOM    291  HD2 PRO A  19       0.470   3.937   1.260  1.00  0.00           H  
ATOM    292  HD3 PRO A  19       1.121   3.461  -0.329  1.00  0.00           H  
ATOM    293  N   SER A  20       1.271   8.822   0.549  1.00  0.00           N  
ATOM    294  CA  SER A  20       0.852  10.027   1.285  1.00  0.00           C  
ATOM    295  C   SER A  20      -0.406  10.657   0.683  1.00  0.00           C  
ATOM    296  O   SER A  20      -0.387  10.916  -0.540  1.00  0.00           O  
ATOM    297  CB  SER A  20       1.972  11.071   1.284  1.00  0.00           C  
ATOM    298  OG  SER A  20       3.120  10.541   1.911  1.00  0.00           O  
ATOM    299  OXT SER A  20      -1.341  10.903   1.473  1.00  0.00           O  
ATOM    300  H   SER A  20       1.969   8.961  -0.165  1.00  0.00           H  
ATOM    301  HA  SER A  20       0.601   9.760   2.310  1.00  0.00           H  
ATOM    302  HB2 SER A  20       2.210  11.338   0.272  1.00  0.00           H  
ATOM    303  HB3 SER A  20       1.636  11.959   1.824  1.00  0.00           H  
ATOM    304  HG  SER A  20       2.831  10.040   2.676  1.00  0.00           H  
TER     305      SER A  20                                                      """)

    t = Xponge.load_pdb(pdb)
    t.add_missing_atoms()
    Xponge.add_solvent_box(t, Xponge.ResidueType.get_type("WAT"), 20)
    Xponge.save_sponge_input(t, "trp_cage")
    cv = CVSystem(t)
    cv.add_cv_rmsd("RMSD", "protein and backbone")
    cv.add_cv_density("rho")
    cv.restrain("rho", 1e6, 1, stop_step=50000)
    cv.restrain("RMSD", 50, 0, max_step=50000, reduce_step=50000, stop_step=100000)
    cv.print("RMSD")
    cv.print("rho")
    cv.output("cv.txt")
    assert run("SPONGE -default_in_file_prefix trp_cage -mode minimization -rst min > min.out") == 0
    assert run("SPONGE -default_in_file_prefix trp_cage -mode nvt \
-thermostat andersen_thermostat -target_temperature 2000 -rst heat \
-cutoff 8 -coordinate_in_file min_coordinate.txt -step_limit 100000 \
-dt 1e-3 -constrain_mode SHAKE > heat.out") == 0
    assert run("SPONGE -default_in_file_prefix trp_cage -mode npt -cv_in_file cv.txt \
-thermostat andersen_thermostat -barostat andersen_barostat -target_temperature 300 \
-cutoff 8 -coordinate_in_file heat_coordinate.txt -step_limit 100000 \
-dt 2e-3 -constrain_mode SHAKE > npt.out") == 0
