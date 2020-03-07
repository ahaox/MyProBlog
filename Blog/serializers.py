"""
序列化数据
"""
from rest_framework import serializers, pagination
from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Article, Category, Tag


class ArticleSerializer(HyperlinkedModelSerializer):
    """文章列表序列化"""
    category = serializers.SlugRelatedField(
        read_only=True,  # 定义外键是否可写
        slug_field='name',  # 指定展示的字段
    )
    tag = serializers.SlugRelatedField(
        many=True,  # 定义多对多是否可写
        read_only=True,
        slug_field='name',
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    url = serializers.HyperlinkedIdentityField(view_name='api-article-detail')

    class Meta:
        model = Article
        fields = ['url', 'id', 'title', 'category', 'tag', 'owner', 'created_time', ]


class ArticleDetialSerializer(ArticleSerializer):
    """文章详细序列化"""
    class Meta:
        model = Article
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content_html', 'created_time', ]


class CategorySerializer(serializers.ModelSerializer):
    """分类列表序列化"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time']


class CategoryDetailSerializer(CategorySerializer):
    """分类详细序列化"""
    articles = serializers.SerializerMethodField('paginated_articles')

    def paginated_articles(self, obj):
        articles = obj.article_set.filter(status=Article.STATUS_NORMAL)  # 外键反向查询
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(articles, self.context['request'])
        serializer = ArticleSerializer(page, many=True, context={
            'request': self.context['request']
        })
        return {
            'count': articles.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', 'articles']


class TagSerializer(serializers.ModelSerializer):
    """标签列表序列化"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_time']


class TagDetailSerializer(TagSerializer):
    """标签详细序列化"""
    articles = serializers.SerializerMethodField('paginated_articles')

    def paginated_articles(self, obj):
        articles = obj.article_set.filter(status=Article.STATUS_NORMAL)  # 外键反向查询
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(articles, self.context['request'])
        serializer = ArticleSerializer(page, many=True, context={
            'request': self.context['request']
        })
        return {
            'count': articles.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_time', 'articles']


