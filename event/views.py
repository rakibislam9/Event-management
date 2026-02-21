from django.shortcuts import render
from django.db.models import Count, Sum, F
from .models import Event

# Create your views here.


def event_list(request):
    events = (
        Event.objects
        .select_related("category")
        .annotate(total_bookings=Count("bookings"))
        .order_by("-created_at")
    )

    return render(request, "event_list.html", {"events": events})
