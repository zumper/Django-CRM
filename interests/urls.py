from django.urls import path
from interests.views import *

app_name = 'interests'

urlpatterns = [
  path('', InterestsListView.as_view(), name='list'),
  path('<int:pk>/view/', InterestDetailView.as_view(), name='view_interest'),
  path('create/', CreateInterestView.as_view(), name='add_interest'),
  path('<int:pk>/edit/', UpdateInterestView.as_view(), name="edit_interest"),
  path('<int:pk>/delete/', RemoveInterestView.as_view(), name="remove_interest"),
]
