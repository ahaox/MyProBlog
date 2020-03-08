from django import forms
from mdeditor.fields import MDTextFormField, MDEditorWidget  # 富文本工具
from dal import autocomplete
from .models import Category, Tag, Article


class ArticleAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    content = MDTextFormField(widget=MDEditorWidget(), label='正文', required=True)

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )

    # class Meta:
    #     model = Article
    #     fields = (
    #         'category', 'tag', 'desc', 'title',
    #         'is_md', 'content'
    #         'status'
    #     )
