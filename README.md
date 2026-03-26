
# My Personal Website

This is the source code for my portfolio website, designed to showcase my skills, projects, and experience in platform engineering and data engineering. It is hosted using Nginx on my Raspberry Pi at home.

## Features

- Hosted on a Raspberry Pi with Nginx
- CI/CD deployment using GitHub Actions
- Live Spotify listening data displayed via a custom API

## Deployment

The site is deployed to a Raspberry Pi running Nginx. On push to the main branch, a GitHub Actions workflow copies the site files over SSH and reloads the Nginx service.

a GitHub Actions workflow copies the site files over SSH and reloads the Nginx service.
## Tech Stack

- HTML5, CSS3, JavaScript
- Nginx (hosting)
- GitHub Actions (CI/CD)
- Raspberry Pi (Ubuntu Server)
- Python (Flask, Spotipy) for Spotify API

## Spotify API Integration

- A Flask app runs on the Raspberry Pi, using Spotipy to fetch current listening and top track data from Spotify.
- The Flask app serves a `/spotify-info` JSON endpoint, proxied by Nginx and accessible to all website visitors.
- The Flask app is managed as a systemd service, ensuring it runs in the background and starts automatically on reboot.
- The website fetches and displays live Spotify data using this endpoint.

## License

This project is for personal and educational use.
