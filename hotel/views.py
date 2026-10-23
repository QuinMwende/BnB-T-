from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Room, Booking
from datetime import datetime

def homepage(request):
    return render(request, 'hotel/homepage.html')


def about(request):
    return render(request, 'hotel/about.html')


def contact(request):
    return render(request, 'hotel/contact.html')


def dashboard(request):
    return render(request, 'hotel/dashboard.html')

@csrf_exempt
def get_rooms(request):
    rooms = Room.objects.all()
    data = []
    for room in rooms:
        data.append({
            'id': room.id,
            'type': room.room_type,
            'status': room.status,
            'price': float(room.price_per_night),
            'guest': room.current_guest,
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def book_room(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        room_id = data['room_id']
        guest_name = data['guest_name']
        check_in = data['check_in']
        check_out = data['check_out']
        payment = data['payment']

        room = get_object_or_404(Room, id=room_id)
        if room.status != 'free':
            return JsonResponse({'error': 'Room not available'}, status=400)

        room.status = 'occupied'
        room.current_guest = guest_name
        room.save()

        Booking.objects.create(
            guest_name=guest_name,
            room=room,
            check_in=datetime.strptime(check_in, '%Y-%m-%d').date(),
            check_out=datetime.strptime(check_out, '%Y-%m-%d').date(),
            payment_method=payment,
            booked_by=request.user
        )

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=405)
