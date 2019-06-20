##
# VarroaPop Wrapper Tools for Python
# code by Jeff Minucci
# 8/7/18
##



import os
import subprocess
import pandas as pd


class InputWriter:
    """
    Class to write a VarroaPop input file

    Takes a named dictionary of VarroaPop input parameters. Also requires the path to where you want to write the file.
    """

    def __init__(self, params, in_path = os.path.join(os.path.abspath(__file__),"files/input"), in_filename = 'vp_input.txt',
                 weather_file = 'Columbus', verbose = False):
        """
        Creates an InputWriter object. Takes params, a named dictionary of VarroaPop inputs.

        @param params Named vector of VarroaPop inputs to be written to .txt file.
        @param in_path Directory to write vp_input.txt file to (optional).
        @param in_filename Filename of the written input file. Defaults to 'vp_input.txt'.
        @param weather_file Full path to the weather file e.g. C:/VarroaPop/weather.wea (must be .wea/.dvf/.wth) OR
            one of either 'Columbus' (default), 'Sacramento', 'Phoenix', 'Yakima', 'Eau Claire', 'Jackson', or 'Durham'
        @param verbose T/F print extra details?
        """
        self.params = params
        self.path = in_path
        self.filename = in_filename
        self.verbose = verbose
        self.weather_file = weather_file.lower()
        self.parent = os.path.dirname(os.path.abspath(__file__))
        weather_dir = os.path.join(self.parent,"files/weather")
        self.weather_locs = {'columbus': os.path.join(weather_dir,'18815_grid_39.875_lat.wea'),
                             'sacramento': os.path.join(weather_dir,'17482_grid_38.375_lat.wea'),
                             'phoenix': os.path.join(weather_dir, '12564_grid_33.375_lat.wea'),
                             'yakima': os.path.join(weather_dir, '25038_grid_46.375_lat.wea'),
                             'eau claire': os.path.join(weather_dir, '23503_grid_44.875_lat.wea'),
                             'jackson': os.path.join(weather_dir, '11708_grid_32.375_lat.wea'),
                             'durham': os.path.join(weather_dir, '15057_grid_35.875_lat.wea')}
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

    Class to run the VarroaPop executable

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
                 log_path = None, log_filename = 'vp_log.txt', logs = False, verbose = False):
        self.exe = exe_file
        self.vrp = vrp_file
        self.input = in_file
        self.output_path = out_path
        self.out_filename = out_filename
        self.log_path = log_path
        self.log_filename = log_filename
        self.logs = logs
        self.verbose = verbose


    def run_VP(self):
        if self.logs:
            if self.log_path is None:
                raise AttributeError('If logs = True, a log path must be specified')
            command = '"' + self.exe + '" "' + self.vrp + '" /b /or "' + os.path.join(self.output_path,self.out_filename) + '" /i "' + self.input + '" /ol "' +\
                      os.path.join(self.log_path,self.log_filename) + '"'
        else:
            command = '"' + self.exe + '" "' + self.vrp + '" /b /or "' + os.path.join(self.output_path,self.out_filename) + '" /i "' + self.input + '"' 
        if self.verbose:
            print(command)
        subprocess.call(command)



class OutputReader:
    '''
    Class to read results from a VarroaPop run output text file

    param out_path Directory to look for results files in (e.g. C:/VarroaPop/output/)
    param out_filename Name of the VarroaPop results file to read (e.g. "myresults.txt")
    '''

    def __init__(self, out_path, out_filename = 'vp_results.txt'):
        self.outvar = ["Date","Colony Size","Adult Drones","Adult Workers", "Foragers", "Capped Drone Brood", "Capped Worker Brood",
             "Drone Larvae", "Worker Larvae", "Drone Eggs", "Worker Eggs", "Free Mites", "Drone Brood Mites",
             "Worker Brood Mites", "Mites/Drone Cell", "Mites/Worker Cell", "Mites Dying", "Proportion Mites Dying",
             "Colony Pollen (g)", "Pollen Pesticide Concentration", "Colony Nectar", "Nectar Pesticide Concentration",
             "Dead Drone Larvae", "Dead Worker Larvae", "Dead Drone Adults", "Dead Worker Adults", "Dead Foragers",
             "Queen Strength", "Average Temperature (celsius)", "Rain"]
        self.out_path = out_path
        self.out_filename = out_filename
        self.out = os.path.join(self.out_path, self.out_filename)

    def read(self):
        """
        Read the VarroaPop output file and return it as a pandas dataframe

        :return: a pandas dataframe of VP outputs (columns) by simulation date (rows)
        """
        df = pd.read_table(self.out, delim_whitespace = True, header = None, names = self.outvar, skiprows = 6)
        return df
