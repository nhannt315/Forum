from django.conf.urls import url
from . import views
from . import api

app_name = 'comments'

urlpatterns = [
    url(r'^(?P<pk>\d+)/add/$', views.CommentCreate.as_view(),
        name='post-comment'),
    url(r'^api/delete/(?P<pk>\d+)/$', api.DeleteCommentAPIView.as_view(),
        name='api-delete')
]
