from spring import euler_int, verlet_int

import numpy as np
import matplotlib.pyplot as plt

# mass, spring constant, initial position and velocity
m = 1
k = 1
x = 0
v = 1

conditions = (m, k, x, v)

# simulation_time
t_max = 7000

def base_truth():
    # set conditions such that amplitude = 1
    amplitude = 1

    w = np.sqrt(k/m)
    f = w /  (2 * np.pi)
    T = 1 / f
    t = t_max % T
    th = 2*np.pi * t/T

    x = amplitude * np.sin(th)

    th = th + (np.pi / 2)
    v = amplitude * np.sin(th)

    return x, v

x_truth, v_truth = base_truth()

def test_ints_error():

    # timestep and time
    dts = np.arange(0.01, 0.1, 0.01)
    t_arrays = [np.arange(0, t_max, dt) for dt in dts]

    euler_error = []
    verlet_error = []

    for dt, t_array in zip(dts, t_arrays):

        # get error
        e_x, e_v = euler_int(conditions, dt, t_array, plot=False)
        v_x, v_v = verlet_int(conditions, dt, t_array, plot=False)

        # use x error
        euler_error.append(np.abs(e_x[-1] - x_truth))
        verlet_error.append(np.abs(v_x[-1] - x_truth))

    return dts, euler_error, verlet_error

def test_euler_error():

    # timestep and time
    dts = np.arange(0.001, 0.05, 0.001)
    t_arrays = [np.arange(0, t_max, dt) for dt in dts]

    euler_error = []

    for dt, t_array in zip(dts, t_arrays):

        # get error
        e_x, e_v = euler_int(conditions, dt, t_array, plot=False)

        # use x error
        euler_error.append(np.abs(e_x[-1] - x_truth))
    
    return dts, euler_error, None

def test_verlet_error():

    # timestep and time
    dts = np.arange(0.01, 2, 0.01)
    t_arrays = [np.arange(0, t_max, dt) for dt in dts]

    verlet_error = []

    for dt, t_array in zip(dts, t_arrays):

        # get error
        v_x, v_v = verlet_int(conditions, dt, t_array, plot=False)

        # use x error
        verlet_error.append(np.abs(v_x[-1] - x_truth))

    return dts, None, verlet_error

def test_verlet_stability(thresh=25, plot=False):

    # timestep and time
    dts = np.arange(0.01, 3, 0.01)
    t_arrays = [np.arange(0, t_max, dt) for dt in dts]

    crit_dt = 0
    crit_x = []
    crit_v = []

    for dt, t_array in zip(dts, t_arrays):

        # get result
        v_x, v_v = verlet_int(conditions, dt, t_array, plot=False)

        if v_x.max() > thresh:
            crit_dt = dt
            crit_x = v_x
            crit_v = v_v
            break

    print(f'Critical dt: {crit_dt} with maximum value of {crit_x.max()}')

    if plot:
        # plot the position-time graph
        plt.figure(1)
        plt.clf()
        plt.xlabel('time (s)')
        plt.grid()
        plt.plot(t_array, crit_x, label='x (m)')
        plt.plot(t_array, crit_v, label='v (m/s)')
        plt.legend()
        plt.show()

    return crit_dt, crit_x

def plot_all(data=[]):
    for graph in data:
        dts, euler_error, verlet_error = graph
        # plot the error graph
        plt.figure(1)
        plt.title('Error')
        plt.clf()
        plt.xlabel('time (s)')
        plt.grid()
        if euler_error != None: plt.plot(dts, euler_error, label='Euler')
        if verlet_error != None: plt.plot(dts, verlet_error, label='Verlot')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    int_e = test_ints_error()
    euler_e = test_euler_error()
    verlet_e = test_verlet_error()
    plot_all([int_e, euler_e, verlet_e])
    test_verlet_stability(thresh=10, plot=True)