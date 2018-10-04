import time
import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from PIL import Image


#if data is available for another city then the CITY_DATA dictionaty has to be modified by
#adding key for the city and file name as a value
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = CITY_DATA.keys()


#to show a list of something to the user to chose from:
# 1. smth1
# 2. smth2
def my_enumerate(iterable, start=0):
    # Implementation of a generator function here
    count = start

    for element in iterable:
        yield count, element
        count  += 1

def saying_bye():
        print('\nThank you for using Bikeshare project')
        print('Prepared by Boris Kushnarev')
        print('for class: Programming for Data Science')
        print('Udacity University')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid input


    while True:
        print("\n You can choose one city from the following list: \n")
        #show a city list to users
        for i, city_list in my_enumerate(cities, 1):
            print("{}.: {}".format(i, city_list.title()))
        city = input("\n Please, type in the chosen city ").lower()
        if city in CITY_DATA.keys():
            print(' --> Your chosen city is', city.title(), '\n')
            break
        else:
            print('\nAttention! Your chosen city is incorrect.')
            print('Do you want to try again or exit the program?')
            ter_var = input('To continue press C, to exit press E: ').lower()
            if ter_var == 'e':
                print('\n Thank you for using Bikeshare project. Bye!')
                sys.exit()

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        #show list of months available for users
        print('The information is available for the following months:')
        for i, month_list in my_enumerate(months[1:7], 1):
            print("{}.: {}".format(i, month_list.title()))
        month = input("Please, type in a month you need to get statistics for or for all months type ALL: ").lower()
        if month in months[1:13]:
            print('-->>Your chosen month is', month.title(), '\n')
            break
        elif month == months[0]:
            print('-->>You chose All months to consider \n')
            break
        else:
            print('\nAttention! Your chosen month is incorrect.')
            print('Do you want to try again or exit the program?')
            ter_var = input('To continue press C, to exit press E: ').lower()
            if ter_var == 'e':
                saying_bye()
                sys.exit()


    # get user input for day of week (all, monday, tuesday, ... sunday)

    days_weeks = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        day = input("Please, type in a day of the week you need to get statistics for or All for all week days: ").lower()
        if day in days_weeks[1:8]:
            print('-->>Your chosen day is', day.title(), '\n')
            break
        elif day == days_weeks[0]:
            print('-->>You chose All days of the week to consider \n')
            break
        else:
            print('\nAttention! Your chosen day is incorrect.')
            print('Do you want to try again or exit the program?')
            ter_var = input('To continue press C, to exit press E: ').lower()
            if ter_var == 'e':
                saying_bye()
                sys.exit()
    print('-'*40)
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

    df = pd.read_csv(CITY_DATA[city]) #read data from .csv file

    show_raw_data = input('Do you want to see the first 5 rows of raw data? Please type yes or no: ').lower()
    if show_raw_data == 'yes':
        number_rows =  len(df.index)
        i = int(input('Please, enter the row number you want to see the data from: '))
        while show_raw_data == 'yes':
            print(df.iloc[i:i+5, :])
            i+=5
            #check for the end of data set
            if i >= number_rows:
                print('-->>The end of data set is reached.\n')
                break
            show_raw_data = input('To see the next 5 rows type in "yes" otherwise "no" ').lower()
            if show_raw_data == 'no':
                break


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days_weeks = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                      'saturday', 'sunday']
        day = days_weeks.index(day.lower())
        df = df[df['day_of_week'] == day]

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    return df

def time_stats(df, month, day, city):
    """Displays statistics on the most frequent times of travel.
       Plot probability distribution of weekly days of bike rental and
       Save the plots to files.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days_weeks = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                  'saturday', 'sunday']

    # display the most common month
    if month != 'all':
        print('\nFor the chosen month {} '.format(month.title()))
    else:
        month_common = df['month'].mode()[0]
        print('-->>The most common month is {}'.format(months[month_common - 1].title()))
    #we will creat a plot and save it to a file. Check if file exists in the current directory, if so, remove it
    for filename in os.listdir():
        if filename.endswith('hist_week_day_time.png'):
            os.remove('hist_week_day_time.png')
        # display the most common day of week
    if day != 'all':
        print('For the chosen day of the week {}'.format(day.title()))
    else:
        day_common = df['day_of_week'].mode()[0]
        print('-->>The most common days is {}'.format(days_weeks[day_common].title()))
        #plot the Probability distribution of dayly bike rental
        n, bins, patches = plt.hist(df['day_of_week'], 6, density=True, facecolor='g', alpha=0.75)
        plt.xlabel('days of week')
        plt.ylabel('Probability')
        plt.title('Probability distribution of weekly days of bike rental in {}'.format(city.title()))
        plt.axis([0, 6, 0, 0.5])
        plt.grid(True)
        plt.savefig('hist_week_day_time.png', bbox_inches='tight') #hist is saved to a file
        print('-->>Probability distribution of start hours has been created and saved to hist_week_day_time.png file in the current directory\n')
        plt.clf()
    return
    #we will creat a plot and save it to a file. Check if file exists in the current directory, if so, remove it
    for filename in os.listdir():
        if filename.endswith('hist_start_time.png'):
            os.remove('hist_start_time.png')
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("-->>The most common start hour is: {}".format(popular_hour))

    #plot Probability distribution of start time and save it to a file.
    n, bins, patches = plt.hist(df['hour'], 23, density=True, facecolor='g', alpha=0.75)
    plt.xlabel('Hours')
    plt.ylabel('Probability')
    plt.title('Probability distribution of start hours of bike rental in {}'.format(city.title()))
    plt.axis([0, 23, 0, 0.15])
    plt.grid(True)
    plt.savefig('hist_start_time.png', bbox_inches='tight') #hist is saved to a file
    print('-->>Probability distribution of start hours has been created and saved to hist_start_time.png file in the current directory\n')
    plt.clf()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    print("-->>The most commonly used start station is: {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("-->>The most commonly used end station is: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    start_end_station = 'Start station: ' + df['Start Station'] + '; End station: ' + df['End Station']
    print('-->>The most common combination of start station and end station trip:\
     \n', start_end_station.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Duration'] = df['End Time'] - df['Start Time']
    print('-->>The total travel time is {}'.format(df['Duration'].sum()))

    # display mean travel time
    print('-->>The mean travel time is {}'.format(df['Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\n -->>Counts of user type:\n{}".format(df['User Type'].value_counts()))
    # Display counts of gender
    if 'Gender' in df.columns:
        print("\n-->Counts of gender:\n{}".format(df['Gender'].value_counts()))
    else:
        print('\n-->>Gender data is not available for {}\n'.format(city))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\n-->>The earliest year of birth: {}".format(df['Birth Year'].min()))
        print("-->>The recent year of birth: {}".format(df['Birth Year'].max()))
        print("-->>The most common year of birth: {}\n".format(df['Birth Year'].mode()[0]))
    else:
        print('\nGender data is not available for {}\n'.format(city))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    print('\n*** Bikeshare project ***')
    print('*** Extract statistical information from data of some US cities presented in a list below\n')
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day, city)
        station_stats(df)
        trip_duration_stats(df)
        ser_stats(df, city)
        if day.lower() == 'all':
            f = Image.open("hist_week_day_time.png").show()
        f = Image.open("hist_start_time.png").show()
        saying_bye()
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
