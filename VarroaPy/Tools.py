##
# Write VarroaPop Inputs
# code by Jeff Minucci
#
##



# Write a VarroaPop input file from a named list or vector
#
# Function to create a single input file from a set of parameters in the form of
# a one row dataframe, where columns are named.
#
# @param params Named vector of VarroaPop inputs to be written to .txt file.
# @param in_path Directory to write vp_input.txt file to (optional).
# @param in_filename Filename of the written input file. Defaults to 'vp_input.txt'.
# @param weather_file Full path to the weather file e.g. C:/VarroaPop/weather.wea (must be .wea/.dvf/.wth) OR
#  one of either 'Columbus' (default), 'Sacramento', 'Phoenix', 'Yakima', 'Eau Claire', 'Jackson', or 'Durham'
# @param verbose T/F print extra details?
#
# @return None... writes inputs to a .txt file in in_path for VarroaPop
#
# @author Jeffrey M Minucci, \email{jminucci2@@gmail.com}
#
# @examples
#  parameters <- c("foo"=15,"bar"=4)
#  write_vp_input(parameters, in_path = "d:/path/to/inputdir")
#
#

import os
import subprocess

class InputWriter:

    def __init__(self, params, in_path = os.path.abspath("files/input"), in_filename = 'vp_input.txt',
                 weather_file = 'Columbus', verbose = False):
        """
        Creates an InputWriter object. Takes params, a named dictionary of VarroaPop inputs. In_path gives the path
        """
        self.params = params
        self.path = in_path
        self.filename = in_filename
        self.verbose = verbose
        self.weather_file = weather_file.lower()
        weather_dir = 'files/weather/'
        self.weather_locs = {'columbus': os.path.abspath(weather_dir + '18815_grid_39.875_lat.wea'),
                             'sacramento': os.path.abspath(weather_dir + '17482_grid_38.375_lat.wea')}
        if self.weather_file in self.weather_locs.keys():
            self.weather_file = self.weather_locs[self.weather_file]



    def write_inputs(self):
        """
        Function to create a single input file from the set of parameters in the form of
        a named dictionary.
        """
        if self.verbose:
            print("Printing input file to: {}".format(self.path))
            print("Weather file location: {}".format(self.weather_file))
        inputs = ['{}={}'.format(key, value) for key, value in self.params.items()]
        inputs = inputs + ['WeatherFileName='+self.weather_file]
        with open(os.path.join(self.path,self.filename), 'w') as file:
            for x in inputs:
                file.write('{}\n'.format(x))



class ModelCaller:
    """
    ModelCaller

    Wrapper code to run the VarroaPop executable

    param exe_file Full path to the VarroaPop.exe file (e.g. 'C:/VarroaPop/bin/VarroaPop.exe').
    param vrp_file Full path to the .vrp file (e.g. 'C:/VarroaPop/bin/default.vrp').
    param in_file Full path to the input file (e.g. 'C:/VarroaPop/input/myfile.txt').
    param out_path Full path to the output folder, with trailing slash (e.g. 'C:/VarroaPop/output/).
    param out_filename Optional: custom file name for the output file.
    param log_path path to the log folder (e.g. 'C:/VarroaPop/logs).(can be omitted if logs=F)
    param logs T/F, should VP write a log file to the log_path folder?
    param verbose T/F, print extra details?

    """

    def __init__(self,exe_file, vrp_file, in_file, out_path, out_filename = 'vp_results.txt',
                 log_path = None, logs = False, verbose = False):
        self.exe = exe_file
        self.vrp = vrp_file
        self.input = in_file
        self.output_path = out_path
        self.out_filename = out_filename
        self.log_path = log_path
        self.log_filename = 'vp_log.txt'
        self.logs = logs
        self.verbose = verbose


    def run_VP(self):
        if self.logs:
            if self.log_path is None:
                raise AttributeError('If logs = True, a log path must be specified')
            command = self.exe + ' ' + self.vrp + ' /b /or ' + os.path.join(self.output_path,self.out_filename) + ' /i ' + self.input + ' /ol ' +\
                      os.path.join(self.log_path,self.log_filename)
        else:
            command = self.exe + ' ' + self.vrp + ' /b /or ' + os.path.join(self.output_path,self.out_filename) + ' /i ' + self.input
        if self.verbose:
            print(command)
        subprocess.call(command)

