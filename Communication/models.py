from django.contrib.auth.models import User
from django.db                  import models
from django.conf                import settings
from django.urls                import reverse



class Room(models.Model):
    name        = models.CharField  (max_length=255)
    slug        = models.SlugField  (unique = True)
    user1       = models.ForeignKey (User, on_delete=models.CASCADE, related_name='chat_user1')
    user2       = models.ForeignKey (User, on_delete=models.CASCADE, related_name='chat_user2')
    
class Message(models.Model):
    room        = models.ForeignKey     (Room, related_name='messages', on_delete=models.CASCADE)
    user        = models.ForeignKey     (User, related_name='messages', on_delete=models.CASCADE)
    content     = models.TextField      ()
    date_added  = models.DateTimeField  (auto_now_add=True)
        
    class Meta:
        ordering = ('date_added',)

class Notification(models.Model):
    recipient   = models.ForeignKey     (settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications')
    actor       = models.ForeignKey     (settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications_sent')
    verb        = models.CharField      (max_length=255)
    target      = models.ForeignKey     ('Communication.Message', on_delete=models.CASCADE,related_name='notifications')
    timestamp   = models.DateTimeField  (auto_now_add=True)
    is_read     = models.BooleanField   (default=False,)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.actor} {self.verb} {self.target}'

    def get_absolute_url(self):
        return reverse('notification_detail', args=[str(self.id)])

class MessagesHome(models.Model):
    name         = models.CharField      (max_length=50)
    phone        = models.CharField      (max_length=20)
    email        = models.EmailField     ()
    message      = models.CharField      (max_length=200)
    
    
