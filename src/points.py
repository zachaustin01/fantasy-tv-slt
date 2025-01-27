import streamlit as st
import json
import os

from .utils import format_name


def show_points_page(selected_league):
    formatted_league_name = format_name(selected_league)
    st.title(f"Points for {formatted_league_name} 🎯")

    # Path to the points.json file for the selected league
    points_file_path = f"src/leagues/{selected_league}/points.json"

    # Check if the file exists
    if os.path.exists(points_file_path):
        # Load the points data
        with open(points_file_path, "r") as file:
            points_data = json.load(file)

        # Display the points in a list
        st.write("Here are the points for activities in this league:")
        for activity, points in points_data.items():
            st.write(f"- {activity}: **{points} points**")
    else:
        st.error(f"Points file for {formatted_league_name} not found.")
