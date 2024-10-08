import os
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

#Team Data
team_data = [
    {'team': 'Arizona', 'abbreviation': 'UA', 'logo_path': 'big12 logos/ua.png'},
    {'team': 'Arizona State', 'abbreviation': 'ASU', 'logo_path': 'big12 logos/asu.png'},
    {'team': 'Baylor', 'abbreviation': 'BU', 'logo_path': 'big12 logos/bu.png'},
    {'team': 'BYU', 'abbreviation': 'BYU', 'logo_path': 'big12 logos/byu.png'},
    {'team': 'Cincinnati', 'abbreviation': 'UC', 'logo_path': 'big12 logos/uc.png'},
    {'team': 'Colorado', 'abbreviation': 'CU', 'logo_path': 'big12 logos/cu.png'},
    {'team': 'Houston', 'abbreviation': 'UH', 'logo_path': 'big12 logos/uh.png'},
    {'team': 'Iowa State', 'abbreviation': 'ISU', 'logo_path': 'big12 logos/isu.png'},
    {'team': 'Kansas', 'abbreviation': 'KU', 'logo_path': 'big12 logos/ku.png'},
    {'team': 'Kansas State', 'abbreviation': 'KSU', 'logo_path': 'big12 logos/ksu.png'},
    {'team': 'Oklahoma State', 'abbreviation': 'OSU', 'logo_path': 'big12 logos/osu.png'},
    {'team': 'TCU', 'abbreviation': 'TCU', 'logo_path': 'big12 logos/tcu.png'},
    {'team': 'Texas Tech', 'abbreviation': 'TTU', 'logo_path': 'big12 logos/tt.png'},
    {'team': 'UCF', 'abbreviation': 'UCF', 'logo_path': 'big12 logos/ucf.png'},
    {'team': 'Utah', 'abbreviation': 'UU', 'logo_path': 'big12 logos/uu.png'},
    {'team': 'West Virginia', 'abbreviation': 'WVU', 'logo_path': 'big12 logos/wv.png'}
]

# Function to create a two-column ranking graphic with centered text and proper spacing
def create_ranking_graphic(ranking_data, team_data, output_image_path='rankings.png'):
    # Set up some parameters
    width, height = 1600, 1200
    background_color = (255, 255, 255)  # White background
    text_color = (0, 0, 0)  # Black text
    line_color = (200, 200, 200)  # Light gray lines

    # Create the canvas
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Load a font (use a default PIL font if you don't have a custom one)
    try:
        font = ImageFont.truetype("arial.ttf", 28)  # Adjust font size
    except IOError:
        font = ImageFont.load_default()

    # Set header and starting position for text
    y_offset = 50
    header = "Big 12 Football Team Rankings"
    draw.text((width // 2 - 200, y_offset), header, font=font, fill=text_color)
    
    # Increment y_offset for spacing
    y_offset += 100

    # Define row height, column positions, and image size for logos
    row_height = 120
    logo_size = (75, 60)
    left_column_x = 50
    right_column_x = 800
    text_spacing_x = [100, 200, 350, 500]  # Define consistent spacing for team, avg, high, low

    # Prepare a dictionary to map team abbreviation to the logo path
    logo_map = {team['abbreviation']: team['logo_path'] for team in team_data}

    # Variables to control column layout
    max_rows_per_column = (len(ranking_data) + 1) // 2  # Divide into two columns
    column_row_count = 0
    x_offset = left_column_x  # Start with the left column

    # Loop through ranking data and add rows with logos and text in two columns
    for index, (team, avg, high, low) in enumerate(ranking_data):
        if column_row_count == max_rows_per_column:
            # Move to the right column after max rows in the left column
            x_offset = right_column_x
            y_offset = 150  # Reset the y_offset for the right column
            column_row_count = 0

        # Draw horizontal separator line
        draw.line([(x_offset, y_offset), (x_offset + 650, y_offset)], fill=line_color, width=2)
        y_offset += 10

        # Get the logo path and open the logo image
        logo_path = logo_map.get(team)
        if logo_path:
            try:
                logo = Image.open(logo_path).resize(logo_size)
                img.paste(logo, (x_offset, y_offset), logo.convert("RGBA"))  # Place logo without background color
            except IOError:
                print(f"Could not open logo for {team}")
        
        # Center text vertically relative to the logo
        text_bbox = font.getbbox(team)
        text_height = text_bbox[3] - text_bbox[1]  # Calculate the text height
        text_y_offset = y_offset + (logo_size[1] - text_height) // 2

        # Add team name and stats next to the logo
        draw.text((x_offset + text_spacing_x[0], text_y_offset), f"{team}", font=font, fill=text_color)
        draw.text((x_offset + text_spacing_x[1], text_y_offset), f"Avg: {avg:.2f}", font=font, fill=text_color)
        draw.text((x_offset + text_spacing_x[2], text_y_offset), f"High: {high}", font=font, fill=text_color)
        draw.text((x_offset + text_spacing_x[3], text_y_offset), f"Low: {low}", font=font, fill=text_color)

        # Increment y_offset for the next row and column_row_count
        y_offset += row_height
        column_row_count += 1

    # Save the image
    img.save(output_image_path)
    print(f"Ranking graphic saved as {output_image_path}")


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
folder_path = 'rankings/week6/'  # Specify your folder path here
rankings = average_rankings_from_folder(folder_path)

for team in rankings:
    print(team)

# create_ranking_graphic(rankings, team_data)
