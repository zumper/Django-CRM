import arrow

from django.db import models
from common.models import User
from django.utils.translation import ugettext_lazy as _


class Teams(models.Model):
  created_by = models.ForeignKey(User, related_name='teams_created', on_delete=models.SET_NULL, blank=True, null=True)
  fallback_team = models.ForeignKey('self',
                                    on_delete=models.SET_NULL, related_name='fallback_teams', blank=True, null=True)
  users = models.ManyToManyField(User, related_name='user_teams')

  created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
  last_modified_on = models.DateTimeField(auto_now=True)

  description = models.TextField()
  name = models.CharField(max_length=128)
  priority = models.DecimalField(default=0, max_digits=8, decimal_places=2)

  def __str__(self):
    return self.name

  class Meta:
    ordering = ('id', 'priority',)

  @property
  def created_on_arrow(self):
    return arrow.get(self.created_on).humanize()

  def get_users(self):
    return ','.join([str(_id) for _id in list(self.users.values_list('id', flat=True))])
    # return ','.join(list(self.users.values_list('id', flat=True)))
