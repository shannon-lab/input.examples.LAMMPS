from ovito.io import import_file, export_file
from ovito.modifiers import ExpressionSelectionModifier, TimeSeriesModifier
import numpy
import matplotlib
matplotlib.use('Agg') # Optional: Activate 'Agg' backend for off-screen plotting.
import matplotlib.pyplot as plt
import sys

# Load a simulation trajectory consisting of several frames:
pipeline = import_file(sys.argv[1])
print("Number of MD frames:", pipeline.source.num_frames)
pipeline.modifiers.append(ExpressionSelectionModifier(expression = 'ParticleType==3 && Position.Z<=45'))
pipeline.modifiers.append(TimeSeriesModifier(operate_on = 'ExpressionSelection.count', sampling_frequency=100, time_attribute='Timestep'))
data = pipeline.compute()
time_series_1 = data.tables['time-series'].xy()

pipeline2 = import_file(sys.argv[1])
pipeline2.modifiers.append(ExpressionSelectionModifier(expression = 'ParticleType==4 && Position.Z<=45'))
pipeline2.modifiers.append(TimeSeriesModifier(operate_on = 'ExpressionSelection.count', sampling_frequency=100, time_attribute='Timestep'))
data = pipeline2.compute()
time_series_2 = data.tables['time-series'].xy()

fig = plt.figure()
plt.plot(time_series_1[ : , 0], time_series_1[ : , 1], label='C')
plt.plot(time_series_2[ : , 0], time_series_2[ : , 1], label='F')
plt.xlabel('Timestep (4E6 steps = 1 ns)')
plt.ylabel('Number of attached particles')
plt.legend()
# plt.savefig('num.of.attached.C.vs.timestep.pdf')
plt.savefig('num.of.attached.C.and.F.vs.timestep.pdf')

# print(type(time_series_1))
numpy.savetxt("num.of.attached.C.vs.timestep.csv", time_series_1, delimiter=",")
numpy.savetxt("num.of.attached.F.vs.timestep.csv", time_series_2, delimiter=",")
