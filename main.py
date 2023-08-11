import requests
import json
import os
import datetime


def update_data():

    # Check if api_key.txt exists, and if not, ask the user for their API key
    if not os.path.exists("api_key.txt"):
        api_key = input("Please enter your Torn API key: ")
        with open("api_key.txt", "w") as f:
            f.write(api_key)
    else:
    with open("api_key.txt", "r") as f:
            api_key = f.read()

    print("Script started.")



    # Check if the JSON file exists
    json_file_path = "faction_revives.json"
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as old_json_file:
            old_json = json.load(old_json_file)
    else:
        old_json = {}

    # Get the current date
    current_date = datetime.datetime.now().date()

    # Check if data was logged today, and if so, skip updates
    if 'date' in old_json and old_json['date'] == str(current_date):
        print("Data was already updated today. Exiting...")
    else:

        # Get faction members' IDs from API response
        response = requests.get(f'https://api.torn.com/faction/?selections=&key={api_key}').json()
        id_list = response["members"]
    
        # Create a dictionary to store new data
        new_json = {
            'date': str(current_date),
            'members': {}
        }
        total_revive_change = 0
        total_revive_skill_change = 0

        for v in id_list:
            member_data = requests.get(f'https://api.torn.com/user/{v}?selections=personalstats&key={api_key}').json()
            member_revives = member_data['personalstats']['revives']
            member_revive_skill = member_data['personalstats']['reviveskill']
            member_name = response['members'][v]['name']

            # Calculate revive change if previous data exists
            if v in old_json.get('members', {}):
                revive_change = member_revives - old_json['members'][v]['revives']
                revive_skill_change = member_revive_skill - old_json['members'][v]['revive_skill']
            else:
                revive_change = 0
                revive_skill_change = 0

            new_json['members'][v] = {
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

        # Log the current time in the text file
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("current_faction_revive_skill.txt", "a") as txt_file:
            txt_file.write(f"Updated on: {current_time}\n")

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
                member_name = new_json['members'][v]['name']
                revive_change = new_json['members'][v]['change']['revives']
                revive_skill_change = new_json['members'][v]['change']['revive_skill']
                member_revives = new_json['members'][v]['revives']
                member_revive_skill = new_json['members'][v]['revive_skill']
                txt_file.write(f"{member_name}:\n")
                txt_file.write(f"  Revive Change: {revive_change}\n")
                txt_file.write(f"  Revive Skill Change: {revive_skill_change}\n")
                txt_file.write(f"  Total Revives: {member_revives}\n")
                txt_file.write(f"  Total Revive Skill: {member_revive_skill}\n\n")

        print('Text file created with faction member revive changes.')


if __name__ == "__main__":
    update_data()
