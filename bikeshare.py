import pandas as pd
import numpy as np
import time
import sys

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print("\n\n", "Hello! Let's explore some US bikeshare data!".center(120, "-"), sep="")
    print('\n\n', 'PLEASE NOTE: When answering the following questions'.center(120, "-"), sep="")
    print("\n\n", "Please enter the letters only.  For 'chicago' you should input chicago".center(120, "-"), sep="")


    # Get user input for city (chicago, new york city, washington)
    city = input_check('\n\nWhich city would you like to explore', ['chicago', 'newyork', 'washington'])

    # Get user input for month (all, january, february, ... , june)
    month = input_check('\n\nWhich month would you like to explore', 
                        ['all', 'january', 'february', 'march', 'april', 'may', 'june'])

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input_check('\n\nWhich day would you like to explore', 
                      ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])


    # User input confirmation
    if day == 'all':
            stars = ('*'*120)
            good_job = (f'\n\nGood job! We are now going to explore "{city}", in "{month}", with "{day}"!\n\n')
            print('\n', stars, good_job, stars, sep="")
    else:
        stars = ('*'*120)
        good_job = (f'\n\nGood job! We are now going to explore "{city}", in "{month}", on a "{day}"!\n\n')
        print('\n', stars, good_job, stars, sep="")


    return city, month, day


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
    CITY_DATA = { 'chicago': 'chicago.csv',
                'newyork': 'new_york_city.csv',
                'washington': 'washington.csv' }


    # Watch for missing files error
    try:
    # Load data file into a dataframe
        df = pd.read_csv(CITY_DATA[city])

    # # Exit program without traceback and errors    
    except FileNotFoundError:
        stars = ('!'*60)
        fileerrormessage = f'\n\nSorry, {CITY_DATA[city]} file does not exist.'
        fileerrormessage += '\n\nPlease restart program when file location corrected\n\n'
        print(stars, fileerrormessage, stars, sep="")
        sys.exit()



    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # Extract month,day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['month'] = df['month'].str.lower()

    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['day_of_week'] = df['day_of_week'].str.lower()

    df['hour'] = df['Start Time'].dt.hour
    

    # Filter by month if applicable
    if month != 'all':
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
        

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""


    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # Display Month Explored if month is not 'all'
    popular_month = df['month'].mode()[0]
    month_check = df['month']
    if all(popular_month == month_check):
        print('Month explored:              ', popular_month)
    else:
        # Display the most common month
        popular_month_count = max(df['month'].value_counts())
        print('Most Popular Month:          ', popular_month, 'with', popular_month_count, 'trips')

    # Display Day Of Week Explored if week is not 'all'
    popular_day_of_week = df['day_of_week'].mode()[0]
    week_check = df['day_of_week']
    if all(popular_day_of_week == week_check):
        print('Day Of Week explored:        ', popular_day_of_week)
    else:
        # Display the most common day of week
        popular_day_of_week_count = max(df['day_of_week'].value_counts())
        print('Most Popular Day Of Week:    ', popular_day_of_week, 'with', popular_day_of_week_count, 'trips')


    # Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = max(df['hour'].value_counts())
    print('Most Popular Start Hour:     ', popular_hour, 'with', popular_hour_count, 'trips')


    # Display time taken to calculate stats
    print("\nThis took %s seconds." % (time.time() - start_time), '\n', ('-'*40), sep="")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = max(df['Start Station'].value_counts())
    print('Most Popular Start Station:', (' '*21), popular_start_station, 'with', popular_start_station_count, 'trips')


    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = max(df['End Station'].value_counts())
    print('Most Popular End Station:', (' '*23), popular_end_station, 'with', popular_end_station_count, 'trips')


    # Display most frequent combination of start station and end station trip
    e2estations = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    e2estations_count = max((df['Start Station'] + ' to ' + df['End Station']).value_counts())
    print('Most Popular Start Station to End Station Trip:  ', e2estations, 'with', e2estations_count, 'trips')


    print("\nThis took %s seconds." % (time.time() - start_time), '\n', ('-'*40), sep="")


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # Convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Display total travel time
    total_travel_time = (df['End Time'] - df['Start Time']).sum()
    print('Total travel time was:   ', total_travel_time)


    # Display mean travel time
    mean_travel_time = (df['End Time'] - df['Start Time']).mean()
    print('Average travel time was: ', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time), '\n', ('-'*40), sep="")


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('See below for User Type Counts:\n')
    print(user_types, '\n\n')

    #Check for Gender and Birth Year Columns
    column_check = list(df.columns)
    if 'Gender' not in column_check:
        print('PLEASE NOTE: Gender and Birth Year data not available for Washington')
    else:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print('See below for Gender Types Counts:\n')
        print(gender_counts, '\n\n')

        # Display earliest, most recent, and most common year of birth
        birth_year_earliest = df['Birth Year'].min()
        print('The earliest year of birth was:      ', birth_year_earliest.astype('int64'))
        birth_year_recent = df['Birth Year'].max()
        print('The most recent year of birth was:   ', birth_year_recent.astype('int64'))
        birth_year_common = df['Birth Year'].mode()[0]
        print('The most common year of birth was:   ', birth_year_common.astype('int64'))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    # User Instruction to see raw data correctly
    print('\nPLEASE NOTE: To see raw data correctly, you will need to widen your output window.')

    # Would you like to see some filtered raw data?
    ask4data = input_check('\nWould you like to see some filtered raw data', ['yes', 'no'])

    # Display filtered raw data if required
    if ask4data == 'yes':
        display_filter_Data(df)


def display_filter_Data(df):
    """Displays filtered data on user request"""

    # Maximise data display
    pd.set_option('display.max_columns', None, 'display.width', None, 'display.max_colwidth', None)

    ask4data = 'yes'

    # Start and end for iloc range
    start_row = 0
    end_row = 5

    # Checking for last row of dataframe
    last_row = (df.iloc[-1].name)

    # Print 5 rows of raw data
    while ask4data != 'no':
        # Check for last row of dataframe
        if end_row > last_row:
            # Print remaining rows
            print('\n\n', ('-'*200), '\n\n', df.iloc[start_row:last_row+1], '\n\n', ('-'*200), '\n', sep="")

            # Ask if want to restart data
            ask4data_check = ['Press <RETURN>', 'no']
            ask4data = input(f'Would you like to see the raw data again?: {ask4data_check}  ')

            # Deal with minor typo errors with CAPS and/or spaces ie 'No' when we want 'no'
            ask4data = check.lower().replace(" ", "").strip()
        
            # Reset start and end for iloc range
            if ask4data != 'no':
                start_row = 0
                end_row = 5
            else:
                return

        # Print 5 rows, want to see more?        
        print('\n\n', ('-'*200), '\n\n', df.iloc[start_row:end_row], '\n\n', ('-'*200), '\n', sep="")
        ask4data_check = ['Press <RETURN>', 'no']
        ask4data = input(f'Would you like to see more raw data?  Options available are: {ask4data_check}  ')

        # Deal with minor typo errors with CAPS and/or spaces ie 'No' when we want 'no'
        ask4data = ask4data.lower().replace(" ", "").strip()

        # Set iloc range for next 5 rows
        start_row += 5
        end_row += 5


def input_check(question, options):
    """Asks a question, checks input against list of correct answers, asks again if incorrect, until correct
        Returns correctly input answer to a designated variable"""
    
    check = input(f'\n{question}? \nOptions available are: {options}\n\n? ')

    # Deal with minor typo errors with CAPS and/or spaces ie 'New York' when we want 'newyork'
    check = check.lower().replace(" ", "").strip()
    
    # Check if correct characters in list of answers
    while check not in options:
            print(f'\n\nWAIT! "{check}" IS NOT AN AVAILABLE OPTION!\n\n')
            check = input(f'\n{question}? \nOptions available are: {options}\n\n? ')


    # Return correctly formatted answer
    return check


def main():
    while True:
        # Watch for keyboard interrupt
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        

            # Ask if restart required
            ask4restart = input_check('Would you like to restart', ['yes', 'no'])
        
            # EXIT if restart NOT required       
            if ask4restart == 'no':
                break

        # Exit program without traceback and errors
        except KeyboardInterrupt:
            stars = ('!'*30)
            keyboardinterruptmess = 'Keyboard Interrupt detected!, exiting program.....'
            print(stars, keyboardinterruptmess, stars, sep="")
            sys.exit()

if __name__ == "__main__":
	main()
