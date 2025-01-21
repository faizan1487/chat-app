from django.urls import path
from .views import (
    send_friend_request,
    friend_requests,
    accept_friend_request,
    remove_friend,
    decline_friend_request,
    cancel_friend_request,
    friend_list_view
)

app_name = "friend"

urlpatterns = [
    path('list/<user_id>/', friend_list_view, name='list'),
    path('friend_remove/', remove_friend, name='remove-friend'),
    path('friend_request/', send_friend_request, name='friend-request'),
    path('cancel_friend_request/', cancel_friend_request, name='friend-request-cancel'),
    path('friend_request/<user_id>/', friend_requests, name='friend-requests'),
    path('accept_friend_request/<friend_request_id>/', accept_friend_request, name='friend-request-accept'),
    path('decline_friend_request/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),
]
