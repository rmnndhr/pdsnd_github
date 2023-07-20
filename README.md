# GitHub Project

## Python U.S. Bikeshare Data Project

### Date created
July 3, 2023

### Project Title
Udacity's Explore U.S. Bikeshare Data

### Description
Using the programming language Python,
- analyze the Bikeshare data available for three major U.S. cities:
  - Chicago
  - New York City
  - Washington
- generate useful descriptive statistics from the dataset such as:
  - Popular times of travel (i.e., occurs most often in the start time)
    - most common month
    - most common day of week
    - most common hour of day
  - Popular stations and trip
    - most common start station
    - most common end station
    - most common trip from start to end (i.e., most frequent combination of start station and end station)
  - Trip duration
    - total travel time
    - average travel time
  - User stats
- build an interactive environment to request input (city, month(s), day(s)) from user and filter the resulting output
- display the raw data (filtered table based on user selected city, month, day) if requested by the user

### Data Wrangling Steps Taken
Washington data didn't have Gender and Birth Year data available. It didn't have any Null values either. For the remaining states, the following data cleaning steps were taken:
- Null User Type entries were replaced with Unspecified
- Null Gender entries were replaced with Unknown
- Null Birth Year entries were interpolated

### Files used
- bikeshare_2.py
- [chicago.csv](https://www.divvybikes.com/system-data)
- [new_york_city.csv](https://www.citibikenyc.com/system-data)
- [washington.csv](https://www.capitalbikeshare.com/system-data)
>**Note**: The .csv files aren't included in the repository, but are needed to run the Python program. The link to the original files are also provided.

### Program versions used
- Python ver.: 3.10.9.final.0
- Visual Studio Code ver.: 1.80.0
- Terminal ver.: 2.12.7 (445)

### Python Package versions used
- pandas 1.5.3
- NumPy 1.23.5

### Credits
[How to convert Seconds into Minutes/Hours/Days - Stackoverflow](https://stackoverflow.com/questions/4048651/function-to-convert-seconds-into-minutes-hours-and-days)
