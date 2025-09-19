# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a volleyball lineup interactive app for coaches to experiment with player lineups. It's a client-side web application built with HTML, CSS, and jQuery using the Gridster.js library for drag-and-drop functionality.

## Architecture

The app uses a simple static web architecture:

- **Main HTML files**: `vb.html`, `vb22.html`, `vb23.html`, `vbORIG.html` - Different versions of the lineup interface
- **Core dependencies**: jQuery 1.7.1+ and Gridster.js for the draggable grid layout
- **Styling**: Custom CSS in `assets/css/styles.css` and Gridster CSS for grid functionality
- **Structure**: 6x4 grid representing volleyball court positions with player cards

## Key Components

### Grid Layout (`vb.html`)
- Uses Gridster.js to create a draggable grid system
- Players are represented as `<li>` elements with jersey numbers and names
- Grid positions use `data-row`, `data-col`, `data-sizex`, `data-sizey` attributes
- Blank positions have `class="blank"` and reduced opacity

### Player Cards
- Display jersey number (h1) and player name (h2)
- Names are split across two lines for better layout
- Cards are styled with shadows and white backgrounds

### File Organization
```
/assets/css/        - Main stylesheets
/dist/              - Gridster.js distribution files
/js/                - Additional JavaScript (mostly empty)
vb.html             - Current/latest version
vb22.html, vb23.html - Previous versions
```

## Development Commands

This is a static HTML/CSS/JS project with no build system:

- **Development**: Open `vb.html` directly in a web browser or serve via local HTTP server
- **Local server**: `python -m http.server 8000` or `npx http-server`
- **No build process**: Files can be edited directly and refreshed in browser
- **No tests**: Currently no test framework in place

## GitHub Pages Preparation

For hosting on GitHub Pages:

1. The main file should be `index.html` (rename `vb.html`)
2. All assets are already using relative paths
3. CDN dependencies (jQuery) should work fine
4. No build step required - can deploy directly

## Current State

- Multiple HTML versions exist (likely different seasons/teams)
- Uses jQuery 1.7.1 (very outdated - should be modernized)
- Gridster.js for drag-and-drop (also outdated)
- No package.json or modern build tooling
- Static player data hardcoded in HTML