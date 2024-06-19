from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, CustomUser, Seat, Booking
from .forms import TeamForm, AddMembersForm, AssignSeatsForm, SeatBookingForm
from datetime import date


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def dashboard(request):
    if request.user.is_manager:
        return render(request, 'accounts/manager_dashboard.html')
    else:
        return render(request, 'accounts/team_member_dashboard.html')


@login_required
def book_seat(request):
    if request.method == 'POST':
        form = SeatBookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            if not Booking.objects.filter(user=request.user, date=booking.date).exists():
                booking.save()
                seat = booking.seat
                seat.is_booked = True
                seat.save()
                messages.success(request, 'Seat booked successfully.')
                return redirect('dashboard')
            else:
                messages.error(request, 'You have already booked a seat for this date.')
    else:
        form = SeatBookingForm(user=request.user)
    return render(request, 'accounts/book_seat.html', {'form': form})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        seat = booking.seat
        seat.is_booked = False
        seat.save()
        booking.delete()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('dashboard')
    return render(request, 'accounts/cancel_booking.html', {'booking': booking})


@login_required
def create_team(request):
    if request.user.is_manager:
        if hasattr(request.user, 'managed_team'):
            messages.error(request, 'You already have a team.')
            return redirect('dashboard')

        if request.method == 'POST':
            form = TeamForm(request.POST)
            if form.is_valid():
                team = form.save(commit=False)
                team.manager = request.user
                team.save()
                team.members.add(request.user)
                team.update_seats()
                request.user.team = team
                request.user.save()
                messages.success(request, 'Team created successfully.')
                return redirect('team_detail', team_id=team.id)
        else:
            form = TeamForm()
        return render(request, 'accounts/create_team.html', {'form': form})
    else:
        return redirect('home')


@login_required
def update_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user != team.manager:
        messages.error(request, 'You do not have permission to update this team.')
        return redirect('home')

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            team.update_seats()
            messages.success(request, 'Team updated successfully.')
            return redirect('team_detail', team_id=team.id)
    else:
        form = TeamForm(instance=team)
    return render(request, 'accounts/update_team.html', {'form': form, 'team': team})

@login_required
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user == team.manager:
        team.delete()
        messages.success(request, 'Team deleted successfully.')
        return redirect('dashboard')
    else:
        messages.error(request, 'You do not have permission to delete this team.')
        return redirect('home')



@login_required
def add_member_to_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user != team.manager:
        messages.error(request, 'You do not have permission to add members to this team.')
        return redirect('home')

    if request.method == 'POST':
        form = AddMembersForm(request.POST)
        if form.is_valid():
            usernames = form.cleaned_data['usernames'].split(',')
            for username in usernames:
                username = username.strip()
                try:
                    user = CustomUser.objects.get(username=username)
                    if user.team is None:
                        team.members.add(user)
                        user.team = team
                        user.save()
                    else:
                        messages.warning(request, f'User {username} is already part of a team.')
                except CustomUser.DoesNotExist:
                    messages.error(request, f'User {username} does not exist. Please ask them to sign up first.')
                    return redirect('signup')
            messages.success(request, 'Team members added successfully.')
            return redirect('team_detail', team_id=team.id)
    else:
        form = AddMembersForm()
    return render(request, 'accounts/add_member.html', {'form': form, 'team': team})



@login_required
def assign_seats(request, team_id):
    team = get_object_or_404(Team, id=team_id, manager=request.user)
    if request.method == 'POST':
        form = AssignSeatsForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seats assigned successfully.')
            return redirect('dashboard')
    else:
        form = AssignSeatsForm(instance=team)
    return render(request, 'accounts/assign_seats.html', {'form': form, 'team': team})


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user != team.manager:
        messages.error(request, 'You do not have permission to view this team.')
        return redirect('home')
    return render(request, 'accounts/team_detail.html', {'team': team})