from django.urls import path
from .views import testimonial_list, testimonial_detail, home_data, about_data, services_data, contact_data

urlpatterns = [
    path('testimonials/', testimonial_list, name='testimonial-list'),
    path('testimonials/<int:id>/', testimonial_detail, name='testimonial-detail'),
    path('home/', home_data, name='home-data'),
    path('about/', about_data, name='about-data'),
    path('services/', services_data, name='services_data'),
    path('contact/', contact_data, name='contact_data'),
]