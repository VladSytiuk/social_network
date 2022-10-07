from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin

from posts.models import UserProfile


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_response(self, request, response, *args, **kwargs):
        if request.user.is_authenticated:
            UserProfile.objects.filter(pk=request.user.pk).update(last_request=now())
        return response
