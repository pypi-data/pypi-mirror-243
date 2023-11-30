"""#Aityz Chess Library Version 1.0
Aityz Chess is a library for integrating useful Chess Analysis functions into Python. It is strongly integrated with chess.com, and has direct integration and scraping. It is strongly focused on plotting data visually, so you can see any interesting effects or correlations.
"""

import json
import os
import random
import re
from collections import Counter

import chess.pgn
import chess.engine
import matplotlib.pyplot as plt
import requests


USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0')

def clear_cache() -> None:
    """Clears all the cache for the Caching System.
    """
    cache_dir = 'aityz_cache'
    if os.path.exists(cache_dir):
        for file in os.listdir(cache_dir):
            os.remove(os.path.join(cache_dir, file))
        os.rmdir(cache_dir)

def sanitize_url(url: str) -> str:
    """Cleans URLs to be used in file names.

    Args:
        url (str): This URL will be used in the name of the file after being sanitized.

    Returns:
        str: A string with the cleansed URL.
    """
    url = url.replace('https://', '')
    url = re.sub(r'\W+', '-', url)
    return url

def save_subset(data: dict, url: str) -> None:
    """Save some JSON data to the Caching System.

    Args:
        data (dict): JSON formatted data that will be saved.
        url (str): The URL (that will be cleansed), and will eventually be the save location.
    """
    cache_dir = 'aityz_cache'
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    safe_subset_name = sanitize_url(url)
    with open(os.path.join(cache_dir, f'{safe_subset_name}.json'), 'w') as f:
        json.dump(data, f, indent=4)

def load_subset(subset_name: str) -> dict:
    """Loads some JSON data from the Caching System.

    Args:
        subset_name (str): This will be an uncleansed URL that will be cleansed, and checked.

    Returns:
        dict: The JSON data for the subset.
    """
    safe_subset_name = sanitize_url(subset_name)
    with open(os.path.join('aityz_cache', f'{safe_subset_name}.json'), 'r') as f:
        data = json.load(f)
    return data

def find_subsets() -> list:
    """Lists all the cache that is stored in the Caching System.

    Returns:
        list: This will be a list of names (without the .json). They will be in Cleansed URL form.
    """
    cache_dir = 'aityz_cache'
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
        return []
    subsets = [file.replace('.json', '') for file in os.listdir(cache_dir)]
    return subsets

def get_pgns(username: str, verbose: bool = False) -> list:
    """Gets all the PGN formats of games from a user.

    Args:
        username (str): User to grab games from.
        verbose (bool, optional): Whether to print out the current subset. Defaults to False.

    Returns:
        list: A list of PGN formatted strings.
    """
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    subsets = response.json()
    cached = find_subsets()
    pgns = []
    for subset in subsets['archives']:
        sanitized_subset = sanitize_url(subset)
        if verbose:
            print(f'Fetching Subset {subset} ...!')
        if sanitized_subset in cached:
            data = load_subset(sanitized_subset)
        else:
            response = requests.get(subset, headers={'User-Agent': USER_AGENT})
            response.raise_for_status()
            data = response.json()
            save_subset(data, subset)
        for game in data['games']:
            try:
                pgns.append(game['pgn'])
            except:
                pass
    return pgns

def get_raw_games(username: str, verbose: bool = False) -> list:
    """Gets games of a user in JSON format, with the PGN inside.

    Args:
        username (str): User to grab games from.
        verbose (bool, optional): Whether to print out the current subset. Defaults to False.

    Returns:
        list: A list of JSON formatted games.
    """
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    subsets = response.json()
    cached = find_subsets()
    games = []
    for subset in subsets['archives']:
        sanitized_subset = sanitize_url(subset)
        if verbose:
            print(f'Fetching Subset {subset} ...!')
        if sanitized_subset in cached:
            data = load_subset(sanitized_subset)
        else:
            response = requests.get(subset, headers={'User-Agent': USER_AGENT})
            response.raise_for_status()
            data = response.json()
            save_subset(data, subset)
        for game in data['games']:
            try:
                games.append(game)
            except:
                pass
    return games

def plot_elo(username: str, time_control: str | list, self: bool = True, verbose: bool = False) -> None:
    """Plots the Elo change over time of a user.

    Args:
        username (str): The user to check.
        time_control (str | list): Formatted like "300" or "900+10". The Chess time control to check.
        self (bool, optional): Whether to plot the user's Elo or not. When False, will plot the user's opponent's Elo ratings. Defaults to True.
        verbose (bool, optional): Whether to print out which subset it is currently on or not. Defaults to False.
    """
    pgns = get_pgns(username, verbose)
    elos = []
    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        if game.headers['TimeControl'] == time_control:
            if self:
                elos.append(int(game.headers['WhiteElo']) if username.lower() == game.headers['White'].lower() else int(game.headers['BlackElo']))
            else:
                elos.append(int(game.headers['BlackElo']) if username.lower() == game.headers['White'].lower() else int(game.headers['WhiteElo']))
    plt.plot(elos)
    plt.title(f'{username}\'s {time_control} Time Control Elo Graph!')
    plt.show()

def plot_streaks(username, histogram=True, time_control: str = None, verbose: bool = False) -> None:
    """Plots the win streaks held by a user.

    Args:
        username (_type_): The user to check.
        histogram (bool, optional): Whether to plot the streaks as a histogram or not. On False, will display as a line graph. Defaults to True.
        time_control (str, optional): The Time Control to check streaks for. Defaults to None.
        verbose (bool, optional): Whether to print subsets or not. Defaults to False.
    """
    pgns = get_pgns(username, verbose)
    streaks = []

    current_streak = 0

    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)

        if time_control is None:
            if game.headers['Result'] == '1-0':
                if game.headers['White'].lower() == username.lower():
                    current_streak += 1
                else:
                    if current_streak > 1:
                        streaks.append(current_streak)
                    current_streak = 0
            elif game.headers['Result'] == '0-1':
                if game.headers['Black'].lower() == username.lower():
                    current_streak += 1
                else:
                    if current_streak > 1:
                        streaks.append(current_streak)
                    current_streak = 0
            else:
                pass
        else:
            if game.headers['TimeControl'] == time_control:
                if game.headers['Result'] == '1-0':
                    if game.headers['White'].lower() == username.lower():
                        current_streak += 1
                    else:
                        if current_streak > 1:
                            streaks.append(current_streak)
                        current_streak = 0
                elif game.headers['Result'] == '0-1':
                    if game.headers['Black'].lower() == username.lower():
                        current_streak += 1
                    else:
                        if current_streak > 1:
                            streaks.append(current_streak)
                        current_streak = 0
                
    if histogram is True:
        plt.hist(streaks, bins=30)
        plt.title(f'{username}\'s streaks')
        plt.show()
    else:
        plt.plot(streaks)
        plt.title(f'{username}\'s streaks')
        plt.show()
    
    print(f'Longest Streak was: {max(streaks)}')

def monte_carlo(whiteElo: int, blackElo: int, games: int) -> None:
    """A Monte Carlo Simulation of Chess.

    Args:
        whiteElo (int): The white player's Elo.
        blackElo (int): The black player's Elo.
        games (int): How many games to simulate.
    """
    results = []
    win_rate = 1 / (1 + 10 ** ((whiteElo - blackElo) / 400)) * 100
    for i in range(games):
        chosen = random.randint(1, 100)
        if chosen <= win_rate:
            results.append(0)
        else:
            results.append(1)
    print(f'Simulated {games} games!')
    print(f'User 1 ({whiteElo}) vs User 2 ({blackElo})')
    print(f'User 1 won {results.count(1)} games!')
    print(f'User 2 won {results.count(0)} games!')
    print(f'Win Rate was: {int(round(100 - win_rate, 0))}%')

def concactenate(username: str) -> None:
    """Concatenates all the games of a user into one PGN.

    Args:
        username (str): The user to create the PGN file for. The file is also named (username).pgn
    """
    pgns = get_pgns(username)
    save_file = open(f'{username}.pgn', 'w')
    for i in range(len(pgns)):
        save_file.write(pgns[i])
        save_file.write('\n\n')
    print('Done!')

def plot_time_controls(username, verbose: bool = False) -> None:
    """Plots time controls that the user plays.

    Args:
        username (_type_): The user to check.
        verbose (bool, optional): Whether to print the subsets or not. Defaults to False.
    """
    pgns = get_pgns(username, verbose=verbose)

    controls = []

    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        controls.append(game.headers['TimeControl'])
    
    controls2 = []

    for control in controls:
        if control == '1/86400':
            controls2.append('Daily')
        elif control == '1/1209600':
            controls2.append('Fortnightly')
        elif control == '1/604800':
            controls2.append('Weekly')
        elif control == '1/259200':
            controls2.append('Tri-Daily')
        elif control == '1/172800':
            controls2.append('Bi-Daily')
        else:
            controls2.append(control)
    
    counter = Counter(controls2)

    counter = dict(counter)

    plt.bar(list(counter.keys()), list(counter.values()), color = 'green', width=0.4)
    plt.title(f'{username}\'s Favorite Time Controls')
    plt.show()

def average_elo(username: str, verbose: bool = False, self: bool = True) -> float:
    """Returns the average Elo of a user, or their opponents.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print subsets or not. Defaults to False.
        self (bool, optional): Whether it is the user's average Elo, or their opponent's. Defaults to True.

    Returns:
        float: Average elo of opponent's or user.
    """
    pgns = get_pgns(username, verbose=verbose)

    elos = []

    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        if self is True:
            if game.headers['White'].lower() == username.lower():
                elos.append(int(game.headers['WhiteElo']))
            else:
                elos.append(int(game.headers['BlackElo']))
        else:
            if game.headers['White'].lower() == username.lower():
                elos.append(int(game.headers['BlackElo']))
            else:
                elos.append(int(game.headers['WhiteElo']))
    
    return sum(elos) / len(elos)

def plot_hour(username: str, verbose: bool = False):
    """Plots with a bar graph that games are usually played in UTC.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print subsets or not. Defaults to False.
    """
    pgns = get_pgns(username, verbose=verbose)

    hours = []

    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        hours.append(f'{game.headers["StartTime"][0]}{game.headers["StartTime"][1]}')
    
    hours = Counter(hours)
    hours = dict(hours)
    hours = dict(sorted(hours.items()))

    plt.bar(list(hours.keys()), list(hours.values()), color='green')
    plt.title(f'{username}\'s Average Playing Time')
    plt.show()

def plot_wdl(username: str, verbose: bool = False):
    """Plots Win/Draw/Loss on a bar graph.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print subsets or not. Defaults to False.
    """
    pgns = get_pgns(username, verbose=verbose)

    stats = []

    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        if game.headers['Result'] == '1-0':
            if game.headers['White'].lower() == username.lower():
                stats.append('W')
            else:
                stats.append('L')
        elif game.headers['Result'] == '0-1':
            if game.headers['Black'].lower() == username.lower():
                stats.append('W')
            else:
                stats.append('L')
        else:
            stats.append('D')
    
    counting = dict(Counter(stats))
    
    plt.bar(list(counting.keys()), list(counting.values()), color='green')
    plt.title(f'{username}\'s Win Draw Loss')
    plt.show()

def plot_favourite_openings(username: str, verbose: bool = False):
    """Plot's a users top 5 favourite ECO openings.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print the subset or not. Defaults to False.
    """
    pgns = get_pgns(username, verbose=verbose)

    openings = []

    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        
        openings.append(game.headers['ECO'])
    
    counter = Counter(openings)

    listing = list(counter)

    options = [
        listing[0],
        listing[1],
        listing[2],
        listing[3],
        listing[4],
    ]

    counter = dict(counter)

    plottable = {
        options[0]: counter[options[0]],
        options[1]: counter[options[1]],
        options[2]: counter[options[2]],
        options[3]: counter[options[3]],
        options[4]: counter[options[4]],
    }

    print(plottable)

    plt.bar(plottable.keys(), plottable.values(), color='green')
    plt.title(f'{username}\'s Favourite Openings')
    plt.show()

def save_favourite_openings(username: str, verbose: bool = False, file_name: str = None, eco_code: bool = False):
    """This will gather a user's favourite openings and save them to a JSON file.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print the subset or not. Defaults to False.
        file_name (str, optional): Custom filename for the JSON file. Defaults to None.
        eco_code (bool, optional): Whether to save the openings as an ECO Code (Example: A00) instead of a URL to the Opening on Chess.com. Defaults to False.
    """

    pgns = get_pgns(username, verbose=verbose)

    openings = []

    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        if eco_code is True:
            openings.append(game.headers['ECO'])
        else:
            openings.append(game.headers['ECOUrl'])
    
    counter = Counter(openings)
    counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))

    if file_name is not None:
        json.dump(counter, open(file_name, 'w'), indent=4)
    else:
        json.dump(counter, open(f'{username}_openings.json', 'w'), indent=4)

def plot_rated(username: str, verbose: bool = False):
    """Plots whether a user prefers rated or unrated chess.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print the subset or not. Defaults to False.
    """
    games = get_raw_games(username, verbose=verbose)

    rated = []

    for game in games:
        if game['rated'] is True:
            rated.append('Rated')
        else:
            rated.append('Unrated')
    
    counter = Counter(rated)

    counter = dict(counter)

    plt.bar(counter.keys(), counter.values(), color='green')
    plt.title(f'{username}\'s Rated vs Unrated')
    plt.show()

def plot_class(username: str, verbose: bool = False):
    """Plots what type of chess a user prefers.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print the subset or not. Defaults to False.
    """
    games = get_raw_games(username, verbose=verbose)

    classes = []

    for game in games:
        classes.append(game['time_class'])
    
    counter = Counter(classes)

    counter = dict(counter)

    plt.bar(counter.keys(), counter.values(), color='green')
    plt.title(f'{username}\'s Class of Chess')
    plt.show()

def save_most_common_positions(username: str, verbose: bool = False, save_file: str = None):
    """Save the most common positions in Forsyth-Edwards Notation (FEN) format. Very memory inefficient, this is why you learn C++ kids (and learn how to cry when using memory pointers)

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print the subsets or not. Defaults to False.
        save_file (str, optional): Where to save the file, default is (username)_positions.json. Defaults to None.
    """
    pgns = get_pgns(username, verbose=verbose)

    positions = []

    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            positions.append(board.fen())
    
    counter = Counter(positions)

    counter = Counter(positions)
    counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))


    if save_file is not None:
        json.dump(counter, open(save_file, 'w'), indent=4)
    else:
        json.dump(counter, open(f'{username}_positions.json', 'w'), indent=4)

def compare(user1: str, user2: str, time_control: str, verbose: bool = False):
    """Compare two user's Elo graphs, to see who is a better learner :D.

    Args:
        user1 (str): User1's username.
        user2 (str): User2's username.
        time_control (str): The time control to check.
        verbose (bool, optional): Whether to print the subsets or not. Defaults to False.
    """
    pgns1 = get_pgns(user1, verbose=verbose)
    pgns2 = get_pgns(user2, verbose=verbose)

    elos1 = []
    elos2 = []

    for pgn in pgns1:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        if game.headers['TimeControl'] == time_control:
            elos1.append(int(game.headers['WhiteElo']) if user1.lower() == game.headers['White'].lower() else int(game.headers['BlackElo']))
    
    for pgn in pgns2:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        if game.headers['TimeControl'] == time_control:
            elos2.append(int(game.headers['WhiteElo']) if user2.lower() == game.headers['White'].lower() else int(game.headers['BlackElo']))
    
    plt.plot(elos1, label=user1)
    plt.plot(elos2, label=user2)
    plt.legend()
    plt.title(f'{user1} vs {user2}')
    plt.show()

def plot_game_len(username: str, verbose: bool = False, time_control: str = None):
    """Plots the length of games played by a user.

    Args:
        username (str): The user to check.
        verbose (bool, optional): Whether to print the subsets or not. Defaults to False.
        time_contorl (str): What time control to check. Defaults to None.
    """
    pgns = get_pgns(username, verbose=verbose)

    lengths = []

    for pgn in pgns:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)
        if time_control is not None:
            if game.headers['TimeControl'] == time_control:
                lengths.append(len(list(game.mainline_moves())))
        else:
            lengths.append(len(list(game.mainline_moves())))
    
    plt.hist(lengths, bins=30)
    plt.title(f'{username}\'s Game Lengths')
    plt.show()

def compare_streaks(User1: str, User2: str, time_control: str = None, verbose: bool = False):
    """Compare two user's streaks.

    Args:
        User1 (str): User1's username.
        User2 (str): User2's username.
        time_control (str, optional): What time control to check. Defaults to None.
        verbose (bool, optional): Whether to print the subsets or not. Defaults to False.
    """
    pgns1 = get_pgns(User1, verbose=verbose)
    pgns2 = get_pgns(User2, verbose=verbose)

    streaks1 = []
    streaks2 = []

    current_streak = 0

    for pgn in pgns1:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)

        if time_control is None:
            if game.headers['Result'] == '1-0':
                if game.headers['White'].lower() == User1.lower():
                    current_streak += 1
                else:
                    if current_streak > 1:
                        streaks1.append(current_streak)
                    current_streak = 0
            elif game.headers['Result'] == '0-1':
                if game.headers['Black'].lower() == User1.lower():
                    current_streak += 1
                else:
                    if current_streak > 1:
                        streaks1.append(current_streak)
                    current_streak = 0
            else:
                pass
        else:
            if game.headers['TimeControl'] == time_control:
                if game.headers['Result'] == '1-0':
                    if game.headers['White'].lower() == User1.lower():
                        current_streak += 1
                    else:
                        if current_streak > 1:
                            streaks1.append(current_streak)
                        current_streak = 0
                elif game.headers['Result'] == '0-1':
                    if game.headers['Black'].lower() == User1.lower():
                        current_streak += 1
                    else:
                        if current_streak > 1:
                            streaks1.append(current_streak)
                        current_streak = 0
    
    current_streak = 0

    for pgn in pgns2:
        with open('data.pgn', 'w') as f:
            f.write(pgn)
        with open('data.pgn', 'r') as f:
            game = chess.pgn.read_game(f)

        if time_control is None:
            if game.headers['Result'] == '1-0':
                if game.headers['White'].lower() == User2.lower():
                    current_streak += 1
                else:
                    if current_streak > 1:
                        streaks2.append(current_streak)
                    current_streak = 0
            elif game.headers['Result'] == '0-1':
                if game.headers['Black'].lower() == User2.lower():
                    current_streak += 1
                else:
                    if current_streak > 1:
                        streaks2.append(current_streak)
                    current_streak = 0
            else:
                pass
        else:
            if game.headers['TimeControl'] == time_control:
                if game.headers['Result'] == '1-0':
                    if game.headers['White'].lower() == User2.lower():
                        current_streak += 1
                    else:
                        if current_streak > 1:
                            streaks2.append(current_streak)
                        current_streak = 0
                elif game.headers['Result'] == '0-1':
                    if game.headers['Black'].lower() == User2.lower():
                        current_streak += 1
                    else:
                        if current_streak > 1:
                            streaks2.append(current_streak)
                        current_streak = 0
        
    plt.hist(streaks1, bins=30, label=User1)
    plt.hist(streaks2, bins=30, label=User2)
    plt.legend()
    plt.title(f'{User1} vs {User2}')
    plt.show()

def compare_classes(User1: str, User2: str, verbose: bool = False):
    """Compare two user's classes.

    Args:
        User1 (str): User1's username.
        User2 (str): User2's username.
        verbose (bool, optional): Whether to print the subsets or not. Defaults to False.
    """
    games1 = get_raw_games(User1, verbose=verbose)
    games2 = get_raw_games(User2, verbose=verbose)

    classes1 = []
    classes2 = []

    for game in games1:
        classes1.append(game['time_class'])
    
    for game in games2:
        classes2.append(game['time_class'])
    
    counter1 = Counter(classes1)
    counter2 = Counter(classes2)

    plt.bar(counter1.keys(), counter1.values(), color='green', label=User1)
    plt.bar(counter2.keys(), counter2.values(), color='blue', label=User2)
    plt.legend()
    plt.title(f'{User1} vs {User2}')
    plt.show()


