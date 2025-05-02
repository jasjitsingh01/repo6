import pickle
import pandas as pd
import streamlit as st
import requests

# ---------------------- Styling ----------------------
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    .movie-title {
        font-weight: bold;
        font-size: 16px;
        text-align: center;
        margin-bottom: 8px;
        color: #ffffff;
    }
    .footer {
        text-align: center;
        color: gray;
        padding-top: 30px;
        font-size: 16px;
    }
    h1, h4, .stSelectbox label, .stButton button {
        color: white !important;
    }
    .stSelectbox > div {
        background-color: #1e1e1e;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Functions ----------------------
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        response = requests.get(url, timeout=7)
        response.raise_for_status()
        data = response.json()

        # If there is a poster path
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"  # Default placeholder if no image

    except Exception as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"  # Default placeholder if error occurs

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster and handle if no poster exists
        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster)
    return recommended_movies, recommended_movies_posters

# ---------------------- Load Data ----------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------------- Header ----------------------
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 iRecommend</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'>Find your next favorite movie 🍿</h4>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------- Select Box ----------------------
selected_movie_name = st.selectbox(
    "Which movie did you like? We'll suggest more!",
    movies['title'].values
)

# ---------------------- Button + Spinner ----------------------
if st.button('🎯 Show Suggestions'):
    with st.spinner('Finding perfect movies for you...'):
        names, posters = recommend(selected_movie_name)

        # Handling layout in columns dynamically
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            if idx < len(names):
                with col:
                    st.markdown(f"<div class='movie-title'>{names[idx]}</div>", unsafe_allow_html=True)
                    st.image(posters[idx])

# ---------------------- Footer ----------------------
st.markdown("<div class='footer'>Made with ❤️ by Jass</div>", unsafe_allow_html=True)
