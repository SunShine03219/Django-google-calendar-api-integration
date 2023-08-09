from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    path('<slug:slug>/',                views.room,         name='chatEnter'),
]