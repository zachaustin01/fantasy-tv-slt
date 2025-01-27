import json
import os
import streamlit as st
from .utils import format_name


def get_team_roster(league_name):
    """Fetch the team roster for the selected league."""
    teams_file_path = f"src/leagues/{league_name}/teams.json"
    if os.path.exists(teams_file_path):
        with open(teams_file_path, "r") as file:
            teams_data = json.load(file)
        return teams_data
    return []


def calculate_contestant_points(league_name, contestant_name):
    """Calculate the total points for a given contestant across all episodes."""
    points_file_path = f"src/leagues/{league_name}/points.json"
    episodes_dir = "data/"

    # Load the league's point system
    if os.path.exists(points_file_path):
        with open(points_file_path, "r") as file:
            points_data = json.load(file)

    total_points = 0
    # Iterate through all episode data to calculate points
    for episode_file in os.listdir(episodes_dir):
        if episode_file.endswith(".json"):
            episode_path = os.path.join(episodes_dir, episode_file)
            with open(episode_path, "r") as file:
                episode_data = json.load(file)
                for event in episode_data["events"]:
                    if event["contestant"] == contestant_name:
                        # Check if the event matches the points system
                        event_points = points_data.get(event["event"], 0)
                        total_points += event_points

    return total_points


def calculate_team_standings(league_name):
    """Calculate the total points for each team and display standings."""
    teams_data = get_team_roster(league_name)

    if not teams_data:
        return

    # Initialize a dictionary to hold the total points for each team
    team_points = {team["name"]: 0 for team in teams_data}

    # Calculate points for each contestant and add to their team's total
    for team in teams_data:
        for contestant in team["roster"]:
            total_points = calculate_contestant_points(league_name, contestant)
            team_points[team["name"]] += total_points

    # Sort the teams by their total points in descending order
    sorted_teams = sorted(team_points.items(), key=lambda x: x[1], reverse=True)

    # Display the standings
    st.title(f"Standings for {format_name(league_name)} 🏆")
    st.write("Here are the current team standings based on total points:")

    for rank, (team_name, points) in enumerate(sorted_teams, start=1):
        st.write(f"{rank}. **{team_name}**: {points} points")
