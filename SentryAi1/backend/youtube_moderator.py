import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from model import is_toxic

# ---------------- CONFIG ----------------
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# ⚠️ Replace this with a FRESH Live Chat ID (per livestream)
LIVE_CHAT_ID = "KicKGFVDVE9OZzRYR1dieUxQcUlTNzZWem5MURILVG1INjhfOUNxY2c"

# Thresholds
DELETE_THRESHOLD = 0.85   # Strong abuse → delete
FLAG_THRESHOLD = 0.60     # Possible joke/sarcasm → flag only
# ---------------------------------------


# -------- AUTH ----------
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json", SCOPES
)
creds = flow.run_local_server(port=0)

youtube = build("youtube", "v3", credentials=creds)

print("\n🛡️ Sentry AI YouTube Moderator (Threshold Mode) Started...\n")

next_page_token = None
seen_messages = set()

# -------- MAIN LOOP ----------
while True:
    try:
        response = youtube.liveChatMessages().list(
            liveChatId=LIVE_CHAT_ID,
            part="snippet,authorDetails",
            pageToken=next_page_token
        ).execute()

        # DEBUG: shows whether messages are being received
        print("DEBUG → items:", len(response.get("items", [])))

        for item in response.get("items", []):
            msg_id = item["id"]

            # Avoid processing the same message twice
            if msg_id in seen_messages:
                continue
            seen_messages.add(msg_id)

            message = item["snippet"]["displayMessage"]
            author = item["authorDetails"]["displayName"]

            toxic, label, score = is_toxic(message)
            score = round(score, 2)

            # -------- CLEAN TERMINAL OUTPUT --------
            print("\n📥 NEW MESSAGE RECEIVED")
            print("────────────────────────")
            print(f"👤 User      : @{author}")
            print(f"💬 Message   : {message}")
            print(f"🧠 Toxic     : {toxic}")
            print(f"📊 Score     : {score}")

            # 🔴 HIGH CONFIDENCE → DELETE
            if toxic and score >= DELETE_THRESHOLD:
                print("🛑 Action    : DELETE (High confidence toxicity)")

                #prof log

                print("🔥 DELETE API CALLED FOR MESSAGE ID:", msg_id)

                try:
                    youtube.liveChatMessages().delete(
                        id=msg_id
                    ).execute()
                    print("✅ Status    : Deleted via YouTube API")
                    time.sleep(1.5)
                except HttpError as e:
                    print("❌ Status    : Delete failed")
                    print("⚠️ Error     :", e)

            # 🟡 MEDIUM CONFIDENCE → FLAG
            elif toxic and score >= FLAG_THRESHOLD:
                print("🚩 Action    : FLAG (Possible joke / sarcasm)")
                print("ℹ️ Status    : Allowed (logged only)")

            # 🟢 LOW CONFIDENCE → ALLOW
            else:
                print("✅ Action    : ALLOW (Clean message)")

        next_page_token = response.get("nextPageToken")
        time.sleep(8)

    except HttpError as e:
        if "liveChatEnded" in str(e):
            print("\n🔴 Stream ended.")
            print("👉 Restart livestream and fetch a NEW Live Chat ID.")
            break
        else:
            print("⚠️ YouTube API error:", e)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 Moderator stopped manually.")
        break
