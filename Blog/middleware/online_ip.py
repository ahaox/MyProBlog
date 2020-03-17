from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class OnlineIpMiddleware(MiddlewareMixin):
    """
    统计ip的中间件, 统计五分钟在线的人数作为在线人数
    list()是将　odict_keys对象转换为list对象
    odict_keys对象在python3.+的版本中不能index操作，切片操作，不能pickle
    """
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        online_ips = list(cache.get("online_ips", []))

        if online_ips:
            online_ips = list(cache.get_many(online_ips).keys())

        cache.set(ip, 0, 5 * 60)

        if ip not in online_ips:
            online_ips.append(ip)

        cache.set("online_ips", online_ips)