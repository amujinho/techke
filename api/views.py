from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TestimonialSerializer, PageSerializer
from saintke.models import Testimonial
from django.utils import timezone

# API testimonials
@api_view(['GET', 'POST'])
def testimonial_list(request):
    if  request.method == 'GET':
        testimonials = Testimonial.objects.all().order_by('-created_at')
        serializer = TestimonialSerializer(testimonials, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TestimonialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
def testimonial_detail(request, id):
    try:
        testimonial = Testimonial.objects.get(id=id)
        serializer = TestimonialSerializer(testimonial)
        return Response(serializer.data)
    except Testimonial.DoesNotExist:
        return Response(status=404)

#api for static pages
@api_view(['GET'])
def home_data(request):
    data = {"title": "Home", "content": f"welcome to the home page. Current time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"}
    serializer = PageSerializer(data)
    return Response(serializer.data) 

@api_view(['GET'])
def about_data(request):
    data = {"title": "About Us", "content": "Learn more about us."}
    serializer = PageSerializer(data)
    return Response(serializer.data) 

@api_view(['GET'])
def services_data(request):
    data = {"title": "Our Services", "content": "Explore our services."}
    serializer = PageSerializer(data)
    return Response(serializer.data)

@api_view(['GET'])
def contact_data(request):
    data = {"title": "Contact Us", "content": "Get in touch with us."}
    serializer = PageSerializer(data)
    return Response(serializer.data)