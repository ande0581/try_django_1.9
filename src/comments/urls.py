# https://github.com/codingforentrepreneurs/Guides/blob/master/all/common_url_regex.md
from django.conf.urls import url

from .views import (
    comment_thread,
    comment_delete,

)

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', comment_thread, name='thread'),
    url(r'^(?P<pk>\d+)/delete/$', comment_delete, name='delete'),
]