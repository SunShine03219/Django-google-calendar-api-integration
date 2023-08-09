import os, string, secrets, time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from ProjectGo.settings import DEFAULT_FROM_EMAIL
from .models import *
from .forms import *
from Communication.models import Room
from django.db.models import Sum, Count
from Company.models import *
from taggit.models import Tag

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

# functions
def generate_url_safe_secret_key(length=9):
    allowed_chars = string.ascii_letters + string.digits
    timestamp = int(time.time() * 1000) # get current timestamp in milliseconds
    random_str = ''.join(secrets.choice(allowed_chars) for i in range(length))
    return f"{timestamp}{random_str}"
#
# General Projects creation. Only a logged user can create a Project
#
@login_required(login_url='/login/')
def create_project(request):
    if request.method == 'POST':
        form = NewProject(request.POST, request.FILES)
        print (request.FILES)
        if form.is_valid():
            secret_key = generate_url_safe_secret_key()
            project = form.save(commit=False)
            project.pr_stakeholder = request.user
            
            categoriesL2 = form.cleaned_data['categoryL2']
            for element in categoriesL2:
                print(element)
            
            project.pr_provider = User.objects.get(id=1)
            project.chatID = secret_key
            project.save()  
            room = Room(name = project.title, slug=secret_key, user1=request.user, user2=request.user)
            room.save()
            rating = Rating(stakeholder=request.user, provider=User.objects.get(id=1), project=project) 
            rating.save()
            form.save_m2m()   
            
            
            return HttpResponseRedirect('/projects/myProjects/') 
        else: 
            form = NewProject()
    else:
        form = NewProject()
    existing_tags = Tag.objects.all().order_by('name')
    return render(request, 'project.html', {'form': form, 'existing_tags': existing_tags})

#
# Project View with sorting functions and dispays only the projects that a logged user 1)created and 2)accepted
#
def _projects_view(request, template_name, filter_field, archive):
    queryset        = Project.objects.filter(**{filter_field: request.user}).filter(archive=archive)
    tags            = Tag.objects.all().order_by('name')
    sort_param  = request.GET.get('sort')
    sort_dir    = request.GET.get('dir', 'asc')
    if sort_param:
        sort_field  = sort_param if sort_dir == 'asc' else f"-{sort_param}"
        queryset    = queryset.order_by(sort_field)
    next_dir = 'desc' if sort_dir == 'asc' else 'asc'
    context = {'queryset': queryset, 'tags': tags, 'sort_param': sort_param, 'sort_dir': sort_dir, 'next_dir': next_dir}
    return render(request, template_name, context)

def _email(subject, mailTemplate, toUser, actionCompany, project, receiver):
    mail_subject = subject
    message = render_to_string(
        mailTemplate,
        {
            "user":     toUser,
            "company":  actionCompany,
            "project":  project,  
        },
    )
    to_email    = receiver
    email       = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"  
    email.send()

@login_required(login_url='/login/')
def my_projects_view(request):
    return _projects_view       (request, 'my_projects.html', 'pr_stakeholder', False)

@login_required(login_url='/login/')
def engaged_projects(request):
    return _projects_view       (request, 'engaged_projects.html', 'pr_provider', False)

@login_required(login_url='/login/')
def my_projects_view_archived(request):
    return _projects_view       (request, 'archived_projects.html', 'pr_stakeholder', True)

@login_required(login_url='/login/')
def engaged_projects_archived(request):
    return _projects_view       (request, 'archived_projects.html', 'pr_provider', True)
#
# Download PDF
#
def download_file(request, id):
    project     = Project.objects.get(pk=id)  
    file_path   = os.path.join(settings.MEDIA_ROOT, project.file.name)
    with open(file_path, 'rb') as f:
        file = f.read()    
    response = HttpResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{project.file.name}"' 
    return response
#
# Project View of the current existing Offers
#
@login_required(login_url='/login/')
def published_projects (request):
    queryset            = Project.objects.filter(status='Y').defer('chatID').exclude(pr_stakeholder=request.user)
    tags                = Tag.objects.all().order_by('name')
    selected_tags       = request.GET.getlist('tags')
    if selected_tags:
        queryset    = queryset.filter(tags__name__in=selected_tags).distinct()
    sort_param      = request.GET.get('sort', None)
    sort_dir        = request.GET.get('dir', 'asc')
    if sort_param:
        sort_field  = sort_param if sort_dir == 'asc' else f"-{sort_param}"
        queryset    = queryset.order_by(sort_field)
    next_dir    = 'desc' if sort_dir == 'asc' else 'asc'
    context     = {'queryset': queryset, 'tags': tags, 'selected_tags': selected_tags, 'sort_param': sort_param, 'sort_dir': sort_dir, 'next_dir': next_dir}
    return render(request, 'published_projects.html', context)   
#
# Delete Project
#
@login_required(login_url='/login/')
def delete_project(request):
    if request.method == 'POST':
        item_pk     = request.POST.get('item_pk')
        item        = get_object_or_404(Project, pk=item_pk)
        item.delete()
    return HttpResponseRedirect('/projects/myProjects/') 
#
# Duplicate Project
#
@login_required(login_url='/login/')
def duplicate_project(request):
    item_pk         = request.POST.get('item_pk')
    item            = get_object_or_404(Project, pk=item_pk)
    secret_key      = generate_url_safe_secret_key()
    duplicatedItem  = Project.objects.create(
        title               = item.title,
        pr_stakeholder      = request.user,
        pr_provider         = User.objects.get(id=1),
        budget              = item.budget,
        categoryL1          = item.categoryL1,
        categoryL2          = item.categoryL2,
        description         = item.description,
        status              = 'Y',
        chatID              = secret_key,
        file                = item.file
    )
    for tag in item.tags.all():
        duplicatedItem.tags.add(tag)
    room = Room(name = item.title, slug=secret_key, user1_id=request.user.id, user2_id=1)
    room.save()  
    return HttpResponseRedirect('/projects/myProjects/') 
#
# Finish the Project
#
@login_required(login_url='/login/')
def finish_project(request):
    if request.method == 'POST':
        item_pk     = request.POST.get('item_pk')
        item        = get_object_or_404(Project, pk=item_pk)
        item.status = 'G'
        item.save()
        companyStakeholder = get_object_or_404(Company, user=item.pr_stakeholder)
        _email("Project Finished", "emails/finished.html", item.pr_provider, companyStakeholder.company, item.title, item.pr_provider.email)
    return HttpResponseRedirect('/projects/myProjects/') 
#
# Cancel Project
#
@login_required(login_url='/login/')
def cancel_project(request):
    if request.method == 'POST':
        item_pk         = request.POST.get('item_pk')
        item            = get_object_or_404(Project, pk=item_pk)
        item.status     ='C'
        item.archive    = True
        item.save()
        companyStakeholder = get_object_or_404(Company, user=item.pr_stakeholder)
        _email("Project cancelled", "emails/cancel.html", item.pr_provider, companyStakeholder.company, item.title, item.pr_provider.email)
    return HttpResponseRedirect('/projects/myProjects/') 
#
# Engage Project
#
@login_required(login_url='/login/')
def take_project(request):
    if request.method == 'POST':
        item_pk                 = request.POST.get('item_pk')
        item                    = get_object_or_404(Project, pk=item_pk)
        item.pr_provider        = User.objects.get(id=request.user.id)
        item.status             = 'B'
        item.engaged_date       = timezone.now().date()
        room                    = get_object_or_404(Room, slug=item.chatID)
        room.user2              = request.user 
        item.save()
        room.save()
        
        companyProvider = get_object_or_404(Company, user=item.pr_provider)
        _email("Project engagement", "emails/taken.html", item.pr_stakeholder, companyProvider.company, item.title, item.pr_stakeholder.email)
    return HttpResponseRedirect('/projects/pubProjects/') 
#
# DASHBOARD
#
@login_required(login_url='/login/')
def dashboard(request):
    # Filter projects by current user
    projects_stakeholder     = Project.objects.filter(pr_stakeholder=request.user)
    projects_provider        = Project.objects.filter(pr_provider=request.user)
    
    company                 = get_object_or_404(Company, user=request.user)
    
    sum_budget              = projects_stakeholder.filter(status="G").aggregate(Sum('budget'))['budget__sum']
    
    categoryL1_res          = projects_stakeholder.values('categoryL1').annotate(count=Count('categoryL1'))
    categoryL1L2_res        = projects_stakeholder.values('categoryL1', 'categoryL2')
    results = {}
    for item in categoryL1L2_res:
        categoryL1 = item['categoryL1']
        categoryL2 = item['categoryL2']
        if categoryL1 not in results:
            results[categoryL1] = { 'categoryL2': {}}
        for category in categoryL2:
            if category not in results[categoryL1]['categoryL2']:
                results[categoryL1]['categoryL2'][category] = 1
            else:
                results[categoryL1]['categoryL2'][category] += 1
                
    companiesWorkedwith = projects_stakeholder.filter(status='G').values('pr_provider','pr_provider__company__company').annotate(count=Count('categoryL1'))
    
    # Group projects by status and count the number of projects in each group
    opened                  = projects_stakeholder.filter(status='Y').count()
    finished                = projects_stakeholder.filter(status='G', archive=False).count()
    assigned                = projects_stakeholder.filter(status='B').count()
    finished_provider       = projects_provider.filter(status='G').count()
    taken                   = projects_provider.filter(status='B').count()

    # Create data object for the chart
    data_stakeholder  = {
        'labels': ['Open', 'Taken', 'Finished'],
        'datasets': [{
            'data': [opened, assigned, finished],
            'backgroundColor': ['#F2C94C', '#32A852', '#3498DB'],
            'hoverBackgroundColor': ['#fff756', '#56ff86', '#56b3ff']
        }]
    }
    
    budget_counts = (
        Project.objects
        .filter(pr_stakeholder=request.user, status='G')
        .values('creation_date')
        .annotate(total_budget=Sum('budget'))
        .order_by('creation_date')
    )

    # Extract the dates and total budgets from the query results
    budgets_labels = [entry['creation_date'].strftime('%Y-%m-%d') for entry in budget_counts]
    data_budgets = [entry['total_budget'] for entry in budget_counts]

    # Prepare the chart data as a JSON structure
    data_budgets = {
        'labels': budgets_labels,
        'datasets': [
            {
                'label': 'History of your Budget',
                'data': data_budgets,
            }
        ]
    }
    
    projects_provider_counts = projects_provider.filter(pr_provider=request.user).values('creation_date').annotate(count=Count('id')).order_by('creation_date')

    labels_provider     = [str(entry['creation_date']) for entry in projects_provider_counts]
    data_provider       = [entry['count'] for entry in projects_provider_counts]
    
    data_provider = {
        'labels': labels_provider,
        'datasets': [{'label': 'History of your Projects', 'data': data_provider,
        }]
    }
    
    current_date = timezone.now().date()
    week_ahead = current_date + timezone.timedelta(days=7)
    
    pr_stakeholder_pov_coming_within_next_week      = projects_stakeholder.filter(start_date__range=[current_date, week_ahead]).exclude(status__in=['G', 'C'])
    pr_provider_pov_coming_within_next_week         = projects_provider.filter(start_date__range=[current_date, week_ahead], status='B')
    
    most_common_tags = projects_provider.filter(archive=False).values('tags__name').annotate(tag_count=Count('tags')).order_by('-tag_count')[:5]
    
    chatchannels_st = projects_stakeholder.values_list('chatID', flat=True).filter(status='B')
    chatchannels_pr = projects_provider.values_list('chatID', flat=True).filter(status='B')
    rooms_st = Room.objects.filter(slug__in=chatchannels_st)
    rooms_pr = Room.objects.filter(slug__in=chatchannels_pr)

    
    return render(request, 'dashboard.html', 
                  {'user':                                          request.user, 
                   'company':                                       company,
                   'budget_sum':                                    sum_budget,
                   'categoryL1_res':                                categoryL1_res,
                   'categoryL1L2_res' :                             categoryL1L2_res,
                   'companiesWorkedwith':                           companiesWorkedwith,
                   'results':                                       results,
                   'data_stakeholder':                              data_stakeholder, 
                   'data_provider':                                 data_provider, 
                   'opened':                                        opened, 
                   'assigned':                                      assigned, 
                   'taken':                                         taken, 
                   'finished':                                      finished,
                   'finished_provider':                             finished_provider,
                   'pr_stakeholder_pov_coming_within_next_week':    pr_stakeholder_pov_coming_within_next_week,
                   'pr_provider_pov_coming_within_next_week':       pr_provider_pov_coming_within_next_week,
                   'most_common_tags':                              most_common_tags,
                   'data_budgets' :                                 data_budgets,
                   'rooms_st':                                      rooms_st,    
                   'rooms_pr':                                      rooms_pr,  
                    })

