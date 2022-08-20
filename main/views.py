from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def event_recos(request):
    return render(request, 'main/event_recos.html')

def gallery(request):
    return render(request, 'main/gallery.html')


def leetcode(request):
    return render(request, 'main/leetcode_th.html')


def members(request):
    return render(request, 'main/members.html')

def profile(request):
    user = request.user
    context = {
            'user_events': user.event_set.all(),
            'user_meetings': user.meeting_set.all(),
        }
    return render(request, 'main/profile.html', context)




