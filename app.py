import streamlit as st
import pickle
import pandas as pd
import requests



def fetch_poster(movie_id):
    try:
        response = requests.get(
            'https://api.themoviedb.org/3/movie/{}?api_key=99ceaa04cb5c7ccea6c15f0eacd32872&language=en-US'.format(movie_id)
        )
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data.get('poster_path', 'default_poster_path.jpg')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return 'default_poster_path.jpg'




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies['title'].iloc[i[0]])
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster



movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommender System')


selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
