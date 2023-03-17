#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
import os
from shutil import copyfile
import in_place

mass_amu_dict = {"Si": 28.0855, "O": 15.9994, "C": 12.0107, "F": 18.9984}

molecule_mass_amu_dict = {}
offset_for_atom_types_dict = {}
run_step_dict = {}

for i in range(5):
    atom1 = 'Si'
    atom2 = 'F'
    if i == 0:
        molecule = atom1
    elif i == 1:
        molecule = atom1 + atom2
    else:
        molecule = atom1 + atom2 + str(i)
    molecule_mass_amu_dict[molecule] = mass_amu_dict[atom1] + i*mass_amu_dict[atom2]
    offset_for_atom_types_dict[molecule] = 0
    run_step_dict[molecule] = np.ceil( 33571*np.sqrt(molecule_mass_amu_dict[molecule]/88.0043) / 1000 ).astype(int) * 1000

for i in range(5):
    atom1 = 'C'
    atom2 = 'F'
    if i == 0:
        molecule = atom1
    elif i == 1:
        molecule = atom1 + atom2
    else:
        molecule = atom1 + atom2 + str(i)
    molecule_mass_amu_dict[molecule] = mass_amu_dict[atom1] + i*mass_amu_dict[atom2]
    offset_for_atom_types_dict[molecule] = 2
    run_step_dict[molecule] = np.ceil( 33571*np.sqrt(molecule_mass_amu_dict[molecule]/88.0043) / 1000 ).astype(int) * 1000

print('molecule_mass_amu_dict:')
print(molecule_mass_amu_dict)
print('offset_for_atom_types_dict:')
print(offset_for_atom_types_dict)
print('run_step_dict:')
print(run_step_dict)


for key in molecule_mass_amu_dict:
    path = "case.molecule." + key

    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    try:
        os.mkdir(path+"/data")
    except OSError as error:
        print(error)

    copyfile("in.stick.lammps", path+"/in.stick.lammps")
    with in_place.InPlace(path+"/in.stick.lammps") as file:
        for line in file:
            if line.startswith("molecule       mol_deposit  XXX1"):
                line = line.replace('XXX1', "../../molecules/data.molecule."+key)
            if line.startswith("variable       offset_for_atom_types equal XXX2"):
                line = line.replace('XXX2', str(offset_for_atom_types_dict[key]))
            if line.startswith("variable       in_mass_amu equal XXX3"):
                line = line.replace('XXX3', str(molecule_mass_amu_dict[key]))
            if line.startswith("variable       run_step equal XXX4"):
                line = line.replace('XXX4', str(run_step_dict[key]))
            file.write(line)
    # copyfile("submit_job.bsub", path+"/submit_job.bsub")
    # os.chdir(path)
    # os.system('ln -s ../submit_job.bsub .')
    # os.chdir('..')
