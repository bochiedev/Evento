from django.urls import path
from events.views import EventCreateView, MyEventView, EventView, EventDeleteView, EventUpdateView

app_name = 'events'

urlpatterns = [
    path('', EventView.as_view(), name="view_events" ),
    path('my-events', MyEventView.as_view(), name="my_events" ),
    path('create/', EventCreateView.as_view(), name="create_event" ),
    path('delete/<int:pk>', EventDeleteView.as_view(), name="delete_event" ),
    path('update/<int:pk>', EventUpdateView.as_view(), name="update_event" ),

]
