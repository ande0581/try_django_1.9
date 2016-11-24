# https://github.com/codingforentrepreneurs/Guides/blob/master/all/common_url_regex.md
from django.conf.urls import url

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete
)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create),
    url(r'^(?P<pk>\d+)/$', post_detail, name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', post_update, name='update'),
    url(r'^(?P<pk>\d+)/delete/$', post_delete),
]
