from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    team = models.OneToOneField('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='member_user')

class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='managed_team', unique=True)
    members = models.ManyToManyField(CustomUser, related_name='member_teams')
    total_seats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def update_seats(self):
        current_seat_count = self.seats.count()
        if self.total_seats > current_seat_count:
            for i in range(current_seat_count + 1, self.total_seats + 1):
                Seat.objects.create(team=self, number=i)
        elif self.total_seats < current_seat_count:
            for seat in self.seats.filter(number__gt=self.total_seats):
                seat.delete()

class Seat(models.Model):
    number = models.PositiveIntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='seats')
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'Seat {self.number}'

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()

    class Meta:
        unique_together = ('seat', 'date')

    def __str__(self):
        return f'{self.user.username} booked {self.seat} on {self.date}'
