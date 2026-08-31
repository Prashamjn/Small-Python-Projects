# YouTube Playlist Builder

A Python terminal application that lets you create a real YouTube playlist by typing song names instead of manually pasting YouTube URLs.

## Features

- Search YouTube by song name
- Show the top 5 video matches
- Choose the correct video
- Add songs one by one
- `list` command
- `remove N` command
- `clear` command
- `stop` command to finish
- Creates an actual YouTube playlist
- Adds selected videos in the same order
- Creates the playlist as private by default
- Uses Google OAuth 2.0
- Keeps OAuth token and client credentials out of Git

## Requirements

- Python 3.10+
- A Google account with a YouTube channel
- A Google Cloud project with YouTube Data API v3 enabled
- OAuth 2.0 Desktop App credentials

## Installation

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Google Cloud setup

1. Open Google Cloud Console.
2. Create a project.
3. Enable **YouTube Data API v3**.
4. Configure the OAuth consent screen.
5. Create an OAuth 2.0 Client ID.
6. Choose **Desktop app** as the application type.
7. Download the JSON credentials.
8. Rename the downloaded file to:

```text
client_secret.json
```

9. Put `client_secret.json` in the project root.

Do NOT commit this file to GitHub.

## Run

```powershell
python main.py
```

The first run opens a Google authorization page in your browser.

After authorization, the program stores a local `token.json` file so you normally do not have to sign in every time.

Do NOT commit `token.json`.

## Example

```text
Playlist name: Evening Songs

Song 1: Tum Hi Ho Arijit Singh

[1] Tum Hi Ho - Aashiqui 2
[2] Tum Hi Ho - Live
[3] Tum Hi Ho - Acoustic Cover
[4] Tum Hi Ho - Slowed
[5] Tum Hi Ho - Lyrics

Choose a result: 1

✓ Added: Tum Hi Ho

Song 2: Kesariya Arijit Singh

...

Song 3: stop
```

The playlist is created as private by default.

## Security

Never commit:

- `client_secret.json`
- `token.json`
- `.env`
- API keys
- OAuth tokens
- passwords

The included `.gitignore` already excludes the OAuth files.

## API quota

YouTube Data API operations consume quota. Searching uses the `search.list` endpoint, while playlist creation and adding playlist items consume additional quota. Avoid unnecessary repeated searches.

## License

Choose a license appropriate for your project before publishing.
