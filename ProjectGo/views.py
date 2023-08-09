from django.http                        import HttpResponseRedirect, HttpResponse
from django.shortcuts                   import render, redirect, get_object_or_404
from django.contrib.auth                import authenticate, login, get_user_model
from django.contrib.auth.views          import LoginView
from django.contrib.auth.tokens         import default_token_generator
from django.contrib.auth.forms          import SetPasswordForm
from django.contrib.sites.shortcuts     import get_current_site
from django.template.loader             import render_to_string
from django.utils.http                  import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding              import force_bytes
from django.core.mail                   import EmailMessage
from django.views.generic               import TemplateView
from ProjectGo.forms                    import *
from Communication.models               import MessagesHome
from Company.models                     import Company
from .forms                             import *
from .tokens                            import account_activation_token

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()         
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)           
            current_site_info = get_current_site(request)
            mail_subject = "Welcome - Confirm your account on projectGo"
            message = render_to_string(
                "emails/confirmation_email.html",
                {
                    "user": user,
                    "domain": current_site_info.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html"  
            email.send()
            
            return HttpResponseRedirect('/companies/edit/')
    else:
        form = SignupForm()
    
    template = 'signup.html'
    
    if request.user_agent.is_mobile :
        print ("SmartPhone")
        template = 'signupSmartPhone.html'

    return render(request, template, {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        company = get_object_or_404(Company, user=user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        company.isConfirmed = True
        company.save()
        user.save()
        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."
        )
    else:
        return HttpResponse("Activation link is invalid!")

def appLogin(request):
    return CustomLoginView.as_view()(request)   
    
def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    mail_subject = "Reset Your Password on ProjectGo"
                    message = render_to_string(
                        "emails/forgotPassword_email.html",
                        {
                            "user": user,
                            "domain": "https://projectgo.lu",
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "token": default_token_generator.make_token(user),
                        },
                    )
                    to_email = form.cleaned_data.get("email")
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.content_subtype = "html"  
                    email.send()
                    return render(request, 'resetPassword_s2.html')
            else:
                return render(request, "forgotPassword.html", {"form": form, "error": "No account found with this email."})
    else:
        form = CustomPasswordResetForm()
    return render(request, "resetPassword_s1.html", {"form": form})

def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('reset_password_done')
        else:
            form = SetPasswordForm(user)
    return render(request, 'resetPassword_s3.html', {'form': form})

def reset_password_done(request):
    return render(request, 'resetPassword_s4.html')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def home (request):
    
    if request.user_agent.is_mobile :
        print ("SmartPhone")
        return render(request, 'homeSmartPhone.html')
    
    if request.user_agent.is_pc:
        print ("PC")
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

def pr_pub(request):
    return render (request, 'projectpub.html')
def pa_con(request):
    return render (request, 'partnercon.html')
def pr_com(request):
    return render (request, 'projectcom.html')

def gdpr_approval(request):
    if request.method == 'POST':
        request.session['gdprIsSet'] = "set"
        if 'accept_all' in request.POST: 
            request.session['cookies1'] = "on"
            request.session['cookies2'] = "on"
        elif 'save_preferences' in request.POST:
            request.session['cookies1'] = request.POST.get("cookies1")
            request.session['cookies2'] = request.POST.get("cookies2")
    request.session.save()
    print (request.session.session_key)
    print (request.session['cookies1'])
    print (request.session['cookies2'])
    print (request.META.get('REMOTE_ADDR'))
    print (request.META.get('HTTP_USER_AGENT'))
    print (request.META.get('HTTP_HOST'))
    return redirect(request.META.get('HTTP_REFERER'))

    
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
             
        if 'authentication_' in request.POST:
            form = self.authentication_form(request.POST)
            print(form)
            print(form.is_valid())
            print(form.errors)
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
    
    def dispatch(self, request, *args, **kwargs):
        if request.user_agent.is_mobile :
            print ("SmartPhone")
            self.template_name = 'homeSmartPhone.html'
    
        if request.user_agent.is_pc:
            print ("PC")
            self.template_name = 'home.html'

        return super().dispatch(request, *args, **kwargs)
    
class CustomLoginView(LoginView):
    print ('Enter')
    authentication_form = SignIn

    def dispatch(self, request, *args, **kwargs):
        if request.user_agent.is_mobile :
            print ("SmartPhoneSI")
            self.template_name = 'signinSmartPhone.html'
    
        if request.user_agent.is_pc:
            print ("PC")
            self.template_name = 'signin.html'

        return super().dispatch(request, *args, **kwargs)