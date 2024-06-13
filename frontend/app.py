import streamlit as st
import requests

# URL of the backend
backend_url = 'http://127.0.0.1:5000'

st.title('Movie Recommendation System')

# Fetch movie options from the backend
movies_response = requests.get(f'{backend_url}/movies')
if movies_response.status_code == 200:
    movie_titles = movies_response.json()
else:
    st.write('Error fetching movies')
    movie_titles = []

# Dropdown for selecting a movie
selected_movie = st.selectbox('Choose a movie:', movie_titles)

if st.button('Get Recommendations'):
    if selected_movie:
        # Make a request to the backend
        response = requests.post(f'{backend_url}/recommend', json={'movie': selected_movie})
        
        if response.status_code == 200:
            recommendations = response.json()
            st.write(f'Recommendations for {selected_movie}:')
            for rec in recommendations:
                st.write(f'- {rec}')
        else:
            st.write('Error: Could not fetch recommendations.')
    else:
        st.write('Please select a movie.')

# Card layout for recommendations
if selected_movie and 'recommendations' in locals():
    for rec in recommendations:
        st.markdown(f"""
        <div style="border:1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 5px;">
            <h4>{rec}</h4>
        </div>
        """, unsafe_allow_html=True)
