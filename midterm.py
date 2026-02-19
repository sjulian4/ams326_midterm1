import numpy as np


import matplotlib.pyplot as plt # need to install matplotlib


# time t = 1 --> Jan 1
# t = 32 --> Feb 1. etc.

# 50 190 366 are the days we need

#assume each month is 31 days, average representing temp on 16th

# (1) Piecewise linear interpolation of the 12 monthly averages.
# todo: check if the t_Values are actually representative of the 16th of every month
t_values = np.array([16, 47, 78, 109, 140, 171, 202, 233, 264, 295, 326, 357]) # the middle of each month, todo fix this data
temps_high = np.array([40,41,48,60,69,77,83,82,75,64,54,45]) # the 'y' value, and rightmost matrix on the page 6 of topic 2 notes
temps_average = np.array([33,34,40,51,60,69,75,74,67,56,47,38])
temps_low = np.array([26,26,32,42,51,61,67,66,60,49,39,31])

def piecewise_linear(t, t_data, y_data):
    # extrapolate using the line between Nov 16 and Dec 16 for past December 16
    if t >= t_data[-1]:
        t0, t1 = t_data[-2], t_data[-1]
        y0, y1 = y_data[-2], y_data[-1]
    #  points before Jan 16 (e.g. Jan 1) by extrapolating Jan-Feb
    elif t <= t_data[0]:
        t0, t1 = t_data[0], t_data[1]
        y0, y1 = y_data[0], y_data[1]
    else:
        # index of the first t_data greater than our target t
        idx = np.searchsorted(t_data, t)
        t0, t1 = t_data[idx-1], t_data[idx]
        y0, y1 = y_data[idx-1], y_data[idx]
        
    #  linear interpolation formula from notes
    return y0 + (t - t0) * (y1 - y0) / (t1 - t0)
print("Part 1:")
print("High value Feb 19: " + str(piecewise_linear(50, t_values, temps_high)))
print("Average value Feb 19: " + str(piecewise_linear(50, t_values, temps_average)))
print("Low value Feb 19: " + str(piecewise_linear(50, t_values, temps_low)))

print("High value July 4: " + str(piecewise_linear(190, t_values, temps_high)))
print("Average value July 4: " + str(piecewise_linear(190, t_values, temps_average)))
print("Low value July 4: " + str(piecewise_linear(190, t_values, temps_low)))

print("High value Dec 25: " + str(piecewise_linear(366, t_values, temps_high)))
print("Average value Dec 25: " + str(piecewise_linear(366, t_values, temps_average)))
print("Low value Dec 25: " + str(piecewise_linear(366, t_values, temps_low)))

# (2) Polynomial interpolation through 9 evenly spaced points over the year using results in (1).

total_days = 31 * 12

interval = np.floor(total_days / 9) # every interval days

days = []
high_values = []
average_values = []
low_values = []
for i in range(9):
    days.append(i*interval + 1)
    high_values.append(piecewise_linear(i*interval + 1, t_values, temps_high))
    average_values.append(piecewise_linear(i*interval + 1, t_values, temps_average))
    low_values.append(piecewise_linear(i*interval + 1, t_values, temps_low))




def P_9(t, data):
    func = 0.0
    for i in range(9):
        coefficient = 1
        for j in range(9):
            if j != i:
                coefficient *= (t - days[j]) / (days[i] - days[j])
        func += data[i] * coefficient
    return func
print("Part 2:")

print("High value Feb 19: " + str(P_9(50, high_values)))
print("Average value Feb 19: " + str(P_9(50, average_values)))
print("Low value Feb 19: " + str(P_9(50, low_values)))

print("High value July 4: " + str(P_9(190, high_values)))
print("Average value July 4: " + str(P_9(190, average_values)))
print("Low value July 4: " + str(P_9(190, low_values)))

print("High value Dec 25: " + str(P_9(366, high_values)))
print("Average value Dec 25: " + str(P_9(366, average_values)))
print("Low value Dec 25: " + str(P_9(366, low_values)))


# (3) Direct 4th-order polynomial fit to the 12 monthly averages.




X = np.column_stack([t_values**0, t_values**1, t_values**2, t_values**3, t_values**4])
X = np.zeros((12, 5))

#establish the matrix
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        X[i,j] += t_values[i] ** j
# Each row becomes [1, t, t^2, t^3, t^4]

coeffs_high = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.transpose(), X)), X.transpose()), temps_high)
coeffs_average = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.transpose(), X)), X.transpose()), temps_average)
coeffs_low = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.transpose(), X)), X.transpose()), temps_low)

def P_4_fit(t, coeffs):
    return coeffs[0] + coeffs[1]*t + coeffs[2]*(t**2) + coeffs[3]*(t**3) + coeffs[4]*(t**4) 
print("Part 3:")
print("High value Feb 19: " + str(P_4_fit(50, coeffs_high)))
print("Average value Feb 19: " + str(P_4_fit(50, coeffs_average)))
print("Low value Feb 19: " + str(P_4_fit(50, coeffs_low)))

print("High value July 4: " + str(P_4_fit(190, coeffs_high)))
print("Average value July 4: " + str(P_4_fit(190, coeffs_average)))
print("Low value July 4: " + str(P_4_fit(190, coeffs_low)))

print("High value Dec 25: " + str(P_4_fit(366, coeffs_high)))
print("Average value Dec 25: " + str(P_4_fit(366, coeffs_average)))
print("Low value Dec 25: " + str(P_4_fit(366, coeffs_low)))