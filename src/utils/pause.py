from datetime import datetime, timedelta

from django.core.cache import cache


def check_for_pause_timer(request, attr_name: str) -> bool:
    pause = request.session.get(attr_name)
    if pause and datetime.strptime(pause, '%Y:%m:%d:%H:%M:%S') > datetime.utcnow():
        return False
    ip = request.headers.get('X-Real-Ip')
    if cache.get(ip):
        return False
    return True


def set_pause_timer(request, attr_name: str) -> None:
    expired_at = datetime.utcnow() + timedelta(seconds=30)
    request.session[attr_name] = expired_at.strftime('%Y:%m:%d:%H:%M:%S')
    request.session.modified = True
    ip = request.headers.get('X-Real-Ip')
    cache.set(ip, True, 30)
