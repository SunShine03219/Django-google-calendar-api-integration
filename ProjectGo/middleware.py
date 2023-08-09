from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from Company.models import Company

class AppAllowedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path

        if not request.user.is_authenticated:
            # If user is not authenticated, do not check anything
            return response

        if path.startswith('/projects/'):
            # Check if the user has permission to use the Task app
            try:
                company = request.user.company
                if not company.isConfirmed:
                    return HttpResponse("Please confirm you registration.")
                elif not company.isAllowed:
                    return HttpResponseRedirect('/companies/firstSteps')
                    #return HttpResponse("You are not allowed to use the Task app.")
            except Company.DoesNotExist:
                # If the user does not have an AppUser instance, redirect to the profile creation page
                return redirect(reverse('company:create'))

        return response