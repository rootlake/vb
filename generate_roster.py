#!/usr/bin/env python3
"""
Script to generate volleyball lineup HTML from CSV roster data.
Usage: python generate_roster.py [roster.csv] [template.html] [output.html]
"""

import csv
import sys
import re
from pathlib import Path

def read_roster(csv_file):
    """Read roster data from CSV file."""
    players = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append({
                'number': row['number'],
                'first_name': row['first_name'],
                'last_name': row['last_name']
            })
    return players

def generate_player_html(player):
    """Generate HTML for a single player card."""
    return f'<li data-row="4" data-col="1" data-sizex="1" data-sizey="1"><h1>{player["number"]}</h1><h2>{player["first_name"]}<br>{player["last_name"]}</h2></li>'

def generate_blank_html():
    """Generate HTML for a blank position."""
    return '<li class="blank" data-row="1" data-col="1" data-sizex="1" data-sizey="1"></li>'

def update_html_with_roster(template_file, output_file, players):
    """Update HTML template with new roster data."""
    with open(template_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Generate player HTML
    player_html_list = []

    # Add blank positions for court layout (rows 1-3)
    blank_positions = [
        '<li class="blank" data-row="1" data-col="1" data-sizex="1" data-sizey="1"></li>',
        '<li data-row="1" data-col="2" data-sizex="1" data-sizey="1"><h1>--</h1><h2>Front<br>Center</h2></li>',
        '<li class="blank" data-row="1" data-col="3" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="2" data-col="1" data-sizex="1" data-sizey="1"></li>',
        '<li data-row="2" data-col="2" data-sizex="1" data-sizey="1"><h1>--</h1><h2>Back<br>Center</h2></li>',
        '<li class="blank" data-row="2" data-col="3" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="2" data-col="4" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="3" data-col="1" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="3" data-col="2" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="3" data-col="3" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="3" data-col="4" data-sizex="1" data-sizey="1"></li>',
    ]

    player_html_list.extend(blank_positions)

    # Add players starting from row 4
    row = 4
    col = 1
    for player in players:
        player_html = f'<li data-row="{row}" data-col="{col}" data-sizex="1" data-sizey="1"><h1>{player["number"]}</h1><h2>{player["first_name"]}<br>{player["last_name"]}</h2></li>'
        player_html_list.append(player_html)

        col += 1
        if col > 4:  # Move to next row after 4 columns
            col = 1
            row += 1

    # Join all player HTML
    new_player_html = '\n\t\t\t'.join(player_html_list)

    # Replace the content between <ul> and </ul> tags
    pattern = r'(<ul[^>]*>)(.*?)(</ul>)'
    replacement = f'\\1\n\t\t\t{new_player_html}\n\n\t\t\\3'

    updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

    # Write the updated HTML
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(updated_html)

    print(f"Generated {output_file} with {len(players)} players")

def main():
    # Default file names
    csv_file = sys.argv[1] if len(sys.argv) > 1 else 'roster.csv'
    template_file = sys.argv[2] if len(sys.argv) > 2 else 'vb.html'
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'index.html'

    # Check if files exist
    if not Path(csv_file).exists():
        print(f"Error: CSV file '{csv_file}' not found")
        sys.exit(1)

    if not Path(template_file).exists():
        print(f"Error: Template file '{template_file}' not found")
        sys.exit(1)

    try:
        # Read roster data
        players = read_roster(csv_file)
        print(f"Loaded {len(players)} players from {csv_file}")

        # Generate HTML
        update_html_with_roster(template_file, output_file, players)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()