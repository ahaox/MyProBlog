""" 自定义分页 """

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def customPage(article_list, request):
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    # book_list = Book.objects.all()
    paginator = Paginator(article_list, 3)  # 告诉分页器我5条分页
    # 如果总页数大于十一页，设置分页
    if paginator.num_pages > 11:
        # 如果当前页数小于5页
        if currentPage - 5 < 1:
            # 页面上显示的页码
            pageRange = range(1, 11)
        #     如果当前页数+5大于总页数显示的页码
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
        else:
            # 在中间显示的十个页码
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = paginator.page_range
    #     捕获路由异常
    try:
        article_list = paginator.page(currentPage)
    #     如果页码输入不是整数则返回第一页的数据
    except PageNotAnInteger:
        article_list = paginator.page(1)
    #     如果页码输入是空值则返回第一页数据
    except EmptyPage:
        article_list = paginator.page(1)

    return locals()

