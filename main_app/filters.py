# reference: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# another reference: https://python.plainenglish.io/how-to-create-a-fancy-range-slider-filter-in-django-890bd0486e13
from .models import Hike
import django_filters

class HikeFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(lookup_expr='icontains')
    length_gt = django_filters.NumberFilter(field_name='length', lookup_expr='gt', label='Min Length')
    length_lt = django_filters.NumberFilter(field_name='length', lookup_expr='lt', label='Max Length')
    class Meta:
        model = Hike
        fields = ['state','route_type','difficulty']