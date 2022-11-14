from bs4 import BeautifulSoup
import requests
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from gsheets import Sheets
import pytz
from datetime import datetime
from django.utils.dateparse import parse_date
from main.models import CustomUser, Event, Meeting
import time

def run():

	# google Drive API stuff
	gauth = GoogleAuth()
	drive = GoogleDrive(gauth)

	#f = open("./storage.json")
	#reg = re.search(r'\"token_expiry\": \"([\s\S]*?)T', s)
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
			#print("IN TRY")
			location = event_info_df['Location'][0]
			#print(event_info_df.columns)
			correct_date = datetime.strptime(event_info_df['Date Time'][0], "%m/%d/%Y %H:%M:%S")
			date_time = pytz.timezone('US/Central').localize(correct_date) # best practice to have timezone aware dates
		# populate fields with blanks
		
		except:
			#print("IN EXCEPT")
			date_time = datetime.now()
		

		# it's possible that an Event object with google_drive_folder_id=[id] has already been created when
		# "Event" folder was "Event 1"; it might have since changed to "Learn to Hack", in which case we only want to 
		# update that Event object, not create an entire new one
		event, created = Event.objects.update_or_create(
			google_drive_folder_id=event_folder_id,
			defaults={'name': event_dict["event_name"], 'location': location, 'date_time': date_time}
			)

		event.organizers.clear() # somebody who is not an organizer now may have been listed as one before
		for email in event_info_df['Organizers']:
			print(email)
			user = CustomUser.objects.get(email=email)
			event.organizers.add(user)
			#event.save()

		attendance_df = event_dict['event_attendance_spread_sheet'].sheets[0].to_frame()
		event.attendees.clear() 
		for email in attendance_df["Tulane Email"]:
			print(email)
			try:
				user = CustomUser.objects.get(email=email)
				event.attendees.add(user)
			except:
				print("User not in system")
			print()
			#event.save()
		print("DONE\n")
	
	# List files in Google Drive
	# '1oVCHPpSL6SaqZixTBA29N6oJc8cNemj9' is '/"Fall 2022"/Meetings' Folder in Google Drive
	fileList = drive.ListFile({'q': "'1oVCHPpSL6SaqZixTBA29N6oJc8cNemj9' in parents and trashed=false"}).GetList()
	meetings_dict = dict()
	# sleep for a couple of minutes to get rid of quota error
	time.sleep(120)
	# iterate over all folders in "meetings" Folder
	for file1 in fileList:
		print('title: %s, id: %s' % (file1['title'], file1['id']))
		
		meeting_dict = dict()

		meeting_folder_id = file1['id'] # id of meeting folder


		meeting_name = file1['title'] # name of meeting folder is always the name of the meeting

		

		meeting_files = drive.ListFile({'q': "'{}' in parents and trashed=false".format(meeting_folder_id)}).GetList()

		# iterate over all files in meeting folder
		for file in meeting_files:
			if file['title'].lower() == 'info':
				meeting_info_spread_sheet = sheets[file['id']]
				

			if file['title'].lower() == 'attendance (responses)':
				attendance_spread_sheet = sheets[file['id']]
				

		meeting_dict["meeting_name"] = meeting_name
		meeting_dict["meeting_info_spread_sheet"] = meeting_info_spread_sheet
		meeting_dict["meeting_attendance_spread_sheet"] = attendance_spread_sheet

		meetings_dict[meeting_folder_id] = meeting_dict


	for meeting_folder_id, meeting_dict in meetings_dict.items():
		print(type(meeting_folder_id))
		print("CREATING/UPDATIN INFORMATION FOR {}".format(meeting_dict["meeting_name"]))
		meeting_info_df = meeting_dict['meeting_info_spread_sheet'].sheets[0].to_frame()

		# "Info" sheets in meeting folders that haven't taken place yet have not been populated
		# trying to get these columns will cause an error
		try:
			#print("IN TRY")
			location = meeting_info_df['Location'][0]
			#print(meeting_info_df.columns)
			correct_date = datetime.strptime(meeting_info_df['Date Time'][0], "%m/%d/%Y %H:%M:%S")
			date_time = pytz.timezone('US/Central').localize(correct_date) # best practice to have timezone aware dates
		# populate fields with blanks
		
		except:
			#print("IN EXCEPT")
			date_time = datetime.now()
		

		# it's possible that an meeting object with google_drive_folder_id=[id] has already been created when
		# "meeting" folder was "meeting 1"; it might have since changed to "Learn to Hack", in which case we only want to 
		# update that meeting object, not create an entire new one
		meeting, created = Meeting.objects.update_or_create(
			google_drive_folder_id=meeting_folder_id,
			defaults={'name': meeting_dict["meeting_name"], 'location': location, 'date_time': date_time}
			)


		meeting.organizers.clear() # somebody who is not an organizer now may have been listed as one before
		for email in meeting_info_df['Organizers']:
			print(email)
			user = CustomUser.objects.get(email=email)
			meeting.organizers.add(user)
			#meeting.save()

		attendance_df = meeting_dict['meeting_attendance_spread_sheet'].sheets[0].to_frame()
		meeting.attendees.clear() 
		for email in attendance_df["Tulane Email"]:
			print(email)
			try:
				user = CustomUser.objects.get(email=email.lower())
				meeting.attendees.add(user)
			except:
				print("User not in system")
			print()
			#meeting.save()
		print("DONE\n")

	# ADD INTERNSHIP PANEL PEOPLE!
	print("ADDING INTERNSHIP WORKSHOP DATA")
	df = pd.read_csv("./data/internship_data.csv")
	attendees_df = df[df["Here?"] == True]
	internship_event = Event.objects.get(name="Internship Prep Workshop")
	internship_event.attendees.clear()
	for email in attendance_df["Tulane Email"]:
		print(email)
		try:
			user = CustomUser.objects.get(email=email)
			internship_event.attendees.add(user)
		except:
			print("User not in system")
		print()




