from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Add a new friend
        """

        if not account in self.friends.all():
            self.friends.add(account)
    
    def remove_friend(self, account):
        """
        Remove a new friend
        """
        if account in self.friends.all():
            self.friends.remove(account)


    def unfriend(self, removee):
        """
        Initiate the action of unfriending someone
        """

        remover_friends_list = self #person terminating the friendship

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friend list
        friend_list = FriendList.objects.get(user=removee)
        friend_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        """
        is this a friend?
        """

        if friend in self.friends.all():
            return True
        return False



# class FriendRequest(models.Model):
#     """
#     A friend request consists of two main parts:
#         1. SENDER
#             - Person sending the friend request
#         2.  RECEIVER
#             - Person receiving the friend request
#     """

#     sender = models.ForeignKey()