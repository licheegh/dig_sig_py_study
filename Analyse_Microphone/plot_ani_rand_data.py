# -*- coding: utf-8 -*-
"""
General Method to Plot New Data

@author: Administrator
"""

# update a distribution based on new data.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as line
from matplotlib import get_backend

print('Backend:'+get_backend())

fig = plt.figure()
ax = plt.axes(xlim=(0,10), ylim=(0,1))
linem = line.Line2D([],[])

def init():
    ax.add_line(linem)
    return linem,
    
def update(i):
    linem.set_xdata(np.arange(0,10,1))
    linem.set_ydata(np.random.rand(10))
    return linem,

ani = animation.FuncAnimation(fig, update,
                              init_func=init, 
                              frames=1,
                              interval=30,
                              blit=True)
