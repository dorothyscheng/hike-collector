from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Photo
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect

class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'reviews/review_delete.html'
    success_url = '/hikes'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            return redirect('login')
        return super().get(request, *args, **kwargs)