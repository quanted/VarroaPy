from Tools import InputWriter
from Tools import ModelCaller
import os

params = {'foo':234, 'bar': 'fubar'}
#params = {'foo':'bar'}

writer = InputWriter(params,verbose=True)
writer.write_inputs()


exe_file = os.path.abspath('files/exe/VarroaPop.exe')
vrp_file = os.path.abspath('files/exe/default.vrp')
in_file = os.path.abspath('files/input/vp_input.txt')
out_path = os.path.abspath('files/output/') + '/'
log_path = os.path.abspath('files/logs/') + '/'




caller = ModelCaller(exe_file, vrp_file, in_file, out_path, log_path = log_path, logs=True, verbose = True)
caller.run_VP()