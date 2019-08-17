
import jwt
from django.http import JsonResponse

TOKEN_KEY='123456'

def login_check(*methods):
    '''
    检查权限token，装饰器
    :param methods:
    :return:
    '''
    def _login_check(func):
        def wrapper(request,*args,**kwargs):
            #获取token
            token=request.META.get('HTTP_AUTHORIZATION')
            if not methods:
                #如果当前没有传递任何参数，则直接返回试图函数
                return func(request,*args,**kwargs)
            else:
                #检查当前request.method 是否在参数列表中
                if request.method not in methods:
                    return func(request,*args,**kwargs)
                #当前必须有token
                if not token:
                    result={'code':109,'error':'please give me token'}
                    return JsonResponse(result)
                try:
                    #判断token是否过期，token是否本站发出去的
                    res=jwt.decode(token,TOKEN_KEY)
                except Exception as e:
                    print('login check is error %s'%(e))
                    result={'code':108,'error':'the token is wrong'}
                    return JsonResponse(result)
                #token校验成功,取出token中的username
                username=res['username']
                #使用用户名查询用户信息数据库
                try:
                    print('用用户名查询数据库')
                    user=1
                except:
                    user=None
                #判断用户是否存在
                if not user:
                    result={'code':110,'error':'the user is not existed'}
                    return JsonResponse(result)

                #用户校验成功，将user对象赋值给request对象
                request.user=user
                return func(request,*args,**kwargs)
            return wrapper
        return _login_check

def get_user_by_request(request):
    '''
    通过request获取user
    :param request:
    :return:
    '''
    pass