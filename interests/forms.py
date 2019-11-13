from django import forms
from interests.models import Interest


class InterestForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super(InterestForm, self).__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs = {"class": "form-control"}

    for key, value in self.fields.items():
      if key == 'phone':
        value.widget.attrs['placeholder'] = "+91-123-456-7890"
      else:
        value.widget.attrs['placeholder'] = value.label

  class Meta:
    model = Interest
    fields = ('building', 'listing', 'email', 'phone', 'tracking_id',
              'agent_email', 'opportunity', 'lead', 'min_price', 'max_price')
