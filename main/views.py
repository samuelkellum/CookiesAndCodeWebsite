from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import CustomUser, Event, Meeting, Semester, EVENT_POINTS, MEETING_POINTS, TIERS_DATA, CURR_SEMESTER


# Create your views here.
def index(request):
    context = {'semester_events': Event.objects.filter(semester=CURR_SEMESTER).order_by('date_time'), 
                'semester_meetings': Meeting.objects.filter(semester=CURR_SEMESTER).order_by('date_time')}

    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about.html')

def event_recos(request):
    return render(request, 'main/event_recos.html')

def gallery(request):
    return render(request, 'main/gallery.html')


def leetcode(request):
    return render(request, 'main/leetcode_th.html')


def members(request):
    for u in CustomUser.objects.all():
        u.get_update_membership_points()
        u.get_update_membership_tier()
    active_members = CustomUser.objects.filter(membership_points__gt=0, is_eboard=False).order_by('-membership_points')
    context = {'event_points': EVENT_POINTS, 
                'meeting_points': MEETING_POINTS, 
                'tiers_data': TIERS_DATA,
                'active_members': active_members} #Python code to get all users
    return render(request, 'main/members.html', context)

def profile(request):
    user = request.user
    # have to wrap in a try-except blog because there might be no logged in User
    # in which case, user.event_set.all() gives error
    try:
        context = {
            'user_events': user.event_set.filter(semester=CURR_SEMESTER).order_by('date_time'),
            'user_meetings': user.meeting_set.filter(semester=CURR_SEMESTER).order_by('date_time'),
            }
    except:
        context = {}
    return render(request, 'main/profile.html', context)





