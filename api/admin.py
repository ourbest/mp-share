from django.contrib import admin
from django.utils.html import format_html

from api.models import *

admin.site.disable_action('delete_selected')


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
    search_fields = ('title',)


@admin.register(WxShareURL)
class WxShareURLAdmin(admin.ModelAdmin):
    list_display = ('wx_user', '_get_title', 'created_at', 'clicks', '_get_uv', 'friend_shares', 'timeline_shares')
    ordering = ('-id',)

    def _get_title(self, obj):
        return format_html('<a href="{url}" width="80" target="_blank">{title}</a>', url=obj.wx_url.url,
                           title=obj.wx_url.title)

    _get_title.short_description = '文章标题'

    def _get_uv(self, obj):
        return WxClick.objects.filter(wx_share_url=obj).values_list('uuid', flat=True).distinct().count()

    _get_uv.short_description = 'UV'
    list_filter = ('wx_user__name',)
    search_fields = ('wx_url__title',)


@admin.register(WxClick)
class WxClickAdmin(admin.ModelAdmin):
    list_display = ('wx_share_url', 'ip', 'ua', 'created_at')
    ordering = ('-id',)
    list_filter = ('wx_share_url__wx_user__name',)

    # def title(self, obj):
    #     return str(obj.wx_share_url)

    # title.short_description = '分享的文章'
