# Copyright 2019 Zumper Inc.
# Author: Tetsuji Ono (tetsuji@zumper.com)
#
# views for interest model


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, View, UpdateView)

from buildings.models import Building
from common.access_decorators_mixins import SalesAccessRequiredMixin
from contacts.models import Contact
from interests.models import Interest
from interests.forms import InterestForm
from leads.models import Lead
from listings.models import Listing
from opportunity.models import Opportunity


class InterestDetailView(SalesAccessRequiredMixin, LoginRequiredMixin, DetailView):
  model = Interest
  context_object_name = 'interest_record'
  template_name = 'view_interest.html'

  def get_queryset(self):
    queryset = super(InterestDetailView, self).get_queryset()
    queryset = queryset.select_related('building', 'contact', 'lead', 'listing', 'opportunity', 'matching_team',)
    return queryset


class InterestListView(SalesAccessRequiredMixin, LoginRequiredMixin, TemplateView):
  model = Interest
  context_object_name = "interest_obj_list"
  template_name = "interests.html"

  def get_queryset(self):
    queryset = self.model.objects.select_related(
        'building', 'contact', 'lead', 'listing', 'opportunity', 'matching_team',
    ).all()
    if (self.request.user.role != "ADMIN" and not
    self.request.user.is_superuser):
      queryset = queryset.filter(
        Q(assigned_to__in=[self.request.user]) |
        Q(created_by=self.request.user))

    request_post = self.request.POST
    if request_post:
      if request_post.get('lead'):
        queryset = queryset.filter(
          listing__icontains=request_post.get('lead'))
      if request_post.get('listing'):
        queryset = queryset.filter(
          listing__icontains=request_post.get('listing'))
      if request_post.get('building'):
        queryset = queryset.filter(
          building__city__icontains=request_post.get('building'))
      if request_post.get('phone'):
        queryset = queryset.filter(
          phone__icontains=request_post.get('phone'))
      if request_post.get('email'):
        queryset = queryset.filter(
          email__icontains=request_post.get('email'))
    return queryset.distinct()

  def get_context_data(self, **kwargs):
    context = super(InterestListView, self).get_context_data(**kwargs)
    context["interest_obj_list"] = self.get_queryset()
    context["per_page"] = self.request.POST.get('per_page')
    search = False
    if (
        self.request.POST.get('listing') or
        self.request.POST.get('phone') or
        self.request.POST.get('email') or
        self.request.POST.get('building')
    ):
      search = True
    context["search"] = search
    return context

  def post(self, request, *args, **kwargs):
    context = self.get_context_data(**kwargs)
    return self.render_to_response(context)


class CreateInterestView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
    model = Interest
    form_class = InterestForm
    template_name = "create_interest.html"

    def post(self, request, *args, **kwargs):
      self.object = None
      form = self.get_form()
      if form.is_valid():
        return self.form_valid(form)

      return self.form_invalid(form)

    def form_valid(self, form):
      # Save Interest
      interest_object = form.save(commit=False)
      interest_object.created_by = self.request.user
      interest_object.save()

      if self.request.POST.get("savenewform"):
        return redirect("interests:new_interest")

      if self.request.is_ajax():
        data = {'success_url': reverse_lazy(
          'interests:list'), 'error': False}
        return JsonResponse(data)

      return redirect("interests:list")

    def get_context_data(self, **kwargs):
      context = super(CreateInterestView, self).get_context_data(**kwargs)
      context["interest_form"] = context["form"]
      context["building"] = Building.objects.all()
      context["listing"] = Listing.objects.all()
      context["lead"] = Lead.objects.all()
      context["opportunity"] = Opportunity.objects.all()
      context["contact"] = Contact.objects.all()
      return context


class UpdateInterestView(SalesAccessRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Interest
    form_class = InterestForm
    template_name = "create_interest.html"

    def post(self, request, *args, **kwargs):
      self.object = self.get_object()
      form = self.get_form()
      if form.is_valid():
        return self.form_valid(form)

      return self.form_invalid(form)


    def form_valid(self, form):
      # Save Interest
      interest_object = form.save(commit=False)
      interest_object.save()

      if self.request.is_ajax():
        return JsonResponse({'error': False})
      return redirect("interests:list")

    def get_context_data(self, **kwargs):
      context = super(UpdateInterestView, self).get_context_data(**kwargs)
      context["interest_obj"] = self.object
      context["interest_form"] = context["form"]
      return context


class RemoveInterestView(SalesAccessRequiredMixin, LoginRequiredMixin, View):

  def get(self, request, *args, **kwargs):
    return self.post(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    interest_id = kwargs.get("pk")
    self.object = get_object_or_404(Interest, id=interest_id)
    self.object.delete()
    if self.request.is_ajax():
      return JsonResponse({'error': False})
    return redirect("interests:list")


class GetInterestsView(LoginRequiredMixin, ListView):
  model = Interest
  context_object_name = "interests"
  template_name = "interests_list.html"
