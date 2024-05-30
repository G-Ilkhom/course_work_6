from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, DeleteView, CreateView, UpdateView
from django.apps import apps
from blog.models import BlogPost
from mailings.forms import ClientForm, MessageForm, MailingForm
from mailings.models import Client, Message, Mailing
import random

MailingsConfig = apps.get_app_config('mailings')
MailingsConfig.ready()


class HomeListView(ListView):
    model = Mailing
    template_name = 'base.html'
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = Mailing.objects.all()
        active_mailings = mailings.filter(status='Запущена').count()
        unique_clients = Client.objects.filter(mailing__in=mailings).distinct('id').count()
        total_mailings = mailings.count()
        all_blogs = list(BlogPost.objects.all())
        random.shuffle(all_blogs)
        context['object_list'] = all_blogs[:3]
        context['active_mailings'] = active_mailings
        context['unique_clients'] = unique_clients
        context['total_mailings'] = total_mailings
        return context


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


def disable_the_mailing(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.status == "Запущена":
        mailing_item.status = "Завершена"

    elif mailing_item.status == "Завершена":
        mailing_item.status = "Запущена"

    mailing_item.save()

    return redirect(reverse('mailings:mailing_list'))


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = self.object.client.all()
        return context


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        model = form.save()
        user = self.request.user
        model.owner = user
        model.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'mailings:client_list'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    success_url = reverse_lazy('mailings:client_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Просмотр клиента'
        return context_data


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        model = form.save()
        user = self.request.user
        model.owner = user
        model.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'mailings:messages_list'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Просмотр сообщения'
        return context_data


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        model = form.save()
        user = self.request.user
        model.owner = user
        model.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')
