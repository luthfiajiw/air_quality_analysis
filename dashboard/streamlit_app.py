import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_number

sns.set(style='dark')

def create_monthly_df(df: pd.DataFrame) -> pd.DataFrame:
  monthly_df = df.resample(rule="M", on="date",).agg({
    'date': 'max',
    'count': 'sum'
  })
  
  return monthly_df

def create_seasonal_df(df: pd.DataFrame) -> pd.DataFrame:
  seasonal_grouped = df.groupby(by='season', as_index=False).agg({
    'count': 'sum'
  })
  
  return seasonal_grouped

def create_casual_workingday_df(df: pd.DataFrame) -> pd.DataFrame:
  casual_workingday_grouped = df.groupby(by='workingday', as_index=False).agg({
    'casual': 'sum',
  }).sort_values(by="casual", ascending=False)
  
  return casual_workingday_grouped

def create_registered_workingday_df(df: pd.DataFrame) -> pd.DataFrame:
  registered_workingday_grouped = df.groupby(by='workingday', as_index=False).agg({
    'registered': 'sum',
  }).sort_values(by="registered", ascending=False)
  
  return registered_workingday_grouped

def create_casual_holiday_df(df: pd.DataFrame) -> pd.DataFrame:
  casual_holiday_grouped = df.groupby(by='holiday', as_index=False).agg({
    'casual': 'sum',
  }).sort_values(by="casual", ascending=False)
  
  return casual_holiday_grouped

def create_registered_holiday_df(df: pd.DataFrame) -> pd.DataFrame:
  registered_holiday_grouped = df.groupby(by='holiday', as_index=False).agg({
    'registered': 'sum',
  }).sort_values(by="registered", ascending=False)
  
  return registered_holiday_grouped

# LOAD PROCESSED DATA
processed_df = pd.read_csv("../dashboard/processed_data.csv")
processed_df["date"] = pd.to_datetime(processed_df["date"])

st.header(':man-biking: Bike Sharing Dashboard')
# SEASONAL RENTALS
seasonal_df = create_seasonal_df(processed_df)
st.subheader('Seasonal Rentals')

col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric("Spring", value=format_number(seasonal_df.iloc[1, 1], locale='en'))
with col2:
  st.metric("Summer", value=format_number(seasonal_df.iloc[2, 1], locale='en'))
with col3:
  st.metric("Fall", value=format_number(seasonal_df.iloc[0, 1], locale='en'))
with col4:
  st.metric("Winter", value=format_number(seasonal_df.iloc[3, 1], locale='en'))
  
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(data=seasonal_df, x="season", y="count", palette=colors)
ax.set_title("Number of Bikes Rented", fontsize=20)
ax.set_ylabel(None)
ax.set_xlabel("Season", fontsize=16)

st.pyplot(fig)

# RENTAL TIME PREFERENCES
casual_workingday_df = create_casual_workingday_df(processed_df)
registered_workingday_df = create_registered_workingday_df(processed_df)

st.subheader("Rental Time Preferences")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3"]

ax[0].set_title("Bikes Rented by Casual Users", fontsize=20)
ax[0].pie(
  x=casual_workingday_df["casual"],
  labels=casual_workingday_df["workingday"],
  autopct='%1.1f%%',
  colors=colors,
  startangle=180,
  textprops={'fontsize': 16}
)

ax[1].set_title("Bikes Rented by Registered Users", fontsize=20)
ax[1].pie(
  x=registered_workingday_df["registered"],
  labels=registered_workingday_df["workingday"],
  autopct='%1.1f%%',
  colors=colors,
  startangle=135,
  textprops={'fontsize': 16}
)

st.pyplot(fig)

# HOLIDAY
casual_holiday_df = create_casual_holiday_df(processed_df)
registered_holiday_df = create_registered_holiday_df(processed_df)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3"]

ax[0].set_title("Bikes Rented by Casual Users", fontsize=20)
ax[0].pie(
  x=casual_holiday_df["casual"],
  labels=casual_holiday_df["holiday"],
  autopct='%1.1f%%',
  colors=colors,
  startangle=90,
  textprops={'fontsize': 16}
)

ax[1].set_title("Bikes Rented by Registered Users", fontsize=20)
ax[1].pie(
  x=registered_holiday_df["registered"],
  labels=registered_holiday_df["holiday"],
  autopct='%1.1f%%',
  colors=colors,
  startangle=90,
  textprops={'fontsize': 16}
)

st.pyplot(fig)

# BIKE RENTAL TRENDS
monthly_df = create_monthly_df(processed_df)
st.subheader("Bike Rental Trends (2011-2012)")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(
  monthly_df["date"],
  monthly_df["count"],
  color=colors[0],
  marker='o'
)
ax.set_title("Bike Rental Trends (2011-2012)")

st.pyplot(fig)
