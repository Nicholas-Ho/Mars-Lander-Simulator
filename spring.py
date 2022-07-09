# uncomment the next line if running in a notebook
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# mass, spring constant, initial position and velocity
m = 1
k = 1
x = 0
v = 1

conditions = (m, k, x, v)

# simulation time, timestep and time
t_max = 100
dt = 0.1
t_array = np.arange(0, t_max, dt)

def euler_int(conditions, dt, t_array):
    # constants and initial conditions
    m, k, x, v = conditions

    # initialise empty lists to record trajectories
    x_list = []
    v_list = []

    # Euler integration
    for t in t_array:

        # append current state to trajectories
        x_list.append(x)
        v_list.append(v)

        # calculate new position and velocity
        a = -k * x / m
        x = x + dt * v
        v = v + dt * a

    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    x_array = np.array(x_list)
    v_array = np.array(v_list)

    # plot the position-time graph
    plt.figure(1)
    plt.clf()
    plt.xlabel('time (s)')
    plt.grid()
    plt.plot(t_array, x_array, label='x (m)')
    plt.plot(t_array, v_array, label='v (m/s)')
    plt.legend()
    plt.show()

def verlet_int(conditions, dt, t_array):
    # constants and initial conditions
    m, k, x, v = conditions

    # initialise lists to record trajectories
    x_list = [x, dt*v]
    v_list = [v]

    # Verlet integration
    # will result in x_list that has an extra entry of t = t_max+1
    for t in range(len(t_array)-1):

        # note: x_list[-1] is current position
        # calculate new position and current velocity
        a = -k * x_list[-1] / m # current acceleration
        x = 2 * x_list[-1] - x_list[-2] + (dt**2) * a
        v = (x - x_list[-2]) / (2 * dt)

        # append new state to trajectories
        x_list.append(x)
        v_list.append(v)

    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    x_array = np.array(x_list[:-1])
    v_array = np.array(v_list)

    # plot the position-time graph
    plt.figure(1)
    plt.clf()
    plt.xlabel('time (s)')
    plt.grid()
    plt.plot(t_array, x_array, label='x (m)')
    plt.plot(t_array, v_array, label='v (m/s)')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    euler_int(conditions, dt, t_array)
    verlet_int(conditions, dt, t_array)