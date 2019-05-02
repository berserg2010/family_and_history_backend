from django.urls import path

from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

#DEBUG
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

# DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
