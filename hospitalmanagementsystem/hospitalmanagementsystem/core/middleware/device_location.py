from django.conf import settings
from django.utils import timezone
from User.Infrastructure.token_model import AuditLogModel
from hospitalmanagementsystem.core.device_location import parse_user_agent, lookup_ip

class DeviceLocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_paths = getattr(settings, 'LOGIN_AUDIT_PATHS', [])
        self.ipinfo_token = getattr(settings, 'IPINFO_TOKEN', '')

    def __call__(self, request):
        should_log = self._should_log(request)
        ua_header = request.META.get('HTTP_USER_AGENT', '') if should_log else ''
        ip = self._extract_ip(request) if should_log else ''
        response = self.get_response(request)
        if should_log:
            self._log(request, response.status_code, ua_header, ip)
        return response

    def _should_log(self, request):
        if request.method != 'POST':
            return False
        path = (request.path or '').lower()
        return any(path.startswith(p) or p in path for p in self.login_paths)

    def _extract_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')

    def _log(self, request, status_code, user_agent, ip):
        ua_data = parse_user_agent(user_agent)
        geo = lookup_ip(ip, self.ipinfo_token)
        try:
            AuditLogModel.objects.create(
                user=request.user if getattr(request, 'user', None) and request.user.is_authenticated else None,
                path=request.path,
                method=request.method,
                status_code=status_code,
                user_agent=user_agent,
                device=ua_data.get('device'),
                os=ua_data.get('os'),
                browser=ua_data.get('browser'),
                ip_address=geo.get('ip'),
                    city=geo.get('city') or '',
    region=geo.get('region') or '',
    country=geo.get('country') or '',
    latitude=geo.get('latitude') or '',
    longitude=geo.get('longitude') or '',
                is_mobile=ua_data.get('is_mobile'),
                is_tablet=ua_data.get('is_tablet'),
                is_pc=ua_data.get('is_pc'),
                created_at=timezone.now(),
                success=200 <= status_code < 400,
            )
        except Exception as e:
            print("AUDIT LOG ERROR:", e)
