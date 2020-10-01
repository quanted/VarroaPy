'''
VarroaPy - VarroaPop Wrapper for Python
code by Jeff Minucci
8/7/18
'''

import os
import pandas as pd
from .Tools import InputWriter, ModelCaller, OutputReader
import json
import uuid

class VarroaPop():

    def __init__(self, parameters = None, weather_file = 'Columbus', vrp_file = None,
                 logs = False, verbose = True, unique = True, keep_files = False, distro='rhel7'):
        '''
        Initialize a VarroaPop model object

        :param parameters: named dictionary of VarroaPop input parameters and their values
        :param weather_file: Full path to the weather file e.g. C:/VarroaPop/weather.wea (must be .wea/.dvf/.wth) OR
            one of either 'Columbus' (default), 'Sacramento', 'Phoenix', 'Yakima', 'Eau Claire', 'Jackson', or 'Durham'
        :param vrp_file: Full path to a custom vrp session file. If none, use the default file
        :param verbose: True or false, print messages?
        :param unique: True or false, give input and results files unique IDs?
        :param keep_files: True or false, save files or delete them?

        :return: Nothing
        '''
        #check file paths
        self.parent = os.path.dirname(os.path.abspath(__file__))
        if distro == 'aws':
            exe = os.path.join(self.parent, 'files/exe/VarroaPop_aws')
        else:
            exe = os.path.join(self.parent, 'files/exe/VarroaPop_rhel7')
        if vrp_file is None:
            vrp_file = os.path.join(self.parent,'files/exe/default.vrp')
        #exe = os.path.abspath('.files/exe/VarroaPop.exe')
        #vrp = os.path.abspath('.files/exe/default.vrp')
        if not os.path.isfile(exe):
            raise FileNotFoundError('VarroaPop executable ' + exe + ' does not exist!')
        if not os.path.isfile(vrp_file):
            raise FileNotFoundError('VarroaPop session file ' + vrp_file + ' does not exist!')
        self.exe = exe
        self.vrp = vrp_file
        self.unique = unique
        self.keep_files = keep_files
        if self.unique:
            self.jobID = uuid.uuid4().hex[0:8]     #generate random jobID
            self.in_filename = 'vp_input_' + self.jobID + '.txt'
            self.log_filename = 'vp_log_' + self.jobID + '.txt'
            self.out_filename = 'vp_results_' + self.jobID + '.txt'
        else:
            self.jobID = ""
            self.in_filename = 'vp_input.txt'
            self.log_filename = 'vp_log.txt'
            self.out_filename = 'vp_results.txt'
        self.in_path = os.path.join(self.parent,'files/input')
        self.input = os.path.join(self.in_path, self.in_filename)
        #self.log_path = os.path.join(self.parent,'files/logs')
        self.out_path = os.path.join(self.parent,'files/output')
        #self.logs = logs
        self.verbose = verbose
        if parameters is not None:
            if not isinstance(parameters, dict):
                raise TypeError('parameters must be a named dictionary of VarroaPop parameters')
        self.parameters = parameters
        self.weather = weather_file
        self.output = None



    def set_parameters(self, parameters, weather_file = None):
        '''
        Set or update the parameters (and optionally the weather file/option)

        :param parameters: named dictionary of VarroaPop input parameters and their values
        :param weather_file: Full path to the weather file e.g. C:/VarroaPop/weather.wea (must be .wea/.dvf/.wth) OR
            one of either 'Columbus' (default), 'Sacramento', 'Phoenix', 'Yakima', 'Eau Claire', 'Jackson', or 'Durham'

        :return: Nothing
        '''
        if not isinstance(parameters, dict):
            raise TypeError('parameters must be a named dictionary of VarroaPop parameters')
        self.parameters.update(parameters)
        if weather_file is not None:
            self.weather = weather_file


    def set_weather(self, weather_file):
        '''
        Set the weather option

        :param weather_file: Full path to the weather file e.g. C:/VarroaPop/weather.wea (must be .wea/.dvf/.wth) OR
            one of either 'Columbus' (default), 'Sacramento', 'Phoenix', 'Yakima', 'Eau Claire', 'Jackson', or 'Durham'
        :return: Nothing
        '''
        self.weather = weather_file


    def run_model(self):
        '''
        Run the VarroaPop model.

        :return: output
        '''

        #check to see if parameters have been supplied
        if self.parameters is None:
            raise Exception('Parameters must be set before running VarroaPop!')
        if self.weather is None:
            raise Exception('Weather must be set before running VarroaPop!')
        #write the inputs
        writer = InputWriter(params = self.parameters, in_path =  self.in_path, in_filename= self.in_filename,
                             verbose = self.verbose)
        writer.write_inputs()

        #run VarroaPop
        caller = ModelCaller(exe_file = self.exe, vrp_file = self.vrp, in_file = self.input, out_path= self.out_path,
                             out_filename = self.out_filename, weather_file=self.weather_file, verbose = self.verbose)
        caller.run_VP()

        #read the results
        reader = OutputReader(out_path= self.out_path, out_filename= self.out_filename)
        output = reader.read()
        self.output = output
        if not self.keep_files:
            self.delete_files()
        return output


    def get_output(self,json_str=False):
        '''

        :param jsonify: return the output as a json string?
        :return: either a json string or a dataframe of the VarroaPop model output
        '''
        if json_str:
            result = json.dumps(self.output.to_dict(orient='list'))
        else:
            result = self.output
        return result


    def get_jobID(self):
        return self.jobID


    def delete_files(self):
        input = os.path.join(self.in_path, self.in_filename)
        output = os.path.join(self.out_path, self.out_filename)
        if os.path.exists(input):
            os.remove(input)
        if os.path.exists(output):
            os.remove(output)
        if self.logs:
            logs = os.path.join(self.log_path, self.log_filename)
            if os.path.exists(logs):
                os.remove(logs)








