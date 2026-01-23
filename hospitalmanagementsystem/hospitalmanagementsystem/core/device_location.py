import requests
from user_agents import parse as ua_parse

def parse_user_agent(user_agent: str):
    ua = ua_parse(user_agent or '')
    return {
        'device': ua.device.family or '',
        'os': f"{ua.os.family} {ua.os.version_string}".strip(),
        'browser': f"{ua.browser.family} {ua.browser.version_string}".strip(),
        'is_mobile': ua.is_mobile,
        'is_tablet': ua.is_tablet,
        'is_pc': ua.is_pc,
    }

def lookup_ip(ip: str, token: str):
    if not ip or not token:
        return {}
    try:
        resp = requests.get(f'https://ipinfo.io/{ip}', params={'token': token}, timeout=3)
        resp.raise_for_status()
        data = resp.json()
        loc = (data.get('loc') or '').split(',')
        return {
            'ip': ip,
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            'latitude': loc[0] if len(loc) == 2 else None,
            'longitude': loc[1] if len(loc) == 2 else None,
        }
    except Exception:
        return {'ip': ip}