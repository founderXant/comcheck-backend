from app.views.building_area import BuildingAreaViewSet
from app.views.last_scrapping import LastFileViewSet
from app.views.scrapping_pdf import ScrapePDFViewSet
from app.views.user_inputs import UserInputsViewSet
from django.urls import include, path
from rest_framework import routers

routers = routers.DefaultRouter()

routers.register('scrapping', ScrapePDFViewSet, basename='scrape-pdf')
routers.register('building-area', BuildingAreaViewSet,
                 basename='building-area')
routers.register('user-inputs', UserInputsViewSet, basename='user-inputs')
routers.register('last-file', LastFileViewSet, basename='last-file')

urlpatterns = [
    path('', include(routers.urls)),
]
