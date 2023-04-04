from django.contrib import admin

from posts.models import Comment, Group, Follow, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug')
    search_fields = ('title', )
    list_filter = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Group, GroupAdmin)
admin.site.register(Comment)
admin.site.register(Follow)
