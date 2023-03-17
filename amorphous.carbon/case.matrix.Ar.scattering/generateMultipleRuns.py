#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
import os
from shutil import copyfile
import in_place

angle_init = 65 # eV
angle_end  = 90 # eV
angle_group = np.arange(angle_init, angle_end, 2)
# angle_group = np.array([60,65,70,75,80,85])
print('angle group:')
print(angle_group)

energy_init = 10 # eV
energy_end  = 5000 # eV
num_energy = 10 # groups
energy_group = 10 ** np.linspace(np.log10(energy_init), np.log10(energy_end), num=num_energy)
energy_group = np.around(energy_group).astype(int)
print('energy group')
print(energy_group)

for i in range(len(angle_group)):
    for j in range(len(energy_group)):
        path = "case.angle." + str(angle_group[i]) + ".energy." + str(energy_group[j])

        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

        try:
            os.mkdir(path+"/data")
        except OSError as error:
            print(error)

        copyfile("Ar.on.ACL.lammps", path+"/Ar.on.ACL.lammps")
        with in_place.InPlace(path+"/Ar.on.ACL.lammps") as file:
            for line in file:
                if line.startswith("variable in_angle_degree equal XXX # degree"):
                    line = line.replace('XXX', str(angle_group[i]))
                if line.startswith("variable in_energy equal YYY # eV"):
                    line = line.replace('YYY', str(energy_group[j]))
                file.write(line)

        copyfile("submit_job.bsub", path+"/submit_job.bsub")
