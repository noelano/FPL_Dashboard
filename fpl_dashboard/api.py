import requests

from pandas.io.json import json_normalize

from fpl_dashboard import (
    BOOTSTRAP_URL, ELEMENT_URL
)


TEST = True


def fetch_bootstrap():
    bootstrap_data = requests.get(BOOTSTRAP_URL)
    bootstrap_data = bootstrap_data.json()

    return bootstrap_data


def fetch_element(id):
    element_data = requests.get(ELEMENT_URL + str(id))
    element_data = element_data.json()

    return element_data


def obtain_player_history_fixtures(bootstrap_data):
    history = []
    fixtures = []

    player_data = bootstrap_data['elements']
    if TEST:
        player_data = [player_data[0]]
    for player in player_data:
        id = player['id']
        element = fetch_element(id)

        # TODO - smarter way to format this data
        for match in element['history']:
            match['player_id'] = id
            history.append(match)

        for fixture in element['fixtures']:
            fixture['player_id'] = id
            fixtures.append(fixture)

    # Convert into dataframes
    history = json_normalize(history)
    fixtures = json_normalize(fixtures)

    # If the history or fixtures are empty, add in a player_id column manually
    if history.shape[0] == 0:
        history['player_id'] = []
    if fixtures.shape[0] == 0:
        fixtures['player_id'] = []

    return history, fixtures


def load_all_data():
    bootstrap_data = fetch_bootstrap()
    players = json_normalize(bootstrap_data['elements'])
    teams = json_normalize(bootstrap_data['teams'])
    history, fixtures = obtain_player_history_fixtures(bootstrap_data)

    # Add full name to the player data
    players['full_name'] = players['first_name'] + ' ' + players['second_name']

    return teams, players, history, fixtures


if __name__ == "__main__":

    teams, players, history, fixtures = load_all_data()
    len(history)
