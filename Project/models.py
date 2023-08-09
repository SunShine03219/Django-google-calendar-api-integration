from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from taggit.managers import TaggableManager

from django.core.exceptions import ValidationError

CAT_LEVEL1 = (
    ('IT', 'Informations & Technology'),
    ('S', 'Financial & Insurrance'),
)

CAT_LEVEL_S = (
    ('F', 'Financial'),
    ('I', 'Insurrance'),
)

CAT_STATUS = (
    ('Y', 'Open'),
    ('B', 'In Progress'),
    ('C', 'Canceled'),
    ('G', 'Done'),
)

def validate_categoryL2(value):
    allowed_values = ['Web Developpement',
                      'Digital Marketing',
                      'Infrastructures',
                      'Networking',
                      'Cloud Technologies',
                      'Artificial Intelligence',
                      'Data Science',
                      'Software Engineering',
                      'DevOps',
                      'ERP Solutions',
                      'General Administration',
                      'Finance',
                      'Insurrance',
                      'Legal Activity',
                      'Graphics and Design',
                      'Photography',
                      'Research',
                      'Coaching'
                      ]
    for val in value:
        if val not in allowed_values:
            raise ValidationError('Invalid value in categoryL2: {}'.format(val))


#
# Model of a Task
#
class Project(models.Model):
    pr_stakeholder      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_task')
    pr_provider         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_task')
    title               = models.CharField(max_length=50)
    budget              = models.FloatField()
    description         = models.TextField()
    categoryL1          = models.CharField(choices=CAT_LEVEL1, max_length=2, default='IT')
    categoryL2          = ArrayField(models.CharField(max_length=100),default=list, blank=True, validators=[validate_categoryL2])
    status              = models.CharField(choices=CAT_STATUS, max_length=1, default='Y')
    creation_date       = models.DateField(default=timezone.now)
    start_date          = models.DateField(default=timezone.now)
    deadline_date       = models.DateField(default=timezone.now)
    engaged_date        = models.DateField(default=timezone.now)
    chatID              = models.CharField()
    tags                = TaggableManager(verbose_name='Tags', blank=True)
    file                = models.FileField(upload_to='tasks/', blank=True)
    archive             = models.BooleanField(default=False)
    

    
    def __str__(self):
        return self.title




