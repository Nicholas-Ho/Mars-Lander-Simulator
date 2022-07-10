import numpy as np

# Universal gravitation constant
G = 6.67430e-11

def euler_int(conditions, dt, t_array):
    # constants and initial conditions
    m, M, R, position, velocity = conditions

    # initialise empty lists to record trajectories
    pos_list = []
    vel_list = []

    # collision checking
    collision = False

    # Euler integration
    for t in t_array:

        # append current state to trajectories
        pos_list.append(position)
        vel_list.append(velocity)

        # check for collisions
        if np.linalg.norm(position) <= R:
            collision = True
            break

        # calculate new position and velocity
        # note: all vectors
        unit_pos = position / np.linalg.norm(position)
        a = -(G*M) * unit_pos / (np.linalg.norm(position)**2)
        position = position + dt * velocity
        velocity = velocity + dt * a

    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    pos_array = np.array(pos_list)
    vel_array = np.array(vel_list)
        
    return pos_array, vel_array, collision

def verlet_int(conditions, dt, t_array):
    # constants and initial conditions
    m, M, R, position, velocity = conditions

    # initialise lists to record trajectories
    pos_list = [position, position + dt*velocity]
    vel_list = [velocity]

    # collision checking
    collision = False

    # Verlet integration
    # will result in x_list that has an extra entry of t = t_max+1
    for t in range(len(t_array)-1):

        # note: x_list[-1] is current position
        # calculate new position and current velocity
        current_pos_unit = pos_list[-1] / np.linalg.norm(pos_list[-1])
        a = -(G*M) * current_pos_unit / (np.linalg.norm(pos_list[-1])**2) # current acceleration

        position = 2 * pos_list[-1] - pos_list[-2] + (dt**2) * a
        velocity = (position - pos_list[-2]) / (2 * dt)

        # append new state to trajectories
        pos_list.append(position)
        vel_list.append(velocity)

        # check for collisions
        if np.linalg.norm(pos_list[-1]) <= R:
            collision = True
            break

    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    pos_array = np.array(pos_list[:-1])
    vel_array = np.array(vel_list)

    return pos_array, vel_array, collision
