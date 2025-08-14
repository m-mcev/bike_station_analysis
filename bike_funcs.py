from pandas import DataFrame as df
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

plt.rcParams['font.family'] = ['Computer Modern Sans Serif','sans-serif']

def hour_breakdown(x, data):

    starts = data[data['Start station number'] == x]
    ends = data[data['End station number'] == x]
    count_starts = starts.groupby(['day','hour']).size().reset_index(name = 'count')
    count_ends = ends.groupby(['day','hour']).size().reset_index(name = 'count')
    avg_starts = count_starts.groupby('hour')['count'].mean()
    avg_ends = count_ends.groupby('hour')['count'].mean()
    all_hours = pd.Series(range(24), name = 'hour')
    avg_starts = avg_starts.reindex(all_hours, fill_value = 0)
    avg_ends = avg_ends.reindex(all_hours, fill_value = 0)

    averages = df()
    averages['starts'] = avg_starts
    averages['ends'] = avg_ends
    averages['difference'] = averages['ends'] - averages['starts']

    xlen = 24
    xloc = np.arange(xlen)
    fig = plt.figure(figsize = (8,5))
    width = .3
    colors = ['ForestGreen' if val >0 else 'FireBrick' for val in averages['difference']]
    plt.bar(xloc, averages['difference'], width, label = 'Pick-ups', color = colors)
    #plt.bar(xloc+width, averages['ends'], width, label = 'Drop-offs', color = 'green')

    title = f"Average Hourly Net Gain or Loss for Station {x}"
    plt.xlabel('Hour of Day')
    plt.ylabel('Gain or Loss')
    plt.title(title)
    plt.xticks(xloc + width/2, ('12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM',
                               '12PM','1PM','2PM','3PM','4PM','5PM','6PM','7PM','8PM','9PM','10PM','11PM'), rotation=90)
    plt.grid(True, axis = 'y')
    #plt.legend()
    #plt.show()

    return fig, averages

def plot_hourly(x, sta_avg_data):
    xlen = 24
    xloc = np.arange(xlen)
    fig = plt.figure(figsize = (8,5))
    width = .3

    plt.bar(xloc, sta_avg_data['starts'], width, label = 'Average Trip Starts', color = 'royalblue')
    plt.bar(xloc+width, sta_avg_data['ends'], width, label = 'Average Trip Ends', color = 'lightskyblue')
    title = f"Average Hourly Activity for Station {x}"
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Bike Activity')
    plt.title(title)
    plt.xticks(xloc + width/2, ('12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM',
                               '12PM','1PM','2PM','3PM','4PM','5PM','6PM','7PM','8PM','9PM','10PM','11PM'), rotation=90)
    plt.grid(True, axis = 'y')
    plt.legend()
    return fig

def sta_destinations(sta, data, station_geo):
    sta_rides = data[data['Start station number'] == sta]
    sta_lat = station_geo[station_geo['BIKE_ID']==sta]['LATITUDE']
    sta_long = station_geo[station_geo['BIKE_ID']==sta]['LONGITUDE']
    sta_name = station_geo[station_geo['BIKE_ID']==sta]['FAC_NAME'].values[0]
    station_origin = {'Station number': sta, 'Latitude':sta_lat, 'Longitude':sta_long, 'size':4000}
    origin = df(station_origin)
    stations_new = sta_rides['End station number'].value_counts().reset_index()
    stations_new.columns = ['Station','count']
    full_stations = stations_new.merge(station_geo, left_on = 'Station',right_on = 'BIKE_ID', how = 'left')
    full_stations.dropna(axis = 0, inplace = True)
    full_stations['Station type'] = full_stations['Station'].apply(
        lambda x: 'Origin' if x == sta else 'Destination'
        )

    title = f"Ride Destinations from Station #{sta} ({sta_name})"
    colors = {'Origin':'red', 'Destination':'lightblue'}
    fig = px.scatter_mapbox(
    full_stations,
    lat = full_stations['LATITUDE'],
    lon = full_stations['LONGITUDE'],
    size = abs(full_stations['count']),
    color = full_stations['Station type'],
    color_discrete_map = colors,
    mapbox_style = 'carto-positron',
    hover_name = full_stations['Station'],
    height = 800,
    width = 1000,
    zoom = 12,
    title = title
        )


    return fig

def member_breakdown(x, data1):
    data = data1[data1['Start station number'] == x]
    Members = data[data['Member type'] =='Member']
    Casuals = data[data['Member type'] == 'Casual']
    all_hours = pd.Series(range(24), name = 'hour')
    total_mem =  Members.groupby('hour').size().reindex(all_hours, fill_value = 0)/5/365
    total_cas = Casuals.groupby('hour').size().reindex(all_hours, fill_value = 0)/5/365

    xlen = 24
    xloc = np.arange(xlen)
    fig = plt.figure(figsize = (8,5))
    width = .3

    plt.bar(xloc, total_mem, width, label = 'Member', color = 'royalblue')
    plt.bar(xloc+width, total_cas, width, label = 'Casual', color = 'lightskyblue')

    #print(total_mem, total_cas)
    title = "Member and Casual Rider Hourly Summary"
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Rides')
    plt.title(title)
    plt.xticks(xloc + width/2, ('12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM',
                               '12PM','1PM','2PM','3PM','4PM','5PM','6PM','7PM','8PM','9PM','10PM','11PM'), rotation=90)
    plt.grid(True, axis = 'y')
    plt.legend()
    return fig

def make_pie_chart(sta, data):
    data1 = data[data['Start station number']==sta]
    data2 = data1[(data1['Member type'] == 'Member') | (data1['Member type']=='Casual')]
    member_numbers = data2['Member type'].value_counts(normalize = True).reset_index()
    member_numbers.columns = ['Rider type', 'percent']
    colors = {'Member': 'royalblue', 'Casual': 'lightskyblue'}
    fig = px.pie(data_frame = member_numbers,
                    names = 'Rider type',
                    values = 'percent',
                    title = 'Rider Type Breakdown',
                    hole = .5,
                    width = 400,
                    height = 400,
                    color = 'Rider type',
                    color_discrete_map = colors)
    return fig
