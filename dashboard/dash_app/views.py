import os
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Data_table
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import F,Q
from django.http import JsonResponse
# from django.db.models import Q
import json
from django.contrib.auth import logout
from datetime import datetime 
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow users to set the page size
    max_page_size = 100  # Maximum limit for page size
# Create your views here.
def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # First, validate that the user existance
        user = User.objects.filter(username=username).first()
        if user:
            messages.error(request, "User already exists")
            return render(request, 'app/signup.html', )

       
        newuser = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "User registered successfully")
        return redirect('login') 

    
    return render(request, 'app/signup.html')

def login_page(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not username or not password:
            messages.error(request,"Username and Password are required")
            return render(request, 'app/login.html')
        else:
            #authenticate the user
            user=authenticate(request,username=username, password=password)
            print(user)
            if user is not None:
                messages.success(request,"Login successful")
                return redirect('dashboard')
            messages.error(request,"invalid user credentials")
         
            return render(request,'app/login.html')  
    return render(request, 'app/login.html')
    

    
# Function to convert date strings to Django-compatible datetime format
def parse_datetime(date_string):
    try:
        # Convert "January, 20 2017 03:51:25" to "2017-01-20 03:51:25"
        return datetime.strptime(date_string, "%B, %d %Y %H:%M:%S")
    except ValueError:
        return None  

def dashboard(request):
    visual=False
    if visual == True:
        
       json_path = os.path.join(settings.BASE_DIR, './dash_app/static/data/jsondata.json')
    
    # Load data from the JSON file
       with open(json_path, encoding='utf-8') as f:
         data = json.load(f)

       for item in data:
         added_date = parse_datetime(item.get('added'))
         published_date = parse_datetime(item.get('published'))

        # Safely retrieve and convert intensity, likelihood, and relevance
         intensity = item.get('intensity')
         likelihood = item.get('likelihood')
         relevance = item.get('relevance')

        # Check and convert intensity
         if intensity in (None, '', ' '):  # Handle empty strings or None
            intensity = 0  # Default value
         else:
            try:
                intensity = int(intensity)  # Ensure it's an integer
            except ValueError:
                intensity = 0  # Default to 0 if conversion fails

        # Check and convert likelihood
         if likelihood in (None, '', ' '):  # Handle empty strings or None
            likelihood = 0  # Default value
         else:
            try:
                likelihood = int(likelihood)  # Ensure it's an integer
            except ValueError:
                likelihood = 0  # Default to 0 if conversion fails

        # Check and convert relevance
         if relevance in (None, '', ' '):  # Handle empty strings or None
            relevance = 0  # Default value
         else:
            try:
                relevance = int(relevance)  # Ensure it's an integer
            except ValueError:
                relevance = 0  # Default to 0 if conversion fails

        # Create the Data_table instance
         Data_table.objects.create(
            end_year=item['end_year'],
            intensity=intensity,
            sector=item['sector'],
            topic=item['topic'],
            insight=item['insight'],
            url=item['url'],
            region=item['region'],
            start_year=item['start_year'],
            impact=item['impact'],
            added=added_date,
            published=published_date,
            country=item['country'],
            relevance=relevance,  # Use the processed relevance value
            pestle=item['pestle'],
            source=item['source'],
            title=item['title'],
            likelihood=likelihood,
         )
    
       return HttpResponse("Data added successfully")
    return render(request,'app/dashboard.html')

 




# data visualisation api -------------------------------

@api_view(['GET'])
def data_visualization_api(request):
    print("start____________________")
    chart_type = request.GET.get('type', 'intensity')  # Default to 'intensity'
    search_query = request.GET.get('search')  # Get the search query

    # List of valid fields with their types (numerical or categorical)
    valid_fields = {
        'intensity': 'numerical',
        'likelihood': 'numerical',
        'relevance': 'numerical',
        'start_year': 'numerical',
        'end_year': 'numerical',
        'country': 'categorical',
        'topic': 'categorical',
        'region': 'categorical', 
    }
    
    if chart_type not in valid_fields:
        return Response({"error": "Invalid chart type"}, status=400)

    queryset = Data_table.objects.all()

    # Apply search filter if search query is provided
    if search_query:
        search_filter = Q(topic__icontains=search_query) | Q(country__icontains=search_query) | Q(region__icontains=search_query) | Q(intensity__icontains=search_query) | Q(likelihood__icontains=search_query) | Q(relevance__icontains=search_query) | Q(start_year__icontains=search_query) | Q(end_year__icontains=search_query)
        queryset = queryset.filter(search_filter)

    # Fetch data based on field type
    if valid_fields[chart_type] == 'numerical':
        data = queryset.values('region', 'country', selected_value=F(chart_type)).filter(**{f'{chart_type}__isnull': False})
    else:
        data = queryset.values('region', 'country', selected_value=F(chart_type)).filter(**{f'{chart_type}__isnull': False})

    response_data = {"data": list(data), "field_type": valid_fields[chart_type]}
    return Response(response_data)


# _-----------------------------------------------------------------------

# --------------data filteration----

@api_view(['GET'])
def data_filteration_api(request):
    print("start_____________ here ............")   
    search_query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', '')
    print(search_query,"HERE IS QUERYSET____________")


    # Initial queryset
    data = Data_table.objects.all()
    print(data,"all data__________")
    # Apply search filter if search query is provided
    if search_query:
        if filter_type:
            # Filter by the selected filter type and search query
            filter_kwargs = {filter_type + '__icontains': search_query}
            data = data.filter(**filter_kwargs)
        else:
            # If no specific filter is selected, apply search across relevant fields
            data = data.filter(
                Q(end_year__icontains=search_query) |
                Q(topic__icontains=search_query) |
                Q(sector__icontains=search_query) |
                Q(region__icontains=search_query) |
                Q(pestle__icontains=search_query) |
                Q(source__icontains=search_query) |
                Q(country__icontains=search_query)
            )
            
            print(data,"filtered data after filteration.................")

    # Pagination logic
    paginator = Paginator(data, 10)  # Display 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the paginated filtered data to the template
    return render(request, 'app/dashboard.html', {
        'search_query':search_query,
        'data': page_obj,  # Paginated data
        'next': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
    })


def custom_logout(request):
    # Log out the user
    logout(request)
    # Redirect to home or any other page
    return redirect('login')
