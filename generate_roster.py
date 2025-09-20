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
    # Court uses 3 columns. Row 1 keeps col 3 for Bella (front right), so we only add blanks for col 1-2 on row 1.
    blank_positions = [
        '<li class="blank" data-row="1" data-col="1" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="1" data-col="2" data-sizex="1" data-sizey="1"></li>',
        # row 1, col 3 reserved for Bella
        '<li class="blank" data-row="2" data-col="1" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="2" data-col="2" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="2" data-col="3" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="3" data-col="1" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="3" data-col="2" data-sizex="1" data-sizey="1"></li>',
        '<li class="blank" data-row="3" data-col="3" data-sizex="1" data-sizey="1"></li>',
    ]

    player_html_list.extend(blank_positions)

    # Find Bella Weinhardt (#15) and place her in front right position (row 1, col 4)
    bella_player = None
    other_players = []

    for player in players:
        if player["number"] == "15" and "Bella" in player["first_name"]:
            bella_player = player
        else:
            other_players.append(player)

    # Add Bella to front right (row 1, col 3) if found
    if bella_player:
        bella_html = f'<li data-row="1" data-col="3" data-sizex="1" data-sizey="1"><h1>{bella_player["number"]}</h1><h2>{bella_player["first_name"]}<br>{bella_player["last_name"]}</h2></li>'
        player_html_list.append(bella_html)

    # Add remaining 12 players starting from row 4 in a neat 3x4 grid
    row = 4
    col = 1
    for player in other_players:
        player_html = f'<li data-row="{row}" data-col="{col}" data-sizex="1" data-sizey="1"><h1>{player["number"]}</h1><h2>{player["first_name"]}<br>{player["last_name"]}</h2></li>'
        player_html_list.append(player_html)

        col += 1
        if col > 4:  # Move to next row after 4 columns
            col = 1
            row += 1

    # Join all player HTML
    new_player_html = '\n\t\t\t'.join(player_html_list)

    # Add NET line if not present
    if 'NET' not in html_content:
        # Add NET line before gridster div
        net_line = '''        <div style="text-align: center; margin: 20px 0; font-family: monospace; font-size: 18px;">
            ═══════════════════ NET ═══════════════════
        </div>'''
        html_content = html_content.replace('<div class="gridster">', f'{net_line}\n        <div class="gridster">')

    # Replace content between the first real <ul> after the gridster div and its closing </ul>
    # This avoids matching a commented-out <ul> in the template.
    pattern = r'(<div class="gridster">[\s\S]*?)(?<!<!--)(<ul[^>]*>)([\s\S]*?)(</ul>)'
    replacement = f'\\1\\2\n\t\t\t{new_player_html}\n\n\t\t\\4'

    updated_html, count = re.subn(pattern, replacement, html_content, flags=re.DOTALL)
    if count == 0:
        # Fallback: replace the last <ul> block in the file
        pattern_last = r'(.*)(<ul[^>]*>)([\s\S]*)(</ul>)([\s\S]*)'
        updated_html = re.sub(pattern_last, f'\\1\\2\n\t\t\t{new_player_html}\n\n\t\t\\4\\5', html_content, flags=re.DOTALL)

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
