import pandas as pd
from main.models import CustomUser, Event, Meeting, Semester, SemesterMembershipStorage

fall_2022_sem = Semester.objects.get_or_create(part_of_term="Fall", year="2022")[0]

for user in CustomUser.objects.all():
	if user.membership_points > 0:
		SemesterMembershipStorage.objects.get_or_create(semester=fall_2022_sem, 
										user=user, 
										membership_points=user.membership_points,
										membership_tier=user.membership_tier)
