from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Booking(models.Model):
	name = models.CharField(max_length=100, blank=False, null=False)
	email = models.EmailField(blank=True, null=True, default=None)
	phone = models.CharField(max_length=10, blank=False, null=False)
	date = models.DateField(blank=False, null=False)
	time = models.TimeField(blank=False, null=False)

	def validate_phone(self, value):
		if len(value) != 10:
			raise ValidationError("Phone number must be 10 digits.")
		if not value.isdigit():
			raise ValidationError("Phone number must contain only digits.")
		if not value.startswith("0"):
			raise ValidationError("Phone number must start with 0.")
		if not value[1] in ["6", "7"]:
			raise ValidationError("Phone number must start with 6 or 7.")

	def validate_date(self, value):
		if timezone.now().date() > value:
			raise ValidationError("Date must be in the future.")
		

	def validate_time(self, value):
		if value < timezone.datetime.strptime("09:00", "%H:%M").time():
			raise ValidationError("Time must be after 09:00.")
		
		if value > timezone.datetime.strptime("17:00", "%H:%M").time():
			raise ValidationError("Time must be before 17:00.")

	def clean(self):
		# Validate phone
		self.validate_phone(self.phone)

		# Validate date
		self.validate_date(self.date)

		# Validate time
		self.validate_time(self.time)

		super().clean()

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.name} - {self.date} - {self.time}"