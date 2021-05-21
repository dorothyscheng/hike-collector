from django.shortcuts import render, get_list_or_404
from .models import Hike

# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    all_hikes = Hike.objects.order_by('name')
    return render(request, 'hikes/index.html', {'hikes': all_hikes})