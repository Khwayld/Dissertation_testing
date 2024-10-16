from django.urls import path
from .views import test_view, kale_example_view

urlpatterns = [
    path('test/', test_view),
    path('kale/', kale_example_view),
]