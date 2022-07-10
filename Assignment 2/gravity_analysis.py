from gravity import euler_int, verlet_int, G
import numpy as np
import matplotlib.pyplot as plt

def plot_alt(data, t_array, name='Altitude'):
    e_pos, e_vel, collision = data

    t_array = t_array[:len(e_pos)]

    e_pos = np.transpose(e_pos)
    e_vel = np.transpose(e_vel)

    plt.figure(1)
    plt.clf()
    plt.xlabel('time (s)')
    plt.grid()
    plt.plot(t_array, e_pos[0], label=name)
    plt.legend()
    plt.show()

    if collision: print('Collision!')
    else: print('No collision.')

def plot_path(data, name='Path'):
    # Orbital plane is the xy-plane (z=0)
    e_pos, e_vel, collision = data

    e_pos = np.transpose(e_pos)

    plt.figure(1)
    plt.clf()
    plt.xlabel('y (m)')
    plt.ylabel('x (m)')
    plt.grid()
    plt.plot(e_pos[1], e_pos[0], label=name)
    plt.legend()
    plt.show()

    if collision: print('Collision!')
    else: print('No collision.')

# Edit experiment constants (except velocity) here
# mass
m = 1

# planet constants
M = 6.42e23
R = 3.3895e6

def orbit(velocity, position=[1e7, 0, 0]):

    # initial position and velocity
    position = np.array(position) # [x, y, z]
    # velocity = np.array([0, 0, 0]) # [x, y, z]

    conditions = (m, M, R, position, velocity)

    # simulation time, timestep and time
    t_max = 100000

    # Euler
    dt = 1
    t_array = np.arange(0, t_max, dt)

    e_data = euler_int(conditions, dt, t_array)

    # Verlet
    dt = 1
    t_array = np.arange(0, t_max, dt)

    v_data = verlet_int(conditions, dt, t_array)

    return e_data, v_data, t_array

def single_degree():

    # initial velocity
    velocity = np.array([0, 0, 0]) # [x, y, z]

    e_data, v_data, t_array = orbit(velocity)

    plot_alt(e_data, t_array, 'Altitude - Euler')
    plot_alt(v_data, t_array, 'Altitude - Verlet')

def elliptical_orbit():

    # initial velocity
    velocity = np.array([0, 1.5e3, 0]) # [x, y, z]

    e_data, v_data, _ = orbit(velocity)

    plot_path(e_data, 'Ellipse - Euler')
    plot_path(v_data, 'Ellipse - Verlet')

def cicular_orbit():

    # initial velocity
    # default initial position is [1e7, 0, 0]
    velocity = np.array([0, np.sqrt(G*M/1e7), 0]) # [x, y, z]

    e_data, v_data, _ = orbit(velocity)

    plot_path(e_data, 'Circular - Euler')
    plot_path(v_data, 'Circular - Verlet')

def hyperbolic_escape():

    # initial velocity
    # default initial position is [1e7, 0, 0]
    velocity = np.array([0, 3e3, 0]) # [x, y, z]

    e_data, v_data, _ = orbit(velocity)

    plot_path(e_data, 'Hyperbolic escape - Euler')
    plot_path(v_data, 'Hyperbolic escape - Verlet')

if __name__ == '__main__':
    single_degree()
    elliptical_orbit()
    cicular_orbit()
    hyperbolic_escape()