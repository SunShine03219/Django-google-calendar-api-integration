"""ProjectGo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

handler404 = 'ProjectGo.views.handler404'

app_name = 'home'

urlpatterns = [

    path('admin/',                      admin.site.urls),
    path('companies/',                  include                 ('Company.urls')),
    path('projects/',                   include                 ('Project.urls')),
    path('comm/',                       include                 ('Communication.urls')),
    path('calendar/',                   include                 ('Calendar.urls')),
    
    path('',                            HomeView.as_view(),                name='home'),  
    path('signup/',                     signup,                            name='signup'),
    path("activate/<uidb64>/<token>/",  activate,                          name="activate",),
    path('login/',                      appLogin,                          name='login'),  
    path('signin/',                     CustomLoginView.as_view(),         name='signin'),
    path('forgot_password/',            forgot_password,                   name='forgot_password'),
    
    
    
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='passwordResetForm.html',
        email_template_name='emails/forgotPassword_email.html',
        success_url='reset_password_done/',
    ), name='reset_password'),
    path('reset_password_done/', reset_password_done, name='reset_password_done'),
    path('reset_password/<uidb64>/<token>/', reset_password, name='reset_password'),
   
    #path('reset_password/<str:token>/', reset_password,                 name='reset_password'),
    
    path('termscond',                   termscond,                      name='termscond'),
    path('pricing',                     pricing,                        name='pricing'),
    path('faq',                         faq,                            name='faq'),
    path('about',                       about,                          name='about'),
    path('gdpr-approval/',              gdpr_approval,                  name='gdpr_approval'),
    
    
    #path('pr_publishement/',  pr_pub,          name='pr_pub'),
    #path('pa_connection/',    pa_con,          name='pa_con'),
    #path('pr_completion/',    pr_com,          name='pr_com'),
    #path('.well-known/pki-validation/20A8C803A0AD77D5B595D84ABD7E9377.txt', validation_file, name='validation_file'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)