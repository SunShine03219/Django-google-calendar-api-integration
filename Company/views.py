
from django.conf                        import settings
from django.shortcuts                   import render, get_object_or_404
from django.contrib.auth                import update_session_auth_hash
from django.contrib.auth.decorators     import login_required
from django.http                        import HttpResponseRedirect  
from .forms                             import CompanyEdit, UpdateUsernameEmail, MyPasswordChangeForm
from .models                            import *
from Project.models                     import Project

import stripe
from django.conf import settings
from django.http import JsonResponse


from django.conf import settings


@login_required
def edit_company(request):
    user = request.user
    company = get_object_or_404(Company, user=user)
    if request.method == 'POST':
        appUserform                 = CompanyEdit(request.POST,request.FILES, instance=company)
        userLoginform               = UpdateUsernameEmail(request.POST)
        passwordLoginform           = MyPasswordChangeForm(user, request.POST)
        if appUserform.is_valid():
            appUserform.save()
        if userLoginform.is_valid():
            user.username   = userLoginform.cleaned_data['username']
            user.email      = userLoginform.cleaned_data['email']
            user.save()
        if passwordLoginform.is_valid():
            update_session_auth_hash(request, user)
            passwordLoginform.save()
            print("Password Changed")
        if user.company.newMember == True:
            user.company.newMemer = False
            return HttpResponseRedirect('/companies/firstSteps')
        else:
            return HttpResponseRedirect('/tasks/')  
    else:
        appUserform = CompanyEdit(instance=company)
        userLoginform = UpdateUsernameEmail(initial={'email': user.email, 'username': user.username})
        passwordLoginform = MyPasswordChangeForm(request.user)
    return render(request, 'editUser.html', {'form': appUserform, 'userLoginform':userLoginform, 'passwordLoginform': passwordLoginform})

def firstSteps(request):
    return render(request, 'firstSteps.html')

def start_checkout_session(request):
    #stripe.api_key = settings.STRIPE_SECRET_KEY
    product_id = 'prod_OJPVSrFlebGw56'
    price_id = 'price_1NYlnME6xWqutRh78ySHjz3I'

    try:
        company_instance = Company.objects.get(user=request.user)
        stripe_customer_id = company_instance.stripe_customer_id
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=[],
            invoice_creation={"enabled": True},
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            customer=stripe_customer_id,
            success_url='https://projectgo.lu/companies/success/',
            cancel_url='https://projectgo.lu/companies/cancel/',
        )
        """
        invoice=stripe.Invoice.create(
            customer=stripe_customer_id,
            collection_method="send_invoice",
            days_until_due=30,
        )
        
        voiceitem=stripe.InvoiceItem.create(
            customer=stripe_customer_id,
            price=price_id,
            invoice=invoice,
        )
        
        stripe.Invoice.finalize_invoice(invoice)
        """
        return HttpResponseRedirect(checkout_session.url)
    except stripe.error.StripeError:
        return HttpResponseRedirect('error_page')
    
def success_page(request):
    company = request.user.company
    if company:
        company.isAllowed = True
        company.save()
    return render(request, 'payment_success.html')

def cancel_page(request):
    return render(request, 'payment_cancel.html')

def rating(request):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=request.POST.get('item_pk'))
        project.archive = True
        project.save()
        provider = project.pr_provider
        rating = Rating.objects.get(project=project)
        rating.provider = provider
        rating.save()
        username = rating.provider.company.company
        
    return render(request, 'rating.html', {'item': rating.pk, 'user':username})

def rating_submit(request):
    if request.method == 'POST':
        rating = Rating.objects.get(pk=request.POST.get('rating_ID'))
        rating.rate = request.POST.get('rating_value_to_send')
        rating.comment = request.POST.get('comments')
        rating.save()
    return HttpResponseRedirect('/projects/myProjects/')  

def list(request):
    queryset = Company.objects.exclude(user__is_superuser=True, user__is_staff=True)
    sort_param = request.GET.get('sort')
    sort_dir = request.GET.get('dir', 'asc')
    if sort_param:
        sort_field = sort_param if sort_dir == 'asc' else f"-{sort_param}"
        queryset = queryset.order_by(sort_field)
    next_dir = 'desc' if sort_dir == 'asc' else 'asc'
    form = CompanyEdit()
    stars_range = range(1, 6)
    context = {'queryset': queryset, 'stars':stars_range, 'sort_param': sort_param, 'sort_dir': sort_dir, 'next_dir': next_dir, 'form': form,}
    return render(request, 'list.html', context)
  
def detail(request):
    if request.method == 'POST':
        item_pk=request.POST.get('item_pk') 
        print(item_pk)
        stars_range = range(1, 6)
        company = get_object_or_404(Company, pk=item_pk)
        return render(request, 'detail.html', {'company': company, 'stars':stars_range})
    else:
        return HttpResponseRedirect('/companies/list') 
 
    
#
#
# Testing
#
#
@login_required(login_url='/companies/login/') 
def company(request):
    return render(request, 'company.html')
