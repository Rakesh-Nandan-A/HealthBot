import os
import json

# Path where profiles are stored
PROFILE_DB_PATH = "App/resource/user_profiles.json"

def load_profiles():
    if not os.path.exists(PROFILE_DB_PATH):
        return {}
    with open(PROFILE_DB_PATH, "r") as f:
        return json.load(f)

def save_profiles(profiles):
    with open(PROFILE_DB_PATH, "w") as f:
        json.dump(profiles, f, indent=4)

def get_user_profile(username):
    profiles = load_profiles()
    return profiles.get(username)

def save_user_profile(username, profile_data):
    profiles = load_profiles()
    profiles[username] = profile_data
    save_profiles(profiles)