from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from app.views import GenerateXMLView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app.views import BuildingAreaViewSet 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('generate-xml/',GenerateXMLView.as_view()),
    path ('app/building-area/update-choice/',BuildingAreaViewSet.as_view({'post': 'update_choice'}),name='update_choice'),
    path ('buttonv2',DeprecationWarning)
]

urlpatterns += staticfiles_urlpatterns()
