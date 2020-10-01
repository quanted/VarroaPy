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
                verbose = False):
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


    def write_inputs(self):
        """
        Function to create a single input file from the set of parameters in the form of
        a named dictionary.
        """
        if self.verbose:
            print("Printing input file to: {}".format(self.path))
            #print("Weather file location: {}".format(self.weather_file))
        inputs = ['{}={}'.format(key, value) for key, value in self.params.items()]
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
    param weather_file: Full path to the weather file e.g. C:/VarroaPop/weather.wea (must be .wea/.dvf/.wth)
    param verbose T/F, print extra details?

    """

    def __init__(self,exe_file, vrp_file, in_file, out_path, out_filename = 'vp_results.txt',
                 weather_file='durham', new_features=False, verbose = False):
        self.exe = exe_file
        self.vrp = vrp_file
        self.input = in_file
        self.output_path = out_path
        self.out_filename = out_filename
        self.weather_file = weather_file
        self.new_features = new_features
        self.verbose = verbose
        self.parent = os.path.dirname(os.path.abspath(__file__))
        weather_dir = os.path.join(self.parent,"files/weather")
        self.weather_locs = {'columbus': os.path.join(weather_dir,'18815_grid_39.875_lat.wea'),
                             'sacramento': os.path.join(weather_dir,'17482_grid_38.375_lat.wea'),
                             'phoenix': os.path.join(weather_dir, '12564_grid_33.375_lat.wea'),
                             'yakima': os.path.join(weather_dir, '25038_grid_46.375_lat.wea'),
                             'eau claire': os.path.join(weather_dir, '23503_grid_44.875_lat.wea'),
                             'jackson': os.path.join(weather_dir, '11708_grid_32.375_lat.wea'),
                             'durham': os.path.join(weather_dir, '15057_grid_35.875_lat.wea')}
        if self.weather_file.lower() in self.weather_locs.keys():
            self.weather_file = self.weather_locs[self.weather_file.lower()]

    def run_VP(self):
        #command = '"' + self.exe + '" -v "' + self.vrp + '" -o "' + os.path.join(self.output_path,self.out_filename) + '" -i "' + self.input + '"' 
        command = self.exe + ' -f -v ' + self.vrp + ' -i ' + self.input + ' -o ' + os.path.join(self.output_path,self.out_filename) + ' -w ' + self.weather_file
        if self.new_features:
            command += ' --forageDayNoTemp --hourlyTemperaturesEstimation --foragersAlwaysAgeBasedOnForageInc --adultAgingBasedOnLaidEggs'  # diverges from win version
            #command += ' --forageDayNoTemp --foragersAlwaysAgeBasedOnForageInc --adultAgingBasedOnLaidEggs'  # same results as above
            #command += ' --foragersAlwaysAgeBasedOnForageInc --adultAgingBasedOnLaidEggs'  # same results as above
            #command += ' --adultAgingBasedOnLaidEggs'  # matches win version
            #command += ' --foragersAlwaysAgeBasedOnForageInc'  # this flag produces the divergence
            #command +=  ' --forageDayNoTemp --hourlyTemperaturesEstimation --adultAgingBasedOnLaidEggs'  # matches win version
        if self.verbose:
            print("Weather file location: {} \n".format(self.weather_file))
            print(command)
        #subprocess.call(command, shell=True)
        #os.chmod(self.exe, 509)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if self.verbose:
            print(result.returncode, result.stdout, result.stderr)



class OutputReader:
    '''
    Class to read results from a VarroaPop run output text file

    param out_path Directory to look for results files in (e.g. C:/VarroaPop/output/)
    param out_filename Name of the VarroaPop results file to read (e.g. "myresults.txt")
    '''

    def __init__(self, out_path, out_filename = 'vp_results.txt'):
        self.outvar =["Colony Size","Adult Drones","Adult Workers","Foragers", "Active Foragers", "Capped Drone Brood", "Capped Worker Brood",
             "Drone Larvae", "Worker Larvae", "Drone Eggs", "Worker Eggs", "Total Eggs", "DD", "L", "N", "P", "dd", "l", "n", "Free Mites", "Drone Brood Mites",
             "Worker Brood Mites", "Mites/Drone Cell", "Mites/Worker Cell", "Mites Dying", "Proportion Mites Dying",
             "Colony Pollen (g)", "Pollen Pesticide Concentration", "Colony Nectar", "Nectar Pesticide Concentration",
             "Dead Drone Larvae", "Dead Worker Larvae", "Dead Drone Adults", "Dead Worker Adults", "Dead Foragers",
             "Queen Strength", "Average Temperature (celsius)", "Rain", "Min Temp", "Max Temp", "Daylight hours", "Forage Inc"]
        self.out_path = out_path
        self.out_filename = out_filename
        self.out = os.path.join(self.out_path, self.out_filename)

    def read(self):
        """
        Read the VarroaPop output file and return it as a pandas dataframe

        :return: a pandas dataframe of VP outputs (columns) by simulation date (rows)
        """
        df = pd.read_csv(self.out, delim_whitespace = True, header = None, names = self.outvar, skiprows = 6)
        return df
