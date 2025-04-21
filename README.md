
---

# 📬 Email Summarizer Using Gemma 2 9B

An intelligent automation tool that fetches unread emails from Gmail, summarizes their content using the **Gemma 2 9B model** via **ChatGroq**, and logs the summaries into a **Google Sheet** for effortless tracking and actionable insights.

---

## 📌 Features

- **📥 Email Fetching**: Automatically retrieves unread emails from Gmail using the **Gmail API**.
- **📝 Summarization**: Leverages the **Gemma 2 9B** (`gemma2-9b-it`) model via **ChatGroq** to generate concise 3-sentence summaries and key action items.
- **📊 Google Sheets Integration**: Logs the sender, subject, summary, and timestamp into a Google Sheet for easy access.
- **🔄 Automation**: Runs continuously in the background, polling for new emails every 10 seconds.

---

## 📑 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Example Output](#example-output)
6. [References](#references)

---

## ✅ Prerequisites

Ensure you have the following before getting started:

- Python 3.8+
- Google Cloud project with:
  - **Gmail API** enabled
  - **Google Sheets API** enabled
- **ChatGroq API Key** for accessing the `gemma2-9b-it` model
- Familiarity with **OAuth 2.0 authentication** for Google APIs

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/email-summarizer.git
   cd email-summarizer
   ```

2. **Install Dependencies**
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib openpyxl langchain-google-genai
   ```

3. **Set Up Environment Variables**
   - Create a `.env` file in the root directory and add:
     ```env
     GOOGLE_API_KEY=your_google_api_key_here
     CHATGROQ_API_KEY=your_chatgroq_api_key_here
     SPREADSHEET_ID=your_google_sheet_id_here
     ```

---

## ⚙️ Configuration

### 1️⃣ Google Cloud Console
- Enable the **Gmail API** and **Google Sheets API**
- Download the `credentials.json` file and place it in your project root

### 2️⃣ ChatGroq API
- Sign up at [ChatGroq](https://www.chatgroq.com) and get your API key
- Add it to your `.env` file under `CHATGROQ_API_KEY`

### 3️⃣ Google Sheets
- Create a new Google Sheet
- Copy its ID from the URL:
  ```
  https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit
  ```
- Add the following headers to the first row:
  ```
  Sender | Subject | Summary | Action Items | Timestamp
  ```

---

## 🚀 Usage

1. Run the email listener:
   ```bash
   python listener.py
   ```

2. Authenticate via the browser popup (for Gmail and Sheets access)

3. The script will:
   - Fetch unread emails every 10 seconds
   - Summarize them using **Gemma 2 9B**
   - Log results into your Google Sheet

---

## 📊 Example Output

### 📩 Input Email:
```
From: Canva Create HQ <canvacreate@engage.canva.com>
Subject: Canva Create spots are filling up fast

Hello,
We’re excited to announce that Canva Create spots are filling up fast! Secure your spot today.

Best regards,
The Canva Team
```

### 📑 Summarized Output:

| Sender                      | Subject                          | Summary                                                   | Timestamp           |
|:----------------------------|:----------------------------------|:----------------------------------------------------------|:-------------------|
| Canva Create HQ `<...>`     | Canva Create spots are filling up | This email announces that Canva Create spots are filling up fast. | 2025-04-21 14:30:00 |

---

## 📚 References

- [Google Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [ChatGroq API](https://www.chatgroq.com)
- [Gemma 2 9B Model Details](https://ai.google.dev/gemma)

---


## 🙌 Acknowledgements

Special thanks to **Google AI**, **ChatGroq**, and the open-source Python community for their fantastic tools and APIs.

---
