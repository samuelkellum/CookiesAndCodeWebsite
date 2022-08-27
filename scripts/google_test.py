from bs4 import BeautifulSoup
import requests
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from gsheets import Sheets
import pytz
from datetime import datetime
from django.utils.dateparse import parse_date
from main.models import CustomUser, Event

def run():

	# google Drive API stuff
	gauth = GoogleAuth()
	drive = GoogleDrive(gauth)

	# google Sheets API stuff
	sheets = Sheets.from_files('./client_secrets.json', './storage.json')

	# List files in Google Drive
		# '1ZSwsY7xRjigiuK9rmdpTTMjM-T7epgSu' is '/"Fall 2022"/Events' Folder in Google Drive
	fileList = drive.ListFile({'q': "'1ZSwsY7xRjigiuK9rmdpTTMjM-T7epgSu' in parents and trashed=false"}).GetList()

	events_dict = dict() # dict where keys are Event Folder IDs and values are dicts holding information about event

	# iterate over all folders in "Events" Folder
	for file1 in fileList:
		print('title: %s, id: %s' % (file1['title'], file1['id']))
		
		event_dict = dict()

		event_folder_id = file1['id'] # id of Event folder


		event_name = file1['title'] # name of Event folder is always the name of the event

		

		event_files = drive.ListFile({'q': "'{}' in parents and trashed=false".format(event_folder_id)}).GetList()

		# iterate over all files in Event folder
		for file in event_files:
			if file['title'].lower() == 'info':
				event_info_spread_sheet = sheets[file['id']]
				

			if file['title'].lower() == 'attendance (responses)':
				attendance_spread_sheet = sheets[file['id']]
				

		event_dict["event_name"] = event_name
		event_dict["event_info_spread_sheet"] = event_info_spread_sheet
		event_dict["event_attendance_spread_sheet"] = attendance_spread_sheet

		events_dict[event_folder_id] = event_dict

	for event_folder_id, event_dict in events_dict.items():
		print(type(event_folder_id))
		print("CREATING/UPDATIN INFORMATION FOR {}".format(event_dict["event_name"]))
		event_info_df = event_dict['event_info_spread_sheet'].sheets[0].to_frame()

		# "Info" sheets in Event folders that haven't taken place yet have not been populated
		# trying to get these columns will cause an error
		try:
			print("IN TRY")
			location = event_info_df['Location'][0]
			print(location)
			correct_date = datetime.strptime(event_info_df['Date Time'][0], "%m/%d/%Y %H:%M")
			date_time = pytz.timezone('US/Central').localize(correct_date) # best practice to have timezone aware dates
		# populate fields with blanks
		except:
			print("IN EXCEPT")
			location = ''
			date_time = datetime.now()

		# it's possible that an Event object with google_drive_folder_id=[id] has already been created when
		# "Event" folder was "Event 1"; it might have since changed to "Learn to Hack", in which case we only want to 
		# update that Event object, not create an entire new one
		event, created = Event.objects.update_or_create(
			google_drive_folder_id=event_folder_id,
			defaults={'name': event_dict["event_name"], 'location': location, 'date_time': date_time}
			)

		for email in event_info_df['Organizers']:
			print(email)
			user = CustomUser.objects.get(email=email)
			event.organizers.add(user)
			#event.save()

		attendance_df = event_dict['event_attendance_spread_sheet'].sheets[0].to_frame()
		for email in attendance_df["Tulane Email"]:
			print(email)
			user = CustomUser.objects.get(email=email)
			event.attendees.add(user)
			#event.save()
		print("DONE\n")

