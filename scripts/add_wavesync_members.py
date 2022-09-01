import pandas as pd
from main.models import CustomUser


def run(org_roster_file_name):
	roster_df = pd.read_csv("./data/{}".format(org_roster_file_name), skiprows=3)

	print("Creating profiles for all users on Cookies & Code Wave Sync Roster...")

	for index, row in roster_df.iterrows():
		
		# If a user with 'email' exists, this line does nothing; otherwise, it creates a new user with the provided arguments
		CustomUser.objects.get_or_create_user(email=row[4].lower(), password="changemeASAP123!", first_name=row[2], last_name=row[3])
		
	print("Successfully created profiles for all users!")