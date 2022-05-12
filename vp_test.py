from VarroaPy.RunVarroaPop import VarroaPop
import numpy as np
import os
import pandas as pd
import datetime
import sys
import io
import resource
import gc
from timeit import default_timer as timer

START_DATE = '06/15/2014'
END_DATE = '10/10/2014'
params = {"ICWorkerAdults": 18000, "ICWorkerBrood": 8000, "SimStart": START_DATE, "SimEnd": END_DATE,
        'IPollenTrips': 8, 'INectarTrips': 17, 'RQEnableReQueen': 'false'}
weather = os.path.abspath('test_data/15055_grid_35.875_lat.txt')
input_file = os.path.abspath('test_data/InputFileFromFeeding_Study_2.txt')
pesticide_file = os.path.abspath('test_data/NutrientContaminationFile.txt')
lib_file = os.path.abspath('liblibvpop_newest.so')
vp = VarroaPop(lib_file, logs=True, keep_files=True, debug=False, verbose=False)
vp.load_weather(weather)
vp.load_input_file(input_file)
vp.set_parameters(params)

max_mem = resource.getrusage(resource.RUSAGE_THREAD).ru_maxrss
print('Thread memory usage max: {} bytes'.format(max_mem))

start = timer()
for i in range(500):
    #vp.set_parameters(params)
    vp.run_model()
end = timer()
print('Time elapsed for 500 simulations: {:.3f} seconds'.format(end - start))

max_mem = resource.getrusage(resource.RUSAGE_THREAD).ru_maxrss
print('Thread memory usage max: {} bytes'.format(max_mem))

start = timer()
for i in range(500):
    #vp.set_parameters(params)
    vp.run_model()
end = timer()
print('Time elapsed for 500 simulations: {:.3f} seconds'.format(end - start))

max_mem = resource.getrusage(resource.RUSAGE_THREAD).ru_maxrss
print('Thread memory usage max: {} bytes'.format(max_mem))

start = timer()
for i in range(500):
    #vp.set_parameters(params)
    vp.run_model()
end = timer()
print('Time elapsed for 500 simulations: {:.3f} seconds'.format(end - start))

max_mem = resource.getrusage(resource.RUSAGE_THREAD).ru_maxrss
print('Thread memory usage max: {} bytes'.format(max_mem))
      
start = timer()
for i in range(500):
   #vp.set_parameters(params)
    vp.run_model()
end = timer()
print('Time elapsed for 500 simulations: {:.3f} seconds'.format(end - start))

max_mem = resource.getrusage(resource.RUSAGE_THREAD).ru_maxrss
print('Thread memory usage max: {} bytes'.format(max_mem))
      
start = timer()
for i in range(500):
    #vp.set_parameters(params)
    vp.run_model()
end = timer()
print('Time elapsed for 500 simulations: {:.3f} seconds'.format(end - start))

max_mem = resource.getrusage(resource.RUSAGE_THREAD).ru_maxrss
print('Thread memory usage max: {} bytes'.format(max_mem))
