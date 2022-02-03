import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

day_list = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Initialization
    city = ''
    month = ''
    day = ''

    print('Hello! Let\'s explore some US bikeshare data!')
     
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA.keys():
        city = str(input("Enter a city (chicago, new york city, washington): ")).lower()

    # get user input for month (all, january, february, ... , june)
    while month not in month_list:
        month = str(input("Enter a month (all, january, february, ... , june): ")).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in day_list:
        day = str(input("Enter a day (all, monday, tuesday, ..., sunday): ")).lower()

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
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from the Start Time column to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    # filter by month if applicable
    if month != month_list[0]:
        # use the index of the months list to get the corresponding int
        month = month_list.index(month)
        # filter by month to create the new dataframe
        df = df[df.month == month]
    
    # filter by day of week if applicable
    if day != day_list[0]:
        # filter by day of week to create the new dataframe
        day = day_list.index(day) - 1
        df = df[df.day_of_week == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = int(df.mode()['month'][0])
    count_month = np.count_nonzero(df['month'].values == popular_month)
    total_count = df.shape[0]
    popular_month = month_list[popular_month]
    print('\nMost Frequent month: {} - {} hits - {:.2f}% of total'.format(popular_month, count_month, count_month/total_count*100))

    # display the most common day of week
    popular_day_of_week = int(df.mode()['day_of_week'][0])
    count_weekday = np.count_nonzero(df['day_of_week'].values == popular_day_of_week)
    popular_day_of_week = day_list[popular_day_of_week+1]
    print('\nMost Frequent day of week: {} - {} hits - {:.2f}% of total'.format(popular_day_of_week, count_weekday, count_weekday/total_count*100))

    # display the most common start hour
    df['Start hour'] = df['Start Time'].dt.hour
    popular_hour = df.mode()['Start hour'][0]
    count_hour = np.count_nonzero(df['Start hour'].values == popular_hour)
    print('\nMost Frequent Start Hour: {}h - {} hits - {:.2f}% of total'.format(int(popular_hour), count_hour, count_hour/total_count*100))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df.mode()['Start Station'][0]
    print('\nMost Frequent Start Station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df.mode()['End Station'][0]
    print('\nMost Frequent End Station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start to End trip'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = df.mode()['Start to End trip'][0]
    print('\nMost Frequent trip (start - end station): ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_travel_hours = df['Trip Duration'].sum()
    print('\nTotal travel time for the filters chosen was {:.2f} hours, or {:.2f} full days (24h), or {:.2f} full weeks.'
          .format(Total_travel_hours, Total_travel_hours/24, Total_travel_hours/24/7))

    # display mean travel time
    Mean_travel_hours = df['Trip Duration'].mean()
    print('\nMean travel time for the filters chosen was {:.2f} hours, or {:.2f} full days (24h).'
           .format(Mean_travel_hours, Mean_travel_hours/24))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    total_count = df.shape[0]
    print('\nHere is a breakdown of the data based on user type: ')
    for i in range(0,user_types.size):
        print('{}: {} - {:.2f}% of total'.format(user_types.index[i], user_types.values[i], user_types.values[i]/total_count*100))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        print('\nHere is a breakdown of the data base on gender type: ')
        for i in range(0,gender_types.size):
            print('{}: {} - {:.2f}% of total'.format(gender_types.index[i], gender_types.values[i], gender_types.values[i]/total_count*100))
        print('{} datapoints (or {:.2f}%) are missing gender data'.format(df['Gender'].isnull().sum().sum(), df['Gender'].isnull().sum().sum()/total_count*100))
    else: print('\nNo gender statistics available for this city')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        count_birth_year = np.count_nonzero(df['Birth Year'].values == df.mode()['Birth Year'][0])
        print('\nOldest person for the filters chosen is from {}, youngest from {} and most common birth year is {} ({} hits)'
              .format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df.mode()['Birth Year'][0]), count_birth_year))    
    else: print('\nNo birth date statistics available for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_input(df):
    """
    Asks user if raw data needs to be displayed, 
    if so the number of hits per time is asked. 
    """
    size = 0
    answer = input('\nWould you like to see some raw data? Type yes if yes, anything else if no. ')
    if answer.lower() == 'yes':
        while size == 0:
            try: 
                size = int(input('\nType the nummber of hits you would like to see at once: '))
            except:
                print('\nThe input was not an integer, please try again')
                size = 0
        #drop columns that were created for analysis, but not necessary in display
        df.drop(['month','day_of_week', 'Start hour', 'Start to End trip'], axis = 1, inplace = True)
        for chunk in chunk_raw_input(df, size):
            for i in chunk.index:
                for j in chunk.columns:
                    print('\n{}: {} '.format(j,chunk[j][i]))
                print('-'*40)
    
def chunk_raw_input(df, size):
    """
    Divide the dataframe into chunks of a given size
    Ask user if more data needs to be displayed 
    and double check if the answer is not yes.
    """
    answer = True  #aks the question at least once
    i = 0
    #end when answer is not yes or when last data is displayed
    while answer and i < df.shape[0]:
        yield df.iloc[i:i+size,1:] #output
        check = input('\nDo you want to continue (if any data left): type yes if yes, anything else if no. ')
        if check.lower() != 'yes':
            double_check = input('\nSure you want to quit? Type no if you changed your mind, anything else if you really want to quit. ')
            if double_check.lower() != 'no':
                answer = False
            else: i = i + size

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_input(df)
        restart = input('\nWould you like to restart? Enter yes or anything else for no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

