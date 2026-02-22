from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Sum, F, Q
from .models import Event, Booking

# Create your views here.


def event_list(request):
    events = (
        Event.objects
        .select_related("category")
        .annotate(total_bookings=Count("bookings"))
        .order_by("-created_at")
    )

    return render(request, "event_list.html", {"events": events})

def dashboard(request):
    total_events = Event.objects.count()
    total_bookings = Booking.objects.count()


    revenue = Booking.objects.aggregate(
        total_revenue = Sum(F("quantity") * F("event__price"))
    )


    context = {
        "total_events" : total_events,
        "total_bookings" : total_bookings,
        "revenue" : revenue["total_revenue"] or 0,
    }

    return render(request, "dashboard.html", context)

@login_required
@transaction.atomic
def book_event(request, event_id):
    event = Event.objects.select_for_update().get(id=event_id)

    quantity = int(request.POST.get("quantity", 1))

    if event.available_seats < quantity:
        messages.error(request, "Not enough seats avaolable!")
        return redirect("event_list")
    
    # Reduce seats
    event.available_seates -= quantity
    event.save()


    #create booling

    Booking.objects.create(
        user=request.user,
        event=event,
        quantity=quantity
    )

    messages.success(request, "Booking successful")
    return redirect("event list")

def event_list(request):
    query = request.GET.get("q")

    events = Event.objects.select_related("category") \
        .annotate(total_bookings=Count("bookings"))

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query)
        )

    paginator = Paginator(events, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "event_list.html", {
        "page_obj": page_obj
    })

def dashboard(request):
    total_events = Event.objects.count()
    total_bookings = Booking.objects.count()

    revenue_data = Booking.objects.aggregate(
        total_revenue=Sum(F("quantity") * F("event__price"))
    )

    revenue = revenue_data["total_revenue"] or 0

    context = {
        "total_events": total_events,
        "total_bookings": total_bookings,
        "revenue": revenue,
    }

    return render(request, "dashboard.html", context)

@login_required
def my_bookings(request):
    bookings = (
        request.user.bookings
        .select_related("event")
        .order_by("-booked_at")
    )

    return render(request, "my_bookings.html", {
        "bookings": bookings
    })

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    total_events = Event.objects.count()
    total_bookings = Booking.objects.count()

    return render(request, "admin_dashboard.html", {
        "total_events": total_events,
        "total_bookings": total_bookings
    })