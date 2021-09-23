from users.views import profiles
from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import message, send_mail
from django.conf import settings

# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
           user=user,
           username=user.username,
           email=user.email,
           name=user.first_name,
        )

        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )     


def updateProfile(sender, instance, created, **kwargs):
    #profile = instance 
    user = instance.user

    if created == False:
        user.first_name = instance.name
        user.username = instance.username
        user.email = instance.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
    

post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)
post_save.connect(updateProfile, sender=Profile)

# sender = instance 

