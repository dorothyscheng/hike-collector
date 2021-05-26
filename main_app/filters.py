# reference: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# another reference: https://python.plainenglish.io/how-to-create-a-fancy-range-slider-filter-in-django-890bd0486e13
from .models import Hike
import django_filters

class HikeFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(lookup_expr='iexact')
    rating_gte = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte', label = 'Min Rating')
    length_gte = django_filters.NumberFilter(field_name='length', lookup_expr='gte', label='Min Length')
    length_lte = django_filters.NumberFilter(field_name='length', lookup_expr='lte', label='Max Length')
    class Meta:
        model = Hike
        fields = ['state','route_type','difficulty']