from app.views.building_area import BuildingAreaViewSet
from app.views.generate_xml import GenerateXMLView
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('generate-xml/', GenerateXMLView.as_view()),
    path('app/building-area/update-choice/',
         BuildingAreaViewSet.as_view({'post': 'update_choice'}), name='update_choice')
]

urlpatterns += staticfiles_urlpatterns()
