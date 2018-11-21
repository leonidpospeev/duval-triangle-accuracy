import numpy as np
import matplotlib.pyplot as plt


# 0 is no region
# 1 is PD
# 2 is T1
# 3 is T2
# 4 is T3
# 5 is D1
# 6 is D2
# 7 is DT
def get_duval_region(w_ch4, w_c2h4):
    reg = 0

    w_h2h2 = 100 - w_c2h4 - w_ch4
    if w_ch4 >= 90:
        reg = 1
    elif w_h2h2 <= 4 and w_c2h4 <= 20 and w_ch4 <= 98:
        reg = 2
    elif w_c2h4 >= 20 and w_c2h4 <= 50 and w_h2h2 <= 4:
        reg = 3
    elif w_h2h2 <= 15 and w_c2h4 >= 50:
        reg = 4
    elif w_h2h2 >= 13 and w_c2h4 <= 23:
        reg = 5
    elif (w_h2h2 >= 29 and w_c2h4 >= 23) or (w_c2h4 >= 23 and w_c2h4 <= 40 and w_h2h2 >= 13):
        reg = 6
    else:
        reg = 7

    return reg


print(get_duval_region(20, 80))