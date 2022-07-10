from unittest import skip
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# make it go faster
skip_factor = 1000

def update_lines(num, data, line):

    num = num*skip_factor

    print(num, data[:, num])
    line.set_data(data[0:2, :num])
    line.set_3d_properties(data[2, :num])
    # line.set_marker("o")
    return line

def plot_anim(data, name='animation', fps=60):

    data = np.transpose(data)

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # NOTE: Can't pass empty arrays into 3d version of plot()
    line = ax.plot(data[0], data[1], data[2])[0]

    ax.set_xlim(-1.1e2,1.1e2)
    ax.set_ylim(-1.1e2,1.1e2)
    ax.set_zlim(-1.1e2,1.1e2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.rcParams['animation.html'] = 'html5'

    line_ani = animation.FuncAnimation(fig, update_lines, 5000, fargs=(data, line),
                                    interval=0.1, blit=False, repeat=False)

    mywriter = animation.FFMpegWriter(fps=fps)
    plt.show()
    # line_ani.save(f'{name}.mp4',writer=mywriter)