from django.core.cache import cache


def is_user_paused(request, attr_name: str) -> bool:
    ip = request.headers.get('X-Real-Ip')
    return attr_name in cache.get(ip, [])


def set_pause_timer(request, attr_name: str) -> None:
    ip = request.headers.get('X-Real-Ip')
    request_cache = cache.get(ip, [])
    request_cache.append(attr_name)
    cache.set(ip, request_cache, 30)
