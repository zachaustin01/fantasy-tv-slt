import streamlit as st
import json
import os


def show_episodes_page(selected_episode_key):
    st.title(f"Episode Data 🎬 - {selected_episode_key}")

    # Path to the data directory
    data_dir = "data/"

    # Construct the file path for the selected episode
    file_path = os.path.join(data_dir, f"{selected_episode_key}.json")

    if os.path.exists(file_path):
        # Load the selected episode data
        with open(file_path, "r") as file:
            episode_data = json.load(file)

        # Display episode details
        st.write(f"**Episode {episode_data['episode']}**")
        st.write("### Events:")

        # Loop through the events and display them as bullet points
        for event in episode_data["events"]:
            st.markdown(
                f"- **{event['contestant']}**: {event['event']} at {event['timestamp']}"
            )
    else:
        st.error(f"Episode data for {selected_episode_key} not found.")
