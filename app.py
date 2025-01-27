import streamlit as st
from src.points import show_points_page, format_league_name
import os


# Fetch available leagues
def get_league_names():
    leagues_dir = "src/leagues/"
    if os.path.exists(leagues_dir):
        return [
            d
            for d in os.listdir(leagues_dir)
            if os.path.isdir(os.path.join(leagues_dir, d))
        ]
    return []


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Points"])

# Sidebar dropdown for league selection
leagues = get_league_names()
formatted_leagues = [format_league_name(league) for league in leagues]
selected_league = st.sidebar.selectbox("Select a league:", formatted_leagues)

# Map formatted league name back to directory name
league_mapping = {format_league_name(league): league for league in leagues}
selected_league_key = league_mapping.get(selected_league)

# Home page
if page == "Home":
    st.title("Bachelor Fantasy League")
    st.write(
        "Welcome to the Bachelor Fantasy League! Choose a page from the sidebar to get started. 🌹"
    )

# Points page
elif page == "Points":
    if selected_league_key:
        show_points_page(selected_league_key)
    else:
        st.error(
            "No leagues found. Please ensure the league folders and JSON files are correctly set up."
        )
