import pandas as pd
from main.models import CustomUser

def run():

	# we don't need to delete any since we use get_or_create method
	'''
	e_board_emails_list = ["bennettkahn101@gmail.com", "skellum@tulane.edu",
							"ljanko@tulane.edu", "bsolanky@tulane.edu", 
							"iemanuel@tulane.edu", "clewis24@tulane.edu", 
							"aanand3@tulane.edu"]

	all_non_bennett_users = CustomUser.objects.exclude(email__in=e_board_emails_list)

	all_non_bennett_users.delete()
	'''
	

	roster_df = pd.read_csv("/Users/bennettkahn/CookiesAndCodeWebsite/data/OrganizationRoster.csv")

	print("Creating profiles for all users on Cookies & Code Wave Sync Roster...")

	for index, row in roster_df.iterrows():

		CustomUser.objects.get_or_create(email=row[4], first_name=row[2], last_name=row[3])
		
	print("Successfully created profiles for all users!")