#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
import os
from shutil import copyfile
import in_place

ratio_group = np.array(['0.2', '0.4', '0.6', '0.8', '1.0'])
print('ratio_group:')
print(ratio_group)

for i in range(len(ratio_group)):
    path = "case.ratio.C.over.CFx." + str(ratio_group[i])

    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    # try:
    #     os.mkdir(path+"/data")
    # except OSError as error:
    #     print(error)

    copyfile("in.deposit.lammps", path+"/in.deposit.lammps")
    with in_place.InPlace(path+"/in.deposit.lammps") as file:
        for line in file:
            if line.startswith("variable       ratio_flux_C_over_CFx equal XXX"):
                line = line.replace('XXX', str(ratio_group[i]))
            file.write(line)
    # copyfile("submit_job.bsub", path+"/submit_job.bsub")
    os.chdir(path)
    os.system('ln -s ../submit_job.bsub .')
    os.chdir('..')
