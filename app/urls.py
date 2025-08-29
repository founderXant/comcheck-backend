# app/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter  # <- import the class, not the module

from app.views.building_area import BuildingAreaViewSet
from app.views.last_scrapping import LastFileViewSet
from app.views.scrapping_pdf import ScrapePDFViewSet
from app.views.user_inputs import UserInputsViewSet
from app.views.generate_xml import GenerateXMLView  # this is an APIView

router = DefaultRouter()
router.register('scrapping', ScrapePDFViewSet, basename='scrape-pdf')
router.register('building-area', BuildingAreaViewSet, basename='building-area')
router.register('user-inputs', UserInputsViewSet, basename='user-inputs')
router.register('last-file', LastFileViewSet, basename='last-file')

urlpatterns = [
    # Plain path for the APIView (no router)
    path('generate-xml/', GenerateXMLView.as_view(), name='generate-xml'),

    # Keep your ViewSets on the router
    path('', include(router.urls)),
]