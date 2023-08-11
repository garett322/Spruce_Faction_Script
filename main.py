import requests
import json
import os

# Load API key from file
with open("api_key.txt", "r") as f:
    api_key = f.read()

print("Script started.")

# Get faction members' IDs from API response
response = requests.get(f'https://api.torn.com/faction/?selections=&key={api_key}').json()
id_list = response["members"]

# Check if the JSON file exists
json_file_path = "faction_revives.json"
if os.path.exists(json_file_path):
    with open(json_file_path, "r") as old_json_file:
        old_json = json.load(old_json_file)
else:
    old_json = {}

# Create a dictionary to store new data
new_json = {}
total_revive_change = 0
total_revive_skill_change = 0

for v in id_list:
    member_data = requests.get(f'https://api.torn.com/user/{v}?selections=personalstats&key={api_key}').json()
    member_revives = member_data['personalstats']['revives']
    member_revive_skill = member_data['personalstats']['reviveskill']
    member_name = response['members'][v]['name']

    # Calculate revive change if previous data exists
    if v in old_json:
        revive_change = member_revives - old_json[v]['revives']
        revive_skill_change = member_revive_skill - old_json[v]['revive_skill']
    else:
        revive_change = 0
        revive_skill_change = 0
    
    new_json[v] = {
        'name': member_name,
        'revives': member_revives,
        'revive_skill': member_revive_skill,
        'change': {
            'revives': revive_change,
            'revive_skill': revive_skill_change
        }
    }

    total_revive_change += revive_change
    total_revive_skill_change += revive_skill_change

# Write the updated data back to the JSON file
with open(json_file_path, "w") as updated_json_file:
    json.dump(new_json, updated_json_file, indent=4)

# Calculate and display total changes
print('Script completed.')
print(f'Total Revive Change: {total_revive_change}')
print(f'Total Revive Skill Change: {total_revive_skill_change}')
print(f'Number of Faction Members: {len(id_list)}')

# Create and write data to the text file
with open("faction_member_revive_changes.txt", "w") as txt_file:
    txt_file.write(f'Total Revive Change: {total_revive_change}\n')
    txt_file.write(f'Total Revive Skill Change: {total_revive_skill_change}\n\n')

    for v in id_list:
        member_name = new_json[v]['name']
        revive_change = new_json[v]['change']['revives']
        revive_skill_change = new_json[v]['change']['revive_skill']
        member_revives = new_json[v]['revives']
        member_revive_skill = new_json[v]['revive_skill']
        txt_file.write(f"{member_name}:\n")
        txt_file.write(f"  Revives: {member_revives}\n")
        txt_file.write(f"  Revive Skill: {member_revive_skill}\n")
        txt_file.write(f"  Revives Change: {revive_change}\n")
        txt_file.write(f"  Revive Skill Change: {revive_skill_change}\n\n")

print('Text file created with faction member revive changes.')
