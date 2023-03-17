# from ovito.io import import_file, export_file
# from ovito.modifiers import ExpressionSelectionModifier, TimeSeriesModifier
import numpy as np
# import matplotlib
# matplotlib.use('Agg') # Optional: Activate 'Agg' backend for off-screen plotting.
import matplotlib.pyplot as plt
import sys
import pandas as pd
from scipy.optimize import curve_fit

# calculate moving average
df = pd.read_csv("num.of.attached.C.vs.timestep.csv", header=None, names=['timestep', 'num'])
# print(df)

def function_L(t, r_L, tau):
    return r_L * tau * (1 - np.exp(-t/tau))

def function_H_scaled(r_times_t, c):
    return r_times_t + c


xdata = df['timestep']/1000-5
ydata = df['num']

ydata = ydata[xdata>=0]
xdata = xdata[xdata>=0]

# print(type(xdata))

parms_min = {'SSE':np.Inf}
for t_b in xdata.iloc[100:1000]:
    popt_L, pcov_L = curve_fit(function_L, xdata[xdata <= t_b], ydata[xdata <= t_b])
    # print(popt_L)
    SSE_L = sum( (ydata[xdata <= t_b] - function_L(xdata[xdata <= t_b], *popt_L))**2 )

    r_H = popt_L[0] * np.exp(-t_b/popt_L[1])
    popt_H, pcov_H = curve_fit(function_H_scaled, r_H*xdata[xdata >= t_b], ydata[xdata >= t_b])
    # print(popt_H)
    SSE_H = sum( (ydata[xdata >= t_b] - function_H_scaled(r_H*xdata[xdata >= t_b], *popt_H))**2 )

    SSE = SSE_L + SSE_H
    print('t_b:', t_b)
    print('SSE:', SSE)
    if(SSE<parms_min['SSE']):
        parms_min['t_b'] = t_b
        parms_min['SSE'] = SSE
        parms_min['popt_L'] = popt_L
        parms_min['popt_H'] = popt_H
        parms_min['r_H'] = r_H

print(parms_min)

fig = plt.figure()
plt.plot(xdata, ydata)
plt.plot(xdata[xdata <= parms_min['t_b']], function_L(xdata[xdata <= parms_min['t_b']], *parms_min['popt_L']), color='r')
r_H = parms_min['popt_L'][0] * np.exp(-parms_min['t_b']/parms_min['popt_L'][1])
plt.plot(xdata[xdata >= parms_min['t_b']], function_H_scaled(r_H*xdata[xdata >= parms_min['t_b']], *parms_min['popt_H']), color='k')
plt.xlabel('Number of incident molecules')
plt.ylabel('Number of sticked C atoms')
plt.savefig('num.of.attached.fitted.pdf')
plt.show()


def plotRollingAverage():
    rollingWindow = 10
    print(df['num'].rolling(rollingWindow, center=True).mean())

    fig = plt.figure()
    plt.subplot(1, 3, 1)
    plt.plot(df['timestep'], df['num'])
    # plt.plot(df['timestep'], df['timestep']/1000-4)

    plt.subplot(1, 3, 2)
    plt.plot(df['timestep'].rolling(rollingWindow, center=True).mean(), df['num'].rolling(rollingWindow, center=True).mean())
    # plt.plot(df['timestep'], df['timestep']/1000-4)

    plt.subplot(1, 3, 3)
    plt.plot(df['timestep']/1000-4, df['num'].rolling(rollingWindow, center=True).mean())
    plt.show()
