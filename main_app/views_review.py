from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Review, Hike
from django.shortcuts import render, redirect
from .forms import ReviewForm
from django.views.generic.edit import DeleteView

def calculate_average_rating(hike):
    all_hike_reviews = Review.objects.filter(hike=hike)
    rating_sum  = 0
    for review in all_hike_reviews:
        rating_sum += review.rating
    return rating_sum // len(all_hike_reviews)

@login_required
def add_review(request, hike_id):
    error_message = ''
    print(request.POST)
    user = request.user
    hike = Hike.objects.get(pk=hike_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = user
            new_review.hike = hike
            new_review.save()
            hike.average_rating = calculate_average_rating(hike)
            hike.save()
            return redirect('hikes:detail', hike_id=hike_id)
        else:
            error_message = 'Invalid review - try again'
    form = ReviewForm()
    context = {
        'form': form,
        'error_message': error_message,
        'hike': hike,
    }
    return render(request, 'reviews/review_add.html', context)

@login_required
def update_review(request, review_id):
    error_message = ''
    review = Review.objects.get(pk=review_id)
    if request.user == review.user:
        if request.method == 'GET':
            form = ReviewForm(instance=review)
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                review.hike.average_rating = calculate_average_rating(review.hike)
                review.hike.save()
                return redirect('hikes:profile', user_id=review.user.id)
        context = {
            'form': form,
            'hike': review.hike
        }
        return render(request, 'reviews/review_update.html', context)
    else:
        error_message = 'Not authorized to edit that review - add your own review here'
        form = ReviewForm()
        context = {
            'form': form,
            'hike': review.hike,
            'error_message': error_message,
        }
        return render(request, 'reviews/review_add.html', context)

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_delete.html'
    success_url = '/hikes'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            return redirect('login')
        return super().get(request, *args, **kwargs)