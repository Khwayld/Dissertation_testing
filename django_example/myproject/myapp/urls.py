from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Homepage view
    path('example/', views.run_example, name='run_example'),
]
