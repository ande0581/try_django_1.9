# https://github.com/codingforentrepreneurs/Guides/blob/master/all/common_url_regex.md
from django.conf.urls import url

from .views import (
    comment_thread,

)

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', comment_thread, name='thread'),
    #url(r'^(?P<slug>[\w-]+)/delete/$', comment_delete),
]