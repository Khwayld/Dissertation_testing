from django.urls import path
from .views import test_view, run_example

urlpatterns = [
    path('test/', test_view),
    path('api/run-example/', run_example, name='run_example'),
]