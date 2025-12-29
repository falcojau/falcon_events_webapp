from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Model for Category
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    slug = models.SlugField(unique=True)  # We use it for pretty URLs 

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


# Model for Event
class Event(models.Model):
    title = models.CharField(max_length=150, verbose_name='Title')
    description = models.TextField(max_length=500, blank=True, verbose_name='Description')
    category = models.ForeignKey(Category, related_name='events', on_delete=models.CASCADE, verbose_name='Category')
    start_datetime = models.DateTimeField(verbose_name='Start Date')
    end_datetime = models.DateTimeField(verbose_name='End Date')
    location = models.CharField(max_length=150, verbose_name='Location')
    capacity = models.IntegerField(blank=True, null=True, verbose_name='Capacity')
    max_guests_per_user = models.IntegerField(default=0, blank=True, null=True, verbose_name='Max Guests')
    created_by = models.ForeignKey(User, related_name='created_events', on_delete=models.CASCADE, verbose_name='User')
    image_event = models.ImageField(upload_to='event/', blank=True, null=True, verbose_name='Image')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    @property   # -- It will be easy to check this methods from everywhere on the project
    def total_attendees(self):
        # Sumamos el usuario que se registra (1) + sus invitados
        registrations = self.registration.all()
        total = registrations.count() # The principal user
        guests = registrations.aggregate(Sum('guests'))['guests__sum'] or 0
        return total + guests

    @property
    def slots_left(self):
        return max(0, self.capacity - self.total_attendees)


# Model for Registration
class Registration(models.Model):
    event = models.ForeignKey(Event, related_name='registration', on_delete=models.CASCADE, verbose_name='Event')
    user = models.ForeignKey(User, related_name='registration', on_delete=models.CASCADE, verbose_name='User')
    registered_at = models.DateTimeField(auto_now_add=True)
    guests = models.IntegerField(blank=True, null=True, verbose_name='Guests')

    class Meta:
        #  An user can't assist twice to an event
        unique_together = ('event', 'user')