from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json", SCOPES
)
creds = flow.run_local_server(port=0)

youtube = build("youtube", "v3", credentials=creds)

# ✅ Correct request (ONLY mine=True)
response = youtube.liveBroadcasts().list(
    part="snippet",
    mine=True
).execute()

if not response["items"]:
    print("❌ No active livestream found.")
else:
    live_chat_id = response["items"][0]["snippet"]["liveChatId"]
    print("🎥 LIVE CHAT ID:", live_chat_id)

