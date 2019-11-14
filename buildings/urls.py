from django.urls import path
from buildings.views import *

app_name = 'buildings'

urlpatterns = [
  path('', BuildingListView.as_view(), name='list'),
  path('create/', CreateBuildingView.as_view(), name='add_building'),
  path('<int:pk>/edit/', UpdateBuildingView.as_view(), name="edit_building"),
  path('<int:pk>/delete/', RemoveBuildingView.as_view(), name="remove_building"),
]
