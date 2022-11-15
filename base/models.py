from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

consumer_group, created = Group.objects.get_or_create(name="Consumer")
provider_group, created = Group.objects.get_or_create(name="Provider")


class Restaurant(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    pin = models.IntegerField(blank=True, null=True)
    about = models.TextField(max_length=400, blank=True, null=True)
    menu = models.ImageField(
        upload_to='static/assets/', default='static/assets/pexels-ray-01.jpg', null=True, blank=True)
    img1 = models.ImageField(
        upload_to='static/assets/', default='static/assets/pexels-ray-01.jpg', null=True, blank=True)
    img2 = models.ImageField(
        upload_to='static/assets/', default='static/assets/pexels-ray-01.jpg', null=True, blank=True)
    img3 = models.ImageField(
        upload_to='static/assets/', default='static/assets/pexels-ray-01.jpg', null=True, blank=True)
    img4 = models.ImageField(
        upload_to='static/assets/', default='static/assets/pexels-ray-01.jpg', null=True, blank=True)
    phone1 = models.IntegerField(blank=True, null=True)
    phone2 = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    openTime = models.TimeField(blank=True, null=True)
    closeTime = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class TableBooking(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, blank=True)
    numGuests = models.IntegerField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True, null=True)

    rest_id = models.IntegerField(null=True, blank=True)
    cust_id = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=TableBooking)
def event_handler(instance, **kwargs):
    try:
        old_instance = TableBooking.objects.get(id=instance.id)
    except TableBooking.DoesNotExist:
        return

    if instance.status != old_instance.status and instance.status == True:
        subject = 'Booking Confirmation Mail'
        message = f'Hi {instance.name}, Your table has been reserved in {Restaurant.objects.get(id=instance.rest_id)} on dated {instance.date} at {instance.time}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.email, ]
        send_mail(subject, message, email_from, recipient_list)
        print("Mail sent")
