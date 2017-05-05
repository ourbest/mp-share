from django.db import models


# Create your models here.
class WxUser(models.Model):
    wx_id = models.CharField('用户的微信ID', max_length=64, unique=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    name = models.CharField('昵称', max_length=64, null=True)
    avatar = models.CharField('头像', max_length=255, null=True)
    sex = models.IntegerField('性别')
    country = models.CharField('国家', max_length=20, null=True)
    province = models.CharField('省份', max_length=20, null=True)
    city = models.CharField('城市', max_length=20, null=True)
    admin = models.IntegerField('是否管理员')

    def __str__(self):
        return '%s-%s' % (self.wx_id, self.name)


class WxURL(models.Model):
    url = models.CharField('链接', max_length=255)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    title = models.CharField('标题', max_length=100)
    image = models.CharField('图片', max_length=255, null=True)

    def __str__(self):
        return '%s - %s' % (self.title, self.url)


class WxShareURL(models.Model):
    wx_url = models.ForeignKey(WxURL)
    wx_user = models.ForeignKey(WxUser)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField('点击数', default=0)
    friend_shares = models.IntegerField('好友、群分享数', default=0)
    timeline_shares = models.IntegerField('朋友圈分享数', default=0)

    def __str__(self):
        return '%s[%s]' % (self.wx_url.url, self.wx_user.name)


class WxClick(models.Model):
    wx_share_url = models.ForeignKey(WxShareURL)
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=20)
    ua = models.CharField(max_length=255)
    uuid = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.ip
