from .models import Booking
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch') # Disable CSRF (DEVELOPMENT ONLY)
class BookingView(View):
	def get(self, request, id=None):
		if id:
			try:
				booking = Booking.objects.get(id=id)
				data = {
					"id": booking.id,
					"name": booking.name,
					"email": booking.email,
					"phone": booking.phone,
					"date": booking.date.isoformat(),
					"time": booking.time.isoformat()
				}
				return JsonResponse(data, status=200)
			except Booking.DoesNotExist:
				return JsonResponse({"error": "Booking not found"}, status=404)
		bookings = Booking.objects.all()
		data = []
		for booking in bookings:
			data.append({
				"id": booking.id,
				"name": booking.name,
				"email": booking.email,
				"phone": booking.phone,
				"date": booking.date.isoformat(),
				"time": booking.time.isoformat()
			})
		return JsonResponse(data, safe=False, status=200)

	def post(self, request):
		try:
			data = json.loads(request.body)
			booking = Booking.objects.create(
				name=data["name"],
				email=data.get("email", None),
				phone=data["phone"],
				date=data["date"],
				time=data["time"]
			)
			data = {
				"id": booking.id,
				"name": booking.name,
				"email": booking.email,
				"phone": booking.phone,
				"date": booking.date.isoformat(),
				"time": booking.time.isoformat()
			}
			return JsonResponse(data, status=201)
		except Exception as e:
			return JsonResponse({"error": str(e)}, status=400)

	def put(self, request, id):
		try:
			booking = Booking.objects.get(id=id)
			data = json.loads(request.body)
			booking.name = data.get("name", booking.name)
			booking.email = data.get("email", booking.email)
			booking.phone = data.get("phone", booking.phone)
			booking.date = data.get("date", booking.date)
			booking.time = data.get("time", booking.time)
			booking.save()
			data = {
				"id": booking.id,
				"name": booking.name,
				"email": booking.email,
				"phone": booking.phone,
				"date": booking.date.isoformat(),
				"time": booking.time.isoformat()
			}
			return JsonResponse(data, status=200)
		except Booking.DoesNotExist:
			return JsonResponse({"error": "Booking not found"}, status=404)
		except Exception as e:
			return JsonResponse({"error": str(e)}, status=400)

	def delete(self, request, id):
		try:
			booking = Booking.objects.get(id=id)
			booking.delete()
			return JsonResponse({"message": "Booking deleted"}, status=204)
		except Booking.DoesNotExist:
			return JsonResponse({"error": "Booking not found"}, status=404)
		except Exception as e:
			return JsonResponse({"error": str(e)}, status=400)