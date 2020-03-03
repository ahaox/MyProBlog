from django.views.generic import ListView
from Blog.views import CommonViewMixin
from .models import Link


# Create your views here.
class LinkListView(CommonViewMixin, ListView):
    """友链视图"""
    queryset = Link.get_normal()
    template_name = 'config/links.html'
    context_object_name = 'link_list'
