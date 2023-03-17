#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
import os
from shutil import copyfile
import in_place
import random

# energy_start = 200 # K
# energy_end  = 310 # K
# energy_group = np.arange(energy_start, energy_end, 20)
energy_group = np.array([10, 20, 50, 100, 250, 500, 750, 1000]) # eV
print('energy group:')
print(energy_group)

num_of_duplicate_cases = 3
duplicate_cases_group = np.arange(1, num_of_duplicate_cases+1)
random.seed(1234)
list_randomSeedForDeposit = [random.randint(1000, 9999) for i in range(num_of_duplicate_cases)]
print(list_randomSeedForDeposit)

for i in range(len(energy_group)):
    for j in range(len(duplicate_cases_group)):
        path = "case.Ar.energy." + str(energy_group[i]) + ".dupli." + str(duplicate_cases_group[j])

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
                if line.startswith("variable       in_energy_Ar equal XXX"):
                    line = line.replace('XXX', str(energy_group[i]))
                if line.startswith("variable       randomSeedForDeposit equal YYY"):
                    line = line.replace('YYY', str(list_randomSeedForDeposit[j]))
                file.write(line)

        # copyfile("submit_job.bsub", path+"/submit_job.bsub")
        os.chdir(path)
        # os.system('ln -s ../submit_job.bsub .')
        os.chdir('..')
