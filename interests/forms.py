from django import forms

from buildings.models import Building
from contacts.models import Contact
from interests.models import Interest
from leads.models import Lead
from listings.models import Listing
from opportunity.models import Opportunity


class InterestForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super(InterestForm, self).__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs = {"class": "form-control"}

    self.fields['building'].queryset = Building.objects.filter()
    self.fields['listing'].queryset = Listing.objects.filter()
    self.fields['lead'].queryset = Lead.objects.filter()
    self.fields['contact'].queryset = Contact.objects.filter()
    self.fields['opportunity'].queryset = Opportunity.objects.filter()

    for key, value in self.fields.items():
      if key == 'phone':
        value.widget.attrs['placeholder'] = "+91-123-456-7890"
      else:
        value.widget.attrs['placeholder'] = value.label

  class Meta:
    model = Interest
    fields = ('building', 'listing', 'email', 'phone', 'tracking_id',
              'agent_email', 'opportunity', 'lead', 'min_price', 'max_price', 'contact')
