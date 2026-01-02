import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# original parameters used by Lorentz
# sigma = 10
# rho = 28
# beta = 8/3
# timestep 0.01

# constants
sigma: int = 10
rho: int = 28
beta: float = 8/3
timestep: float = 0.01

# vector field === we prescribe this differently in the lorenz() function
# x_d = sigma * (y-x)
# y_d = x * (rho - z) - y
# z_d = x*y - beta*z

# initial conditions
y0: list = [-8, 8, 27]

def lorenz(t, y):
    d_y = [
        sigma * (y[1] - y[0]),
        y[0]* (rho - y[2]) - y[1],
        y[0] *y[1] - beta * y[2]
    ]
    return np.array(d_y)

# defaults preloaded
def rk4singletimestep(fun = lorenz, dt = 0.01, t0 = 0, y0 = [-8, 8, 27]):
    f1 = fun(t0, y0)
    f2 = fun(t0+dt/2, y0+dt/2*f1)
    f3 = fun(t0+dt/2, y0+dt/2*f2)
    f4 = fun(t0+dt, y0+dt*f3)
    yout = y0+ dt/6*(f1 + 2*f2 + 2*f3 + f4)
    return yout

def multicalculate(fun, t, starts: list, num_time_pts: int):

    positions: list = np.zeros((len(starts), 3, num_time_pts))

    for n in range(len(starts)):

        # Initial variables
        Y = np.zeros((3, num_time_pts))
        Y[:, 0] = starts[n]
        yin = starts[n]

        # Simulate timepoints
        for i in range(num_time_pts - 1):
            yout = rk4singletimestep(lorenz, dt, t[i], yin)
            Y[:, i + 1] = yout  # add what we calculated to the list of positions
            yin = yout

        positions[n] = Y

    return positions

def multiplot(positions: list, linewidth_var = 2, color_var= 'red'):
    for n in range(len(positions)):
        ax = plt.figure().add_subplot(projection='3d')
        ax.plot(
            positions[n][0, :],
            positions[n][1, :],
            positions[n][2, :],
        linewidth = linewidth_var,
        color = color_var)

        plt.show(block=False)  # show immediately
        plt.pause(0.1)
    plt.show()



# Initial variables
dt = 0.01 # timestep - think 'simulation tick'
T = 5 # 'overall time' - think *seconds*
num_time_pts = int(T / dt) # then converted to total time steps given fractional steps
t = np.linspace(0, T, num_time_pts) # start, stop, num

# Call the functions
n_starts = 5
starts = [np.random.randint(1, 20, 3) for i in range(n_starts)]

positions = multicalculate(lorenz, t, starts, num_time_pts)
print(positions[0])
print(len(positions))

multiplot(positions, linewidth_var=0.3, color_var = 'orangered')