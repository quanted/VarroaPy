[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3461090.svg)](https://doi.org/10.5281/zenodo.3461090)


# VarroaPy
Python-based wrapper for the VarroaPop+Pesticide bee colony model

Developed by: Jeffrey Minucci
<br><br>

#### Quick Start guide: 

1. **Requirements:** 
    * You must have **VarroaPop version 3.2.8.16** installed locally. To download VarroaPop from the USDA ARS, try [this link](https://www.ars.usda.gov/research/software/download/?softwareid=75), or contact crystalriverconsulting@gmail.com. Or you can use the installer found in this repo at VarroaPy/VarroaPop/VarroaPopSetup.msi
    * You must also have the **pandas** package installed in python.


2. **Clone this repo**, ideally into the directory where your python code or project will be.

3.  **Import the VarroaPop class** from  VarroaPy/VarroaPy/RunVarroaPop in python,
    e.g.:
    
        from VarroaPy.VarroaPy.RunVarroaPop import VarroaPop
    
    
    if VarroaPy is cloned to the same directory that your python script is     in.
    
4. **Create a VarroaPop object**, using a dictionary of parameters (parameter_name: value), and a weather file option.


        params = {"ICWorkerAdults": 10000, "ICWorkerBrood": 8000, "SimStart": "04/13/2015", "SimEnd": "09/15/2015"}
        weather = "Columbus"
        vp = VarroaPop(parameters= params, weather_file = weather)
     
    Note that weather can be a path to a valid .wea or .wth file, or one of the included base weather locations, which are:    "Columbus" (OH; default), "Sacramento", "Phoenix", "Yakima", "Eau Claire", "Jackson" (MS), or "Durham (NC)"
    
    Parameters that are not set in the dictionary will take the default values from the VarroaPop session file found at 'VarroaPy/VarroaPy/files/exe/default.vrp'. If you'd like to modify these defaults you can open this session file in the VarroaPop GUI, edit it, and save it.
    
    For a list of exposed parameters, see docs/VarroaPop_exposed_parameters.xlsx


5. **Run the Model** 
    ```
    vp.run_model()
    ```
    An output .txt file will be saved to 'VarroaPy/VarroaPy/files/output'

6. Optionally, **read the output** into a python object, either as a pandas dataframe or a json string
    ```
    output = vp.get_output() #pandas dataframe
    output_json = vp.get_output(json_str= True) #json string
    ```
    
7. You can give new parameters and/or update previously set ones (and optionally set a new weather file), and then run the model again. Parameters that were previously defined will remain set

    ```
    params_new = {"ICWorkerAdults": 22200, "InitColPollen": 4000}
    #Updates value for ICWorkerAdults, new value for InitColPollen, other values set previously remain the same.
    vp.set_parameters(parameters = params_new, weather_file = "Yakima")
    vp.run_model()
    ```
