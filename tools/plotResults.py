# coding: utf-8

import numpy as np
import sympy
import matplotlib.pyplot as plt
from scipy.stats import norm

RSSI = [[-70,-70,-70,-70,-70,-70,-70,-70,-70,-70,-71,-71,-71,-71,-71,-70,-70,-70,-70],[-77,-77,-77,-77,-77,-77,-71,-71,-71,-71,-71,-72,-72,-72,-72,-72,-72,-72,-72,-72],[-78,-73,-73,-73,-73,-73,-73,-73,-73,-73,-73,-73,-73,-73,-73,-73,-80,-80,-80,-80],[-80,-77,-77,-77,-77,-77,-82,-82,-82,-82,-82,-76,-76,-76,-76,-76,-80,-80,-80,-80],[-60,-57,-57,-57,-57,-57,-58,-58,-58,-58,-58,-58,-58,-58,-58,-58,-64,-64,-64,-64]]

for RSSI_position in RSSI:
#    ave = np.sum(RSSI_position) / len(RSSI_position)
    xs = range(len(RSSI_position))
    line = np.poly1d(np.polyfit(xs, RSSI_position, 1))
    plt.plot(RSSI_position, label="dBm")
    plt.plot(xs, line(xs), c="r", label ="hypothesis")
    plt.xlabel("numero da amostra")
    plt.ylabel("dBm(mW)")
    plt.legend(loc="best")
plt.show()


# plt.plot(RSSI_1)
# plt.plot(RSSI_2)
# plt.plot(RSSI_3)
# plt.plot(RSSI_4)
# plt.plot(RSSI_5)
# plt.xlabel("numero da amostra")
# plt.ylabel("dbm (xx)")
# plt.show()