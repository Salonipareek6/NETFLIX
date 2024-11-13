# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
st.title("Data Analysis and Visualization App")

# Upload CSV file
uploaded_file = st.file_uploader("data.csv", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("### Data Preview", data.head())
    
    # Data Info
    st.write("### Data Info")
    buffer = data.info(buf=None)
    st.text(buffer)

    # Unique release years
    unique_release_years = sorted(data['releaseYear'].unique())
    st.write("### Unique Release Years", unique_release_years)
    
    # Release Year Distribution
    st.write("### Distribution of Release Years")
    plt.figure(figsize=(20, 8))
    sns.countplot(x='releaseYear', data=data)
    plt.title('Distribution of Release Years')
    plt.xlabel('Release Year')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=90, ha='right')
    st.pyplot(plt.gcf())
    
    # Unique Genres
    data['genres'] = data['genres'].astype(str).str.strip().str.lower()
    unique_genres = sorted(data['genres'].unique())
    st.write("### Unique Genres", unique_genres)
    
    # Genre Distribution
    genre_counts = {}
    for genres in data['genres']:
        for genre in genres.split(','):
            genre = genre.strip()
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    genre_df = pd.DataFrame({'Genre': list(genre_counts.keys()), 'Count': list(genre_counts.values())})
    genre_df = genre_df.sort_values('Count', ascending=False)
    st.write("### Distribution of Genres")
    plt.figure(figsize=(20, 10))
    sns.barplot(x='Genre', y='Count', data=genre_df, palette='viridis')
    plt.xticks(rotation=90, ha='right')
    st.pyplot(plt.gcf())

    # Top 10 Genres Pie Chart
    st.write("### Top 10 Genres")
    top_10_genres = genre_df.head(10)
    plt.figure(figsize=(5, 5))
    plt.pie(top_10_genres['Count'], labels=top_10_genres['Genre'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
    st.pyplot(plt.gcf())

    # Genre Rating Analysis
    genre_ratings = data.groupby('genres')['imdbAverageRating'].agg(['mean', 'max', 'min'])
    max_avg_rating_genre = genre_ratings['mean'].idxmax()
    max_avg_rating = genre_ratings['mean'].max()
    min_avg_rating_genre = genre_ratings['mean'].idxmin()
    min_avg_rating = genre_ratings['mean'].min()

    st.write(f"**Genre with the maximum average IMDb rating:** {max_avg_rating_genre} ({max_avg_rating:.2f})")
    st.write(f"**Genre with the minimum average IMDb rating:** {min_avg_rating_genre} ({min_avg_rating:.2f})")

    # Type Analysis
    type_counts = data['type'].value_counts()
    st.write("### Most Watched Type")
    st.write(f"The most watched type is: {type_counts.idxmax()}")

    # Average IMDb Rating by Type
    type_ratings = data.groupby('type')['imdbAverageRating'].mean()
    st.write("### Average IMDb Rating by Type")
    plt.figure(figsize=(4, 4))
    colors = ['blue' if rating >= type_ratings.mean() else 'cyan' for rating in type_ratings]
    plt.pie(type_ratings, labels=type_ratings.index, autopct='%1.1f%%', startangle=90, colors=colors)
    st.pyplot(plt.gcf())

    # Unique URLs Count
    unique_url_count = data['url'].nunique()
    st.write(f"**Total unique URLs in the 'url' column:** {unique_url_count}")

    # Replace NaN values in IMDb Ratings
    data['imdbAverageRating'].fillna(0, inplace=True)
    sorted_data = data.sort_values('imdbAverageRating', ascending=False)
    st.write("### Top Movies by IMDb Rating", sorted_data[['title', 'imdbAverageRating']])
