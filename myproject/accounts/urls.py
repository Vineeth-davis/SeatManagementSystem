from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('book-seat/', book_seat, name='book_seat'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('create-team/', create_team, name='create_team'),
    path('add-member/', add_member_to_team, name='add_member'),
    path('assign-seats/<int:team_id>/', assign_seats, name='assign_seats'),
    path('create-team/', create_team, name='create_team'),
    path('update-team/<int:team_id>/', update_team, name='update_team'),
    path('delete-team/<int:team_id>/', delete_team, name='delete_team'),
    path('add-member/<int:team_id>/', add_member_to_team, name='add_member_to_team'),
    path('team/<int:team_id>/', team_detail, name='team_detail'),
]