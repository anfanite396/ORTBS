from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurant, TableBooking


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, help_text='Required')
    last_name = forms.CharField(max_length=200, help_text='Required')
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')


class RestaurantCreationForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'
        exclude = ['host']


class DateInput(forms.DateInput):
    input_type = 'date'


class TableBookingForm(ModelForm):
    class Meta:
        model = TableBooking
        fields = '__all__'
        widgets = {
            'date': DateInput(),
        }
        exclude = ['cust_id', 'created', 'rest_id', 'status']
