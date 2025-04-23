from django.urls import path
from .views import home, start_training, testimonials, about, our_services, contact_us

urlpatterns = [
    path('', home, name='home'),
    path('testimonial/', testimonials, name='testimonial'),
    path('about/', about, name='about'),
    path('our-services/', our_services, name='our-services'),
    path('contact-us/', contact_us, name='contact-us'),
    #path('submit-testimonial/', submit_testimonial, name='submit_testimonial'),
    #path('testimonial_success/', testimonial_success, name='testimonial_success'),
    path('train/<str:symbol>/', start_training, name='start_training'),
]