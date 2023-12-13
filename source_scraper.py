'''
ver 1.3 9/12/23
'''
import pandas as pd
from datetime import timedelta
from datetime import datetime as dt

class K_statistics():
    def __init__(self):
        pass

    # ---------This sub seperate the time duration of the rides to seperate weeks DF-----------#
    def weekly_rides_seperator_DF(self, df, conf):
        weekly_rides = pd.DataFrame(columns=['Date', 'Distance', 'Duration', 'Count'])
        DAYS = timedelta(7)  # week
        Day = timedelta(1)  # one day
        if conf[5]: # start on certain date
            week_start_date = pd.to_datetime(conf[0])
        elif conf[3]: # from day one
            week_start_date = df['Date'].min()
        else: # conf 4 - from the beginning of the year
            week_start_date =  dt.strptime(f"01/01/{dt.now().year}", '%d/%m/%Y')



        # ------chose the first comming Sunday ----------#
        while week_start_date.weekday() != 6:
            week_start_date -= Day
        last_date = df['Date'].max()
        while week_start_date <= last_date:
            weekly_activities = df[(df['Date'] >= week_start_date) & (df['Date'] < (week_start_date + DAYS))]

            weekly_rides = weekly_rides.append(
                {'Date': week_start_date, 'Distance': weekly_activities.Distance.sum(),
                 'Duration': weekly_activities.Duration.sum(), 'Count': weekly_activities.Distance.count()},
                ignore_index=True)

            week_start_date += DAYS

        return weekly_rides

    # ---------This sub initiate the time duration of the rides from a start date DF-----------#
    def detailed_rides_from_date_DF(self, df, conf):
        detailed_rides = pd.DataFrame(columns=['Date', 'Distance', 'Duration', 'Count'])
        Day = timedelta(1)

        if conf[5]:  # start on certain date
            start_date = pd.to_datetime(conf[0])
        elif conf[3]:  # from day one
            start_date = df['Date'].min()
        else:  # conf 4 - from the beginning of the year
            start_date = dt.strptime(f"01/01/{dt.now().year}", '%d/%m/%Y')
        last_date = df['Date'].max()
        while start_date <= last_date:
            daily_activitis = df[df['Date'] == start_date]

            activitis_to_add = pd.DataFrame({'Date': daily_activitis['Date'], 'Distance': daily_activitis['Distance'],'Duration': daily_activitis['Duration'], 'Count': 1})
            detailed_rides = detailed_rides.append(activitis_to_add, ignore_index=True)

            start_date += Day
        return detailed_rides





