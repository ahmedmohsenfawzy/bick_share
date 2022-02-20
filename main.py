import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

filter_fwd = ''


def get_filters():
    global filter_fwd
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        print("would you like to see data for Chicago, new york city, or Washington?")
        city = input().lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("try again")

    while True:

        print("Would you like to filter the data by month, day, both, or not at all? type \"none\" for no time filter ")
        dis = input().lower()
        if dis == 'both':
            print("which month? January, February, March April, May, or June")
            month = input().lower()
            print("Which day? Please type your response as an integer (e.g., 0=Monday, 6=Sunday)")
            try:
                day = int(input())
            except ValueError:
                day = "all"
            filter_fwd = "both"
            break
        elif dis == 'month':
            print("which month? January, February, March April, May, or June? Please type out the frill month name")
            month = input().lower()
            day = "all"
            filter_fwd = "month"
            break
        elif dis == "day":
            print("Which day? Please type your response as an integer (e.g., 0=Monday, 6=Sunday)")
            try:
                day = int(input())
            except ValueError:
                day = "all"
            month = "all"
            filter_fwd = "day"
            break
        elif dis == "none":
            month = "all"
            day = "all"
            filter_fwd = "none"
            break
        print("try again")

    if month not in ['january', 'february', 'march', 'april', 'may', 'june', "all"]:
        month = "all"
    if day not in [0, 1, 2, 3, 4, 5, 6, "all"]:
        day = "all"
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df["Start Time"])

    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.weekday
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    global filter_fwd

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df["Start Time"])
    print("what is the most common month?")
    df["month"] = df["Start Time"].dt.month
    popular_month = df["month"].mode()[0]
    count_months = df["month"].count()
    print('Most Frequent Start Month:', popular_month, "count:", count_months, "filter:", filter_fwd)

    print("what is the most common day of week")
    df['day_of_week'] = df["Start Time"].dt.weekday
    popular_day_of_week = df["day_of_week"].mode()[0]
    count_days = df["day_of_week"].count()
    print("Most Frequent Start Day_of_week:", popular_day_of_week, "count:", count_days, "filter:", filter_fwd)

    print("what is the most common hour?")
    df['hour'] = df["Start Time"].dt.hour
    popular_hour = df["hour"].mode()[0]
    count_hours = df["hour"].count()

    print('Most Frequent Start Hour:', popular_hour, "count:", count_hours, "filter:", filter_fwd)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    global filter_fwd

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("what is the most commonly used start station?")
    popular_start_station = df["Start Station"].mode()[0]
    print("most frequent start_station:", popular_start_station, "filter:", filter_fwd)

    print("what is the most commonly used end station?")
    popular_end_station = df["End Station"].mode()[0]
    print("most frequent end_station:", popular_end_station, "filter:", filter_fwd)

    print("what is the most commonly used start station and end station?")
    frequent_stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(frequent_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    global filter_fwd

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_trip = df["Trip Duration"].sum(axis=0)
    print("total travel time:", total_trip)
    print("count:", df["Trip Duration"].count())
    avg_trip = df["Trip Duration"].mean()
    print("mean travel time:", avg_trip)
    print("filter:", filter_fwd)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    global filter_fwd

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    count_user_types = df["User Type"].value_counts().to_frame()
    print("count of user type:", count_user_types)
    try:
        count_of_gender = df["Gender"].value_counts().to_frame()
        print("count of gender:", count_of_gender)
        earliest_year_of_birth = df["Birth Year"].max()
        recent_year_of_birth = df["Birth Year"].min()
        most_common_year_of_birth = df["Birth Year"].mode()[0]
        print("earliest year of birth:", earliest_year_of_birth, ", recent year of birth:", recent_year_of_birth,
              ", most common year of birth:", most_common_year_of_birth)
    except KeyError:
        print("washington don't have Gender or Birth year columns")

    print("filter:", filter_fwd)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display(df):
    print("\ndata users!!!")

    i = 0
    while True:
        user_input = input("would you like to display 5 rows of raw data? , please type [yes or no]\n ").lower()
        if user_input not in ['yes', 'no']:
            print('that\'s invalid choice, pleas type yes or no\n')
            print("try again\n")
        elif user_input in ['yes', 'no']:
            break

    if user_input != 'yes':
        print('thank you')
    else:

        while i + 5 < df.shape[0]:
            print(df.iloc[i:i + 5])
            i += 5

            user_input = input("would you like to display more 5 rows of raw data?if you want type [Yes]\n").lower()
            if user_input != "yes":
                print("thank you")
                break


def main():
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
