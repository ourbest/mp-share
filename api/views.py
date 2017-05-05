# Create your views here.
import hashlib
import time
import uuid

import requests
from django.conf import settings
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from api import utils
from api.models import WxShareURL, WxClick, WxURL, WxUser


def redirect(request, page):
    ip = utils.get_ip(request)
    ua = request.META.get('HTTP_USER_AGENT')

    db_page = WxShareURL.objects.filter(id=page).select_related('wx_url').first()

    cookie = request.COOKIES.get(settings.COOKIE_NAME)

    if db_page:
        redirect_response = HttpResponseRedirect(db_page.wx_url.url)
        if not cookie:
            cookie = str(uuid.uuid4()).replace('-', '')
            redirect_response.set_cookie(settings.COOKIE_NAME, cookie, max_age=365 * 24 * 60 * 60, path='/')

        WxClick(wx_share_url=db_page, ip=ip, ua=ua, uuid=cookie).save()
        WxShareURL.objects.filter(id=page).update(clicks=F('clicks') + 1)
        return redirect_response
    else:
        return HttpResponse(404)


def auth(request):
    code = utils.get_param(request, 'code')
    user_token_response = get_user_token(code)
    token = user_token_response.get('access_token')
    uid = user_token_response.get('openid')
    user_info = get_user_info(token, uid)
    db = WxUser.objects.filter(wx_id=uid).first()
    if not db:
        db = WxUser(wx_id=uid)

    db.name = user_info.get('nickname')
    db.sex = user_info.get('sex')
    db.province = user_info.get('province')
    db.city = user_info.get('city')
    db.country = user_info.get('country')
    db.avatar = user_info.get('headimgurl')
    db.save()

    utils.set_user(request, db.id)

    return HttpResponseRedirect('/pages')


def pages(request):
    wx_id = utils.get_user(request)
    if wx_id == 1:
        return HttpResponseRedirect('https://open.weixin.qq.com/connect/oauth2/authorize?'
                                    'appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo'
                                    '&state=STATE#wechat_redirect' % (settings.WX_APP_KEY,
                                                                      'http%3A%2F%2Fwx.creditdev.com%2Fauth'))

    db = WxURL.objects.order_by('-pk').all()[0:20]
    # return JsonResponse({
    #     'code': 0,
    #     'data': [{
    #         'id': x.id,
    #         'title': x.title,
    #         'url': x.url,
    #         'create_time': x.created_at.strftime('%Y-%m-%d')
    #     } for x in db]
    # })

    return render(request, 'list.html', {'urls': db})


def share_page(request, page):
    share_url = get_share_url(page, request)

    ts = time.time()
    nonce = str(ts)[-6:]
    sig = sign('http://wx.creditdev.com/share/%s' % page, int(ts), nonce)

    return render(request, 'share.html', {'url': share_url, 'wx': {
        'app': '1234',
        'time': int(ts),
        'nonce': nonce,
        'sig': sig
    }})


def get_share_url(page, request):
    wx_id = utils.get_user(request)
    share_url = WxShareURL.objects.filter(wx_url_id=page, wx_user_id=wx_id).select_related('wx_url').first()
    if not share_url:
        share_url = WxShareURL(wx_url_id=page, wx_user_id=wx_id)
        share_url.save()
    return share_url


def add_share(request):
    page = utils.get_param(request, 'id')
    share_url = get_share_url(page, request)


def sign(url, ts, nonce):
    ticket = get_ticket()
    before = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' % (ticket, nonce, ts, url)
    return hashlib.sha1(before.encode()).hexdigest()


def get_token():
    key = settings.WX_APP_KEY
    secret = settings.WX_APP_SECRET
    response = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (key, secret))
    return response.json().get('access_token')


def get_user_token(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'
    response = requests.get(url % (settings.WX_APP_KEY, settings.WX_APP_SECRET, code))
    return response.json()


def get_user_info(token, uid):
    url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % (token, uid)
    return requests.get(url).json()


def get_ticket():
    global tickets
    token = get_token()
    if tickets and tickets['expire'] > time.time():
        response = requests.get('https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % token)
        ticket = response.json().get('ticket')
        tickets = {
            'expire': time.time() + 3600,
            'value': ticket
        }
    else:
        return tickets['value']


tickets = None
