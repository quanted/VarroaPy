##
# VarroaPop Wrapper Tools for Python
# code by Jeff Minucci
# 8/7/18
##

import os, sys
import io
import ctypes
import subprocess
import pandas as pd

colnames = ["Date","Colony Size","Adult Drones","Adult Workers","Foragers", "Active Foragers", "Capped Drone Brood", "Capped Worker Brood",
             "Drone Larvae", "Worker Larvae", "Drone Eggs", "Worker Eggs", "Total Eggs", "DD", "L", "N", "P", "dd", "l", "n", "Free Mites", "Drone Brood Mites",
             "Worker Brood Mites", "Mites/Drone Cell", "Mites/Worker Cell", "Mites Dying", "Proportion Mites Dying",
             "Colony Pollen (g)", "Pollen Pesticide Concentration", "Colony Nectar", "Nectar Pesticide Concentration",
             "Dead Drone Larvae", "Dead Worker Larvae", "Dead Drone Adults", "Dead Worker Adults", "Dead Foragers",
             "Queen Strength", "Average Temperature (celsius)", "Rain", "Min Temp", "Max Temp", "Daylight hours", "Forage Inc", "Forage Day"]

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

    """

    def __init__(self, lib_file, new_features=False, verbose = False):
        #self.exe = exe_file
        #self.vrp = vrp_file
        #self.input = in_file
        #self.output_path = out_path
        #self.out_filename = out_filename
        self.parameters = dict()
        self.weather_file = None
        self.contam_file = None
        self.new_features = new_features
        self.verbose = verbose
        self.results = None
        self.lib = ctypes.CDLL(lib_file)
        self.parent = os.path.dirname(os.path.abspath(__file__))
        self.a = None
        weather_dir = os.path.join(self.parent,"files/weather")
        if self.lib.InitializeModel():  # Initialize model
            self.a = self.lib.InitializeModel()
            if self.verbose:
                print(self.a)
                print('Model initialized')
        else:
            raise Exception('libvpop could not be initialized.')
        self.clear_buffers()
    
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
        if self.lib.ClearErrorList():
            if self.verbose:
                    print('Error list cleared')
        else :
                raise Exception('Error clearing error list')
        if self.lib.ClearInfoList():
            if self.verbose:
                    print('Info Cleared')
        else :
                raise Exception('Error clearing info')
        
    def load_input_file(self, in_file):
        self.input_file = in_file
        #Load the Initial Conditions
        icf = open(self.input_file)
        inputs = icf.readlines()
        icf.close()
        input_d = dict(x.replace(" ","").replace("\n","").split("=") for x in inputs)
        self.param_update(input_d)
        inputlist = []
        for k, v in self.parameters.items():
            inputlist.append('{}={}'.format(k, v))
        CPA = (ctypes.c_char_p * len(inputlist))()
        inputlist_bytes = StringList2CPA(inputlist)
        CPA[:] = inputlist_bytes
        if self.lib.SetICVariablesCPA(CPA, len(inputlist)):
            if self.verbose:
                print('Loaded parameters from file')
        else:
            raise Exception("Error loading parameters from file")
        del CPA
        del inputlist_bytes
        return self.parameters
    
    def param_update(self,parameters):
        to_add = dict((k.lower(), v) for k, v in parameters.items())
        self.parameters.update(to_add)
    
    def set_parameters(self, parameters=None):
        refresh = False
        if parameters is not None:
            self.param_update(parameters)
        else:
            refresh = True
            if self.parameters is None:
                return
        inputlist = []
        for k, v in self.parameters.items():
            inputlist.append('{}={}'.format(k, v))
        CPA = (ctypes.c_char_p * len(inputlist))()
        inputlist_bytes = StringList2CPA(inputlist)
        CPA[:] = inputlist_bytes
        if self.lib.SetICVariablesCPA(CPA, len(inputlist)):
            if self.verbose and not refresh:
                print('Set parameters')
        else:
            raise Exception("Error setting parameters")
        del CPA  # shouldn't be needed but trying to fix progressive slowdown issue
        del inputlist_bytes
        return self.parameters
    
    def get_parameters(self):
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
        wf = open(self.weather_file)
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
        self.set_parameters()
        del CPA  # shouldn't be needed but trying to fix progressive slowdown issue
        del weatherline_bytes
    
    def load_contam_file(self, contam_file):
        self.contam_file = contam_file
        ct = open(contam_file)
        contamlines = ct.readlines()
        ct.close()
        CPA = (ctypes.c_char_p * len(contamlines))()
        contamlines_bytes = StringList2CPA(contamlines)
        CPA[:] = contamlines_bytes
        if self.lib.SetContaminationTableCPA(CPA, len(contamlines)):
            if self.verbose:
                print('Loaded contamination file')
        else:
            raise Exception("Error loading contamination file")
        del CPA  # shouldn't be needed but trying to fix progressive slowdown issue
        del contamlines_bytes

    def run_VP(self, debug=False):
        if self.lib.RunSimulation():
            self.a = 1
            if self.verbose:
                print('Simulation ran successfully')
        else :
            self.a = 2
            if self.verbose:
                print('Error in sumulation')
        if debug:
            self.clear_buffers()
            return None
        # Get results
        theCount = ctypes.c_int(0)
        #p_Results = ctypes.POINTER(ctypes.c_char_p)
        p_Results = ctypes.POINTER(ctypes.c_char_p)()
        if self.lib.GetResultsCPA(ctypes.byref(p_Results),ctypes.byref(theCount)):
            # Store Reaults
            n_result_lines = int(theCount.value)
            self.lib.ClearResultsBuffer()
            out_lines = []
            for j in range(0, n_result_lines-1): 
                out_lines.append(p_Results[j].decode('utf-8'))
            out_str = io.StringIO('\n'.join(out_lines))
            out_df = pd.read_csv(out_str, delim_whitespace=True, skiprows=3, names = colnames, dtype={'Date': str})
            self.results = out_df
        self.clear_buffers()
        del theCount  # shouldn't be needed but trying to fix progressive slowdown issue
        del p_Results
        return self.results
        
    def write_results(self, file):
        results_file = file
        if self.results is None:
            raise Exception("There are no results to write. Please run the model first")
        self.results.to_csv(results_file, index=False)
        #outfile = open(results_file, "w")
        #for j in range(0, self.n_result_lines -1): 
            #outfile.write(p_Results[j].decode("utf-8"))
        #outfile.close()
        if self.verbose():
            print('Wrote results to file')
            
    def write_errors_info(self):
        # Get Info and Errors
        p_Errors = ctypes.POINTER(ctypes.c_char_p)()
        NumErrors = ctypes.c_int(0)
        errorpath = os.path.abspath('./errors.txt')
        infopath = os.path.abspath('./info.txt')
        if self.lib.GetErrorListCPA(ctypes.byref(p_Errors), ctypes.byref(NumErrors)):
            # Get Errors
            max = int(NumErrors.value)
            outfile = open(errorpath, "w")
            for j in range(0,max-1):
                outfile.write(p_Errors[j].decode("utf-8"))
            outfile.close()
            if self.verbose and (max > 0):
                print('Wrote errors to {}'.format(errorpath))
            self.lib.ClearErrorList()
        p_Info = ctypes.POINTER(ctypes.c_char_p)()
        NumInfo = ctypes.c_int(0)
        if self.lib.GetInfoListCPA(ctypes.byref(p_Info), ctypes.byref(NumInfo)):
            # Get Info
            max = int(NumInfo.value)
            outfile = open(infopath, "w")
            for j in range(0,max-1) :
                outfile.write(p_Info[j].decode("utf-8"))
            outfile.close()
            if self.verbose and (max > 0):
                print('Wrote info list to {}'.format(infopath))
            self.lib.ClearInfoList()
            
    def close_library(self):
        #del self.lib
        dlclose_func = ctypes.CDLL(None).dlclose
        dlclose_func.argtypes = [ctypes.c_void_p]
        handle = self.lib._handle
        del self.lib
        #print('dlclose returned {:d}'.format(dlclose_func(handle)))
        #print(self.lib)
        self.lib = None