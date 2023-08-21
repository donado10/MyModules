#!/usr/bin/env python3

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class DriveAPI:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def getCredentials(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', DriveAPI.SCOPES)
            return creds
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', DriveAPI.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def getFiles(self,file_number:int=10):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = self.getCredentials()

        try:
            service = build('drive', 'v3', credentials=creds)

            # Call the Drive v3 API
            results = service.files().list(
                pageSize=file_number, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    def searchFile(self,size,query):
        creds = self.getCredentials()
        try:
            service = build('drive', 'v3', credentials=creds)
            results = service.files().list(
            pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
            else:
                print('Files:')
                for item in items:
                    print(item)
                    print('{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
    
    def uploadFile(self,path,fileName,folder_id=None):
        creds = self.getCredentials()

        try:
            service = build('drive', 'v3', credentials=creds)

            #folder_id = "1AC_HD1gH8EcplbnOLWF6A67vEtIjU3nV"
            if folder_id:
                file_metadata = {
                    'name': fileName,
                    'parents': [folder_id]
                }
            else:
                file_metadata = {
                    'name': fileName
                }

            media = MediaFileUpload(f'{path}/{fileName}',
                                    mimetype='application/x-pem-file')
            file = service.files().create(body=file_metadata, media_body=media,
                                                fields='id').execute()
            print(F'File ID: {file.get("id")}')
            return True
        except:
            return False
