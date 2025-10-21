from django.db import models

# If you want to store generated trips in a database, uncomment and use these models
# class Trip(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # If you add user authentication
#     budget = models.DecimalField(max_digits=10, decimal_places=2)
#     starting_point = models.CharField(max_length=255)
#     destination = models.CharField(max_length=255)
#     trip_duration_days = models.IntegerField()
#     interests = models.CharField(max_length=500, blank=True) # Storing as comma-separated string
#     generated_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Trip to {self.destination} for {self.trip_duration_days} days"
#
# class ItineraryItem(models.Model):
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itinerary_items')
#     day_number = models.IntegerField()
#     description = models.TextField() # The detailed plan for the day
#     travel_mode = models.CharField(max_length=100, blank=True, null=True)
#     accommodation = models.CharField(max_length=255, blank=True, null=True)
#     food_spots = models.TextField(blank=True, null=True)
#     attractions = models.TextField(blank=True, null=True)
#
#     class Meta:
#         ordering = ['day_number']
#
#     def __str__(self):
#         return f"Day {self.day_number} of {self.trip.destination} trip"from django.db import models

# If you want to store generated trips in a database, uncomment and use these models
# from django.contrib.auth.models import User # If you add user authentication
# class Trip(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # If you add user authentication
#     budget = models.DecimalField(max_digits=10, decimal_places=2)
#     starting_point = models.CharField(max_length=255)
#     destination = models.CharField(max_length=255)
#     trip_duration_days = models.IntegerField()
#     interests = models.CharField(max_length=500, blank=True) # Storing as comma-separated string
#     generated_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Trip to {self.destination} for {self.trip_duration_days} days"
#
# class ItineraryItem(models.Model):
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itinerary_items')
#     day_number = models.IntegerField()
#     description = models.TextField() # The detailed plan for the day
#     travel_mode = models.CharField(max_length=100, blank=True, null=True)
#     accommodation = models.CharField(max_length=255, blank=True, null=True)
#     food_spots = models.TextField(blank=True, null=True)
#     attractions = models.TextField(blank=True, null=True)
#
#     class Meta:
#         ordering = ['day_number']
#
#     def __str__(self):
#         return f"Day {self.day_number} of {self.trip.destination} trip"