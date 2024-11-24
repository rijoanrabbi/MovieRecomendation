import pickle
import streamlit as st
import pandas as pd
import os
import requests

api_key = '660c1c3e094e3c1129d4bef8e25b8d7a'
language = 'en-US'


def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=660c1c3e094e3c1129d4bef8e25b8d7a&language=en-US"
                             .format(movie_id))
    data=response.json()
    return "http://image.tmdb.org/t/p/w500/"+data['poster_path']
def recommend (movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate (distances)), reverse=True, key =lambda x: x[1]) [1:6]
    recommended_movies = []
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

similarity= pickle.load(open('similarity.pkl', 'rb'))
# Ensure file exists and is accessible
file_path = os.path.join(os.getcwd(), 'movie_dict.pkl')  # Build absolute path
if not os.path.exists(file_path):
    st.error("Error: 'movie_dict.pkl' file not found. Please ensure it exists.")
else:
    try:
        # Attempt to load the pickle file
        with open(file_path, 'rb') as f:
            movies_dict = pickle.load(f)

        movies = pd.DataFrame(movies_dict)
        st.title('Movies Recommender System')


        # movies_list = movies['title'].values
        selected_movie_name=st.selectbox(
            'Search you Movie:',
            movies['title'].values )


        if st.button('Show Recommendation'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    st.text(recommended_movie_names[i])
                    st.image(recommended_movie_posters[i])


        # if st.button('Show Recommendation'):
        #     recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
        #     col1, col2, col3, col4, col5 = st.columns(5)
        #     with col1:
        #         st.text(recommended_movie_names[0])
        #         st.image(recommended_movie_posters[0])
        #     with col2:
        #         st.text(recommended_movie_names[1])
        #         st.image(recommended_movie_posters[1])
        #
        #     with col3:
        #         st.text(recommended_movie_names[2])
        #         st.image(recommended_movie_posters[2])
        #     with col4:
        #         st.text(recommended_movie_names[3])
        #         st.image(recommended_movie_posters[3])
        #     with col5:
        #         st.text(recommended_movie_names[4])
        #         st.image(recommended_movie_posters[4])

    except (pickle.UnpicklingError, FileNotFoundError) as e:
        st.error(f"Error loading pickle file: {e}")
