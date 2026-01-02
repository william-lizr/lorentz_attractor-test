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

# params: list = [sigma, rho, beta, timestep]

# vector field === we prescribe this differently in the lorenz() function
# x_d = sigma * (y-x)
# y_d = x * (rho - z) - y
# z_d = x*y - beta*z

# initial conditions
y0: list = [-8, 8, 27]

# notation: fun(t, x) !!!!: NOT FUN(x, t)
# y is a vector of states for each coordinate in the system

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

# compute trajectory
dt = 0.01
T = 10 # given in ?seconds?
num_time_pts = int(T / dt) # then converted to total time steps given fractional steps
t = np.linspace(0, T, num_time_pts) # start, stop, num

Y = np.zeros((3, num_time_pts))
Y[:, 0] = y0 # the entire trajectory
yin = y0

for i in range(num_time_pts - 1):
    yout = rk4singletimestep(lorenz, dt, t[i], yin)
    Y[:,i+1] = yout # add what we calculated to the list of positions
    yin = yout # rewrite input vector to what we just calculated


ax = plt.figure().add_subplot(projection = '3d')
ax.plot(Y[0,:], Y[1,:], Y[2,:], 'b')
# END OF *OUR* CODE
# NOW COMPARE TO THE PYTHON BUILT IN INTEGRATION FOR RK4
# ==========================
# we pass: vector field equations, timespan, initial conditions, t_eval?
lorenz_solution = solve_ivp(lorenz, (0, T), y0, t_eval=t)
# plot for comparison
t = lorenz_solution.t
y = lorenz_solution.y.T
ax.plot(y[:,0], y[:, 1], y[:,2], 'r')
plt.show()

