import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

day_df = pd.read_csv('day_df.csv')
hour_df = pd.read_csv('hour_df.csv')

st.sidebar.header('Filter Data')
min_date_day = day_df['dteday'].min() 
max_date_day = day_df['dteday'].max() 

min_date_hour = hour_df['dteday'].min()
max_date_hour = hour_df['dteday'].max()

date_range = st.sidebar.date_input(
    label='Pilih Rentang Tanggal',
    min_value=min_date_day,
    max_value=max_date_day,
    value=[min_date_day, max_date_day]
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date_day, max_date_day

season_options = st.sidebar.multiselect(
    label = 'Pilih Musim',
    options = day_df['season_label'].unique(),
    default=day_df['season_label'].unique()
)

day_filtered = day_df[
    (day_df['dteday'] >= str(start_date)) & 
    (day_df['dteday'] <= str(end_date)) &
    (day_df['season_label'].isin(season_options))
]

hour_filtered = hour_df[
    (hour_df['dteday'] >= str(start_date)) & 
    (hour_df['dteday'] <= str(end_date)) &
    (hour_df['season_label'].isin(season_options))
]

st.title('Dasboard Analisis Data')
st.markdown('Bike Sharing Dataset')

col1, col2, col3 = st.columns(3)
col1.metric(label='Total Peminjaman', value=day_filtered['cnt'].sum())
col2.metric(label='Rata-rata Peminjaman', value=day_filtered['cnt'].mean())
col3.metric(label='Total Hari', value=len(day_filtered))

st.markdown('---')

#1
st.header('Pengaruh Cuaca terhadap Peminjaman Sepeda')

col1, col2 = st.columns(2)
with col1 :
    weather_agg = day_filtered.groupby(by='weathersit_label')['cnt'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=weather_agg.index, y=weather_agg.values, palette='Blues_r')
    ax.set_title('Rata-rata Peminjaman Sepeda per Kategori Cuaca')
    ax.set_xlabel('Kategori Cuaca')
    ax.set_ylabel('Rata-rata Peminjaman Sepeda')
    st.pyplot(fig)
    
with col2 :
    fig,ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x='temp', y='cnt', data=day_filtered, hue='weathersit_label', palette='Blues_r')
    ax.set_title('Hubungan Temperatur terhadap Peminjaman Sepeda')
    ax.set_xlabel('Temperatur')
    ax.set_ylabel('Peminjaman Sepeda')
    st.pyplot(fig)

st.markdown('---')

#2
st.header('Jumlah Peminjaman Sepeda per Jam Hari Kerja dan Akhir Pekan')

hourly_pattern = (
    hour_filtered.groupby(['hr','workingday'])['cnt'].mean().unstack()
    .reindex(index=range(24), columns=[0, 1], fill_value=0)
)
hourly_pattern.columns = ['Non-Workingday','Workingday']

fig, ax = plt.subplots(figsize=(10, 5))
plt.plot(hourly_pattern.index, hourly_pattern['Non-Workingday'], marker='o', label='Non-Workingday')
plt.plot(hourly_pattern.index, hourly_pattern['Workingday'], marker='o', label='Workingday')
ax.set_title('Rata-rata Peminjaman Sepeda per Jam pada Hari Kerja dan Libur')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Peminjaman Sepeda')
ax.legend()
ax.set_xticks(range(0,24))
ax.grid()
st.pyplot(fig)

st.markdown('---')

st.header('Analisis Lanjutan')

tab1, tab2 = st.tabs(["Sensitivitas terhadap Cuaca", "Pola Jam Casual vs Registered"])

with tab1:
    weather_user = day_filtered.groupby("weathersit_label")[["casual", "registered"]].mean()
    st.dataframe(weather_user)
    fig, ax = plt.subplots(figsize=(7, 4))
    weather_user.plot(kind="bar", ax=ax)
    ax.set_title("Rata-rata Casual vs Registered per Kategori Cuaca")
    ax.set_ylabel("Rata-rata jumlah peminjaman")
    plt.xticks(rotation=15)
    st.pyplot(fig)
    
with tab2:
    day_type = st.radio("Pilih tipe hari:", ["Workingday", "Non-Workingday"], horizontal=True)
    casual_pattern = (
        hour_filtered.groupby(["hr", "workingday"])["casual"].mean().unstack()
        .reindex(index=range(24), columns=[0, 1], fill_value=0)
    )
    casual_pattern.columns = ["Non-Workingday", "Workingday"]

    registered_pattern = (
        hour_filtered.groupby(["hr", "workingday"])["registered"].mean().unstack()
        .reindex(index=range(24), columns=[0, 1], fill_value=0)
    )
    registered_pattern.columns = ["Non-Workingday", "Workingday"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(casual_pattern.index, casual_pattern[day_type], marker="o", label=f"Casual - {day_type}")
    ax.plot(registered_pattern.index, registered_pattern[day_type], marker="o", label=f"Registered - {day_type}")
    ax.set_title(f"Pola Jam Casual vs Registered ({day_type})")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata jumlah peminjaman")
    ax.set_xticks(range(0, 24))
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)