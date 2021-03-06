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
        return '%s - %s' % (self.wx_id, self.name)


class WxURL(models.Model):
    url = models.CharField('链接', max_length=255)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    title = models.CharField('标题', max_length=100)
    image = models.CharField('图片', max_length=255, null=True)
    memo = models.CharField('分享文案', max_length=255, default='')

    def __str__(self):
        return '%s - %s' % (self.title, self.url)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = ' 文章列表'


class WxShareURL(models.Model):
    wx_url = models.ForeignKey(WxURL, verbose_name='文章')
    wx_user = models.ForeignKey(WxUser, verbose_name='用户')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    clicks = models.IntegerField('点击数', default=0)
    friend_shares = models.IntegerField('好友、群分享数', default=0)
    timeline_shares = models.IntegerField('朋友圈分享数', default=0)

    def __str__(self):
        return '[%s]%s' % (self.wx_user.name, self.wx_url.title)

    class Meta:
        verbose_name = '文章分享'
        verbose_name_plural = '文章分享列表'


class WxClick(models.Model):
    wx_share_url = models.ForeignKey(WxShareURL, verbose_name='分享的文章')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    ip = models.CharField('IP', max_length=20)
    ua = models.CharField('客户端', max_length=255)
    uuid = models.CharField('用户唯一ID', max_length=64, default='')

    def __str__(self):
        return '%s - %s - %s - %s' % (
            self.wx_share_url.wx_url.title, self.uuid, self.ip, self.created_at.strftime('%Y-%m-%d %H:%M'))

    class Meta:
        verbose_name = '点击记录'
        verbose_name_plural = '点击列表'
