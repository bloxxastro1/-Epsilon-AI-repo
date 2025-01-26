import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

def load_data():
    df = pd.read_csv("movies.csv")
    df.drop(columns=['Gross', 'ONE-LINE', 'VOTES'], inplace=True, errors='ignore')
    df.drop_duplicates(inplace=True)
    df.dropna(subset=['MOVIES'], inplace=True)
    
    # Clean and preprocess
    df['STARS'] = df['STARS'].astype(str).apply(lambda x: x.replace("\n", ""))
    df['Director'] = df['STARS'].str.extract(r'Director:([\w\s]+)\|')
    df['Director'].fillna(df['Director'].mode()[0], inplace=True)
    return df

df = load_data()

st.title("Movies Dataset Analysis")

# Show dataset
if st.checkbox("Show raw data"):
    st.write(df.head())

# Display dataset information
st.subheader("Dataset Info")
st.write(df.describe())

# Visualization
st.subheader("Director Distribution")
fig, ax = plt.subplots()
df['Director'].value_counts().head(10).plot(kind='bar', ax=ax)
st.pyplot(fig)

# Filtering option
director = st.selectbox("Select a Director", df['Director'].unique())
filtered_data = df[df['Director'] == director]
st.write(filtered_data)
