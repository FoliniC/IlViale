from django.urls import path
from . import views

app_name = 'emotion_tracker'

urlpatterns = [
    path('', views.identifier_view, name='identifier'),
    path('history/', views.history_view, name='history'),
    path('detail/<int:pk>/', views.detail_view, name='detail'),
    path('delete/<int:pk>/', views.delete_view, name='delete'),
]