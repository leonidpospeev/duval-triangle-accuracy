import numpy as np
import matplotlib.pyplot as plt


LDL_CH4 = 5
LDL_C2H4 = 5
LDL_C2H2 = 5

RANGE_CH4 = 5000
RANGE_C2H4 = 5000
RANGE_C2H2 = 5000

NUM_SAMPLES = 100


# 0 is no region
# 1 is PD
# 2 is T1
# 3 is T2
# 4 is T3
# 5 is D1
# 6 is D2
# 7 is DT
def get_duval_region(c_ch4, c_c2h4, c_c2h2):
    reg = 0

    w_ch4 = 100 * c_ch4 / (c_ch4 + c_c2h2 + c_c2h4)
    w_c2h4 = 100 * c_c2h4 / (c_ch4 + c_c2h2 + c_c2h4)

    w_c2h2 = 100 - w_c2h4 - w_ch4

    #print(f'>> {w_ch4} a {w_c2h4} a {w_c2h2}')
    if w_ch4 >= 98:
        reg = 1
    elif w_c2h2 <= 4 and w_c2h4 <= 20 and w_ch4 <= 98:
        reg = 2
    elif w_c2h4 >= 20 and w_c2h4 <= 50 and w_c2h2 <= 4:
        reg = 3
    elif w_c2h2 <= 15 and w_c2h4 >= 50:
        reg = 4
    elif w_c2h2 >= 13 and w_c2h4 <= 23:
        reg = 5
    elif (w_c2h2 >= 29 and w_c2h4 >= 23) or (w_c2h4 >= 23 and w_c2h4 <= 40 and w_c2h2 >= 13):
        reg = 6
    else:
        reg = 7

    return reg


def generate_samples():
    msrmnts = np.empty([NUM_SAMPLES, 11])
    for i in range(NUM_SAMPLES):
        msrmnts[i][0] = i
        msrmnts[i][1] = np.random.uniform(RANGE_CH4)
        msrmnts[i][2] = np.random.uniform(RANGE_C2H4)
        msrmnts[i][3] = np.random.uniform(RANGE_C2H2)
        msrmnts[i][4] = get_duval_region(msrmnts[i][1], msrmnts[i][2], msrmnts[i][3])
        msrmnts[i][5] = 100 * msrmnts[i][1] / (msrmnts[i][1] + msrmnts[i][2] + msrmnts[i][3])
        msrmnts[i][6] = 100 * msrmnts[i][2] / (msrmnts[i][1] + msrmnts[i][2] + msrmnts[i][3])
        msrmnts[i][7] = 1
        msrmnts[i][8] = msrmnts[i][1] + 1000 * np.random.randn()
        msrmnts[i][9] = msrmnts[i][2] + 5 * np.random.randn()
        msrmnts[i][10] = msrmnts[i][3] + 5 * np.random.randn()
    return msrmnts


A = generate_samples()
print(A)

fig, ax = plt.subplots()
ax.plot(A[:, 0], A[:, 8], label='8', marker='o')
ax.plot(A[:, 0], A[:, 1], label='1', marker='x')
plt.show()