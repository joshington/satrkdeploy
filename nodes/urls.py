
from django.urls import path

from . import views
from nodes.views import *



app_name = 'main'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("rpc/<uuid:token>/", views.rpc_proxy),
]