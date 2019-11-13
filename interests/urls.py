# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# url endpoints for interest views

from django.urls import path
from interests.views import *

app_name = 'interests'

urlpatterns = [
  path('', InterestsListView.as_view(), name='list'),
  path('<int:pk>/view/', InterestDetailView.as_view(), name='view_interest'),
  path('create/', CreateInterestView.as_view(), name='add_interest'),
  path('<int:pk>/edit/', UpdateInterestView.as_view(), name="edit_interest"),
  path('<int:pk>/delete/', RemoveInterestView.as_view(), name="remove_interest"),

  path('get/list/', GetInterestsView.as_view(), name="get_lead"),
]
