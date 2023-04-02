# Required packages
import time
import pandas as pd
import numpy as np
import sys
import warnings
import datetime

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# The function below is used to get user input for city, month, and day.
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('You will be guided throughout the script with interactive prompts.')
    print('Please ensure that you read the instructions carefully, otherwise you may have to restart the script.')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            'Please enter the name of the city you wish to analyse (e.g., chicago/chi, new york city/nyc, washington/wa) or type "bye" to exist the script:')
        city = city.lower().strip()
        if city in ['chicago', 'chi', 'new york city', 'nyc', 'washington', 'wa']:
            city_mapping = {
                'chi': 'chicago',
                'nyc': 'new york city',
                'wa': 'washington'
            }
            city = city_mapping.get(city, city)
            print('I found this city in the database. I am now proceeding to do analysis for',
                  city.capitalize().strip(), 'city.')
        elif city in ['bye']:
            print('Bye bye! Exiting the program.')
            sys.exit()
        else:
            warnings.warn(
                'I cannot find this city!')
            print("Please check your input!")

    # get user input for month (all, january, february, ... , june)
        month = input(
            'Please enter the name or number of a month from january to june (e.g., january / 1, february / 2, ... , june / 6) to select the month or enter "all" to select all months or type "bye" to exist the script:')
        month = month.lower().strip()
        if month in ['1', 'january', '2', 'february', '3', 'march', '4', 'april', '5', 'may', '6', 'june']:
            months_mapping = {'1': 'january', '2': 'february',
                              '3': 'march', '4': 'april', '5': 'may', '6': 'june'}
            month = months_mapping.get(month, month)
            print('Analysing data for', month.capitalize().strip() + '.')
        elif month in ['bye']:
            print('Bye bye! Exiting the program.')
            sys.exit()
        elif month == 'all':
            month = 'all available months'
            print('All months will be included.')
        else:
            warnings.warn(
                'I cannot find this month!')
            print("Please check your input!")

    # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input(
            'Please enter the day of week (e.g., monday / 1, tuesday / 2, ... , sunday / 7)) or enter "all" to select all days or type "bye" to exist the script:')
        day = day.lower().strip()
        if day in ['1', 'monday', '2', 'tuesday', '3', 'wednesday', '4', 'thursday', '5', 'friday', '6', 'saturday', '7', 'sunday']:
            days_mapping = {'1': 'monday', '2': 'tuesday', '3': 'wednesday',
                            '4': 'thursday', '5': 'friday', '6': 'saturday', '7': 'sunday'}
            day = days_mapping.get(day, day)
            print('Analysing data for', day.capitalize().strip() + '.')
        elif day in ['bye']:
            print('Bye bye! Exiting the program.')
            sys.exit()
        elif day == 'all':
            day = 'all available days'
            print('All days will be included.')
        else:
            warnings.warn(
                'I cannot find this day!')
            print("Please check your input!")
    # return the output
        print('Will be returning the results for', city.capitalize() +
              ', ' + month.capitalize() + ', and ' + day.capitalize() + '.')
        print('-'*40)
        return city, month, day

# The function below is used to load data from the csv files.
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # prepare mappings
    months_mapping = {'january': '1', 'february': '2', 'march': '3',
                      'april': '4', 'may': '5', 'june': '6'}

    days_mapping = {'monday': '1', 'tuesday': '2', 'wednesday': '3',
                    'thursday': '4', 'friday': '5', 'saturday': '6', 'sunday': '7'}

    # load data file into a dataframe
    try:
        df = pd.read_csv(CITY_DATA.get(city, city))
        # Tidy columns
        df.columns = df.columns.str.strip().str.lower().str.replace(
            ' ', '_', regex=False).str.replace('(', '', regex=False).str.replace(')', '', regex=False)
        # Extract data from start and end time
        df['start_time'] = pd.to_datetime(
            df['start_time'], infer_datetime_format=True)
        df['end_time'] = pd.to_datetime(
            df['end_time'], infer_datetime_format=True)
        df['start_hour'] = df['start_time'].dt.hour
        df['end_hour'] = df['end_time'].dt.hour
        df['month'] = df['start_time'].dt.month
        df['day_week'] = df['start_time'].dt.dayofweek
        df['day_week_iso'] = df['day_week'] + 1
        df['day_month'] = df['start_time'].dt.day
        df['trip'] = (df['start_station'] + ' <to> ' + df['end_station'])
        df['trip_duration'] = df['end_time'] - df['start_time']
        df['trip_duration'] = df['trip_duration'].dt.total_seconds().astype(int)
    except (FileNotFoundError, UnboundLocalError) as e:
        print("Please check your input, I cannot find the file. Exiting the program.")
        sys.exit()
    # filter by month if applicable
    if month == 'all available months':
        pass
    elif month in months_mapping.keys():
        df = df[df['month'] == int(months_mapping[month])]

    # filter by day if applicable
    if day == 'all available days':
        pass
    elif day in days_mapping.keys():
        df = df[df['day_week_iso'] == int(days_mapping[day])]

    return df

# The following function is used to display the most common month, day of week and hour of day.
def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
                Args:
                (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months_mapping = {'1': 'january', '2': 'february',
                      '3': 'march', '4': 'april', '5': 'may', '6': 'june'}

    days_mapping = {'1': 'monday', '2': 'tuesday', '3': 'wednesday',
                    '4': 'thursday', '5': 'friday', '6': 'saturday', '7': 'sunday'}

    # display and print  the most common month
    the_month = df['month'].value_counts().idxmax()
    the_month = months_mapping.get(str(the_month), the_month)
    print('The most common month is', the_month.capitalize().strip() + '.')

    # displayv the most common day of week
    the_day_of_week = df['day_week_iso'].value_counts().idxmax()
    the_day_of_week = days_mapping.get(str(the_day_of_week), the_day_of_week)
    print('The most common day of week is',
          the_day_of_week.capitalize().strip() + '.')

    # display and print  the most common start hour
    the_start_hour = df['start_hour'].value_counts().idxmax()

    if the_start_hour < 12:
        the_start_hour = str(the_start_hour) + ' AM'
    else:
        the_start_hour = str(the_start_hour - 12) + ' PM'

    print('The most common start hour is', the_start_hour + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# The function display and print the most popular stations and trip.
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display and print the most commonly used start station
    the_start_station = df['start_station'].value_counts().idxmax()
    print('The most commonly used start station is', the_start_station + '.')

    # display and print the most commonly used end station
    the_end_station = df['end_station'].value_counts().idxmax()
    print('The most commonly used end station is', the_end_station + '.')

    # display and print the most frequent combination of start station and end station trip
    the_trip = df['trip'].value_counts().idxmax()
    print('The most frequent combination of start station and end station trip is', the_trip + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# The following function shows duration statistics.
def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
        Args:
            (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display and print  total travel time
    total_travel_time = df['trip_duration'].sum() / 3600
    print('The total travel time is', total_travel_time, 'hours.')

    # display and print  mean travel time
    mean_travel_time = df['trip_duration'].mean() / 60
    print('The mean travel time is', mean_travel_time, 'minutes.')

    # display and print  median travel time
    median_travel_time = df['trip_duration'].median() / 60
    print('The median travel time is', median_travel_time, 'minutes.')

    # display and print  the shortest travel time
    shortest_travel_time = df['trip_duration'].min() / 60
    print('The shortest travel time is', shortest_travel_time, 'minute(s).')

    # display and print the longest travel time
    longest_travel_time = df['trip_duration'].max() / 60
    print('The longest travel time is', longest_travel_time, 'minute(s).')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# The following function displays statistics on bikeshare users.
def user_stats(df, city):
    """
    Displays statistics on bikeshare users.
            Args:
                (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
                (str) city - name of the city to analyze
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display and print  counts of user types
    the_user_types = df['user_type'].value_counts()

    print('The counts of user types are:'
          '\n\tSubscriber: ' + str(the_user_types.get('Subscriber')) +
          '\n\tCustomer: ' + str(the_user_types.get('Customer')) +
          '\n\tDependent: ' + str(the_user_types.get('Dependent')) +
          '\n')

    if city != 'washington':
        # Display and print  counts of gender
        the_user_gender = df['gender'].value_counts()

        print('The counts of user gender are:'
              '\n\tMen: ' + str(the_user_gender.get('Male')) +
              '\n\tWomen: ' + str(the_user_gender.get('Female')) +
              '\n')

        # Display and print  earliest, most recent, and most common year of birth
        the_earliest_birth_year = round(df['birth_year'].min())
        the_most_recent_birth_year = round(df['birth_year'].max())
        the_most_common_birth_year = round(
            df['birth_year'].value_counts().idxmax())
        the_min_age = round(
            min(max(df['end_time'].dt.year) - df['birth_year']))
        the_max_age = round(
            max(max(df['end_time'].dt.year) - df['birth_year']))
        the_average_age = round(
            np.mean(max(df['end_time'].dt.year) - df['birth_year']))

        print('The earliest recorded birth year of a user is', str(the_earliest_birth_year) + '.' + '\n' +
              'The most recent recorded birth year of a user is', str(the_most_recent_birth_year) + '.' + '\n' +
              'The most commonly recorded birth year of a user is', str(the_most_common_birth_year) + '.' + '\n' +
              'The average age of an user is', str(the_average_age) + ' years old.' + '\n' +
              'The youngest user is', str(the_min_age) + ' year(s) old.' + '\n' +
              'The oldest user is', str(the_max_age) + ' years old.')
    else:
        print('I am sorry, however, the columns gender and birth year are not available for Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# The following function is used to display 5 rows of raw data on bikeshare users based on user prompt.
# This function was added based on reviewer comments.
def view_raw_data(df,
                  prompt='Would you like to view 5 rows of individual trip data? Enter "yes" or "no"\n',
                  valid_entries=['yes', 'no']):
    """
    Displays 5 rows of raw data on bikeshare users based on user prompt.
        Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """

    try:

        user_input = input(str(prompt)).lower()

        while user_input not in valid_entries:
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! the chosen entry is: {}\n'.format(user_input))

    except:
        print('Seems like there is an issue with your input')

    start_loc = 0

    while(user_input == 'yes'):
        print('-'*40)
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        try:
            user_input = input("Do you wish to continue?: ").lower()

            while user_input not in valid_entries:
                print('Sorry... it seems like you\'re not typing a correct entry.')
                print('Let\'s try again!')
                user_input = str(input(prompt)).lower()
        except:
            print('Seems like there is an issue with your input')
            print('-'*40)

# Run this if the code is run as a script


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city=city)
        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print(
                'Thank you for using the interactive analysis tool for bikeshare data. Goodbye!')
            break


# Condition to execute main() function defined above:
if __name__ == "__main__":
    main()  # Main states this is run only if __main__ is True, i.e., file is run as a script
