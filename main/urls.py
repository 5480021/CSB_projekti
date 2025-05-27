from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('secret/', views.secret_page, name='secret'),
    path('upload/', views.upload_file, name='upload'),
]
