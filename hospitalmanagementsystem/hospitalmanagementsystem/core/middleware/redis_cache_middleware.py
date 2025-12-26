# import json
# from django.http import JsonResponse
# from django.core.cache import cache

# class RedisCacheMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def _build_cache_key(self, request):
#         return f"cache:{request.path}?{request.META.get('QUERY_STRING', '')}"

#     def __call__(self, request):
#         if request.method != 'GET':
#             return self.get_response(request)

#         cache_key = self._build_cache_key(request)
#         cached_response = cache.get(cache_key)

#         if cached_response:
#             print("🔁 Cache HIT")
#             response = JsonResponse(json.loads(cached_response), safe=False)
#             response["X-Cache"] = "HIT"
#             return response

#         print("🚫 Cache MISS")
#         response = self.get_response(request)

#         if response.status_code == 200 and "application/json" in response.get("Content-Type", ""):
#             try:
#                 content_json = json.loads(response.content)
#                 cache.set(cache_key, json.dumps(content_json), timeout=600)
#             except Exception as e:
#                 print("⚠️ Cache Set Failed:", e)

#         response["X-Cache"] = "MISS"
#         return response







# for security and user based cache use logout event expire also this improve memory usage because of expiring the data that stored in the cache
# @cache_invalidate([
#     ("user_profile", str(user_id)),
# ])
# def handle_logout_event(event: LogoutEvent):
#     ...

