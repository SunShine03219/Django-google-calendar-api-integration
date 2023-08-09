import json
from django.http                    import HttpResponse
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.shortcuts               import render, get_object_or_404
from django.utils.safestring        import mark_safe
from .models                        import *

from Project.models                 import Project
from Company.models                 import Company


@login_required
def room(request, slug):
    room            = Room.objects.get(slug=slug)
    project         = Project.objects.get(chatID=slug)
    user1           = project.pr_stakeholder.username
    user1Logo       = Company.objects.get(user = project.pr_stakeholder).logo
    if not user1Logo:
        user1Logo = Company.objects.get(user=1).logo
    user1Company    = Company.objects.get(user= project.pr_stakeholder).company
    user2           = project.pr_provider.username
    user2Logo       = Company.objects.get(user= project.pr_provider).logo
    if  not user2Logo:
        user2Logo = Company.objects.get(user=1).logo
    user2Company    = Company.objects.get(user= project.pr_provider).company
    messages        = Message.objects.filter(room=room)
    return render(request, 'chatEnter.html', {
        'room':room, 
        'messages':messages, 
        'user1':user1, 
        'user2':user2, 
        'user1Logo': user1Logo,
        'user2Logo': user2Logo, 
        'user1Company':user1Company,
        'user2Company':user2Company,
        }) 
