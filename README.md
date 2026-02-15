# 🛡️ Sentry AI – Real-Time YouTube Live Chat Moderation System

Sentry AI is a real-time AI-powered moderation system for YouTube Live chats.  
It detects toxic, abusive, or offensive messages using a transformer-based NLP model and automatically allows, flags, or deletes them based on configurable thresholds.

---

## 🚀 Features

- Real-time YouTube Live chat monitoring
- Transformer-based toxicity detection (DistilBERT)
- Confidence-based moderation (Allow / Flag / Delete)
- Secure OAuth 2.0 authentication
- FastAPI backend
- Transparent terminal logging

---

## 🧠 AI Model

- Model: `unitary/toxic-bert`
- Architecture: DistilBERT (Transformer-based deep learning)
- Framework: Hugging Face Transformers
- Output: Toxic label + confidence score (0–1)

Unlike keyword filters, the model understands contextual meaning.

Example:
- "You are stupid" → Toxic
- "This game is stupidly hard" → Likely non-toxic

---

## ⚙️ Tech Stack

- Python 3.10+
- FastAPI
- Hugging Face Transformers
- PyTorch
- YouTube Data API v3
- OAuth 2.0

---

## 🏗️ System Flow

1. User sends message in YouTube Live Chat
2. YouTube API fetches chat messages
3. Message is sent to FastAPI backend
4. AI model analyzes toxicity
5. Threshold logic determines action
6. If toxic, message is deleted via YouTube API

---

# 🛠 Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/SentryAI.git
cd SentryAI
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is missing:

```bash
pip install fastapi uvicorn transformers torch google-api-python-client google-auth-oauthlib
```

---

# 🔐 Google Cloud Setup (Required)

## Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable **YouTube Data API v3**

## Configure OAuth Consent Screen

1. Go to APIs & Services → OAuth Consent Screen
2. Choose **External**
3. Add your Gmail as Test User
4. Save

## Create OAuth Client ID

1. Go to APIs & Services → Credentials
2. Create Credentials → OAuth Client ID
3. Select **Desktop Application**
4. Download the JSON file

Rename the downloaded file to:

```
client_secret.json
```

Place it inside:

```
backend/
```

⚠️ IMPORTANT: Do NOT upload this file to GitHub.

Ensure your `.gitignore` contains:

```
client_secret.json
token.json
```

---

# ▶ Running the Moderator

## Step 1: Get Live Chat ID

```bash
python get_live_chat_id.py
```

Copy the printed Live Chat ID.

---

## Step 2: Update Live Chat ID

Open:

```
backend/youtube_moderator.py
```

Replace:

```python
LIVE_CHAT_ID = "YOUR_LIVE_CHAT_ID"
```

---

## Step 3: Start Moderator

```bash
python youtube_moderator.py
```

A browser window will open for OAuth authorization.

After approval:
- `token.json` will be generated automatically.
- The system will begin monitoring live chat.

---

# 🎯 Moderation Logic

```python
DELETE_THRESHOLD = 0.85
FLAG_THRESHOLD = 0.60
```

- Score ≥ 0.85 → Delete
- 0.60 ≤ Score < 0.85 → Flag
- Score < 0.60 → Allow

Thresholds can be adjusted for sensitivity.

---

# 📊 Performance Notes

- AI inference time: <200ms per message
- Average moderation latency: ~4–5 seconds (API polling dependent)
- Default YouTube API quota: 10,000 units/day
- Delete request cost: 50 units

---

# ⚠️ Limitations

- Subject to YouTube API quota limits
- Uses polling (public API constraint)
- Sarcasm detection remains a general NLP challenge

---

# 🔮 Future Improvements

- Web dashboard UI
- Multi-language support
- Real-time WebSocket integration
- Cloud deployment for scalability

---

# 📄 License

This project is for educational and demonstration purposes.
