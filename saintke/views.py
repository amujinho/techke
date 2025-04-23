from django.shortcuts import render, redirect
from . models import Service, StockPrediction, Testimonial
from .forms import TestimonialForm, PlanRequestForm
from django.http import JsonResponse
import datetime
import torch
import torch.optim as optim
from .rl_agent import DQNAgent, StockTradingEnv, QNetwork
from .utils import fetch_stock_data
from django.contrib import messages

def home(request):
    #f request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #return JsonResponse(data)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    form = PlanRequestForm()

    services = Service.objects .all()

    context = {
        'current_time': current_time,
        'form': form,
        'services': services
    }
    return render(request, 'saintke/home.html', context)

def about(request):
    return render(request, 'saintke/about-us.html')

def our_services(request):
    return render(request, 'saintke/our-services.html')

def contact_us(request):
    return render(request, 'saintke/contact-us.html')

def submit_form(request):
    form = PlanRequestForm()

    if request.method == "POST":
        form = PlanRequestForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            reason = form.cleaned_data['reason']

            PlanRequestForm.objects.create(name=name, email=email, reason=reason)
            messages.success(request, "Form submitted successfully!")
        else:
            messages.error(request, "There was an error submitting the form.")
    else:
        form = PlanRequestForm()
    
    return render(request, 'saintke/plan_form.html', {"form": form})
def testimonials(request):
    testimonial = Testimonial.objects.all().order_by('-created_at')
    if request.method == "POST":
        testimonial = Testimonial.objects.create(
            user = request.user,
            name = request.POST.get('name'),
            title = request.POST.get('title'),
            content = request.POST.get('content'),
            image = request.POST.get('image')
        )
        return redirect('testimonial')

    context = {
        'testimonial': testimonial
    }    
    return render(request, 'saintke/testimonials.html', context)


def start_training(request, symbol="AAPL"):
    # Fetch historical or live stock data
    data = fetch_stock_data(symbol)
    env = StockTradingEnv(data)
    
    # Define input/output dimensions based on your environment and actions
    input_dim = env.observation_space.shape[0]
    output_dim = env.action_space.n
    
    # Initialize Q-network and agent
    q_network = QNetwork(input_dim, output_dim)
    agent = DQNAgent(q_network, env)
    
    # Start training
    agent.train(episodes=500)

    # After training, retrieve latest predictions to display
    recent_predictions = StockPrediction.objects.filter(stock_symbol=symbol).order_by('-timestamp')[:10]
    
    # Render training status and recent predictions
    return render(request, 'training_page.html', {
        'symbol': symbol,
        'recent_predictions': recent_predictions,
        'training_status': "Training in progress"  # Update as needed for real-time status
    })




