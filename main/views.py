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




