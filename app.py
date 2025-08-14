from pandas import DataFrame as df
import pandas as pd
import numpy as np
import random
import plotly.express as px
from collections import Counter
import bike_funcs
from bike_funcs import hour_breakdown, sta_destinations, plot_hourly, member_breakdown, make_pie_chart
import streamlit as st

data = pd.read_csv('novtrips.csv')
geo_data = pd.read_csv('BikeshareLocs2.csv')
stations = data['Start station number'].drop_duplicates().sort_values()
time_opts = ['All','Weekdays','Weekends']

st.set_page_config(page_title = "Bikeshare Station Analysis", layout = 'wide')

st.title('Capital Bikeshare Station Analysis')
col_1, col_2, col_3, col_4 = st.columns(4)

with col_1:
        sta = st.selectbox(
        'Station Number', stations, index = 69
        )
with col_2:
        time = st.selectbox(
        'Filter by Day of Week', time_opts
        )

if st.button("Analyze"):
    sta_name = geo_data[geo_data['BIKE_ID'] == sta ]['FAC_NAME'].iloc[0]
    st.header(f"Analysis of Station {sta} - {sta_name} ({time})")
    st.subheader('Station Ridership Activity')
    if time == "All":
        data=data
    elif time == "Weekdays":
        data = data[data['weekday']<5]
    elif time == "Weekends" :
        data = data[data['weekday']>=5]
    else:
        data=data
    left_column, right_column = st.columns(2)
    with right_column:
        fig1, avgs = hour_breakdown(sta, data)
        st.pyplot(fig1)
    with left_column:
        fig2 = plot_hourly(sta, avgs)
        st.pyplot(fig2)

    st.subheader('Trip Destinations')
    fig4 = sta_destinations(sta, data, geo_data)
    st.plotly_chart(fig4, use_countainer_width = False)

    st.subheader('Ridership by Registration Status')
    left_column, right_column = st.columns(2)

    with left_column:
        fig3 = member_breakdown(sta, data)
        st.pyplot(fig3)
    with right_column:
        fig5 = make_pie_chart(sta, data)
        st.plotly_chart(fig5, use_countainer_width=True)
else:
    st.info("Select a Station Number and click 'Analyze' to begin.")
