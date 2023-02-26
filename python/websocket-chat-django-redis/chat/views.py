from django.views.generic import DetailView, ListView, FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from .models import Room, Message
from .forms import CompanionNameForm ,MessageForm


class ChatRoomListView(LoginRequiredMixin, FormView):
    template_name = "chat/chat_room_search.html"
    form_class = CompanionNameForm

    def form_valid(self, form):
        from django.contrib.auth import get_user_model

        other_username = form.cleaned_data.get("username")
        if get_user_model().objects.get(username=other_username):
            return HttpResponseRedirect("/chat/%s" % other_username)
        return Http404


class ChatRoomView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = "chat/chat_room.html"
    form_class = MessageForm
    context_object_name = "chat_room"

    def get_success_url(self):
        return self.request.path

    def get_object(self, *args, **kwargs):
        from django.db.models import prefetch_related_objects

        other_username = self.kwargs.get("username")
        chat_room = Room.objects.get_or_create_or_400(self.request.user, other_username)
        return chat_room

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        room = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        Message.objects.create(user=user, room=room, content=message)
        return super().form_valid(form)
