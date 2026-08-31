from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

BASE_DIR = Path(__file__).resolve().parent

CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "token.json"


def get_youtube_service():

    # --------------------------------------------------------
    # Check OAuth client file
    # --------------------------------------------------------

    if not CLIENT_SECRET_FILE.exists():

        raise FileNotFoundError(
            "\nclient_secret.json was not found.\n\n"
            "Put your Google OAuth Desktop App JSON file "
            "in the same folder as main.py.\n"
        )


    credentials = None


    # --------------------------------------------------------
    # Load existing token
    # --------------------------------------------------------

    if TOKEN_FILE.exists():

        credentials = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES
        )


    # --------------------------------------------------------
    # Refresh expired token
    # --------------------------------------------------------

    if credentials:

        if credentials.expired and credentials.refresh_token:

            print("\nRefreshing Google authorization...")

            credentials.refresh(Request())


    # --------------------------------------------------------
    # First-time authentication
    # --------------------------------------------------------

    if not credentials or not credentials.valid:

        print("\nGoogle authorization required.")
        print("Opening your browser...")

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CLIENT_SECRET_FILE),
            SCOPES
        )

        credentials = flow.run_local_server(
            host="localhost",
            port=0,
            access_type="offline",
            prompt="consent",
            open_browser=True
        )


    # --------------------------------------------------------
    # Save token
    # --------------------------------------------------------

    TOKEN_FILE.write_text(
        credentials.to_json(),
        encoding="utf-8"
    )


    # --------------------------------------------------------
    # Create YouTube API client
    # --------------------------------------------------------

    youtube = build(
        "youtube",
        "v3",
        credentials=credentials,
        cache_discovery=False
    )


    return youtube