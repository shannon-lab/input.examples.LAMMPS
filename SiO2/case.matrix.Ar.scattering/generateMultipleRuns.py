#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
# from os import listdir
import os
import pandas as pd
# import sys
from shutil import copyfile
import in_place

energy_init = 10 # eV
energy_end  = 5000 # eV
num_energy = 10 # groups

energy_group = 10 ** np.linspace(np.log10(energy_init), np.log10(energy_end), num=num_energy)
# print(energy_group)
energy_group = np.around(energy_group).astype(int)
print(energy_group)

angle_init = 75 # eV
angle_end  = 89 # eV
num_angle = 15 # groups

angle_group = np.linspace(angle_init, angle_end, num_angle).astype(int)
print(angle_group)


for i in range(len(angle_group)):
    for j in range(len(energy_group)):
        path = "angle." + str(angle_group[i]) + ".energy." + str(energy_group[j])

        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

        try:
            os.mkdir(path+"/data")
        except OSError as error:
            print(error)

        copyfile("template.lammps", path+"/test.lammps")
        with in_place.InPlace(path+"/test.lammps") as file:
            for line in file:
                if line.startswith("variable in_energy equal XXX"):
                    line = line.replace('XXX', str(energy_group[j]))
                if line.startswith("variable in_angle_degree equal YYY"):
                    line = line.replace('YYY', str(angle_group[i]))
                file.write(line)

        copyfile("submit_job.bsub", path+"/submit_job.bsub")
