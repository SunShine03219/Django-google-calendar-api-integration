from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from Project.models import Project

import stripe
#stripe.api_key = settings.STRIPE_SECRET_KEY

# User
COUNTRY = (
    ('L', 'Luxembourg'),
    ('F', 'France'),
    ('BE', 'Belgique'),
    ('DE', 'Allemagne'),
)

# Extending User Model Using a One-To-One Link
class Company(models.Model):
    user                = models.OneToOneField      (User, on_delete=models.CASCADE)
    company             = models.CharField          (max_length=100, default = "Company")
    stripe_customer_id  = models.CharField          (max_length=100, blank=True, null=True)
    logo                = models.ImageField         (upload_to='logo/', blank=True)
    tva                 = models.CharField          (max_length=20)
    emailToContact      = models.EmailField         (null=True, blank=True)
    telephone           = models.CharField          (max_length=20)
    address             = models.CharField          (max_length=30)
    postcode            = models.CharField          (max_length=10)
    city                = models.CharField          (max_length=50)
    state               = models.CharField          (choices=COUNTRY, max_length=2)
    interests           = ArrayField                (models.CharField(max_length=20), blank=True, null=True)
    description         = models.CharField          (max_length=10000)
    isConfirmed         = models.BooleanField       (default = False)
    isAllowed           = models.BooleanField       (default = False)
    darkMode            = models.BooleanField       (default=True)
    newMember           = models.BooleanField       (default=True)
    
    def __str__(self):
        return self.user.username

    def check_is_allowed(self):
        if not self.isAllowed:
            raise Exception("This Company is not allowed to be used.")

def create_stripe_customer(email, name=None):
    try:
        customer = stripe.Customer.create(
            email=email,
            name=name  # Optional: You can include the customer's name if available
        )
        return customer.id
    except stripe.error.StripeError as e:
        # Handle the error as needed
        print(e)
        return None
 
# When User is created, create a corresponding Company with Stripe customer id   
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Company.objects.create(user=instance)
        stripe_customer_id = create_stripe_customer(email=instance.email, name=instance.username)
        company = Company.objects.get(user=instance)
        company.stripe_customer_id = stripe_customer_id
        company.save()

# Problem: When this signal is called, the stripe_customer_id is not saved in the db.
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.company.save() 

@receiver(post_delete, sender=User)
def delete_user_stripe_customer(sender, instance, **kwargs):
    # Delete the Stripe customer associated with the deleted User
    try:
        company = Company.objects.get(user=instance)
        if company.stripe_customer_id:
            stripe.Customer.delete(company.stripe_customer_id)
    except Company.DoesNotExist:
        pass
    except stripe.error.StripeError as e:
        # Handle the error as needed
        print(e)
    


class Rating (models.Model):
    stakeholder         = models.ForeignKey     (User, on_delete=models.CASCADE, related_name='stakeholder',)
    provider            = models.ForeignKey     (User, on_delete=models.CASCADE, related_name='provider')
    project             = models.OneToOneField  (Project, on_delete=models.CASCADE, related_name='project')
    rate                = models.IntegerField   (validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    comment             = models.CharField      (max_length=1000)
    
    def save(self, *args, **kwargs):
        if self.project.status == 'C':
            raise ValueError("Cannot create a rating for a project with status 'C'")

        super().save(*args, **kwargs)