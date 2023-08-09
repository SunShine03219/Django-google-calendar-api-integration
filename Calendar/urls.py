from django.urls import path
from . import views

app_name = 'calendar'

urlpatterns = [
    path('',            views.calendar_view,    name='calendar_view'),
    path('events/',     views.get_events,       name='events'),
    path('add_event/',  views.add_event,        name='add_event'),
    path('stakeholder_projects_titles/', views.get_stakeholder_projects_titles, name='stakeholder_projects_titles'),
]