from django import forms
from ckeditor.widgets import CKEditorWidget  # 富文本工具


class ArticleAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    content = forms.CharField(widget=CKEditorWidget(), label='正文', required=True)