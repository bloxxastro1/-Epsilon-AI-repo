import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re  # Import regex module

# Load Data Function
def load_data():
    df = pd.read_csv("movies.csv")  # Load CSV file into df
    df.drop(columns=['Gross', 'ONE-LINE', 'VOTES'], inplace=True, errors='ignore')
    df.drop_duplicates(inplace=True)
    df.dropna(subset=['MOVIES'], inplace=True)
    return df  # Return the DataFrame

# **Genre Cleaning Function**
def clean_genre(genre):
    if isinstance(genre, str):  # Ensure the value is a string
        genre = genre.strip().replace("\n", "").replace("$$", "")
        return genre.split(",")[0]  # Return the first genre
    return genre  # Return unchanged if not a string

# **Year Cleaning Function**
def clean_year(year):
    if pd.isna(year):  # Handle NaN values
        return None  

    year = str(year).strip()  # Convert to string and strip spaces
    year = re.sub(r'[^0-9]', '', year)  # Remove non-numeric characters

    if year.isdigit() and len(year) >= 4:
        return int(year[:4])  # Convert first 4 digits to integer
    
    return None  # Return None for invalid values

# Load Data
df = load_data()

# Apply genre and year cleaning functions
df["GENRE"] = df["GENRE"].apply(clean_genre)
df["YEAR"] = df["YEAR"].apply(clean_year)

# Clean 'STARS' column
df['STARS'] = df['STARS'].astype(str).apply(lambda x: x.replace("\n", ""))

# Extract Director's name
df['Director'] = df['STARS'].str.extract(r'Director:\s*([\w\s]+)\|')

# Fill missing directors with the most common one
df['Director'].fillna(df['Director'].mode()[0], inplace=True)

# Convert RunTime to hours
df["RunTime"] = df["RunTime"] / 60

# Streamlit UI
st.title("Movies Dataset Analysis")

# Show dataset
if st.checkbox("Show raw data"):
    st.write(df.head())

# Display dataset information
st.subheader("Dataset Info")
st.write(df.describe())

# Visualization - Director Distribution
st.subheader("Top 10 Directors with Most Movies")
fig, ax = plt.subplots()
df['Director'].value_counts().head(10).plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
ax.set_xlabel("Director")
ax.set_ylabel("Number of Movies")
st.pyplot(fig)

# Filtering Option
director = st.selectbox("Select a Director", df['Director'].dropna().unique())
filtered_data = df[df['Director'] == director]
st.write(filtered_data)

# **Histograms**
st.subheader("Histograms")

# **Year Histogram**
fig, ax = plt.subplots()
df.dropna(subset=['YEAR'], inplace=True)  # Drop missing years before plotting
df['YEAR'].hist(bins=20, color='skyblue', edgecolor='black', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Frequency")
ax.set_title("Movie Release Year Distribution")
st.pyplot(fig)

# **Rating Histogram**
fig, ax = plt.subplots()
df['RATING'].hist(bins=20, color='skyblue', edgecolor='black', ax=ax)
ax.set_xlabel("Rating")
ax.set_ylabel("Frequency")
ax.set_title("Movie Rating Distribution")
st.pyplot(fig)

# **RunTime Histogram**
fig, ax = plt.subplots()
df['RunTime'].hist(bins=20, color='skyblue', edgecolor='black', ax=ax)
ax.set_xlabel("Runtime (Hours)")
ax.set_ylabel("Frequency")
ax.set_title("Movie Runtime Distribution")
st.pyplot(fig)

# **Genre Distribution (Fixed)**
st.subheader("Genre Distribution")
fig, ax = plt.subplots()
df['GENRE'].value_counts().head(10).plot(kind='bar', ax=ax, color='lightcoral', edgecolor='black')
ax.set_xlabel("Genre")
ax.set_ylabel("Number of Movies")
ax.set_title("Top 10 Most Frequent Movie Genres")
st.pyplot(fig)
