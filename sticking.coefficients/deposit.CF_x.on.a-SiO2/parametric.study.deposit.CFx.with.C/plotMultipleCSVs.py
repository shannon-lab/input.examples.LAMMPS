#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

file_list = os.listdir('.')
folder_list = [x for x in file_list if x.startswith('case.ratio.C') and x[-1].isdigit()]
# print(folder_list)

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def plot_attached_atoms_vs_timestep(atom, movingWindowSize = 3):
    fig = plt.figure()
    lwidth = 1

    for folder in folder_list:
        df = pd.read_csv(folder+'/num.of.attached.XXX.vs.timestep.csv'.replace('XXX',atom))
        # df = pd.read_csv(folder+'/num.of.Si.and.O.vs.timestep.csv')
        xdata = df.iloc[:, 0].values
        ydata = df.iloc[:, 1].values
        legendStr = folder.replace('case.ratio.','').replace('.over.','/').replace('CFx.','CFx = ')
        plt.plot(moving_average(xdata, movingWindowSize), moving_average(ydata, movingWindowSize), label=legendStr, linewidth=lwidth)#), markersize=5)
        lwidth=lwidth+0.05

    plt.legend()
    plt.xlabel('Timestep (4E6 steps = 1 ns)')
    plt.ylabel('Number of attached XXX atoms'.replace('XXX',atom))
    # plt.xlim([0, 5E5])
    # plt.show()

    plt.savefig('summary.num.of.attached.XXX.vs.timestep.pdf'.replace('XXX',atom))

plot_attached_atoms_vs_timestep('C', movingWindowSize=5)
plot_attached_atoms_vs_timestep('F', movingWindowSize=5)
