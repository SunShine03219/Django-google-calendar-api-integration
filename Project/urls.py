from django.urls import path
from .views import *

app_name = 'projects'

urlpatterns = [
    path('',                        dashboard,                  name='dashboard'),
    path('newProject/',             create_project,             name='create_project'),
    path('myProjects/',             my_projects_view,           name='my_projects_view'),
    path('engagedProjects/',        engaged_projects,           name='engaged_projects'),
    path('myProjectsA/',            my_projects_view_archived,  name='my_projects_view_archived'),
    path('engagedProjectsA/',       engaged_projects_archived,  name='engaged_projects_archived'),
    path('pubProjects/',            published_projects,         name='published_projects'),
    path('delete/',                 delete_project,             name='delete_project'),
    path('duplicate/',              duplicate_project,          name='duplicate_project'),
    path('take/',                   take_project,               name='take_project'),
    path('finish/',                 finish_project,             name='finish_project'),
    path('cancel/',                 cancel_project,             name='cancel_project'),
    path('download_file/<int:id>/', download_file,              name='download_file'),
]
