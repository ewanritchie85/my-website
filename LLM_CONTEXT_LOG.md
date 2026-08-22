# LLM Context Log — my-website

> Rolling high-signal summary for any coding assistant. Read this first — don't re-discover.

## Current Snapshot

- **Stack:** Static `HTML5/CSS3/jQuery` frontend (`index.html`, `projects.html`, `certificates.html`, `navbar.html`), `css/style.css`, `js/{functions,load-navbar,spotify-now-playing,turbo-death-warrior}.js`, Flask+Spotipy backend `backend/get_spotify_info.py` on `:5050` (`/spotify-info`), `pytest` suite `tests/` (40 tests), Nginx on Raspberry Pi (reverse proxy), GitHub Actions `test`+`deploy` pipeline `master`.
- **Hosting:** Pi at `/var/www/html` (static), `/home/ewanritchie/spotipy_project/` (Flask via `systemd: spotify-flask`), Cloudflare DNS. Local dev: `python3 -m http.server 8000` or `pytest -v` / `npm test`.
- **2026-08-22 state:** Structure refactor committed `3b7d807` (pushed). New test suite + CI gating staged (not yet committed): `tests/{conftest, test_backend_spotify, test_frontend_structure, test_javascript_logic, test_integration}.py` (40 tests), `requirements-dev.txt`, `package.json:6` `scripts.test`, `.github/workflows/actions.yaml:10` `test` job. Verified `pytest -v 40 passed` + `curl 200` on `css/style.css`/`js/*.js`. Untracked: `AGENTS.md`.
- **Live content:** 11 project sections in `projects.html:22-33` (NikitAI, Turbo Death Warrior, Spotify API, Notebook Data, Met Office ETL, Word Wheel, Task Manager, My Website, Ten10 x2, Northcoders).

## Architecture

```
my-website/
├── index.html / projects.html / certificates.html / navbar.html / favicon.ico
├── css/style.css
├── js/{functions.js, load-navbar.js, spotify-now-playing.js, turbo-death-warrior.js}
├── images/{logos/, certs/, nikitai_screenshots/, notebook_data_graphs/, ...}
├── backend/{get_spotify_info.py, requirements.txt, run-spotipy}
├── tests/{conftest.py, test_backend_spotify.py, test_frontend_structure.py, test_javascript_logic.py, test_integration.py}
├── requirements-dev.txt
├── .github/workflows/actions.yaml  # test (ubuntu-latest) -> deploy (self-hosted, needs:test)
├── .editorconfig / .gitattributes / .gitignore
└── LLM_CONTEXT_LOG.md / README.md / AGENTS.md / package.json
```

- **Frontend routing:** No bundler. `js/load-navbar.js:1` `fetch('navbar.html')` → `#site-navbar`. `js/functions.js:1` handles `.project` show/hide, lightbox, Word Wheel `POST /api/solve` → expects `{words:[]}`.
- **Dynamic:** Spotify section `projects.html:91` triggers `js/spotify-now-playing.js` → `GET /spotify-info` → renders `currently_playing` + `top_tracks` (10, `short_term`). Backend: `backend/get_spotify_info.py:22` `SpotifyOAuth` (`user-read-currently-playing user-top-read`, `cache_path` from `SPOTIPY_CACHE_PATH`, `open_browser=False`).
- **Infra:** Nginx serves `/var/www/html`, proxies `/spotify-info→127.0.0.1:5050` and `/api/solve` → Word Wheel backend, `/tdw-api/` → Turbo Death Warrior service. `backend/run-spotipy:1` creates `venv`, installs `backend/requirements.txt` ( `flask`, `python-dotenv` ), runs `get_spotify_info.py`.
- **Deploy:** `.github/workflows/actions.yaml:10-53` — `test` job on `ubuntu-latest` (`actions/checkout@v5`, `actions/setup-python@v6` Node 24, `setup-python 3.11`, `pip install -r backend/requirements.txt -r requirements-dev.txt`, `pytest -v`) gates `deploy` job (`needs:test`, `if: refs/heads/master`, `runs-on:self-hosted`, `actions/checkout@v5`) → `sudo cp backend/get_spotify_info.py` + `systemctl restart spotify-flask` → `rm -rf /var/www/html/*` + `cp -r ./*` → `rm -rf backend/tests/.pytest_cache` + `reload nginx`. `cp -r ./*` intentionally skips dotfiles (`.env` never deployed). Local `npm test` → `pytest -v` via `package.json:7`. Requires self-hosted runner ≥ v2.327.1 for Node 24 (checkout v5 / setup-python v6).

## Safety + Auth Boundaries

- **Secrets:** `SPOTIPY_CLIENT_ID/SECRET/REDIRECT_URI` in `.env:1` (gitignored `.gitignore:8`), loaded via `load_dotenv()` `backend/get_spotify_info.py:6`. `.env` never committed or deployed (`cp ./*` skips dotfiles, `.gitignore:8`). `SPOTIFY_ACCESS_TOKEN` in `.env` is ephemeral.
- **Spotify auth:** `backend/get_spotify_info.py:18` `SpotifyOAuth` with `cache_path=BASE_DIR/.spotipy_cache` or `SPOTIPY_CACHE_PATH` (systemd override on Pi). `scope` limited to read-only playback/top-read.
- **NikitAI note:** Not hosted here — separate FastAPI repo — but docs note human-confirmation gate for side-effects (MSAL device-code flow).
- **OS hygiene:** `.gitignore:14-16` ignores `.DS_Store/**/.DS_Store`; `images/logos/.DS_Store` removed from index `2026-08-22`. `venv/` + `__pycache__/` ignored. `Thumbs.db` ignored.
- **Production exposure:** `actions.yaml:25` removes `backend/` from web root so Flask source not web-accessible. Nginx is TLS termination point.

## Active Priorities

- [x] Commit & push 2026-08-22 refactor `3b7d807` — done.
- [ ] Deploy with new test gate — push test suite and watch `test` → `deploy` on Pi (verify `spotify-flask` restart).
- [ ] Verify Nginx proxy still routes `/spotify-info` and `/api/solve`/`/tdw-api/` → test live Spotify + Word Wheel + TDW after deploy.
- [ ] Consider `venv/` cleanup on Pi (`backend/run-spotipy` creates its own venv inside `spotipy_project/`; repo `venv/` is local-only).
- [ ] Add `robots.txt`/`404.html` and subresource integrity if adding bundler later — deferred.

## Change Log Entries

### 2026-08-22 — NikitAI Trainer domain implemented — update project description

- **Date:** 2026-08-22
- **Scope:** `projects.html:44-67`
- **Summary:** Updated NikitAI intro to mark `Trainer` as implemented (ingests Garmin Connect activity/sleep/HR/HRV/Body Battery to summarise load/recovery/readiness) and `Platform Nerd` as active (systemd/Nginx/Runner awareness); trimmed `Next up` to exclude Trainer (`expanding the Platform Nerd domain`).
- **Why:** Trainer sub-agent is now live, matching the new `nikitai_screengrab_trainer.jpg` evidence — prior copy said `Trainer ... is planned next`.
- **Impact:** `projects.html:49-51` now lists all three sub-agents as operational; `projects.html:66-67` roadmap no longer lists Trainer as future work.
- **Validation:** Verified `projects.html:44-67` text via file read; `pytest -q` still 40 passed; no lightbox/CSS/JS change.
- **Follow-ups:** None. Future: consider adding Garmin sync detail/tech stack icon if Trainer gets dedicated logo.

### 2026-08-22 — NikitAI screenshots: three-domain gallery side-by-side

- **Date:** 2026-08-22
- **Scope:** `projects.html:79-86`, `images/nikitai_screenshots/nikitai_screengrab_organiser.jpg` (new), `images/nikitai_screenshots/nikitai_screengrab_platform_nerd.jpg` (new), `images/nikitai_screenshots/nikitai_screengrab_trainer.jpg` (new), `images/nikitai_screenshots/nikitai-screengrab1.jpg` (deleted), `images/nikitai_screenshots/nikitai-screengrab2.jpg` (deleted), `images/nikitai_screenshots/calendar-event.jpg` (deleted)
- **Summary:** Replaced NikitAI `Example Interaction` gallery (2 + 1 stacked images) with single flex row of 3 images side-by-side: Organiser (left), Platform Nerd (centre), Trainer (right) at `300×340` `object-fit:cover` within `.example-data-gallery.analysis-gallery`.
- **Why:** User supplied new domain-specific captures; requested side-by-side layout preserving existing click-to-expand/close lightbox.
- **Impact:** `projects.html:81-84` now references new filenames in correct order; lightbox unchanged (`js/functions.js:43` `'.analysis-gallery img'` selector still applies, no JS/CSS change needed, responsive wrap via `flex-wrap`).
- **Validation:** Verified `projects.html:79-86` order organiser→platform_nerd→trainer; `ls images/nikitai_screenshots/` shows 3 new jpgs (112K/106K/150K), old 3 deleted; `grep 'nikitai_screengrab'` confirms 3 hits with correct alt text.
- **Follow-ups:** None. Old images removed from index; deploy will `cp -r ./*` new screenshots to `/var/www/html/images/nikitai_screenshots/`.

### 2026-08-22 — Fix Node 20 deprecation in GitHub Actions (checkout v5 / setup-python v6)

- **Date:** 2026-08-22
- **Scope:** `.github/workflows/actions.yaml:13,16,37`
- **Summary:** Bumped `actions/checkout@v4→@v5` (test + deploy jobs) and `actions/setup-python@v5→@v6` to Node 24 runtime.
- **Why:** GitHub warns `Node.js 20 is deprecated` and force-runs `checkout@v4`/`setup-python@v5` on Node 24; scheduled removal 2026-09-16. Bump silences warnings per https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/.
- **Impact:** Both `test` (ubuntu-latest) and `deploy` (self-hosted) jobs now run natively on Node 24; no behavior change.
- **Validation:** `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/actions.yaml'))"` → `yaml ok`; verified file shows `checkout@v5` (x2) and `setup-python@v6`.
- **Follow-ups:** Ensure Pi self-hosted runner ≥ v2.327.1 (`actions/runner` release for Node 24) else `checkout@v5` will fail to run.

### 2026-08-22 — Reorder Turbo Death Warrior to second in projects list

- **Date:** 2026-08-22
- **Scope:** `projects.html:22-33`
- **Summary:** Moved `<li data-project="turbo-death-warrior">` from sixth to second position, directly underneath `nikitai`, in `.project-list`.
- **Why:** Requested prominence for Turbo Death Warrior as second item.
- **Impact:** Visual order on `/projects.html` now NikitAI → Turbo Death Warrior → Spotify API → …; no JS logic change (selection by `data-project` id).
- **Validation:** Verified `projects.html:22-33` order via file read; `li` sequence correct.
- **Follow-ups:** Optionally reorder `div#turbo-death-warrior` content block to match list order (currently remains after `word-wheel-solver`).

### 2026-08-22 — Full test suite + CI gating (staged)

- **Date:** 2026-08-22
- **Scope:** `tests/conftest.py` (new), `tests/test_backend_spotify.py` (new, 11 tests), `tests/test_frontend_structure.py` (new, 17 tests), `tests/test_javascript_logic.py` (new, 10 tests), `tests/test_integration.py` (new, 2 tests), `requirements-dev.txt` (new), `.github/workflows/actions.yaml`, `package.json`, `.gitignore`, `venv/` (deps installed)
- **Summary:** Added 40-test `pytest` suite (backend mocked `spotipy`, frontend BeautifulSoup, JS pure-function emulation, integration `http.server` smoke) and `test` job in `actions.yaml:10` that installs `backend/requirements.txt` + `requirements-dev.txt` and runs `pytest -v` on `ubuntu-latest`, gating `deploy` (`needs:test`, `if: master`, `runs-on:self-hosted`). Updated `package.json:7` `scripts.test: pytest -v`, extended `.gitignore:8` with `.venv/.pytest_cache/.spotipy_cache/*.log`, and cleaned deploy step to purge `tests/.pytest_cache/requirements-dev.txt` from web root.
- **Why:** No automated verification prior; deploy copied untested static + Flask code directly to Pi. Need regression safety for asset refs, `Pi files→backend` rename, `CRLF` fixes, and API error paths.
- **Impact:** `push:master` now fails fast if tests break; local `pytest -v` / `npm test` / `venv/bin/python -m pytest` all 40 passed; Pi only deploys after `test` greens.
- **Validation:** `~/.pyenv/versions/3.11.1/bin/python -m pytest tests/ -v` → `40 passed in 1.23s`; `venv/bin/python -m pytest -q` → `40 passed in 1.89s`; `python -c "import yaml; yaml.safe_load(open('.github/workflows/actions.yaml'))"` → syntax ok; `git diff --cached --stat` → 8 paths for this entry.
- **Follow-ups:** Push and watch GitHub Actions `test` → `deploy`; add coverage (`pytest-cov`) and `flake8` later if desired.

### 2026-08-22 — Project structure best-practice refactor (committed 3b7d807)

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
