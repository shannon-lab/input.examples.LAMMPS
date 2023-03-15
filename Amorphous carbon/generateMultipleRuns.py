#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
import os
import pandas as pd
# import sys
from shutil import copyfile
import in_place

energy_group = np.array([1, 20, 80, 120])
print(energy_group)

for j in range(len(energy_group)):
    path = "deposit.energy." + str(energy_group[j])

    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    try:
        os.mkdir(path+"/data")
    except OSError as error:
        print(error)

    copyfile("C.deposit.on.Si.lammps", path+"/C.deposit.on.Si.lammps")
    with in_place.InPlace(path+"/C.deposit.on.Si.lammps") as file:
        for line in file:
            if line.startswith("variable in_energy equal YYY # eV"):
                line = line.replace('YYY', str(energy_group[j]))
            file.write(line)

    copyfile("submit_job.bsub", path+"/submit_job.bsub")
