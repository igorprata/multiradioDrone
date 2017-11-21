# -*- coding: utf-8 -*-
import localization as lx


##################### Codigo de multilateração de dados obtidos durante o voo que substituirá o código atual#############################
# Só é possivel usar métodos diferentes do LSE se os circulos das dist6ancias se conectarem.
# Otimizar os valores toleráveis e só importar esses
# Lib utilizada: https://pypi.python.org/pypi/Localization/0.1.4


P=lx.Project(mode="Earth1",solver="LSE")

# Currently three modes are supported:
# 1-2D
# 2-3D
# 3-Earth1
#
# Also three solvers can be utilized:
# 1-LSE for least square error
# 2-LSE_GC for least square error with geometric constraints. Geometric constraints force the solutions to be in the intersection areas of all multilateration circles.
# 3-CCA for centroid method, i.e., the solution will be the centroid of the intersection area. If no common intersection area exist, the area with maximum overlap is used.

# Fabio
# anchor = [(-22.86985120,-43.1051227),(-22.86983310,-43.1051285),(-22.86984080,-43.1051355),(-22.86983130,-43.1051311),(-22.86984440,-43.1051408),(-22.86987940,-43.1051325),(-22.86986800,-43.1051353),(-22.86986740,-43.1051099),(-22.86982530,-43.1051313),(-22.86986990,-43.1051268),(-22.86987800,-43.1051076),(-22.86984740,-43.1051061),(-22.86984480,-43.1051351),(-22.86984460,-43.1051185),(-22.86986010,-43.1051341),(-22.86987300,-43.1051315),(-22.86985720,-43.1051022),(-22.86986560,-43.1051251),(-22.86986950,-43.1051279),(-22.86987230,-43.1051344),(-22.86984940,-43.1051007),(-22.86984500,-43.1051201),(-22.86992110,-43.1050613),(-22.86984650,-43.1050980),(-22.86997450,-43.1050409),(-22.86984980,-43.1050972),(-22.86989680,-43.1050272),(-22.86984260,-43.1050673),(-22.86982940,-43.1050112),(-22.86996080,-43.1050254)]
# dist_wf = (0.000251189,0.000271227,0.000292864,0.000316228,0.000316228,0.000398107,0.000398107,0.000398107,0.000398107,0.000429866,0.000429866,0.000464159,0.000464159,0.000501187,0.000681292,0.000735642,0.000926119,0.001000000,0.001079775,0.001165914,0.001165914,0.001847850,0.001847850,0.002712273,0.002712273,0.002928645,0.002928645,0.003162278,0.003981072,0.005843414)

# Voo de 17 Nov 2017
anchor = [(-20.7463786,-41.2290764),(-20.7465702,-41.2290774),(-20.7465712,-41.2293447),(-20.7463795,-41.2293439)]
dist_wf = (0.0130352714943,0.0163173436884,0.00627227441873,0.0041974967925)


t, label = P.add_target()


for i in range(len(dist_wf)):
    radius = dist_wf[i]
    anchorlatlon = anchor[i]
    point = "point%03i" % i
    P.add_anchor(point,anchorlatlon)
    t.add_measure(point,radius)

P.solve()
print t.loc
print t


