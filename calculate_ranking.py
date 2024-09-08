import os
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

#Team Data
team_data = [
    {'team': 'Arizona', 'abbreviation': 'UA', 'logo_path': 'big 12 logos/ua.png'},
    {'team': 'Arizona State', 'abbreviation': 'ASU', 'logo_path': 'big 12 logos/asu.png'},
    {'team': 'Baylor', 'abbreviation': 'BU', 'logo_path': 'big 12 logos/bu.png'},
    {'team': 'BYU', 'abbreviation': 'BYU', 'logo_path': 'big 12 logos/byu.png'},
    {'team': 'Cincinnati', 'abbreviation': 'UC', 'logo_path': 'big 12 logos/uc.png'},
    {'team': 'Colorado', 'abbreviation': 'CU', 'logo_path': 'big 12 logos/cu.png'},
    {'team': 'Houston', 'abbreviation': 'UH', 'logo_path': 'big 12 logos/uh.png'},
    {'team': 'Iowa State', 'abbreviation': 'ISU', 'logo_path': 'big 12 logos/isu.png'},
    {'team': 'Kansas', 'abbreviation': 'KU', 'logo_path': 'big 12 logos/ku.png'},
    {'team': 'Kansas State', 'abbreviation': 'KSU', 'logo_path': 'big 12 logos/ksu.png'},
    {'team': 'Oklahoma State', 'abbreviation': 'OSU', 'logo_path': 'big 12 logos/osu.png'},
    {'team': 'TCU', 'abbreviation': 'TCU', 'logo_path': 'big 12 logos/tcu.png'},
    {'team': 'Texas Tech', 'abbreviation': 'TTU', 'logo_path': 'big 12 logos/ttu.png'},
    {'team': 'UCF', 'abbreviation': 'UCF', 'logo_path': 'big 12 logos/ucf.png'},
    {'team': 'Utah', 'abbreviation': 'UU', 'logo_path': 'big 12 logos/uu.png'},
    {'team': 'West Virginia', 'abbreviation': 'WVU', 'logo_path': 'big 12 logos/wvu.png'}
]

# Function to plot the ranking data with logos
def plot_rankings_with_logos(ranking_data, team_data):
    # Create a mapping of abbreviations to logos from team_data
    logo_map = {team['abbreviation']: team['logo_path'] for team in team_data}

    # Extract team names, average rankings, highest, and lowest
    teams, avg_rankings, highest_rankings, lowest_rankings = zip(*ranking_data)
    
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create a horizontal bar plot for average rankings
    y_pos = range(len(teams))
    ax.barh(y_pos, avg_rankings, color='skyblue', edgecolor='black')
    
    # Add the highest and lowest rankings as text annotations
    for i, (avg, high, low) in enumerate(zip(avg_rankings, highest_rankings, lowest_rankings)):
        ax.text(avg + 0.2, i, f'High: {high}', va='center', fontsize=9)
        ax.text(avg + 0.8, i, f'Low: {low}', va='center', fontsize=9)
    
    # Add team logos next to each bar
    for i, team in enumerate(teams):
        logo_path = logo_map.get(team, None)
        if logo_path:
            img = Image.open(logo_path)
            img.thumbnail((40, 40), Image.ANTIALIAS)
            imagebox = OffsetImage(img, zoom=0.5)
            ab = AnnotationBbox(imagebox, (0, i), frameon=False, boxcoords="offset points", pad=0.5, xybox=(-40, 0))
            ax.add_artist(ab)

    # Set labels, title, and adjust layout
    ax.set_yticks(y_pos)
    ax.set_yticklabels(teams)
    ax.set_xlabel('Average Ranking')
    ax.set_title('Big 12 Football Team Rankings')
    plt.tight_layout()

    # Show the plot
    plt.show()


# Function to calculate average rankings and find highest/lowest ranks
def average_rankings_from_folder(folder_path):
    # Dictionary to store rankings
    rankings_dict = defaultdict(lambda: {'total': 0, 'count': 0, 'highest': float('inf'), 'lowest': 0})

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                # Read team names from the file
                teams = file.read().splitlines()

                # Update ranking data for each team
                for rank, team in enumerate(teams, start=1):
                    rankings_dict[team]['total'] += rank
                    rankings_dict[team]['count'] += 1
                    # Track highest ranking (lowest rank number is best)
                    rankings_dict[team]['highest'] = min(rankings_dict[team]['highest'], rank)
                    # Track lowest ranking
                    rankings_dict[team]['lowest'] = max(rankings_dict[team]['lowest'], rank)

    # Calculate the average rankings and sort teams by average rank
    average_rankings = []
    for team, data in rankings_dict.items():
        average = data['total'] / data['count']
        average_rankings.append((team, average, data['highest'], data['lowest']))

    # Sort by average rank (ascending order)
    sorted_rankings = sorted(average_rankings, key=lambda x: x[1])

    # Print or return the sorted rankings
    return sorted_rankings

# Example usage
folder_path = 'rankings/week 2/'  # Specify your folder path here
rankings = average_rankings_from_folder(folder_path)

plot_rankings_with_logos(rankings, team_data)
