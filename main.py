import numpy as np
import matplotlib.pyplot as plt


# Here the index 0 denotes values related to CH4, 1 to C2H4, 2 to C2H2
LDL = np.array([5, 5, 5])
RANGE = np.array([10000, 10000, 10000])


#
# A function to generate three gases concentrations all uniformly distributed in its respected measurement range
# These concentrations are used as true values
#
def generate_concentrations(num_samples):
    concentrations = np.empty([num_samples, 3])
    for i in range(num_samples):
        concentrations[i][0] = np.random.uniform(RANGE[0])
        concentrations[i][1] = np.random.uniform(RANGE[1])
        concentrations[i][2] = np.random.uniform(RANGE[2])
    return concentrations


#
# A function to generate three gases concentrations as measured by the measurement instrument
# Calculated as normal distribution with the true value being the mean and uncertainty being
# twice standard deviation
#
def generate_measured_concentrations(msrmnts, acc):
    measured_concentrations = np.empty([len(msrmnts), 3])
    for i in range(len(msrmnts)):
        measured_concentrations[i][0] = msrmnts[i][0] + max(msrmnts[i][0] * acc / 100, LDL[0]) * np.random.randn() / 2
        measured_concentrations[i][1] = msrmnts[i][1] + max(msrmnts[i][1] * acc / 100, LDL[1]) * np.random.randn() / 2
        measured_concentrations[i][2] = msrmnts[i][2] + max(msrmnts[i][2] * acc / 100, LDL[2]) * np.random.randn() / 2
    return measured_concentrations


#
# A function to determine a Duval region corresponding to a given set of concentrations
# Result 0 means no region (something went wrong), 1 is PD, 2 is T1, 3 is T2, 4 is T3, 5 is D1, 6 is D2, 7 is DT
#
def get_duval_region(concentrations):
    region = np.empty(len(concentrations), dtype=int)
    for i in range(len(region)):
        w_ch4 = 100 * concentrations[i][0] / sum(concentrations[i])
        w_c2h4 = 100 * concentrations[i][1] / sum(concentrations[i])
        w_c2h2 = 100 - w_c2h4 - w_ch4
        if w_ch4 >= 98:
            region[i] = 1
        elif w_c2h2 <= 4 and w_c2h4 <= 20 and w_ch4 <= 98:
            region[i] = 2
        elif w_c2h4 >= 20 and w_c2h4 <= 50 and w_c2h2 <= 4:
            region[i] = 3
        elif w_c2h2 <= 15 and w_c2h4 >= 50:
            region[i] = 4
        elif w_c2h2 >= 13 and w_c2h4 <= 23:
            region[i] = 5
        elif (w_c2h2 >= 29 and w_c2h4 >= 23) or (w_c2h4 >= 23 and w_c2h4 <= 40 and w_c2h2 >= 13):
            region[i] = 6
        else:
            region[i] = 7

    return region


#
# Run measurements
# Given the measurements of the NUM_SAMPLES amount and accuracy acc, calculate the number of measurements where
# Duval triangle region calculated for true values matches that of measured values and vice versa
#
def generate_single_result(num_samples, acc):
    a = generate_concentrations(num_samples)
    b = generate_measured_concentrations(a, acc)
    a_duval = get_duval_region(a)
    b_duval = get_duval_region(b)
    c1 = c2 = 0
    for i in range(num_samples):
        if a_duval[i] == b_duval[i]:
            c1 += 1
        else:
            c2 += 1
    return np.array([acc, c1, c2, 100 * c1 / (c1 + c2)], dtype=int)


#
# A function to generate a set of measurements with accuracy changing from 0% to 100%
# with the points of amount num_acc_step and the amount of results per each accuracy value num_acc_samples
#
def generate_result(num_samples, num_acc_step, num_acc_samples):
    result = np.empty([num_acc_step * num_acc_samples, 4], dtype=int)
    accuracy = np.linspace(0, 100, num=num_acc_step)
    mean_result = np.empty([num_acc_step, 2])
    for i in range(num_acc_step):
        m = 0
        for j in range(num_acc_samples):
            result[i * num_acc_samples + j] = generate_single_result(num_samples, accuracy[i])
            m += result[i * num_acc_samples + j][3]
        mean_result[i] = np.array([accuracy[i], m / num_acc_samples])
        print(f'i >> {i}')
    return result, mean_result


#
# Do the same as the function above but the results are visualized and saved to csv file
#
def show_result(num_samples, num_acc_step, num_acc_samples):
    A, B = generate_result(num_samples, num_acc_step, num_acc_samples)
    np.savetxt('data.csv', A, delimiter=',', fmt='%10.1f')
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.scatter(A[:, 0], A[:, 3], marker='o')
    ax1.set_ylim([0, 110])
    ax2.plot(B[:, 0], B[:, 1], marker='x', color='r')
    ax2.set_ylim([0, 110])
    plt.show()


#
# Check how true and measured values relate to each other
#
def check_measurements():
    A = generate_concentrations(100)
    B = generate_measured_concentrations(A, 10)
    C = 100 * (B - A) / A
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    ax1.plot(C[:, 0], marker='x')
    ax2.plot(C[:, 1], marker='x')
    ax3.plot(C[:, 2], marker='x')
    plt.show()

show_result(20, 21, 200)