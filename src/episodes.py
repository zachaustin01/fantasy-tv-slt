import streamlit as st
import json
import os


def show_episodes_page(selected_episode_key, selected_league):
    st.title(f"Episode Data 🎬 - {selected_episode_key}")

    # Path to the data directory
    data_dir = "data/"

    # Construct the file path for the selected episode
    file_path = os.path.join(data_dir, f"{selected_episode_key}.json")

    # Points file path for the selected league
    points_file_path = f"src/leagues/{selected_league}/points.json"

    if os.path.exists(file_path):
        # Load the selected episode data
        with open(file_path, "r") as file:
            episode_data = json.load(file)

        # Load the points data for the selected league
        if os.path.exists(points_file_path):
            with open(points_file_path, "r") as points_file:
                points_data = json.load(points_file)
        else:
            st.error(f"Points file for {selected_league} not found.")
            return

        # Display episode details
        st.write(f"**Episode {episode_data['episode']}**")
        st.write("### Events:")

        # Loop through the events and display them as bullet points with points if applicable
        for event in episode_data["events"]:
            event_points = points_data.get(event["event"], 0)  # Get points for the event
            st.markdown(f"- **{event['contestant']}**: {event['event']} (Points: {event_points})")
    else:
        st.error(f"Episode data for {selected_episode_key} not found.")
