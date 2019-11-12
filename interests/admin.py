# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# register app for interest model

from django.contrib import admin

from interests.models import Interest

admin.site.register(Interest)
