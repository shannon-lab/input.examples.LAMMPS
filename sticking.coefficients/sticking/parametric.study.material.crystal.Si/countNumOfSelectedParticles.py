from ovito.io import import_file, export_file
from ovito.modifiers import ExpressionSelectionModifier, TimeSeriesModifier, CreateBondsModifier
from ovito.data import BondType
import numpy
import matplotlib
matplotlib.use('Agg') # Optional: Activate 'Agg' backend for off-screen plotting.
import matplotlib.pyplot as plt
import sys
import pandas as pd
from os import listdir, getcwd

DICT_PARTICLES = {'Si':1, 'O':2, 'C':3, 'F':4}

DICT_BONDS = {('Si','Si') : {'bondID' : 1, 'cutoff' : 2.5},
              ('Si','C')  : {'bondID' : 2, 'cutoff' : 2.0},
              ('Si','F')  : {'bondID' : 3, 'cutoff' : 1.83},
              ('C','F')   : {'bondID' : 4, 'cutoff' : 1.5} }


def countNumOfSelectedParticles(fileName='Si.300K.sticked.10.dat', SELECTED_PARTICLE_TYPE = 3, SELECTED_BOND_TYPE = 2):
    pipeline = import_file(fileName)

    for bond_name_tuple, bond_info_dict in DICT_BONDS.items():
        bond_name = bond_name_tuple[0] + '-' + bond_name_tuple[1]
        # print('Name:', bond_name)
        # print('Bond ID:', bond_info_dict['bondID'])
        # print('Elem1:', DICT_PARTICLES[bond_name_tuple[0]], 'Elem2:', DICT_PARTICLES[bond_name_tuple[1]])
        # print()
        bond_type = BondType(name=bond_name, id=bond_info_dict['bondID'])

        create_bonds_modifier = CreateBondsModifier(mode=CreateBondsModifier.Mode.Pairwise, bond_type=bond_type)
        create_bonds_modifier.set_pairwise_cutoff(DICT_PARTICLES[bond_name_tuple[0]], DICT_PARTICLES[bond_name_tuple[1]], bond_info_dict['cutoff'])
        pipeline.modifiers.append(create_bonds_modifier)

    # pipeline.modifiers.append(ExpressionSelectionModifier(expression = 'ParticleType==3'))
    # pipeline.modifiers.append(TimeSeriesModifier(operate_on = 'ExpressionSelection.count', sampling_frequency=100, time_attribute='Timestep'))
    data = pipeline.compute()

    # print(data.particles)
    df_particles = pd.DataFrame(columns=['Particle ID', 'Particle Type'])
    for index, identifier in enumerate(data.particles['Particle Identifier']):
        df_particles.loc[len(df_particles)] = [identifier, data.particles['Particle Type'][index]]

    # print(df_particles.to_string())

    dict_bond_id_name = {bond_type.id:bond_type.name for bond_type in data.particles.bonds.bond_types.types}
    df_bonds = pd.DataFrame(columns=['Bond Type', 'Bond Name', 'Topology.1', 'Topology.2'])
    for index, bond_type_id in enumerate(data.particles.bonds['Bond Type']):
        bond_topology = [elem for elem in data.particles.bonds['Topology'][index]]
        df_bonds.loc[len(df_bonds)] = [bond_type_id, dict_bond_id_name[bond_type_id], bond_topology[0], bond_topology[1]]

    # count number of selected atoms with bonds
    df_selected_particles_by_bond_type = df_particles.iloc[pd.concat([df_bonds[df_bonds['Bond Type']==SELECTED_BOND_TYPE]['Topology.1'], df_bonds[df_bonds['Bond Type']==SELECTED_BOND_TYPE]['Topology.2']]).unique()]
    df_selected_particles = df_selected_particles_by_bond_type[df_selected_particles_by_bond_type['Particle Type']==SELECTED_PARTICLE_TYPE]
    # print(df_selected_particles)
    # print('Numer of selected particles:', df_selected_particles.shape[0])
    # print(df_bonds.to_string())

    # for a in data.particles.bonds['Topology']:
    #     print(a)

    df_count = pd.Series(data.particles.bonds['Bond Type']).value_counts().reset_index()
    df_count.columns = ['Bond Type', 'Count']
    df_count['Bond Name'] = [dict_bond_id_name[bond_type] for bond_type in df_count['Bond Type']]
    df_count = df_count[['Bond Type', 'Bond Name', 'Count']]
    # print(df_count)

    return df_selected_particles.shape[0]


files = [x for x in listdir() if x.endswith('.dat') and x.startswith('Si.300K.sticked.')]
sum = 0
max = 0
for file in files:
    print(file)
    sum = sum + countNumOfSelectedParticles(fileName=file, SELECTED_PARTICLE_TYPE = 1, SELECTED_BOND_TYPE = 1) - 2106
    # sum = sum + countNumOfSelectedParticles(fileName=file)
    max = max + 5
    print('sum =', sum)
    print('max =', max)
    print()


# time_series_1 = data.tables['time-series'].xy()

# fig = plt.figure()
# # plt.plot(time_series_1[ : , 0], time_series_1[ : , 1], label='C')
# # plt.plot(time_series_2[ : , 0], time_series_2[ : , 1], label='F')
# plt.xlabel('Timestep (4E6 steps = 1 ns)')
# plt.ylabel('Number of attached particles')
# # plt.legend()
# # plt.savefig('num.of.attached.C.vs.timestep.pdf')
# # plt.savefig('num.of.attached.C.and.F.vs.timestep.pdf')
# plt.show()

#
# # print(type(time_series_1))
# numpy.savetxt("num.of.attached.C.vs.timestep.csv", time_series_1, delimiter=",")
# numpy.savetxt("num.of.attached.F.vs.timestep.csv", time_series_2, delimiter=",")
