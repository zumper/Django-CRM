# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# urls for api

from django.urls import path

from api.views import InterestApiView, ListableApiView

app_name = 'api'

urlpatterns = [
    path('create_interest/', InterestApiView.as_view(), name='add_interest'),
    path('listables/', ListableApiView.as_view(), name='listables'),
]
