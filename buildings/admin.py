# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
#

from django.contrib import admin
from buildings.models import Building, BuildingAdmin

admin.site.register(Building, BuildingAdmin)
