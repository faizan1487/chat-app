from django.db import models
from django.conf import settings
# Create your models here.


class PublicChatRoom(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, help_text='users who are connected to the chat room', blank=True)

    def __str__(self):
        return self.title

    def connect_user(self, user):
        """
        Return True if user is added to the chat room
        """
        is_user_added = False
        if not user in self.user.all():
            self.user.add(user)
            is_user_added = True
        elif user in self.user.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        """
        Return True if user is removed from the chat room
        """
        is_user_removed = False
        if user in self.user.all():
            self.user.remove(user)
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        return f'PublicChatRoom-{self.id}'


class PublicRoomChatManager(models.Manager):
    def by_room(self, room):
        qs = PublicRoomChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs


class PublicRoomChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    objects = PublicRoomChatManager()

    def __str__(self):
        return self.content
