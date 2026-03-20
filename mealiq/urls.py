from django.urls import path
from . import views

app_name = 'mealiq'

urlpatterns = [
    path('', views.index, name='index'),
    path('next-step/', views.next_step, name='next_step'),
    path('analyze/', views.analyze, name='analyze'),
]
