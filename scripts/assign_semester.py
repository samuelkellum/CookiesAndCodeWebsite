import pandas as pd
from main.models import CustomUser, Event, Meeting, Semester, SemesterMembershipStorage

fall_2022_sem = Semester.objects.get_or_create(part_of_term="Fall", year="2022")[0]

for event in Event.objects.all():
	event.semester = fall_2022_sem
	event.save()

for meeting in Meeting.objects.all():
	meeting.semester = fall_2022_sem
	meeting.save()

