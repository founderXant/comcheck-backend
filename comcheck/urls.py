from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from app.views import GenerateXMLView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('generate-xml/',GenerateXMLView.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
