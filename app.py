import streamlit as st
import os
import json
from src.points import show_points_page
from src.episodes import show_episodes_page
from src.teams import show_teams_page
from src.standings import calculate_team_standings
from src.utils import format_name


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


# Fetch available episodes
def get_episode_names():
    data_dir = "data/"
    if os.path.exists(data_dir):
        return [f.split(".")[0] for f in os.listdir(data_dir) if f.endswith(".json")]
    return []


# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:", ["Home", "Points", "Episode Data", "Teams", "Standings"]
)

# Sidebar dropdown for league selection
leagues = get_league_names()
formatted_leagues = [format_name(league) for league in leagues]
selected_league = st.sidebar.selectbox("Select a league:", formatted_leagues)

# Map formatted names back to directory names
league_mapping = {format_name(league): league for league in leagues}
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

# Episode Data page
elif page == "Episode Data":
    # Fetch available episodes
    episodes = get_episode_names()
    formatted_episodes = [format_name(episode) for episode in episodes]

    # Episode dropdown specific to this page
    selected_episode = st.selectbox("Select an episode:", formatted_episodes)

    # Map formatted names back to episode names
    episode_mapping = {format_name(episode): episode for episode in episodes}
    selected_episode_key = episode_mapping.get(selected_episode)

    if selected_episode_key:
        show_episodes_page(selected_episode_key)
    else:
        st.error("No episode selected. Please select an episode.")

# Teams page
elif page == "Teams":
    st.title("Teams 🏆")
    if selected_league_key:
        show_teams_page(selected_league_key)
    else:
        st.error("Please select a league to view teams.")

# Standings page
elif page == "Standings":
    st.title("Standings 🏅")
    if selected_league_key:
        calculate_team_standings(selected_league_key)
    else:
        st.error("Please select a league to view standings.")
