import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    city = input('Please enter chicago, new york city or washington.\n').lower()
    while True:
        if city not in cities:
            print('Please try again.\n')
            city = input('Please enter chicago, new york city or washington.\n').lower()
        else:
            print(('Your city is {}').format(city))
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ["january", "february", "march", "april", "may", "june", "all"]
    month = input('Please select a month from January through June or "all" if desired.\n').lower()
    while True:
        if month in months:
            print(('You have chosen {}.').format(month))
            break
        else:
            print('Please try again.\n')
            month = input('Please select a month from January through June or "all" if desired.\n').lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday','tuesday','wednesday','thursday','friday','saturday', 'sunday','all']
    day = input('Please enter your desired day of the week or "all" if desired.\n').lower()
    while True:
        if day in days:
            print(('You have chosen {}.').format(day))
            break
        else:
            print('Please try again.\n')
            day = input('Please enter your desired day of the week or "all" if desired.\n').lower()
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


    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        print("The most common month is: {}".format(str(df['month'].mode().values[0])))
    else:
        print("Common month is unavailable since a specific month was selected")

    # TO DO: display the most common day of week
    if day == 'all':
        print("The most common day is: {}".format(str(df['day_of_week'].mode().values[0])))
    else:
        print("Common day is not available since a specific day was selected")


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is: {}".format(str(df['hour'].mode().values[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station= df['Start Station'].value_counts().head(1)
    print('The most common starting station is: {}'.format(start_station.to_string()))

    # TO DO: display most commonly used end station
    end_station= df['End Station'].value_counts().head(1)
    print('The most common ending station is: {}'.format(end_station.to_string()))

    # TO DO: display most frequent combination of start station and end station trip
    combo=df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).head(1)
    print('The most common station combination is: \n {}.'.format(combo.to_string()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    df['Difference'] = df['End Time'] - df['Start Time']
    print('The total travel time is: {}'.format(df['Difference'].sum()))

    # TO DO: display mean travel time
    travel_time_mean = df['Difference'].mean()
    print('The mean travel time is: {}'.format(travel_time_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types=df['User Type'].value_counts()
    print('The user types are \n{}\n'.format(user_types.to_string()))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:

        genders=df['Gender'].value_counts()
        print('The gender count is \n{}\n'.format(genders.to_string()))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:

        earliest= df['Birth Year'].min()
        print('The earliest birth year is {0:g}\n'.format(earliest))


        most_recent= df['Birth Year'].max()
        print('The most recent birth year is {0:g}\n'.format(most_recent))


        most_common= df['Birth Year'].mode().values[0]
        print('The most common birth year is {}\n'.format(int(most_common)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes':
        if view_data == 'yes':
            print(df.iloc[start_loc: start_loc + 5])
            start_loc += 5
            view_data = input('Do you wish to continue? Enter yes or no\n').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
