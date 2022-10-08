from django import forms
from django import forms

from .models import ReviewRating


class RatingForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['rating', 'subject', 'review']