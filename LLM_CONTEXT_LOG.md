# LLM Context Log — my-website

> Rolling high-signal summary for any coding assistant. Read this first — don't re-discover.

## Current Snapshot

- **Stack:** Static `HTML5/CSS3/jQuery` frontend (`index.html`, `projects.html`, `certificates.html`, `navbar.html`), `css/style.css`, `js/{functions,load-navbar,spotify-now-playing,turbo-death-warrior}.js`, Flask+Spotipy backend `backend/get_spotify_info.py` on `:5050` (`/spotify-info`), Nginx on Raspberry Pi (reverse proxy), GitHub Actions self-hosted runner `master`.
- **Hosting:** Pi at `/var/www/html` (static), `/home/ewanritchie/spotipy_project/` (Flask via `systemd: spotify-flask`), Cloudflare DNS. Local dev: `python3 -m http.server 8000`.
- **2026-08-22 state:** Structure refactor + context log staged but **not yet committed** on `master` (ahead of `origin/master`). `git status` shows 19 staged paths: renames `style.css->css/style.css`, `*.js->js/*.js`, `Pi files/->backend/`, plus `.editorconfig/.gitattributes`, `LLM_CONTEXT_LOG.md` (new), fixes to `*.html`, `README.md`, `package.json`, `.gitignore`, `.github/workflows/actions.yaml`. Verified `200` via `curl` on `css/style.css` and `js/*.js`. Untracked ignored: `.cache`, `.DS_Store`, `venv/` (`AGENTS.md` untracked).
- **Live content:** 11 project sections in `projects.html:22-33` (NikitAI, Spotify API, Notebook Data, Met Office ETL, Word Wheel, Turbo Death Warrior, Task Manager, My Website, Ten10 x2, Northcoders).

## Architecture

```
my-website/
├── index.html / projects.html / certificates.html / navbar.html / favicon.ico
├── css/style.css
├── js/{functions.js, load-navbar.js, spotify-now-playing.js, turbo-death-warrior.js}
├── images/{logos/, certs/, nikitai_screenshots/, notebook_data_graphs/, ...}
├── backend/{get_spotify_info.py, requirements.txt, run-spotipy}
├── .github/workflows/actions.yaml
├── .editorconfig / .gitattributes / .gitignore
└── LLM_CONTEXT_LOG.md / README.md / AGENTS.md
```

- **Frontend routing:** No bundler. `js/load-navbar.js:1` `fetch('navbar.html')` → `#site-navbar`. `js/functions.js:1` handles `.project` show/hide, lightbox, Word Wheel `POST /api/solve` → expects `{words:[]}`.
- **Dynamic:** Spotify section `projects.html:91` triggers `js/spotify-now-playing.js` → `GET /spotify-info` → renders `currently_playing` + `top_tracks` (10, `short_term`). Backend: `backend/get_spotify_info.py:22` `SpotifyOAuth` (`user-read-currently-playing user-top-read`, `cache_path` from `SPOTIPY_CACHE_PATH`, `open_browser=False`).
- **Infra:** Nginx serves `/var/www/html`, proxies `/spotify-info→127.0.0.1:5050` and `/api/solve` → Word Wheel backend, `/tdw-api/` → Turbo Death Warrior service. `backend/run-spotipy:1` creates `venv`, installs `backend/requirements.txt` ( `flask`, `python-dotenv` ), runs `get_spotify_info.py`.
- **Deploy:** `.github/workflows/actions.yaml:16-29` on `push:master` → `sudo cp backend/get_spotify_info.py /home/ewanritchie/spotipy_project/` + `systemctl restart spotify-flask` → `rm -rf /var/www/html/*` + `cp -r ./*` → `rm -rf backend` + `reload nginx`. `cp -r ./*` intentionally skips dotfiles (`.env` never deployed).

## Safety + Auth Boundaries

- **Secrets:** `SPOTIPY_CLIENT_ID/SECRET/REDIRECT_URI` in `.env:1` (gitignored `.gitignore:8`), loaded via `load_dotenv()` `backend/get_spotify_info.py:6`. `.env` never committed or deployed (`cp ./*` skips dotfiles, `.gitignore:8`). `SPOTIFY_ACCESS_TOKEN` in `.env` is ephemeral.
- **Spotify auth:** `backend/get_spotify_info.py:18` `SpotifyOAuth` with `cache_path=BASE_DIR/.spotipy_cache` or `SPOTIPY_CACHE_PATH` (systemd override on Pi). `scope` limited to read-only playback/top-read.
- **NikitAI note:** Not hosted here — separate FastAPI repo — but docs note human-confirmation gate for side-effects (MSAL device-code flow).
- **OS hygiene:** `.gitignore:14-16` ignores `.DS_Store/**/.DS_Store`; `images/logos/.DS_Store` removed from index `2026-08-22`. `venv/` + `__pycache__/` ignored. `Thumbs.db` ignored.
- **Production exposure:** `actions.yaml:25` removes `backend/` from web root so Flask source not web-accessible. Nginx is TLS termination point.

## Active Priorities

- [ ] Commit & push staged 2026-08-22 refactor (verify Pi deploy succeeds; `spotify-flask` restarts).
- [ ] Verify Nginx proxy still routes `/spotify-info` and `/api/solve` → test live Spotify + Word Wheel after deploy.
- [ ] Remove local `Pi files/` reference drift (grep confirms none); update any external docs linking to old path.
- [ ] Consider `venv/` cleanup on Pi (`backend/run-spotipy` creates its own venv inside `spotipy_project/`; repo `venv/` is local-only).
- [ ] Add `robots.txt`/`404.html` and subresource integrity if adding bundler later — deferred.

## Change Log Entries

### 2026-08-22 — Project structure best-practice refactor (staged)

- **Date:** 2026-08-22
- **Scope:** `index.html`, `projects.html` (+copy edit `oldschool→old school`), `certificates.html`, `css/style.css` (from `style.css`), `js/*.js` (from `*.js`), `Pi files/`→`backend/`, `.gitignore`, `.editorconfig` (new), `.gitattributes` (new), `README.md`, `package.json`, `.github/workflows/actions.yaml`, `images/logos/.DS_Store` (deleted), `LLM_CONTEXT_LOG.md` (new)
- **Summary:** Fixed broken asset refs after `css/`/`js/` split (`href="style.css"`→`css/style.css`, `src="functions.js"`→`js/functions.js` etc. — 8 refs across 3 HTML files); renamed `Pi files` (space) → `backend` via `git mv`; removed tracked `images/logos/.DS_Store`; normalized `CRLF→LF` on 4 files (`index.html`, `projects.html`, `css/style.css`, `js/functions.js`) and added `.editorconfig`/` .gitattributes` (`* text=auto eol=lf`); updated `.gitignore` to `venv/__pycache__/**/.DS_Store/.cache`; fixed `package.json` (`main`/`directories.doc` → `private:true`); updated `README.md:36-99` structure docs; fixed `actions.yaml:18,25` to `backend/` and to purge `backend/.editorconfig` from web root.
- **Why:** Previous layout left `css/`/`js/` untracked (`??` in `git status`) while `style.css`/`*.js` marked `D` — live site would 404. Space in `Pi files/` breaks quoting/tooling. Tracked `.DS_Store` and `CRLF` caused noisy diffs. `package.json:5` `main: functions.js` was invalid.
- **Impact:** Static site now resolves via `python3 -m http.server 8000` and Nginx `/var/www/html` without 404s; deploy workflow quotes no longer needed; repo `git ls-files` clean; diffs are `LF`-only.
- **Validation:** `git diff --cached --stat` — 19 paths (including `LLM_CONTEXT_LOG.md`), `R094-R100` renames, `D images/logos/.DS_Store`; `grep -n 'href="css\|src="js' index.html projects.html certificates.html` — 8 hits correct; `curl -w "%{http_code}" http://127.0.0.1:8001/css/style.css` `200`, `js/functions.js` `200`, `js/load-navbar.js` `200`, `js/spotify-now-playing.js` `200`; `git check-ignore -v .cache` → `.gitignore:20:.cache`; no `grep -r "Pi files"` hits.
- **Follow-ups:** Commit/push staged changes; smoke-test Pi deploy (`systemctl status spotify-flask`, live `/spotify-info`); audit Nginx conf for `/spotify-info` proxy still pointing at `:5050`.

## Update Protocol

- **When:** After any meaningful code change (feature, fix, refactor, infra, docs with architectural impact).
- **Where:** Append entry under `## Change Log Entries` newest-first, and if change touches snapshot/architecture/safety/auth/priorities, update those sections in place (don't rely on log alone).
- **Format per entry:**
  ```
  ### YYYY-MM-DD — <short title>
  - **Date:** YYYY-MM-DD
  - **Scope:** comma-separated file paths (prefer paths over prose)
  - **Summary:** 1-3 factual sentences
  - **Why:** reason/motivation
  - **Impact:** user/infra/repo effect
  - **Validation:** commands/tests/files checked (e.g., `curl 200`, `pytest`, `git diff --stat`)
  - **Follow-ups:** TODOs/deferred items
  ```
- **Style:** Factual, short, file-path-centric. No speculation. Verify via execution before logging.
