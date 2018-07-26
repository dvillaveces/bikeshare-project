import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': ['chicago.csv', 2704958],
              'new york city': ['new_york_city.csv', 8537673],
              'washington': ['washington.csv', 681170]}

def get_filters():
    """
    Asks user to specify cities, month, and day to analyze.

    Returns:
        (list) cities - list containing names of the cities to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    print('\nWe will start by filtering the data. If you want to compare two cities, enter their names separated by a comma. If you want to explore a single city just type its name.\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = set('a')
    while not cities.issubset(CITY_DATA) or len(cities) > 2:
        cities = set(map(str.strip, input('Which city would you like to explore? (Chicago, New York City, Washington): ').lower().split(',')))

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Which month should I filter by? (all, January, February, ... , June): ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Which day of week should I filter by? (all, Monday, Tuesday, ... , Sunday): ').lower()

    print('-'*40)
    return list(cities), month, day


def load_data(cities, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (list) cities - list containing names of the cities to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        dfs - list of Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a list of dataframes
    dfs = [pd.read_csv(CITY_DATA[city][0]) for city in cities]

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # for each df, convert the Start Time column to datetime
    for i in range(len(dfs)):
        dfs[i]['Start Time'] = pd.to_datetime(dfs[i]['Start Time'])

        # extract month and day of week from Start Time to create new columns
        dfs[i]['month'] = dfs[i]['Start Time'].dt.month
        dfs[i]['day_of_week'] = dfs[i]['Start Time'].dt.weekday_name

        # filter by month to create the new dataframe
        if month != 'all':
            dfs[i] = dfs[i][dfs[i]['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day to create the new dataframe
            dfs[i] = dfs[i][dfs[i]['day_of_week'] == day.title()]

    return dfs


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # get the most common month in numbers
    month_mode = df['month'].mode()[0]
    # use months list to get corresponding month name
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_mode = months[month_mode - 1]
    print('Most common month was:', month_mode.title())

    # display the most common day of week
    day_mode = df['day_of_week'].mode()[0]
    print('The most common day of week was:', day_mode)

    # display the most common start hour
    hour_mode = df['Start Time'].dt.hour.mode()[0]
    print('The most common hour to start the trip was: {}:00 - {}:00'.format(hour_mode, (hour_mode + 1) % 23))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    print('Most common start station was:', start_station_mode)

    # display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    print('Most common end station was:', end_station_mode)

    # display most frequent combination of start station and end station trip
    trip_start, trip_end = df.groupby(['Start Station','End Station']).count().sort_values('Unnamed: 0').index[-1]
    print('The most frequent trip was from {} to {}'.format(trip_start, trip_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # access total time in seconds
    tot_time = df['Trip Duration'].sum()
    # convert time in seconds to days, hours, minutes, seconds
    m, s = divmod(tot_time, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print('Total trip time was: {} days {} hours {} minutes and {} seconds'.format(int(d),int(h),int(m),int(round(s))))

    # display mean travel time
    # access mean time in seconds
    mean_time = df['Trip Duration'].mean()
    # convert mean time to minutes and seconds
    m, s = divmod(mean_time, 60)
    print('Mean trip time was: {} minutes and {} seconds'.format(int(m), int(round(s))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,cities):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Subscribers:',user_types['Subscriber'],'\n'+'Customers:',user_types['Customer'],'\n')

    # if city is Washington, indicate that no gender or birth year data is available
    if cities[0] == 'washington':
        print('Gender and birth year data are not available for Washington.')
    else:
        # Display counts of gender
        genders = df['Gender'].value_counts()
        print('Gender breakdown:\nFemale:',genders['Female'],'\n'+'Male:',genders['Male'])

        # Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print('\nBirth year stats:')
        print('Earliest: {}\nMost recent: {}\nMost common: {}'.format(earliest, most_recent, most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def comparison_stats(dfs, cities):
    """Displays comparison statistics between two cities."""

    print('\nCalculating Comparison Stats...\n')
    start_time = time.time()

    # display mean travel time comparison for each city
    for city, df in zip(cities, dfs):
        # access mean time in seconds
        mean_time = df['Trip Duration'].mean()
        # convert mean time to minutes and seconds
        m, s = divmod(mean_time, 60)
        print('Mean trip time for {} was: {} minutes and {} seconds'.format(city.title(), int(m), int(round(s))))

    print()

    # display total trips comparison for each city
    for city, df in zip(cities, dfs):
        tot_trips = df.shape[0]
        trips_per_100k = (tot_trips / CITY_DATA[city][1]) * 100000
        print('{} took {} total trips.'.format(city.title(), tot_trips))
        print('That is {} trips per 100.000 inhabitants!'.format(round(trips_per_100k)))

    print()

    # display gender comparison for each city
    for city, df in zip(cities, dfs):
        if city == 'washington':
            print('No gender data are available for Washington.')
        else:
            genders = df['Gender'].value_counts()
            female_ratio = round((genders['Female'] / (genders['Female'] + genders['Male'])) * 100, 2)
            print('In {}, {}% of trips were taken by women.'.format(city.title(), female_ratio))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        cities, month, day = get_filters()
        dfs = load_data(cities, month, day)
        if len(dfs) == 1:
            time_stats(dfs[0])
            station_stats(dfs[0])
            trip_duration_stats(dfs[0])
            user_stats(dfs[0], cities)
        else:
            comparison_stats(dfs, cities)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
