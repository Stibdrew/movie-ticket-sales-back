from django.urls import path
from .views import TicketTypeListView

urlpatterns = [
    path('ticket-types/', TicketTypeListView.as_view(), name='ticket-type-list'),
]
