### Date created
01.4.2023

### Bikeshare Data Analysis 

### Description
The following project provides small python program that allows user to do an interactive data analysis bfor bikeshere data from the Motivate (bikesharing provider in the U.S.).

The analysis prompts the user to select one of the datasets representing cities. The choices are Chicago, New York City, or Washington. The original data can be downloaded from here - https://citibikenyc.com/system-data, however, the project utilises simplified version of data in .csv.

Upon choosing the city, the user is offered to choose further options to filter the results by month and day.

Once all filter choices are made, the user is presented with key statistics for the chosen filter. Specifically, these cover frequent times, stations, trip durations, and user characteristics. Afterwards, the user can choose to print first five rows of data and continue to do that until they select 'No'.

The final option is to re-run the entire script from the beggining.

### Files used
chicago.csv, new_york_city.csv, washington.csv

### Running instructions

The user needs to import the following packages to run the script:

import time
import pandas as pd
import numpy as np
import sys
import warnings
import datetime

The supported Python version is 3.10.8 and using miniconda is recomended. 

### Credits
https://github.com/udacity/pdsnd_github
https://stackoverflow.com
https://marketplace.visualstudio.com/items?itemName=codezombiech.gitignore
https://citibikenyc.com/system-data