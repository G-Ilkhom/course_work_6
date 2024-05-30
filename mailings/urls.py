from django.urls import path
from django.apps import apps
from mailings.apps import MailingsConfig
from mailings.views import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, MailingCreateView, \
    MailingDeleteView, MailingDetailView, MailingUpdateView, MailingListView, HomeListView, disable_the_mailing

app_name = MailingsConfig.name

MailingsConfig = apps.get_app_config('mailings')
MailingsConfig.ready()

urlpatterns = [
    path('', HomeListView.as_view(), name='home_list'),
    path('mailings/mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('activity/<int:pk>', disable_the_mailing, name='disable_the_mailing'),
]
