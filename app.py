import streamlit as st
import os
import json
from src.points import show_points_page
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
page = st.sidebar.radio("Go to:", ["Home", "Points", "Episode Data"])

# Sidebar dropdown for league selection
leagues = get_league_names()
formatted_leagues = [format_name(league) for league in leagues]
selected_league = st.sidebar.selectbox("Select a league:", formatted_leagues)

# Sidebar dropdown for episode selection
episodes = get_episode_names()
formatted_episodes = [format_name(episode) for episode in episodes]
selected_episode = st.sidebar.selectbox("Select an episode:", formatted_episodes)

# Map formatted names back to directory names
league_mapping = {format_name(league): league for league in leagues}
selected_league_key = league_mapping.get(selected_league)

episode_mapping = {format_name(episode): episode for episode in episodes}
selected_episode_key = episode_mapping.get(selected_episode)

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
    if selected_episode_key:
        st.title(f"Episode Data for {selected_episode}")
        # Fetch the corresponding episode data
        episode_data_path = f"data/{selected_episode_key}.json"
        if os.path.exists(episode_data_path):
            with open(episode_data_path, "r") as file:
                episode_data = json.load(file)

            # Display the episode data (customize based on data structure)
            st.json(
                episode_data
            )  # Or you could customize how to display it (e.g., with markdown, tables, etc.)
        else:
            st.error(f"Episode data for {selected_episode} not found.")
    else:
        st.error("No episode selected. Please select an episode.")
