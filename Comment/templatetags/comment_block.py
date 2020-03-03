"""抽象出评论模块组件"""

from django import template

from Comment.forms import CommentForm
from Comment.models import Comment


register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
    """自定义评论标签"""
    # 在使用地方添加 {% comment_block request.path %} 使用。request.path为参数传递给comment_block()
    # return给block.html
    return {
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target)
    }

