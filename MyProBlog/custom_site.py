"""
分离文章管理端,本项目暂时没用
"""

from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'MyProBlog'
    site_title = 'Blog管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')