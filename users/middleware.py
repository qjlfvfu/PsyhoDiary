from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class UpdateLastActiveMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            # Обновляем только если прошло больше 5 минут
            now = timezone.now()
            last = request.user.last_active
            if not last or (now - last).total_seconds() > 300:  # 5 минут
                request.user.last_active = now
                request.user.save(update_fields=["last_active"])
        return response
