from django.db import models

class TherapistAppointment(models.Model):
    class Status(models.TextChoices):
        PENDING='pending','pending'
        CONFIRMED='confirmed','confirmed'
        CANCELLED='cancelled','cancelled'
        COMPLETE = 'completed','completed'

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)    
    therapist =models.CharField(max_length=255)     
    patient =models.CharField(max_length=255) 
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()
    notes = models.TextField()
    date_created= models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'therapist appointment'
        verbose_name_plural = 'therapist appointments'
