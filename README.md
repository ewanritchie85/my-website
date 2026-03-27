
# My Personal Website

a GitHub Actions workflow copies the site files over SSH and reloads the Nginx service.

# My Personal Website

This is the source code for my portfolio website, designed to showcase my skills, projects, and projects in platform engineering and data engineering. It is hosted using Nginx on my Raspberry Pi at home.

## Features

- Hosted on a Raspberry Pi with Nginx
- CI/CD deployment using GitHub Actions
- Live Spotify listening data displayed via a custom API

## Tech Stack

- HTML5, CSS3, JavaScript
- Nginx (hosting)
- GitHub Actions (CI/CD)
- Raspberry Pi (Ubuntu Server)
- Python (Flask, Spotipy) for Spotify API

## Deployment Overview

The site is deployed to a Raspberry Pi running Ubuntu Server and Nginx. On push to the main branch, a GitHub Actions workflow copies the site files over SSH and reloads the Nginx service.

## Hosting & Backend Setup

### 1. Raspberry Pi Setup
- Install Ubuntu Server on your Raspberry Pi.
- Set up a static IP or use Dynamic DNS for remote access.
- Install required packages:
	```sh
	sudo apt update && sudo apt install nginx python3 python3-pip python3-venv git
	```

### 2. Clone the Repository
- Clone this repo to your Pi:
	```sh
	git clone <your-repo-url>
	cd my-website
	```

### 3. Set Up the Python Backend (Spotify API)
- Create a Python virtual environment and install dependencies:
	```sh
	python3 -m venv venv
	source venv/bin/activate
	pip install flask spotipy
	```
- Add your Spotify API credentials to the backend config or environment variables as required by your Flask app.

### 4. Create a systemd Service for Flask
- Create a file at `/etc/systemd/system/spotify-flask.service`:
	```ini
	[Unit]
	Description=Spotify Flask Backend
	After=network.target

	[Service]
	User=pi
	WorkingDirectory=/home/pi/my-website/Pi files
	ExecStart=/home/pi/my-website/venv/bin/python3 /home/pi/my-website/Pi files/get_spotify_info.py
	Restart=always
	Environment=FLASK_ENV=production

	[Install]
	WantedBy=multi-user.target
	```
- Reload systemd and start the service:
	```sh
	sudo systemctl daemon-reload
	sudo systemctl enable spotify-flask
	sudo systemctl start spotify-flask
	sudo systemctl status spotify-flask
	```

### 5. Nginx Configuration
- Edit `/etc/nginx/sites-available/default` (or your custom site config):
	```nginx
	server {
			listen 80;
			server_name your.domain.com;
			root /home/pi/my-website;
			index index.html;

			location / {
					try_files $uri $uri/ =404;
			}

			location /spotify-info {
					proxy_pass http://127.0.0.1:5000/spotify-info;
					proxy_set_header Host $host;
					proxy_set_header X-Real-IP $remote_addr;
					proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
					proxy_set_header X-Forwarded-Proto $scheme;
			}
	}
	```
- Test and reload Nginx:
	```sh
	sudo nginx -t
	sudo systemctl reload nginx
	```

### 6. GitHub Actions CI/CD
- Set up a GitHub Actions workflow to deploy on push:
	- Use `scp` or `rsync` to copy files to the Pi.
	- Use `ssh` to reload Nginx and restart the Flask service.

## Spotify API Integration
- The Flask app runs on the Pi, using Spotipy to fetch current listening and top track data from Spotify.
- The Flask app serves a `/spotify-info` JSON endpoint, proxied by Nginx and accessible to all website visitors.
- The Flask app is managed as a systemd service, ensuring it runs in the background and starts automatically on reboot.
- The website fetches and displays live Spotify data using this endpoint.

## License

This project is for personal and educational use.
