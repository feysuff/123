# audit_log/middleware.py
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("audit_log")

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._log_meta = {
            "ip": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
        }

    def process_view(self, request, view_func, view_args, view_kwargs):
        import time
        request._start_time_ms = int(time.time() * 1000)

    def process_response(self, request, response):
        try:
            user = getattr(request, "user", None)
            meta = getattr(request, "_log_meta", {})
            record = {
                "path": request.path,
                "ip": meta.get("ip"),
                "user": user if user and user.is_authenticated else None,
                "meta": {"method": request.method, "status_code": response.status_code},
            }
            logger.info(f"request {request.method} {request.path} -> {response.status_code}", extra=record)
        except Exception:
            logger.exception("failed to log request")
        return response
