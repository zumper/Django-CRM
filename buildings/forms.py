# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# forms for building view

from django import forms

from buildings.models import Building
from teams.models import Teams
from common import enums


class BuildingForm(forms.ModelForm):
  teams_queryset = []
  teams = forms.MultipleChoiceField(choices=teams_queryset)

  def __init__(self, *args, **kwargs):
    super(BuildingForm, self).__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs = {"class": "form-control"}

    self.fields['description'].widget.attrs.update({
      'rows': '6'})

    for key, value in self.fields.items():
      if key == 'phone':
        value.widget.attrs['placeholder'] = "+91-123-456-7890"
      else:
        value.widget.attrs['placeholder'] = value.label

    self.fields['building_status'].choices = enums.PropertyStatus.choices()
    self.fields['building_status'].required = True

    self.fields["teams"].choices = [(team.get('id'), team.get('name')) for team in
                                    Teams.objects.all().values('id', 'name')]
    self.fields["teams"].required = False

  class Meta:
    model = Building
    fields = (
        'account', 'address', 'deal', 'zumper_id', 'agent_email', 'brokerage_key', 'building_name', 'building_status',
        'contact_email', 'contact_phone',
        'description', 'internal_features', 'notes'
    )
