import json
import os
import streamlit as st


def get_contestant_points(contestant_name, league):
    """Get the total points for a contestant based on events."""
    total_points = 0
    data_dir = "data/"

    # Loop through each episode to get points for the contestant
    episode_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    for episode_file in episode_files:
        episode_path = os.path.join(data_dir, episode_file)
        with open(episode_path, "r") as file:
            episode_data = json.load(file)
            for event in episode_data.get("events", []):
                if event["contestant"] == contestant_name:
                    # Look up points from the league's points.json
                    points_file_path = f"src/leagues/{league}/points.json"
                    if os.path.exists(points_file_path):
                        with open(points_file_path, "r") as points_file:
                            points_data = json.load(points_file)
                        # Look up points for the specific event
                        event_points = points_data.get(event["event"], 0)
                        total_points += event_points
    return total_points


def show_teams_page(selected_league):
    """Displays the teams and rosters for the selected league."""

    # Path to the teams.json file for the selected league
    teams_file_path = f"src/leagues/{selected_league}/teams.json"

    # Check if the file exists
    if os.path.exists(teams_file_path):
        # Load the teams data
        with open(teams_file_path, "r") as file:
            teams_data = json.load(file)

        # Make sure teams_data is a list
        if isinstance(teams_data, list):
            st.write("### Teams and Rosters:")

            for team in teams_data:
                st.write(f"**{team['name']}**")
                st.write("**Roster:**")

                total_team_points = 0
                for member_name in team["roster"]:
                    # Get the total points for each contestant in the roster
                    member_points = get_contestant_points(member_name, selected_league)
                    st.write(f"- {member_name} (Points: {member_points})")
                    total_team_points += member_points

                st.write(f"**Total Points for {team['name']}:** {total_team_points}")
                st.write("---")
        else:
            st.error("The teams data is not in the correct format. Expected a list.")
    else:
        st.error(f"Teams file for {selected_league} not found.")
