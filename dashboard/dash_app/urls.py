from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import dashboard,signup_page,login_page,data_visualization_api,data_filteration_api,custom_logout
urlpatterns = [
#    path('',first,name='/'),#through this url i have only store the json file data into the database
    path('',dashboard, name='dashboard'),
   path('signup/',signup_page,name='signup'),
   path('login/',login_page,name='login'),
   # path('api/chart-data/', chart_data, name='chart-data'),
    path('api/data-visualization/',data_visualization_api, name='data-visualization-api'),
    path('api/data_filteration/',data_filteration_api, name='data-filteration-api'),
    
     path('logout/', custom_logout, name='logout'),
    # this view for the setup
   # path('dash/',dashboard,name='dash'),   
    # path('search/',searching, name='search'),
    
   
]

