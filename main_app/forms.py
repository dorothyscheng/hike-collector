# reference: https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from django.forms.widgets import MediaDefiningClass
from .models import Review, Hike, Activity
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=300, help_text='Required.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=300, help_text='Required.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating','review')

class HikeForm(forms.ModelForm):
    class Meta:
        model = Hike
        fields = ['name', 'location', 'state', 'description', 'length', 'elevation_gain', 'route_type', 'difficulty','activities']
    activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all().order_by('activity'),
        widget=forms.CheckboxSelectMultiple
    )