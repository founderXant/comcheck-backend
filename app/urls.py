from rest_framework import routers
from django.urls import path, include
from app.views import ScrapePDFViewSet, BuildingAreaViewSet, UserInputsViewSet

routers = routers.DefaultRouter()
routers.register('scrapping', ScrapePDFViewSet, basename='scrape-pdf')
routers.register('building-area', BuildingAreaViewSet, basename='building-area')   
routers.register('user-inputs', UserInputsViewSet, basename='user-inputs')

urlpatterns = [    
    path('', include(routers.urls)),
]

 
 
