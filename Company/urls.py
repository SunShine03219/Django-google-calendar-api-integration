from django.urls import path
from .views import *
from .forms import *
from django.contrib.auth.views import LogoutView

app_name = 'companies'

urlpatterns = [
    
    path('edit/',           edit_company,           name='edit'),
    path('rating/',         rating,                 name='rating'),
    path('rating_submit',   rating_submit,          name='rating_submit'),
    path('list',            list,                   name='list'),
    path('detail',          detail,                 name='detail'),
    path('firstSteps',      firstSteps,             name='firstSteps'),
    path('start_checkout/', start_checkout_session, name='start_checkout'),
    path('success/',        success_page,           name='success_page'),
    path('cancel/',         cancel_page,            name='cancel_page'),
    path('logout/',         LogoutView.as_view  (next_page='/'),name='logout'),
    
    
    
]
