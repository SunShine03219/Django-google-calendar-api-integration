from django.http                        import HttpResponseRedirect
from django.shortcuts                   import render, redirect
from django.contrib.auth                import authenticate, login
from django.contrib.auth.views          import LoginView
from django.views.generic               import TemplateView
from .forms                             import MessagesHomeForm
from Company.forms                      import SignIn
from Communication.models               import MessagesHome



    

def handler404(request, exception):
    return render(request, '404.html', status=404)

def home (request):
    return render(request, 'home.html')

def termscond (request):
    return render(request, 'termscond.html')

def pricing (request):
    print (request.session.get('test',{}))
    return render(request, 'pricing.html')

def faq (request):
    request.session['test'] = 'Chakib'
    return render(request, 'faq.html')

def about (request):
    return render(request, 'about.html')

def howTo(request):
    return render (request, 'tutorial.html')

def gdpr_approval(request):
    if request.method == 'POST':
        request.session['gdprIsSet'] = "set"
        if 'accept_all' in request.POST: 
            request.session['cookies1'] = "on"
            request.session['cookies2'] = "on"
        elif 'save_preferences' in request.POST:
            request.session['cookies1'] = request.POST.get("cookies1")
            request.session['cookies2'] = request.POST.get("cookies2")
        
        test = request.POST.get('test')
        request.session['test'] = test
        gdpr_consent = request.POST.get('gdprConsent')
        if gdpr_consent:
            request.session['gdpr_approval'] = True
        else:
            request.session['gdpr_approval'] = False
        return redirect('/')  # Replace 'home' with the URL name of your home page

    return redirect('/')  # Handle cases where the view is accessed directly via URL

def some_view(request):
    if request.session.get('gdpr_approval', False):
        pass
        # User has given GDPR consent, proceed with required actions
        # ...
    else:
        # User has not given GDPR consent, handle accordingly
        # ...
        pass 
    
class HomeView(LoginView, TemplateView):
    template_name       = 'home.html'
    authentication_form = SignIn
    message_form        = MessagesHomeForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authentication_form']  = self.authentication_form()
        context['message_form']         = self.message_form()
        return context

    def post(self, request, *args, **kwargs):
        if 'name' and 'phone' in request.POST:
            form = self.message_form(request.POST)
            if form.is_valid():
                name    = form.cleaned_data['name']
                phone   = form.cleaned_data['phone']
                email   = form.cleaned_data['email']
                message = form.cleaned_data['message']

                MessagesHome.objects.create(
                    name=name,
                    phone=phone,
                    email=email,
                    message=message
                )
           
            else:
                # Optionally, you can redirect the user to a success page or any other desired URL
                return redirect('success_page')  # Replace 'success_page' with the URL or view name you want to redirect to

        return super().post(request, *args, **kwargs)