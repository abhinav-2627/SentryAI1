from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json", SCOPES
)
creds = flow.run_local_server(port=0)

youtube = build("youtube", "v3", credentials=creds)

req = youtube.channels().list(
    part="snippet",
    mine=True
)
res = req.execute()

print("✅ Connected to channel:", res["items"][0]["snippet"]["title"])
