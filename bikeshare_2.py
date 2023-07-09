import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def print_line():
    """
    Print a set of lines.
    """
    print('-'*40)


def print_invalid():
    """
    Print a set of lines, followed by a text stating invalid entry.
    """
    print_line()
    print('Invalid input received.')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
   
    # List of unique months in the dataframe
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    # List of unique days in the dataframe
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    # counter variable denoting if entered city exists in the CITY_DATA dictionary
    city_counter = 1
    # counter variable denoting if entered month exists in the months list or equals all
    month_counter = 1
    # counter variable denoting if entered day exists in the days list or equals all
    day_counter = 1

    print('Hello! Let\'s explore some US bikeshare data!')

    while(city_counter):
        # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input("Enter the name of a city (Select from 'Chicago', 'New York City', or 'Washington' only): ").lower()
        # If city exists in the CITY_DATA key, set counter to 0, making loop invalid
        if city in CITY_DATA:
            city_counter = 0
        # If any character other than the city names existing in the CITY_DATA key is entered, print error message and continue loop
        else:
            print_invalid()
            print_line()

    while(month_counter):
        # TO DO: get user input for month (all, january, february, ... , june)
        month = input("Enter a month (Please select 'all' or select from: {} only): ".format(months)).lower()
        # If user entered all, or if month exists in the months list, set counter to 0; making while loop invalid
        if month.lower() == 'all' or month.title() in months:
            month_counter = 0
            # If all isn't entered or if month doesn't exist in the months list, print error message and continue loop
        else:
            print_invalid()
            print_line()

    while(day_counter):
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Enter a day (Please select 'all' or select from: {} only): ".format(days)).lower()
        # If user entered all or if day exists in the days list, set counter to 0; making while loop invalid
        if day.lower() == 'all' or day.title() in days:
            day_counter = 0
        # If any character other than all or days existing in the days list is entered, print error message and continue loop
        else:
            print_invalid()
            print_line()

    print_line()
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city, filters by month and day, and deals with Nan values if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.strftime('%B')
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    # Resolve NaN values in User Type, Gender and Birth Year columns
    # Only for Chicago & New York City since Washington doesn't have those two columns
    if city != 'washington':
        # Fill Null User Types with Unspecified
        df['User Type'] = df['User Type'].fillna('Unspecified')
        # Fill Null Genders with Unknown
        df['Gender'] = df['Gender'].fillna('Unknown')
        # Interpolate Null Birth Years
        df['Birth Year'] = df['Birth Year'].interpolate(method = 'linear', axis = 0)
        
    return df

def get_mode(modeof):
    """
    Calculates the mode of the passed arguments.
    
    Args:
        (object) modeof - Pandas DataFrame column to calculate mode of
    
    Returns:
        (str) popular_value - Mode of passed Pandas DataFrame column
    """

    # Calculate mode of the DataFrame column modeof and select the value
    popular_value = modeof.mode()[0]  

    return popular_value

def seconds_interval(in_seconds):
    """
    Converts seconds into days, hours, minutes, seconds.
    
    Args:
        (numpy.int64) in_seconds - Seconds integer to convert into separate time intervals
    Returns:
        (str) time_interval - Time interval string created by appending intervals in time_list list
    """

    # Assign the total time in seconds as 'datetime.timedelta' object
    seconds_timedel = timedelta(seconds = int(in_seconds))
    # Collect days attribute of 'datetime.timedelta' object
    tot_days = seconds_timedel.days

    # Assign it as 'datetime.datetime' object by adding it to Jan 1, 0001
    seconds_datetim = datetime(1,1,1) + seconds_timedel
    # Collect hour, minute and second attribute of 'datetime.datetime' object
    rem_hours = seconds_datetim.hour
    rem_minutes = seconds_datetim.minute
    rem_seconds = seconds_datetim.second

    # Assign the values to intervals dictionary
    intervals = {'days': tot_days, 'hours': rem_hours, 'minutes': rem_minutes, 'seconds': rem_seconds}
    # List of intervals created from in_seconds
    time_list = []

    # Create a list of intervals from in_seconds
    # Only add intervals with non-zero entries
    # If interval is 1, change key to singular
    time_list = [
        "{} {}".format(value, key.rstrip('s')) if value == 1 
        else "{} {}".format(value, key)
        for key, value in intervals.items() if value
    ]
    
    # Join the values in time_list to form a string separated by ','
    time_interval = ', '.join(time_list)

    return time_interval


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df - Modified DataFrame with filtered data
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    # If all is not selected for month, the entered month will always be the most common month
    if month == 'all':
        # Find the most common month (string)
        popular_month = get_mode(df['Month'])
        print('The most Popular Month is: {}'.format(popular_month))
    # Display user entered month
    else:
        print('The Month you entered is: {}'.format(month.title()))

    # TO DO: display the most common day of week
    
    # If all is not selected for day, the entered day will always be the most common day
    if day == 'all':
        # Find the most common day of the week
        popular_day_of_week = get_mode(df['Day of Week'])
        print('The most Popular Day of Week is: {}'.format(popular_day_of_week))
    # Display user entered day
    else:
        print('The Day you entered is: {}'.format(day.title()))

    # TO DO: display the most common start hour

    # Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # Find the most popular hour
    popular_hour = get_mode(df['hour'])

    print('The most Popular Start Hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        (DataFrame) df - Modified DataFrame with filtered data
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    # Find the most common start station (string)
    popular_start_station = get_mode(df['Start Station'])

    print('The most Popular Start Station is:', popular_start_station)

    # TO DO: display most commonly used end station

    # Find the most common end station (string)
    popular_end_station = get_mode(df['End Station'])

    print('The most Popular End Station is:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip

    # First, create a combination of start station and end station trip
    # New column created with local scope to pull sum of Start Station and End Station columns
    df['combination_stations'] = df['Start Station'] + ' - ' + df['End Station']

    # Find the most frequent combination of start station and end station trip (string)
    popular_combination_station = get_mode(df['combination_stations'])

    print('The most Popular Combination of Start and End Station Trip is:', popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        (DataFrame) df - Modified DataFrame with filtered data
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    # Calculate total seconds by adding the Trip Duration column
    # Call seconds_interval() function to convert seconds to time intervals
    total_travel = seconds_interval(df['Trip Duration'].sum())

    print('Total Travel Time is: {}'.format(total_travel))

    # TO DO: display mean travel time
    # Calculate mean of the Trip Duration column
    # Call seconds_interval() function to convert seconds to time intervals 
    mean_travel = seconds_interval(df['Trip Duration'].mean())

    print('Mean Travel Time is: {}'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        (DataFrame) df - Modified DataFrame with filtered data
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print(user_types_count)

    # TO DO: Display counts of gender
    try:
        genders_count = df['Gender'].value_counts()
        print(genders_count)
    except:
        print('Gender column is not available for Washington city.')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        # Find the minimun of the birth year to calculate the earliest birth year
        earliest_birth = int(df['Birth Year'].min())
        print('The earliest year of birth is: {}'.format(earliest_birth))

        # Find the maximum of the birth year to calculate the most recent birth year
        newest_birth = int(df['Birth Year'].max())
        print('The most recent year of birth is: {}'.format(newest_birth))

        # Find the mode of the birth year to calculate the most common birth year
        common_birth = int(get_mode(df['Birth Year']))
        print('The most common year of birth is: {}'.format(common_birth))
    except:
        print('Birth Year column is not available for Washington city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()

def print_raw_data(df):
    """
    Prompts user if they wish to display raw data and iterates over filtered table
    to display raw data as user wishes, in increments of 5 rows.
    
    Args:
        (DataFrame) df - Modified DataFrame with filtered data
    """

    # Assign 0 to variable counter to keep track of the lines of rows printed
    counter = 0

    while counter < len(df.index):
        if not(counter):
            # TO DO: get user input if they want to print the first few raw data of the filtered dataset
            display_yes = input("Do you want to see the first 5 lines of raw data? Enter 'yes' or 'no': ").lower()
        else:
            # Ask print the next lines if asking for the second time
            display_yes = input("Do you want to see the next 5 lines of raw data? Enter 'yes' or 'no': ").lower()
        try:
            if display_yes == 'yes':
                print(df.iloc[counter: counter + 5])
                counter += 5
            elif display_yes == 'no':
                break
            else:
                print_invalid()
        finally:
            print_line()


def main():

    # Assign no_restart variable as 0
    # When the user enters no to restart prompt, this will be changed to 1, the second while loop will break and the follwing loop will be invalid
    no_restart = 0

    # Call the functions initially and after user has entered yes to restart the program
    while not no_restart:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)

        # Assigning counter to 1 to keep track of user pressing yes to restart
        counter = 1

        # Stay in the while loop until the user presses either 'yes' or 'no'
        while counter:
            restart = input("\nWould you like to restart? Enter 'yes' or 'no': ").lower()
            try:
                # If user presses yes, set counter to 0; breaking this loop
                if restart == 'yes':
                    print_line()
                    print('Restarting.')
                    counter = 0
                # If user presses no, set no_restart to 1, so that the previous while loop will not run
                elif restart == 'no':
                    print_line()
                    print('Exiting.')
                    no_restart = 1
                    break 
                else:
                    print_invalid()             
            finally:
                print_line()


if __name__ == "__main__":
	main()
