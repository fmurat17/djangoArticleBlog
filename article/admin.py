from django.contrib import admin

from .models import Article, Comment
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    class Meta:
        model = Article

    list_display = [
        "title",
        "author",
        "created_date"
    ]

    list_display_links = [
        "title",
        "author",
        "created_date"
    ]

    search_fields = [
        "title"
    ]

    list_filter = [
        "title",
        "created_date"
    ]

admin.site.register(Comment)