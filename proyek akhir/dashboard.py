import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')

data_day = pd.read_csv("../day.csv")
data_h = pd.read_csv("../hour.csv")

data_day['dteday'] = pd.to_datetime(data_day['dteday'])
data_h['dteday'] = pd.to_datetime(data_h['dteday'])

min_date = data_day['dteday'].min()
max_date = data_day['dteday'].max()

def count_user(df):
    items = df.resample(rule='D', on='dteday').agg({
        "instant" : "nunique", 
        "cnt" : "sum"
    })
    items = items.reset_index()
    items.rename(
        columns={
            "instant" : "id",
            "cnt" : "user_count"
        },inplace=True
    )
    return items

def count_registered(df):
    items = df.resample(rule='D', on='dteday').agg({
        "instant" : "nunique", 
        "registered" : "sum"
    })
    items = items.reset_index()
    items.rename(
        columns={
            "instant" : "id",
            "registered" : "user_count"
        },inplace=True
    )
    return items

def count_casual(df):
    items = df.resample(rule='D', on='dteday').agg({
        "instant" : "nunique", 
        "casual" : "sum"
    })
    items = items.reset_index()
    items.rename(
        columns={
            "instant" : "id",
            "casual" : "user_count"
        },inplace=True
    )
    return items

def get_temperature(df):
    items = df.groupby(by="dteday").agg({
        "temp" : "mean"
    })
    return items
def get_windspeed(df):
    items = df.groupby(by="dteday").agg({
        "windspeed" : "mean"
    })
    return items
def get_hum(df):
    items = df.groupby(by="dteday").agg({
        "hum" : "mean"
    })
    return items
def get_atemp(df):
    items = df.groupby(by="dteday").agg({
        "atemp" : "mean"
    })
    return items

def get_user_season(df):
    items = df.sort_values(by="dteday")
    return items

st.header("Dashboard Bike")

with st.sidebar:
    start_date, end_date = st.date_input(
        label="Rentang waktu", 
        min_value=min_date, 
        max_value=max_date, 
        value=[min_date, max_date]
    )
    
    mn_df = data_day[(data_day['dteday'] >= str(start_date)) & 
                 (data_day['dteday'] <= str(end_date))
                 ]
    daily_user = count_user(mn_df)
    daily_registered = count_registered(mn_df)
    daily_casual = count_casual(mn_df)
    daily_temp = get_temperature(mn_df)
    daily_wind = get_windspeed(mn_df)
    daily_hum = get_hum(mn_df)
    daily_atemp = get_atemp(mn_df)
    daily_season = get_user_season(mn_df)
    
st.subheader("Daily User")
col1, col2, col3 = st.columns(3)

with col1:
    total_order = daily_user.user_count.sum()
    st.metric("Total Users", value=total_order)
with col2:
    total_order2 = daily_registered.user_count.sum()
    st.metric("Total Registered Users", value=total_order2)
with col3:
    total_order3 = daily_casual.user_count.sum()
    st.metric("Total Casual Users", value=total_order3)

fig, ax = plt.subplots(figsize=(12,10))
ax.plot(daily_user['dteday'],
         daily_user['user_count'],
         marker="o",
         linewidth=2
         )
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig) 

st.subheader("Environment Condition")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Mean Temperature", value="{:.2f}".format(daily_temp.temp.mean()))   
with col2:
    st.metric("Mean Windspeed", value="{:.2f}".format(daily_wind.windspeed.mean()))   
with col3:
    st.metric("Mean Humidity", value="{:.2f}".format(daily_hum.hum.mean()))   
with col4:
    st.metric("Mean Feeling Temp", value="{:.2f}".format(daily_atemp.atemp.mean()))   

st.subheader("Season")
fig, ax = plt.subplots(figsize=(12,10))
sns.barplot(x="season", y="cnt", data=daily_season, hue="season")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig) 
