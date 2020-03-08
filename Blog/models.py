"""内容相关的Model"""
import mistune
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils.functional import cached_property
from mdeditor.fields import MDTextField
 

# Create your models here.
class Category(models.Model):
    """分类表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        """设置返回字符串"""
        return self.name

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_navs(cls):
        """获取导航信息"""
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)  # 获取状态正常的分类
        nav_categories = []  # 导航分类
        normal_categories = []  # 一般的正常分类
        # 实现一次查询，解决N+1问题
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'navs': nav_categories,  # 导航栏
            'categories': normal_categories,  # 普通分类
        }

    class Meta:
        verbose_name_plural = "分类"


class Tag(models.Model):
    """标签表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    @classmethod
    def get_all(cls):
        # 优化查询方式，一次性查询出所有数据。解决N+1问题
        return cls.objects.all()

    class Meta:
        verbose_name_plural = "标签"


class Article(models.Model):
    """文章表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = MDTextField(verbose_name="正文", help_text="正文必须为 MarkDown 格式")
    content_html = models.TextField(verbose_name="正文HTML代码", blank=True, editable=False)
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE)
    # 对于多对多的关系，在数据库中不会存在tag字段，会自动抽象出第三张关系表
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    # 用pv和uv统计文章的访问量
    is_top = models.BooleanField(default=False, verbose_name="顶置")
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    @classmethod
    def hot_article(cls, with_related=True):
        """获取最热文章"""
        queryset = cache.get('hot_articles')
        if not queryset:
            queryset = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv').only('title', 'id')
            if with_related:
                queryset = queryset.select_related('owner', 'category').prefetch_related('tag')
            cache.set('hot_articles', queryset, 10 * 60)
        return queryset

    @classmethod
    # 获取最新文章
    def latest_articles(cls, with_related=True):
        """
        将queryset获取封装到Model层
        @:param with_related 控制返回的数据是否需要加上外键或者多对多的查询(N+1)

        select_related: 解决外键N+1
        prefetch_related: 解决多对多N+1

        """
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-id')
        if with_related:
            queryset = queryset.select_related('owner', 'category').prefetch_related('tag')
        return queryset

    @cached_property
    def tags(self):
        """
        cached_property帮我们把返回的数据绑定到实例上面
        配置sitemap
        """
        return ','.join(self.tag.values_list('name', flat=True))

    def save(self, *args, **kwargs):
        """保存为markdown格式"""
        self.content_html = mistune.markdown(self.content)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "文章"
        # 通过id进行降序排列
        ordering = ['-id']


class ToppedArticles(models.Model):
    """顶置文章表"""
    AREA_RIGHT = 0
    AREA_LEFT = 1
    AREA_ITEMS = (
        (AREA_LEFT, '左置顶区'),
        (AREA_RIGHT, '右顶置区'),
    )
    top_area = models.PositiveIntegerField(choices=AREA_ITEMS, default=AREA_LEFT, verbose_name="置顶区域")
    article = models.ForeignKey('Article', verbose_name="关联文章", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="设置顶置时间")
    topped_expired_time = models.DateTimeField(verbose_name="顶置失效时间")

    @classmethod
    def get_top(cls):
        from django.utils import timezone
        queryset = cache.get('top_articles')
        if not queryset:
            # 按设置顶置时间　升序查询　在顶置有效期内的文章
            queryset = cls.objects.filter(topped_expired_time__gt=timezone.now()).order_by('created_time')
            cache.set('top_articles', queryset, 10 * 60)
            print(queryset)
        return queryset

    class Meta:
        verbose_name_plural = "顶置文章"
        ordering = ['-created_time']