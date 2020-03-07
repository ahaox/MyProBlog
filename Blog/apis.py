from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Article, Category, Tag
from .serializers import (
    ArticleSerializer, ArticleDetialSerializer,
    CategorySerializer, CategoryDetailSerializer,
    TagSerializer, TagDetailSerializer,
)


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """提供文章接口"""
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(status=Article.STATUS_NORMAL)
    # 写入时的权限校验
    # permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """重写serializer_class，不同接口使用不同Serializer"""
        self.serializer_class = ArticleDetialSerializer
        return super().retrieve(request, *args, **kwargs)

    # def filter_queryset(self, queryset):
    #     """获取某个分类下的文章列表"""
    #     category_id = self.request.query_params.get('tag')  # 获取URL上Query中的category参数
    #     if category_id:
    #         queryset = queryset.filter(tag_id=category_id)
    #     return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """提供分类接口"""
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """提供标签接口"""
    serializer_class = TagSerializer
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TagDetailSerializer
        return super().retrieve(request, *args, **kwargs)



