from django.shortcuts import render, get_object_or_404
from .models import Hike

# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    all_hikes = Hike.objects.order_by('name')
    return render(request, 'hikes/index.html', {'hikes': all_hikes})

def detail(request, hike_id):
    selected_hike = get_object_or_404(Hike, pk=hike_id)
    return render(request, 'hikes/detail.html', {'selected': selected_hike})