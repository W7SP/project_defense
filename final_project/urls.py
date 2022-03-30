from django.contrib import admin
from django.urls import path, include

urlpatterns = (
    path('admin/', admin.site.urls),
    path('accounts/', include('final_project.accounts.urls')),
    path('', include('final_project.main.urls')),
)
