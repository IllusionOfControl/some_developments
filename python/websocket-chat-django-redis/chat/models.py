from django.conf import settings
from django.db import models
from django.http import HttpResponseBadRequest
from django.db.models.signals import post_save


# from .utils import broadcast_msg_to_chat, trigger_welcome_message


class RoomManager(models.Manager):
    def get_chats_by_user(self, user):
        # todo view qs
        include_lookup = models.Q(first_user=user) | models.Q(second_user=user)
        exclude_lookup = models.Q(first_user=user) & models.Q(second_user=user)
        qs = self.get_queryset().filter(include_lookup).exclude(exclude_lookup).distinct()
        return qs

    def get_or_create_or_400(self, user, other_username):
        username = user.username
        if username == other_username:
            raise HttpResponseBadRequest
        initiator_chat_lookup = models.Q(first_user__username=username) & models.Q(second_user__username=other_username)
        respondent_chat_lookup = models.Q(first_user__username=other_username) & \
                                 models.Q(second_user__username=username)
        qs = self.get_queryset().filter(initiator_chat_lookup | respondent_chat_lookup).distinct()
        object_count = qs.count()
        if object_count == 1:
            return qs.prefetch_related("messages__user").first()
        else:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            second_user = User.objects.get(username=other_username)
            room = self.model(
                first_user=user,
                second_user=second_user
            )
            room.save()
            return room


class Room(models.Model):
    first_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="first_user_id")
    second_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="second_user_id")
    updated_at = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = RoomManager()

    @property
    def room_name(self):
        return "chat_%d" % self.id

    # todo
    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_name, user='admin')
            return True
        return False


class Message(models.Model):
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL, related_name="messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='sender',
                             on_delete=models.CASCADE,
                             related_name="user_id")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# todo
def new_user_receiver(sender, instance, created, *args, **kargs):
    if created:
        # UserKlass = instance.__class__
        # my_admin_user = UserKlass.objects.get(id=1)
        # obj, created = Thread.objects.get_or_new(my_admin_user, instance.username)
        # obj.broadcast(msg='Hello and welcome')

        sender_id = 1  # admin user, main sender
        receiver_id = instance.id
        # trigger_welcome_message(sender_id, receiver_id)

# post_save.connect(new_user_receiver, sender=settings.AUTH_USER_MODEL)
