from django.contrib import admin
from .models import Link, SideBar, AboutBlogOwner


# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time', )
    fields = ('title', 'href', 'status', 'weight', )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar)
class SiderBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time', 'status', )
    fields = ('title', 'display_type', 'content', )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SiderBarAdmin, self).save_model(request, obj, form, change)


@admin.register(AboutBlogOwner)
class AboutBlogAdmin(admin.ModelAdmin):
    list_display = ('blog_owner', 'explain', 'email', 'top_explain')
    fields = ('blog_owner', 'explain', 'email', 'top_explain')
