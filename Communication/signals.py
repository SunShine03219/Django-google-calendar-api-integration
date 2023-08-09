from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User


@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, **kwargs):
    pass
    #room = instance.room
    #sender = instance.user
    #other_user = User.objects.filter(
    #Q(messages__room=room) & ~Q(messages__user=sender)).first()
    #if other_user:
        
        # Create a new notification for the other user
    #    notification = Notification(
    #        recipient=other_user,
    #        actor=sender,
    #        verb='sent you a message',
    #        target=instance,
    #        description=instance.content,
    #    )
    #    notification.save()