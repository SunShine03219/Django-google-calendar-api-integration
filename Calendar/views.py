from django.shortcuts import render
from django.http import JsonResponse
from Project.models import Project
from .models import Meetings
from django.views.decorators.http import require_POST
from .forms import MeetingForm
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


# from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import uuid
# import datetime
import pickle
import os.path

SCOPES = [
    'https://www.googleapis.com/auth/calendar', 
    'https://www.googleapis.com/auth/calendar.events'
    ]

def calendar_view(request):
    return render(request, 'calendar.html')

def get_events(request):
    user = request.user

    # Assuming 'start_date' and 'deadline_date' are the start and end date fields in the Meetings model
    meetings_events = Meetings.objects.filter(user=user)
    meetings_data = [
        {
            'title': metting.title + " ( " + metting.google_meet + " ) ",
            'start': metting.start_datetime.isoformat(),
            'end': metting.end_datetime.isoformat(),
            'description': metting.google_meet
        } 
        for metting in meetings_events
    ]

    project_events = Project.objects.filter(pr_stakeholder=user)
    project_data = [
        {
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.deadline_date.isoformat(),
            'url': event.google_meet
        } 
        for event in project_events
    ]

    # Combine the data from both models into a single list
    data = meetings_data + project_data

    return JsonResponse(data, safe=False)

def get_stakeholder_projects_titles(request):
    user = request.user
    project_events              = Project.objects.filter(pr_stakeholder=user)
    stakeholder_projects_titles = [project.title for project in project_events]
    project_ids                 = [project.id for project in project_events]
    return JsonResponse({'titles': stakeholder_projects_titles, 'project_ids': project_ids}, safe=False)

def create_calendar_event(meeting_name, start_datetime, end_datetime):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    print(meeting_name, start_datetime, end_datetime)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=SCOPES)

            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        # Refer to the Python quickstart on how to setup the environment:
        # https://developers.google.com/calendar/quickstart/python
        # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
        # stored credentials.
        event = {
            'summary': meeting_name,
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'GMT',
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': 'GMT',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            "attendees": [{"email": "sunshine03219@gmail.com"}],
            'conferenceData': {
                'createRequest': {
                    'requestId': "random123",
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet',
                    },
                },
            },
        }

        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

        google_meet = event.get('hangoutLink')

        return google_meet

    except HttpError as error:
        print('An error occurred: %s' % error)

def add_event(request):
 
    if request.method == 'POST':
        print (request.POST)

        print('------------------')

        form = MeetingForm(request.POST)

        try:
            if form.is_valid():
                # Extract data from the form

                metting_name = form.cleaned_data['metting_name']
                metting_date = form.cleaned_data['metting_date']
                metting_start_time = form.cleaned_data['metting_start_time']
                metting_end_time = form.cleaned_data['metting_end_time']
                
                start_datetime = datetime.combine(metting_date, metting_start_time)
                start_datetime = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
                
                end_datetime = datetime.combine(metting_date, metting_end_time)
                end_datetime = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')

                google_meet = create_calendar_event(metting_name, start_datetime, end_datetime)
                
                Meetings.objects.create(
                    title=metting_name,
                    google_meet=google_meet,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                    user=request.user,
                )
                
                # Return a JSON response indicating success
                return JsonResponse({'status': 'success'})
        except:
            # If the form is not valid, return a JSON response indicating failure
            print (form.errors)
            return JsonResponse({'status': 'error', 'message': 'Form data is invalid.'}, status=400)

    # If the request method is not POST, return a JSON response indicating failure
    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'}, status=400)

