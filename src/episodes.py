import streamlit as st
import json
import os
import pandas as pd


def show_episodes_page():
    st.title("Episode Data 🎬")

    # Path to the data directory
    data_dir = "data/"

    # Fetch episode files
    episode_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]

    if episode_files:
        # Dropdown to select an episode file
        selected_file = st.selectbox("Select an episode:", episode_files)

        # Load the selected episode data
        file_path = os.path.join(data_dir, selected_file)
        with open(file_path, "r") as file:
            episode_data = json.load(file)

        # Display episode details
        st.markdown(f"**Episode {episode_data['episode']}**")
        st.markdown("### Events:")

        # Create a DataFrame to display events in a table format
        events_df = pd.DataFrame(episode_data["events"])

        # Display the DataFrame as a table
        st.dataframe(events_df)

        # Optionally, you can also display the events in a more narrative style:
        st.markdown("#### Event Highlights:")
        for event in episode_data["events"]:
            st.write(
                f"**{event['contestant']}**: {event['event']} at **{event['timestamp']}**"
            )

    else:
        st.error("No episode data files found.")
