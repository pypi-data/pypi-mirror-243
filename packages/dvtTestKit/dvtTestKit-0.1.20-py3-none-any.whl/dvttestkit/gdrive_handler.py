import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def list_files():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=10, fields="nextPageToken, files(name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item['name'])

def upload_file(filename, filepath):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID:', file.get('id'))

def download_file(file_id, destination):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)

    with open(destination, 'wb') as f:
        f.write(request.execute())

# Example usage
list_files()
upload_file('example.pdf', 'path/to/example.pdf')
download_file('file_id', 'path/to/destination.pdf')

