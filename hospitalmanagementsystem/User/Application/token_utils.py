import requests

class TokenUtils:
    @staticmethod
    def get_client_ip(request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')

    @staticmethod
    def get_device_info(request):
        return request.META.get('HTTP_USER_AGENT', '')

    @staticmethod
    def get_location_from_ip(ip):
        try:
            res = requests.get(f'https://ipapi.co/{ip}/json/')
            return res.json() if res.status_code == 200 else {}
        except:
            return {}
