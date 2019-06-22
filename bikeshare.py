import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAY_OF_WEEK = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']


def get_city(prompt):
    """
       Asks user to specify a city to analyze data
       Args:
           (str) prompt - user input for the city to analyze
       Returns:
           (str) value - name of the city to analyze
    """
    while True:
        try:
            value = input(prompt).lower()
        except (ValueError, KeyboardInterrupt):
            print("Sorry, I didn't understand that.")
            continue

        if value not in CITY_DATA:
            print("Sorry, your response is invalid, try again...")
            continue
        else:
            break
    return value


def get_month(prompt):
    """
       Asks user to specify month filter data.

       get_month() method
       Args:
           (str) prompt - user input for the month to filter
       Returns:
           (str) value - name of the month to filter by, or "all" to apply no month filter
    """
    while True:
        try:
            value = input(prompt).lower()
        except (ValueError, KeyboardInterrupt):
            print("Sorry, I didn't understand that.")
            continue

        if value not in MONTHS:
            print("Sorry, your response is invalid, try again...")
            continue
        else:
            break
    return value


def get_day(prompt):
    """
       Asks user to specify a day filter data.
       Args:
           (str) prompt - user input for day of week to filter
       Returns:
           (str) value - name of the day of week to filter by, or "all" to apply no day filter
    """
    while True:
        try:
            value = input(prompt).lower()
        except (ValueError, KeyboardInterrupt):
            print("Sorry, I didn't understand that.")
            continue

        if value not in DAY_OF_WEEK:
            print("Sorry, your response is invalid, try again...")
            continue
        else:
            break
    return value


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

    # converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    using mode()[0] takes the first return mode value each time
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]

    print('Most Popular Day of Week:', popular_dow)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]

    print('Start Station:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]

    print('End Station:', popular_end)

    # display most frequent combination of start station and end station trip
    trip = (df['Start Station'] + ' - ' + df['End Station'])
    popular_trip = trip.mode()[0]

    print('Trip (Start - End):', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('Total trip duration:', total_travel_time)

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()

    print('Average trip duration:', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating user statistics...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print('Breakdown of users\n')
    print(user_types)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()

        print('\nBreakdown of gender\n')
        print(gender)
    except KeyError:
        print('Oops! Gender is not available in this city...\n')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_dob = df['Birth Year'].min()
        most_recent_dob = df['Birth Year'].max()
        most_popular_dob = df['Birth Year'].mode()[0]

        print('\nBreakdown of Year of Birth\n')
        print('Most Popular year: {}'.format(most_popular_dob))
        print('Oldest year: {}'.format(earliest_dob))
        print('Youngest year: {}'.format(most_recent_dob))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
    except KeyError:
        print('Oops! Birth Year is not available in this city...\n')
    print('-' * 40)


def user_individual_data(city):
    """Display 5 rows of individual trip"""
    while True:
    	try:
    		df = pd.read_csv(CITY_DATA[city])
    		show_individual_data = input('\nWould you like to view 5 rows of individual trip?\nEnter yes or no.\n')
    		if show_individual_data.lower() == 'yes':
    			view_5_rows = df.head()
    			five_rows = view_5_rows.to_dict('records')
    			for row in five_rows:
    				print(row)
    			continue
    		elif show_individual_data.lower() == 'no':
    			break
    	except (ValueError, KeyboardInterrupt):
    		print("Sorry, your response is invalid, try again...")



def main():
    while True:

        # get user input for city (chicago, new york city, washington).
        print('Would you like to analyze data for Chicago, New York City, or Washington?')
        city = get_city("Please enter the city: ")
        print('-' * 40)

        # get user input for month (all, january, february, ... , june)
        print('\nWhich month would like to filter data for?')
        print('January, February, March, April, May, June or "all" to apply no month filter')
        month = get_month("Please enter the month: ")
        print('-' * 40)

        # get user input for day of week (all, monday, tuesday, ... sunday)
        print('\nWhich day would you like to filter data for?')
        print('Monday, Tuesday, Wednesday, Thursday, Friday, Saturday Sunday or "all" to apply no day filter')
        day = get_day("Please enter the day: ")
        print('-' * 40)

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        user_individual_data(city)
        try:
            restart = input('\nWould you like to restart?\nEnter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except (ValueError, KeyboardInterrupt):
            print("Sorry, your response is invalid, try again...")

if __name__ == "__main__":
    main()
