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

class InputWriter:

    def __init__(self, params, in_path = "./inputs", in_filename = 'vp_input.txt',
                 weather_file = 'Columbus', verbose = False):
        self.params = params
        self.path = in_path
        self.filename = in_filename
        self.verbose = verbose
        self.weather_file = weather_file.lower()
        weather_dir = './weather/'
        self.weather_locs = {'columbus': weather_dir + '18815_grid_39.875_lat.wea',
                             'sacramento': weather_dir + '17482_grid_38.375_lat.wea'}
        if self.weather_file in self.weather_locs.keys():
            self.weather_file = self.weather_locs[self.weather_file]



    def write_inputs(self):
        """
        Function to create a single input file from a set of parameters in the form of
        a one row dataframe, where columns are named.
        """
        if self.verbose:
            print("Printing input file to: {}".format(self.path))
            print("Weather file location: {}".format(self.weather_file))
        inputs = ['{}={}'.format(key, value) for key, value in self.params.items()]
        with open(os.path.join(self.path,self.filename), 'w') as file:
            for x in inputs:
                file.write('{}\n'.format(x))



