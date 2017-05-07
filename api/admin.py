from django.contrib import admin
from django.utils.html import format_html

from api.models import *


# Register your models here.

# admin.site.register(WxUser)

@admin.register(WxURL)
class WxURLAdmin(admin.ModelAdmin):
    list_display = ('title', '_get_image', 'created_at')

    def _get_image(self, obj):
        return format_html('<img src="{}" width="80"/>', obj.image)

    _get_image.short_description = '图片'
    _get_image.allow_tags = True
    ordering = ('-id',)


@admin.register(WxShareURL)
class WxShareURLAdmin(admin.ModelAdmin):
    list_display = ('wx_url', 'wx_user', 'created_at', 'clicks', '_get_uv', 'friend_shares', 'timeline_shares')
    ordering = ('-id',)

    def _get_uv(self, obj):
        return WxClick.objects.filter(wx_share_url=obj).values_list('uuid', flat=True).distinct().count()

    _get_uv.short_description = 'UV'


@admin.register(WxClick)
class WxClickAdmin(admin.ModelAdmin):
    list_display = ('wx_share_url', 'ip', 'ua', 'created_at')
    ordering = ('-id',)

    # def title(self, obj):
    #     return str(obj.wx_share_url)

    # title.short_description = '分享的文章'
