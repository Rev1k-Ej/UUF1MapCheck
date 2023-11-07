import requests
import os
import json
import time
from bs4 import BeautifulSoup

oldName = ""
oldGamemode = ""
url = 'https://www.battlemetrics.com/servers/squad/22310472'

def GetInfo():
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the div with class 'col-md-6 server-info'
        server_info_div = soup.find('div', class_='col-md-6 server-info')

        if server_info_div:
            # Find the dt element with text 'Map' within the 'col-md-6 server-info' context
            map_name_element = server_info_div.find('dt', text='Map')

            if map_name_element:
                # Extract the map name from the corresponding dd element
                map_name = map_name_element.find_next('dd').text.strip()
                print(f"The current map is: {map_name}")
                return map_name
            else:
                print("Map information not found on the webpage.")
                return "0"
        else:
            print("Div with class 'col-md-6 server-info' not found on the webpage.")
            return "0"
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return response.status_code

def ParseMapName(map):
    # Parse the map name to get the map prefix
    map_name = map.split('_', 2)[0]
    gamemode = map.split('_', 2)[1]
    # print(f"The map prefix is: {map_name}")
    # print(f"The gamemode is: {gamemode}")
    return map_name, gamemode

def update_json_file(current_name, current_gamemode):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_directory, "data.json")

    try:
        # Load existing data from the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty data structure
        data = {}

    # Update the data structure with the currentName and currentGamemode
    map_name_key = 'Maps'
    gamemode_key = 'Gamemodes'

    # Update currentName count
    data.setdefault('UUF1', {}).setdefault(map_name_key, {}).setdefault(current_name, 0)
    data['UUF1'][map_name_key][current_name] += 1

    # Update currentGamemode count
    data.setdefault('UUF1', {}).setdefault(gamemode_key, {}).setdefault(current_gamemode, 0)
    data['UUF1'][gamemode_key][current_gamemode] += 1

    # Save the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

while True:
    sessionType = GetInfo()
    currentName, currentGamemode = ParseMapName(sessionType)

    if currentName != oldName and currentGamemode != oldGamemode:
        update_json_file(currentName, currentGamemode)
        oldName = currentName
        oldGamemode = currentGamemode
    print(currentName, currentGamemode)
    time.sleep(300)
