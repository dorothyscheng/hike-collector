# reference: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
from .models import Hike
import django_filters
from django.db import models
from django import forms

class HikeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Hike Name')
    location = django_filters.CharFilter(lookup_expr='icontains', label='Park Name')
    state = django_filters.CharFilter(lookup_expr='iexact')
    rating_gte = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte', label = 'Rating')
    length = django_filters.RangeFilter(field_name='length')
    ROUTE_TYPE_CHOICES = [
        ('LP', 'Loop'),
        ('OB', 'Out & back'),
        ('PP', 'Point to point'),
    ]
    route_type = django_filters.MultipleChoiceFilter(choices = ROUTE_TYPE_CHOICES, widget = forms.CheckboxSelectMultiple)
    DIFFICULTY_CHOICES = [
        ('E','Easy'),
        ('M','Moderate'),
        ('H','Hard'),
    ]
    difficulty = django_filters.MultipleChoiceFilter(choices = DIFFICULTY_CHOICES, widget = forms.CheckboxSelectMultiple)
    class Meta:
        model = Hike
        fields = ['name', 'location','state','route_type','difficulty']