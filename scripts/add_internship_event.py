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

df = pd.read_csv("./data/internship_data.csv")
attendees_df = df[df["Here?"] == True]