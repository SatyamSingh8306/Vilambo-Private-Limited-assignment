import os.path
import base64
import time
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from summarizer import summarizeEmail
from dotenv import load_dotenv
import os 

load_dotenv()

# Define scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

def authenticate():
    """
    Authenticate and return Gmail and Sheets API services.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=5000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    gmail_service = build('gmail', 'v1', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)
    return gmail_service, sheets_service


def get_email_body(payload):
    """
    Extract and decode the email body from the payload.
    """
    if 'parts' in payload:
        parts = payload['parts']
        for part in parts:
            mime_type = part['mimeType']
            body = part['body']
            if mime_type == 'text/plain' and 'data' in body:
                return base64.urlsafe_b64decode(body['data']).decode('utf-8')
            elif mime_type == 'text/html' and 'data' in body:
                return base64.urlsafe_b64decode(body['data']).decode('utf-8')
    elif 'body' in payload and 'data' in payload['body']:
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    return "No body found"


def log_to_google_sheets(sheets_service, spreadsheet_id, data):
    """
    Append data to the Google Sheet.
    """
    range_name = 'A:E'  # Columns A to E
    value_input_option = 'USER_ENTERED'
    values = [data]
    body = {
        'values': values
    }
    sheets_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption=value_input_option,
        body=body
    ).execute()


def fetch_new_emails(gmail_service, sheets_service, spreadsheet_id):
    """
    Fetch unread emails, summarize them, and log to Google Sheets.
    """
    try:
        results = gmail_service.users().messages().list(userId='me', q='is:unread').execute()
        messages = results.get('messages', [])
        
        if not messages:
            print("No new emails found.")
            return
        
        for msg in messages:
            
            msg_data = gmail_service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = msg_data['payload']['headers']
            
            # Extract sender, subject, and body
            sender = next(header['value'] for header in headers if header['name'] == 'From')
            subject = next(header['value'] for header in headers if header['name'] == 'Subject')
            body = get_email_body(msg_data['payload'])
            print(f"Message recevied:\n Sender: {sender}\n subject: {subject}")
            
            summary = summarizeEmail(body)
            print("Summarized...")
            
            # Log to Google Sheets
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_to_google_sheets(sheets_service, spreadsheet_id, [sender, subject, summary, timestamp])
            
            # Mark email as read
            gmail_service.users().messages().modify(
                userId='me',
                id=msg['id'],
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main function to listen for new emails and log data.
    """
    gmail_service, sheets_service = authenticate()
    spreadsheet_id = os.environ.get("SPREDSHEET_ID")  # Replace with your Google Sheet ID
    print("Listening for new emails...")
    
    while True:
        fetch_new_emails(gmail_service, sheets_service, spreadsheet_id)
        time.sleep(10)  # Poll every 10 seconds


if __name__ == '__main__':
    main()