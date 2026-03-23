from django.urls import path
from . import views

app_name = 'mealiq'

urlpatterns = [
    path('', views.index, name='index'),
    path('vision-analyze/', views.vision_analyze, name='vision_analyze'),
    path('next-step/', views.next_step, name='next_step'),
    path('analyze/', views.analyze, name='analyze'),
]
