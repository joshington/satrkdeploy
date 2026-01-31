
from django.urls import path

from . import views
from nodes.views import *



app_name = 'nodes'

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("deploy/", views.deploy_node, name="deploy_node"),
    path("destroy/<int:node_id>/", views.destroy_node, name="destroy_node"),
    path("rpc/<uuid:token>/", views.rpc_proxy),
]