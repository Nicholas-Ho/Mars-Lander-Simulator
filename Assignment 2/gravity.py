import numpy as np
import matplotlib.pyplot as plt
from plot_utils import plot_anim

# Universal gravitation constant
G = 6.67430e-11

def euler_int(conditions, dt, t_array, plot=False):
    # constants and initial conditions
    m, M, position, velocity = conditions

    # initialise empty lists to record trajectories
    pos_list = []
    vel_list = []

    # Euler integration
    for t in t_array:

        # append current state to trajectories
        pos_list.append(position)
        vel_list.append(velocity)

        # calculate new position and velocity
        # note: all vectors
        unit_pos = position / np.linalg.norm(position)
        a = -(G*M) * unit_pos / (np.linalg.norm(position)**2)
        position = position + dt * velocity
        velocity = velocity + dt * a

    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    pos_array = np.array(pos_list)
    vel_array = np.array(vel_list)

    if plot:
        plot_anim(pos_array, 'Euler', fps=6000)
        
    return pos_array, vel_array

def verlet_int(conditions, dt, t_array, plot=False):
    # constants and initial conditions
    m, M, position, velocity = conditions

    # initialise lists to record trajectories
    pos_list = [position, position + dt*velocity]
    vel_list = [velocity]

    # Verlet integration
    # will result in x_list that has an extra entry of t = t_max+1
    for t in range(len(t_array)-1):

        # note: x_list[-1] is current position
        # calculate new position and current velocity
        current_pos_unit = pos_list[-1] / np.linalg.norm(pos_list[-1])
        a = -(G*M) * current_pos_unit / (np.linalg.norm(pos_list[-1])**2) # current acceleration

        x = 2 * pos_list[-1] - pos_list[-2] + (dt**2) * a
        v = (x - pos_list[-2]) / (2 * dt)

        # append new state to trajectories
        pos_list.append(x)
        vel_list.append(v)

    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    pos_array = np.array(pos_list[:-1])
    vel_array = np.array(vel_list)

    if plot:
        plot_anim(pos_array, 'Verlet', fps=6000)

    return pos_array, vel_array

# Testing

# mass, spring constant, initial position and velocity
m = 1
M = 6.42e23
position = np.array([1e2, 0, 0]) # [x, y, z]
velocity = np.array([0, 0, 0]) # [x, y, z]

conditions = (m, M, position, velocity)

# simulation time, timestep and time
t_max = 1e3

if __name__ == "__main__":

    dt = 0.1
    t_array = np.arange(0, t_max, dt)

    euler_int(conditions, dt, t_array, plot=True)

    # dt = 1
    # t_array = np.arange(0, t_max, dt)

    # verlet_int(conditions, dt, t_array, plot=True)