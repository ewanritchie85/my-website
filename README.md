
# My Personal Website

This repository contains the source code for my portfolio website. It is a static HTML/CSS/JavaScript site with a couple of dynamic integrations served from backend APIs.

The site is hosted on my Raspberry Pi behind Nginx, and deployment is automated with GitHub Actions on a self-hosted runner.

## Live Site Content

The website currently has three top-level pages:

- About Me page
- Projects page
- Certificates page

The Projects page includes sections for:

- NikitAI
- Spotify API
- Notebook Data Analysis Refresher
- Met Office ETL Pipeline
- Word Wheel Solver
- Task Manager App
- This Website
- Ten10 Platform Training
- Ten10 Core Training
- Northcoders

## Tech Stack

- HTML5
- CSS3
- JavaScript (jQuery)
- Nginx on Raspberry Pi (hosting)
- GitHub Actions (deployment)
- Python Flask + Spotipy (Spotify backend in backend/)

## Repository Structure

- index.html: About Me page
- projects.html: Interactive projects page
- certificates.html: Certificates gallery
- navbar.html + js/load-navbar.js: Shared navbar injected into each page
- js/functions.js: Core client-side behavior (project switching, lightbox, Word Wheel form submit)
- js/spotify-now-playing.js: Fetches and renders Spotify data from spotify-info endpoint
- js/turbo-death-warrior.js: CRT terminal game frontend
- css/style.css: Global styling and responsive layout
- images/: Logos, screenshots, diagrams, certificates, and profile image
- backend/get_spotify_info.py: Flask app exposing spotify-info endpoint
- backend/run-spotipy: Helper script to create venv, install deps, and run Flask app
- backend/requirements.txt: Python dependencies for Spotify backend

## Dynamic Features

### 1. Spotify Now Playing

Frontend behavior:

- Triggered when Spotify API project section is opened on projects page.
- Calls spotify-info and renders:
  - currently playing track
  - monthly top tracks

Backend behavior:

- Implemented in backend/get_spotify_info.py.
- Flask route: /spotify-info
- Default Flask bind: 0.0.0.0:5050
- Uses environment variables:
  - SPOTIPY_CLIENT_ID
  - SPOTIPY_CLIENT_SECRET
  - SPOTIPY_REDIRECT_URI

### 2. Word Wheel Solver

Frontend behavior:

- Form on the projects page posts JSON to /api/solve.
- Expects a response shape containing words array.

Note: This repository contains only the frontend call for /api/solve. The solver backend is expected to be hosted separately and reverse-proxied by Nginx.

## Local Development

To preview the static site locally from the repository root:

python3 -m http.server 8000

Then open:

- http://localhost:8000/index.html
- http://localhost:8000/projects.html
- http://localhost:8000/certificates.html

If no local backend is running, Spotify and Word Wheel API sections will not return live data.

## Spotify Backend (backend/)

From backend/ directory:

1. Ensure python3 and python3-venv are installed.
2. Create a .env file with SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI.
3. Run:

./run-spotipy

This script will:

- create venv if missing
- upgrade pip
- install dependencies from requirements.txt
- run get_spotify_info.py

## Deployment (Current Workflow)

GitHub Actions workflow file:

- .github/workflows/actions.yaml

Current workflow behavior on push to master:

1. Runs on self-hosted runner.
2. Checks out repository.
3. Removes existing files from /var/www/html.
4. Copies repository files into /var/www/html.
5. Reloads Nginx.

## Production Routing Notes

For full site functionality in production, Nginx should:

- serve static files from web root
- route /spotify-info to Flask app on port 5050
- route /api/solve to Word Wheel backend service

## License

Personal and educational use.
