"""MyProBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls



# from .custom_site import custom_site
from Blog.apis import ArticleViewSet, CategoryViewSet, TagViewSet
from Blog.rss import LatestArticleFeed
from Blog.sitemap import ArticleSitemap
from Blog.views import (
    IndexView, CategoryView, TagView,
    ArticleDetailView, SearchView, AuthorView,
)
from Config.views import LinkListView
from Comment.views import CommentView

from .autocomplete import CategoryAutocomplete, TagAutocomplete


router = DefaultRouter()
router.register('article', ArticleViewSet, basename='api-article')
router.register('category', CategoryViewSet, basename='api-category')
router.register('tag', TagViewSet, basename='api-tag')


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('category/<int:category_id>.html', CategoryView.as_view(), name="category-list"),
    path('tag/<int:tag_id>.html', TagView.as_view(), name="tag-list"),
    path('article/<int:article_id>.html', ArticleDetailView.as_view(), name="article-detail"),
    path('search/', SearchView.as_view(), name="search"),
    path('author/<int:owner_id>.html', AuthorView.as_view(), name="author-list"),
    path('link.html', LinkListView.as_view(), name="links-list"),
    path('comment/', CommentView.as_view(), name='comment'),
    path('rss|feed.html/', LatestArticleFeed(), name='rss'),
    path('sitemap.xml/', cache_page(60 * 20, key_prefix='sitemap_cache_')(sitemap_views.sitemap), {'sitemaps': {'article': ArticleSitemap}}, name='sitemap'),
    path('myadmin/', admin.site.urls, name="admin"),
    path('api/', include(router.urls)),
    path('api/docs/', include_docs_urls(title='MyProBlog apis'), name='api-doc'),
    path('mdeditor/', include('mdeditor.urls')),
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



