from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

""" 	
	page_token = None
	while True:
		calendar_list = service.calendarList().list(pageToken=page_token).execute()
		for calendar_list_entry in calendar_list['items']:
			print(calendar_list_entry['summary'])
			print(calendar_list_entry['id'] + '\n')
		page_token = calendar_list.get('nextPageToken')
		if not page_token:
			break

	now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

	print('Getting the upcoming 10 events')
	events_result = service.events().list(calendarId='primary', timeMin=now,
										  maxResults=10, singleEvents=True,
										  orderBy='startTime').execute()
	events = events_result.get('items', [])

	if not events:
		print('No upcoming events found.')
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		print(start, event['summary'])

	
	print('Getting the upcoming 10 events')
	events_result = service.events().list(calendarId=ExampleCalendarId, timeMin=now,
										  maxResults=10, singleEvents=True,
										  orderBy='startTime').execute()
	events = events_result.get('items', [])

	if not events:
		print('No upcoming events found.')
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		print(start, event['summary'])
"""

class googleCalendar:

	def __init__(self):
		self.SCOPES = ['https://www.googleapis.com/auth/calendar']
		self.event = json.loads(open('EventParameters.json', "r").read())

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

		self.service = build('calendar', 'v3', credentials=creds)

	def _reportEvent(self, temporalEvent):
		print('Id: ', temporalEvent.get('id'))
		print('Summary: ', temporalEvent.get('summary'))
		print('Status: ', temporalEvent.get('status'))
		print('Start: ', temporalEvent.get('start'))
		print('Attendees: ', temporalEvent.get('attendees'))
				
	def createEvent(self, calendarId):
		""" Method to create a new calendar event """
		temporalEvent = self.service.events().insert(calendarId=calendarId, sendUpdates="all",
                                      supportsAttachments = True,  body = self.event).execute()
		self._reportEvent(temporalEvent)

	def getEvent(self, calendarId, eventId):
		""" Method to get the calendar event information"""
		temporalEvent = self.service.events().get(
			calendarId = calendarId, eventId = eventId).execute()
		self._reportEvent(temporalEvent)

	def deleteEvent(self, calendarId, eventId):
		""" Method to delet the calendar event information"""
		responseEvent = self.service.events().delete(
			calendarId = calendarId, eventId =  eventId, sendUpdates = "all").execute()
		print(responseEvent)

if __name__ == '__main__':

	calendarId = 's4160deki8usjf5kufaqs4b0bs@group.calendar.google.com'
	eventId = '7lcd8jhp3fmlj3362pu2a1ac34'

	gcInstance = googleCalendar()
	#gcInstance.createEvent(calendarId)
	#gcInstance.getEvent(calendarId, eventId)
	gcInstance.deleteEvent(calendarId, eventId)
