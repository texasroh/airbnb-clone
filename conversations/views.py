from django.shortcuts import redirect, render
from django.http import Http404
from django.db.models import Q
from django.urls import reverse
from django.views.generic import View
from users import models as user_models
from . import models, forms


def go_conversation(request, a_pk, b_pk):
    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)
    if user_one and user_two:
        conversation = models.Conversation.objects.get_or_none(
            Q(participants=user_one) & Q(participants=user_two)
        )
        if not conversation:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)

    return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()

        form = forms.AddCommentForm()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation, "form": form},
        )

    def post(self, *args, **kwargs):
        form = forms.AddCommentForm(self.request.POST)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        message = self.request.POST.get("message", None)
        if message:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
