
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
import re

class MyMiddleWare(MiddlewareMixin):


    def process_request(self, request):
        print("中间件MyMiddleWare.process_request方法被调用")
        if re.match(r'^/bookstore', request.path_info) \
                and ('userinfo' not in request.session):
            return HttpResponseRedirect('/userinfo/login')
        return None

    def process_response(self,request,response):
        print("中间件方法 process_response 被调用")
        return response


class VisitLimit(MiddlewareMixin):
    '''此中间件限制一个IP地址对应的访问/user/login 的次数不能改过10次,超过后禁止使用'''
    visit_times = {}  # 此字典用于记录客户端IP地址有访问次数
    def process_request(self, request):
        ip_address = request.META['REMOTE_ADDR']  # 得到IP地址
        # if not re.match('^/test', request.path_info):
        #     return
	#放到redis中去，设置一个5s的有效时间，如果某个值大于一定次数，就把ip放到另一个redis的集合中去，有限时间设置一天，禁止用户登录一天
        times = self.visit_times.get(ip_address, 0)
        print("IP:", ip_address, '已经访问过', times, '次!:', request.path_info)
        self.visit_times[ip_address] = times + 1
        if times < 5:
            return
        return HttpResponse('你已经访问过' + str(times) + '次，您被禁止了')
