from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from events.models import Event
from events.forms import EventForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages

# Create your views here.

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/create_event.html'
    form_class = EventForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        messages.success(self.request ,f'Event Successfully Added!')
        return redirect('events:create_event')

class EventView(ListView):
    model = Event
    template_name = 'events/event_view.html'


class MyEventView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/my_event.html'

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(created_by=owner)

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('events:view_events')

    def get_queryset(self):
        owner = self.request.user
        messages.success(self.request ,f'Event Deleted Successfully!')
        return self.model.objects.filter(created_by=owner)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'date', 'venue', 'description']
    template_name = 'events/event_update.html'
    success_url = reverse_lazy('events:view_events' )

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(created_by=owner)
