##
# VarroaPop Wrapper Tools for Python
# code by Jeff Minucci
# 8/7/18
##



import os, sys
import ctypes
import subprocess
import pandas as pd

def  StringList2CPA(theList):
    theListBytes = []
    for i in range(len(theList)):
        theListBytes.append(bytes(theList[i], 'utf-8'))
    return theListBytes

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



class VPModelCaller:
    """
    VPModelCaller

    Class to run the VarroaPop executable

    param exe_file Full path to the VarroaPop.exe file (e.g. 'C:/VarroaPop/bin/VarroaPop.exe').
    param vrp_file Full path to the .vrp file (e.g. 'C:/VarroaPop/bin/default.vrp').
    param in_file Full path to the input file (e.g. 'C:/VarroaPop/input/myfile.txt').
    param out_path Full path to the output folder, with trailing slash (e.g. 'C:/VarroaPop/output/).
    param out_filename Optional: custom file name for the output file.
    param weather_file: Full path to the weather file e.g. C:/VarroaPop/weather.wea (must be .wea/.dvf/.wth)
    param verbose T/F, print extra details?

    """

    def __init__(self, lib_file, new_features=False, verbose = False):
        #self.exe = exe_file
        #self.vrp = vrp_file
        #self.input = in_file
        #self.output_path = out_path
        #self.out_filename = out_filename
        self.parameters = []
        self.weather_file = None
        self.contam_file = None
        self.new_features = new_features
        self.verbose = verbose
        self.results = None
        self.lib = ctypes.CDLL(lib_file)
        self.parent = os.path.dirname(os.path.abspath(__file__))
        self.a = None
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
        if self.lib.InitializeModel():  # Initialize model
            self.a = self.lib.InitializeModel()
            if self.verbose:
                print(self.a)
                print('Model initialized')
        else:
            raise Exception('libvpop could not be initialized.')
    
    def clear_buffers(self):  
        if self.lib.ClearResultsBuffer():  # Clear Results and weather lists
            if self.verbose:
                print('Results buffer cleared')
        else :
             raise Exception('Error clearing results buffer.')
        if self.lib.ClearWeather():  # Clear weather
            if self.verbose:
                print('Weather Cleared')
        else :
            raise Exception('Error Clearing Weather')
    
    def load_input_file(self, in_file):
        self.input_file = in_file
        #Load the Initial Conditions
        icf = open(self.input_file)
        inputlist = icf.readlines()
        icf.close()
        CPA = (ctypes.c_char_p * len(inputlist))()
        inputlist_bytes = StringList2CPA(inputlist)
        CPA[:] = inputlist_bytes
        if self.lib.SetICVariablesCPA(CPA, len(inputlist)):
            if self.verbose:
                print('Loaded parameters from file')
        else:
            raise Exception("Error loading parameters from file")
    
    def set_parameters(self, parameters):
        if parameters is None:
            return None
        self.parameters.update(parameters)
        inputlist = []
        for k, v in self.parameters.items()
            intputlist.append('{}={}'.format(k, v))
        CPA = (ctypes.c_char_p * len(inputlist))()
        inputlist_bytes = StringList2CPA(inputlist)
        CPA[:] = inputlist_bytes
        if self.lib.SetICVariablesCPA(CPA, len(inputlist)):
            if self.verbose:
                print('Set parameters')
        else:
            raise Exception("Error setting parameters")
        return self.parameters
            
    def load_weather(self, weather_file='durham'):
        self.weather_file = weather_file
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
        wf = open(weatherpath)
        weatherlines = wf.readlines()
        wf.close()
        CPA = (ctypes.c_char_p * len(weatherlines))()
        weatherline_bytes = StringList2CPA(weatherlines) 
        CPA[:] = weatherline_bytes
        if self.lib.SetWeatherCPA(CPA, len(weatherlines)):
            if self.verbose:
                print('Loaded Weather')
        else:
            raise Exception("Error Loading Weather")
    
    def load_contam_file(self, contam_file):
        self.contam_file = contam_file
        ct = open(contam_file)
        contamlines = ct.readlines()
        ct.close()
        CPA = (ctypes.c_char_p * len(contamlines))()
        contamlines_bytes = StringList2CPA(contamlines)
        CPA[:] = contamlines_bytes
        if self.lib.SetContaminationTableCPA(CPA, len(contamlines)):
            if verbose:
                print('Loaded contamination file')
        else:
            raise Exception("Error loading contamination file")

    def run_VP(self):
        if selflib.RunSimulation():
            self.a = 1
            if self.verbose:
                print('Simulation ran successfully')
        else :
            self.a = 2
            if self.verbose:
                print('Error in sumulation')
        # Get results
        theCount = ctypes.c_int(0)
        p_Results = ctypes.POINTER(ctypes.c_char_p)()
        if self.lib.GetResultsCPA(ctypes.byref(p_Results),ctypes.byref(theCount)):
            # Store Reaults
            self.n_result_lines = int(theCount.value)
            if verbose:
                print('Number lines of results: {}'.format(self.n_result_lines))
            self.results = p_Results
            self.lib.ClearResultsBuffer()
            return self.results.decode('utf-8')
        
    def write_results(self, file):
        results_file = file
        if self.results is None:
            raise Exception("There are no results to write. Please run the model first")
        outfile = open(results_file, "w")
        for j in range(0, self.n_result_lines -1): 
            outfile.write(p_Results[j].decode("utf-8"))
        outfile.close()
        if self.verbose():
            print('Wrote results to file')
                      
        



class OutputReader:
    '''
    Class to read results from a VarroaPop run output text file

    param out_path Directory to look for results files in (e.g. C:/VarroaPop/output/)
    param out_filename Name of the VarroaPop results file to read (e.g. "myresults.txt")
    '''

    def __init__(self, out_path, out_filename = 'vp_results.txt'):
        self.outvar =["Date","Colony Size","Adult Drones","Adult Workers","Foragers", "Active Foragers", "Capped Drone Brood", "Capped Worker Brood",
             "Drone Larvae", "Worker Larvae", "Drone Eggs", "Worker Eggs", "Total Eggs", "DD", "L", "N", "P", "dd", "l", "n", "Free Mites", "Drone Brood Mites",
             "Worker Brood Mites", "Mites/Drone Cell", "Mites/Worker Cell", "Mites Dying", "Proportion Mites Dying",
             "Colony Pollen (g)", "Pollen Pesticide Concentration", "Colony Nectar", "Nectar Pesticide Concentration",
             "Dead Drone Larvae", "Dead Worker Larvae", "Dead Drone Adults", "Dead Worker Adults", "Dead Foragers",
             "Queen Strength", "Average Temperature (celsius)", "Rain", "Min Temp", "Max Temp", "Daylight hours", "Forage Inc", "Forage Day"]
        self.out_path = out_path
        self.out_filename = out_filename
        self.out = os.path.join(self.out_path, self.out_filename)

    def read(self):
        """
        Read the VarroaPop output file and return it as a pandas dataframe

        :return: a pandas dataframe of VP outputs (columns) by simulation date (rows)
        """
        df = pd.read_csv(self.out, delim_whitespace = True, header = None, names = self.outvar, skiprows = 6, index_col=0)
        return df
