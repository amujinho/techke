from django import forms
from .models import Testimonial, PlanRequest

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'title', 'content', 'image']

class PlanRequestForm(forms.ModelForm):
    class Meta:
        model = PlanRequest
        fields = '__all__'